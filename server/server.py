import json
from flask import Flask, request

from modules.readWriteProjectList import ManageProjectList
from modules.manageApp import ManageApp, authenticate, checkProjectRecord

projectRecord = ManageProjectList()

app = Flask(__name__)


# Return the available port number for new service
def getPort():
    try:
        port = json.loads(projectRecord.readRecord()).pop()["port"]
    except:
        port = 3000
    return port


@app.route('/', methods=['GET', 'POST'])
def home():
    return {"serverStatus": "Up & Running..."}


@app.route('/authenticate', methods=['GET', 'POST'])
def authenticateUser():
    return {"status": True} if authenticate(request.json['passCode']) else {"status": False}


@app.route('/checkProject', methods=['GET', 'POST'])
def checkIfValidProject():
    projectName = request.json['name']
    projectInfo = checkProjectRecord(projectName)
    return {"status": projectInfo["mainFile"]} if(projectInfo) else {"status": False}


@app.route('/create', methods=['POST'])
def create():
    port = getPort()+1
    clientPass = request.json['passCode']
    projectName = request.json['name']
    domain = request.json['domain']
    mainFile = request.json['mainFile']

    currentProject = ManageApp(projectName, domain, port, mainFile)
    if(authenticate(clientPass)):
        if(not checkProjectRecord(projectName)):
            try:
                currentProject.moveAndUnzip()
            except:
                return {"ERROR": 'Unable to Expand Project Archive in Server!'}
            try:
                currentProject.installAndActivateApp()
            except:
                return {"ERROR": 'Unable to Create PM2 instance in Server!'}
            try:
                currentProject.createApacheConf()
            except:
                return {"ERROR": 'Unable to Create Apache .conf file in Server!'}
            try:
                currentProject.activateDomain()
            except:
                return {"ERROR": f"Unable to Activate {domain} in Server!"}
            try:
                projectRecord.createRecord(projectName, domain, port, mainFile)
            except:
                return {"ERROR": 'Unable to Create Project Record in Server!'}

            return {"Success": f"{domain} is running on port: {port}"}

        else:
            return {"ERROR": 'Project is Already in the Server! Try Updating!'}

    else:
        return {"ERROR": 'Unable to Authenticate!'}


@app.route('/update', methods=['POST'])
def update():
    clientPass = request.json['passCode']
    projectName = request.json['name']

    if(authenticate(clientPass)):
        try:
            projectInfo = json.loads(projectRecord.readRecord())
        except:
            projectInfo = None
            return {"ERROR": 'Project Not found in Server!'}
        if projectInfo:
            for project in projectInfo:
                if project["name"] == projectName:
                    currentProject = ManageApp(
                        projectName, project["domain"], project["port"], '')
                    try:
                        currentProject.moveAndUnzip()
                    except:
                        return {"ERROR": 'Unable to Expand Project Archive in Server!'}
                    try:
                        currentProject.installAndRestart()
                    except:
                        return {"ERROR": 'Unable to Restart PM2 instance in Server!'}

                    return {"Success": f"{projectName} is Updated"}

            return {"ERROR": 'Project Not found in Server!'}
        else:
            return {"ERROR": 'Project Not found in Server!'}
    else:
        return {"ERROR": 'Unable to Authenticate!'}


@app.route('/remove', methods=['POST'])
def remove():
    clientPass = request.json['passCode']
    projectName = request.json['name']

    if(authenticate(clientPass)):
        try:
            projectInfo = json.loads(projectRecord.readRecord())
        except:
            projectInfo = None
            return {"ERROR": 'Project Not found in Server!'}
        if projectInfo:
            for project in projectInfo:
                if project["name"] == projectName:
                    currentProject = ManageApp(
                        projectName, project["domain"], project["port"], '')
                    try:
                        currentProject.removeFiles()
                    except:
                        return {"ERROR": 'Unable to Project Files in Server!'}
                    try:
                        currentProject.removePM2Instance()
                    except:
                        return {"ERROR": 'Unable to Restart PM2 instance in Server!'}
                    try:
                        currentProject.removeConf()
                    except:
                        return {"ERROR": 'Unable to Remove Apache and Certbot Conf in Server!'}
                    try:
                        projectRecord.removeRecord(projectName)
                    except:
                        return {"ERROR": 'Unable to Remove Project Record in Server!'}

                    return {"Success": f"{projectName} is Removed"}

            return {"ERROR": 'Project Not found in Server!'}
        else:
            return {"ERROR": 'Project Not found in Server!'}
    else:
        return {"ERROR": 'Unable to Authenticate!'}


if __name__ == '__main__':
    app.run(debug=False)
