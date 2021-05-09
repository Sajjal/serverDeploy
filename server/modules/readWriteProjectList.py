import json


class ManageProjectList:

    # instance initialization
    def __init__(self):
        self.fileName = './config/projectList'

    # instance methond
    def readRecord(self):
        try:
            return open(f"{self.fileName}.json", "r").read()
        except FileNotFoundError:
            self.writeRecord([])
            return open(f"{self.fileName}.json", "r").read()

    def writeRecord(self, dataList):
        f = open(f"{self.fileName}.json", "w", encoding='utf-8')
        json.dump(dataList, f, ensure_ascii=False, indent=4)
        return f.close()

    def createRecord(self, name, domain, port, mainFile):
        dataList = []
        data = {"name": name, "domain": domain,
                "port": port, "mainFile": mainFile}

        if(len(self.readRecord())):
            dataList = json.loads(self.readRecord())

        dataList.append(data)
        self.writeRecord(dataList)

    def removeRecord(self, name):
        projectList = json.loads(self.readRecord())
        newList = []
        if(projectList):
            for data in projectList:
                if data["name"] != name:
                    newList.append(data)

            self.writeRecord(newList)
