import os
import json
import tarfile


def readSetupFile(fileName):
    try:
        return json.loads(open(f"./config/{fileName}", "r").read())
    except:
        print(
            '\n' + f'Error: Unable to Read{fileName} Make sure it is Valid JSON '+'\n')
        return False


def authenticate(clientPass):
    return True if readSetupFile('serverSetup.json')["passCode"] == clientPass else False


def checkProjectRecord(name):
    projectList = readSetupFile('projectList.json')
    if(projectList):
        for data in projectList:
            if data["name"] == name:
                return data
    return False


class ManageApp:

    def __init__(self, projectName, domain, port, mainFile):
        config = readSetupFile('serverSetup.json')
        self.source = config["scpDir"]
        self.destination = config["projectsDir"]
        self.projectName = projectName
        self.domain = domain
        self.port = port
        self.mainFile = mainFile
        self.exclude_files = [f"{projectName}/node_modules"]

    def moveAndUnzip(self):
        os.system(
            f'mv {self.source}/{self.projectName}.tar.gz {self.destination}/ && cd {self.destination}/ && tar -xf {self.projectName}.tar.gz && rm -rf {self.projectName}.tar.gz')
        return

    def installAndActivateApp(self):
        pm2Config = {"apps": [{"instances": "1"}]}
        pm2Config["apps"][0]["name"] = self.projectName
        pm2Config["apps"][0]["script"] = "./"+self.mainFile
        pm2Config["apps"][0]["port"] = self.port

        pm2Conf = open(
            f"{self.destination}/{self.projectName}/pm2Conf.json", "w", encoding='utf-8')
        json.dump(pm2Config, pm2Conf, ensure_ascii=False, indent=4)
        pm2Conf.close()

        os.system(
            f'cd {self.destination}/{self.projectName} && npm install -f && pm2 start pm2Conf.json && pm2 save')
        return

    def installAndRestart(self):
        os.system(
            f'cd {self.destination}/{self.projectName} && npm install -f && pm2 restart {self.projectName}')
        return

    def createApacheConf(self):
        newLine = '\n'
        tab = '\t'
        partA = f'<VirtualHost *:80> {newLine}{tab}{newLine}ServerName {self.domain}{newLine}{newLine}<Proxy balancer://mycluster> {newLine}'
        partB = f'{tab}BalancerMember http://127.0.0.1:{self.port}{newLine}'
        partC = f'</Proxy>{newLine}{newLine}{tab}ProxyPreserveHost On {newLine}{tab}ProxyPass / balancer://mycluster/ {newLine}{tab}ProxyPassReverse / balancer://mycluster/{newLine}</VirtualHost>'
        confFile = open(
            f"{self.destination}/{self.projectName}/{self.domain}.conf", "w")
        confFile.write(partA+partB+partC)
        confFile.close()

        os.system(
            f'cd {self.destination}/{self.projectName} && sudo mv {self.domain}.conf /etc/apache2/sites-available/')
        return

    def activateDomain(self):
        os.system(
            f'sudo a2ensite {self.domain}.conf && sudo service apache2 reload && sudo certbot --apache -n  --redirect -d {self.domain}')
        return

    def filter_function(self, tarinfo):
        filename = tarinfo.name
        return None if filename in self.exclude_files or os.path.splitext(filename)[1] in self.exclude_files else tarinfo

    def compress(self):
        tar = tarfile.open(f"{self.destination}/{self.projectName}.tar.gz", "w:gz")
        tar.add(f"{self.destination}/{self.projectName}",
                arcname=self.projectName, filter=self.filter_function)
        tar.close()
        return f"{self.destination}/{self.projectName}.tar.gz"

    def removeArchive(self):
        os.system(f'rm {self.destination}/{self.projectName}.tar.gz')
        return

    def removeFiles(self):
        os.system(f'cd {self.destination}/ && rm -rf {self.projectName}')
        return

    def removePM2Instance(self):
        os.system(
            f'pm2 stop {self.projectName} && pm2 delete {self.projectName} && pm2 save')
        return

    def removeConf(self):
        os.system(
            f'cd /etc/apache2/sites-available/ && sudo rm {self.domain}.conf && sudo rm {self.domain}-le-ssl.conf && sudo certbot delete --cert-name {self.domain} && sudo a2dissite {self.domain} && sudo service apache2 reload')
        return
