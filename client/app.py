#!/usr/bin/env python3

import requests
import os
import json
import getpass
from modules.setupConfig import SetupConfig, colors
from modules.compressDir import CompressDirectory

stream = os.popen('pwd')
projectLocation = stream.read().strip()


# Reading setup.json file for authentication
def readConfig(fileName):
    try:
        return json.load(open(f"{fileName}", "r"))
    except:
        print(
            '\n'+colors.RED + f'ERROR: Unable to Read {fileName} | Make sure it is Valid JSON' + colors.ENDC+'\n')
        exit()


user_home_dir = os.path.expanduser('~')
setupInfo = readConfig(f'{user_home_dir}/serverDeploy/client/setup.json')

newConfFile = SetupConfig(setupInfo["wildCardDomain"])
generateConf = newConfFile.userOption()


def copyToServer(projectInfo):
    projectName = projectInfo['name']
    compressProject = CompressDirectory(projectLocation, projectName)
    compressProject.compress()
    try:
        os.system(
            f'scp -i {setupInfo["sshKey"]} {projectLocation}/{projectName}.tar.gz {setupInfo["serverSCPInfo"]} && rm -rf {projectLocation}/{projectName}.tar.gz')
    except:
        print(
            '\n'+colors.RED + 'ERROR: Server Auth Error; Modify setup.json file with correct info' + colors.ENDC+'\n')
        exit()


def copyFromServer(remoteLocation, projectName):
    try:
        os.system(
            f'scp -i {setupInfo["sshKey"]} {setupInfo["serverSCPInfo"].split(":")[0]}:{remoteLocation}  {projectLocation}')
        os.system(f'cd {projectLocation} && tar -xf {projectName}.tar.gz && rm -rf {projectName}.tar.gz')
    except:
        print(
            '\n'+colors.RED + 'ERROR: Server Auth Error; Modify setup.json file with correct info' + colors.ENDC+'\n')
        exit()


def authenticateClient():
    generateConf["passCode"] = getpass.getpass('Server PassCode: ')
    url = f'{setupInfo["serverName"]}/authenticate'
    try:
        res = requests.post(url, json={"passCode": generateConf["passCode"]})
        return json.loads(res.text)["status"]
    except:
        return False


def checkIfProjectExist():
    checkProjectUrl = f'{setupInfo["serverName"]}/checkProject'
    try:
        res = requests.post(checkProjectUrl, json=generateConf)
        return json.loads(res.text)["status"]
    except:
        return False


if(generateConf and generateConf['type'] == 1):
    if(authenticateClient()):
        projectStatus = checkIfProjectExist()
        if not projectStatus:
            try:
                copyToServer(generateConf)
                url = f'{setupInfo["serverName"]}/create'
                res = requests.post(url, json=generateConf)
                print(res.text)
            except:
                print('\n'+colors.RED +
                      'Error: Unable to Archive and Copy via SCP!' + colors.ENDC+'\n')
        else:
            print('\n'+colors.RED +
                  'Error: Project is Already in the Server! Try Updating!' + colors.ENDC+'\n')

    else:
        print('\n'+colors.RED + 'Error: Unable to Authenticate' + colors.ENDC+'\n')


elif(generateConf and generateConf['type'] == 2):
    if(authenticateClient()):
        projectStatus = checkIfProjectExist()
        if(projectStatus):
            confirm = input('\n' + colors.YELLOW + 'WARN: Make Sure your mainFile is still ' + projectStatus +
                            ' Continue? y/n   ' + colors.ENDC)
            if (confirm == 'y' or confirm == 'Y'):
                try:
                    copyToServer(generateConf)
                    url = f'{setupInfo["serverName"]}/update'
                    req = requests.post(url, json=generateConf)
                    print(req.text)
                except:
                    print(
                        '\n'+colors.RED+'Error: Unable to Archive and Copy via SCP!'+colors.ENDC+'\n')

            else:
                print('\n'+colors.YELLOW +
                      'Closing Program....' + colors.ENDC + '\n')
                exit()
        else:
            print('\n'+colors.RED +
                  'Error: Project not found in Server' + colors.ENDC+'\n')

    else:
        print('\n'+colors.RED + 'Error: Unable to Authenticate' + colors.ENDC+'\n')


elif(generateConf and generateConf['type'] == 3):
    if(authenticateClient()):
        projectStatus = checkIfProjectExist()
        if(projectStatus):
            try:
                url = f'{setupInfo["serverName"]}/download'
                req = requests.post(url, json=generateConf)
                archiveLocation = json.loads(req.text)
                archiveLocation = archiveLocation['archiveLocation']
            except:
                print(
                    '\n'+colors.RED+'ServerError: Unable to communicate with Server!'+colors.ENDC+'\n')
            try:
                copyFromServer(archiveLocation, generateConf['name'])
                print('\n'+generateConf['name'] + ' downloaded successfully! \n')
            except:
                print(
                    '\n'+colors.RED+'ServerError: Unable to download archive via SCP!'+colors.ENDC+'\n')

        else:
            print('\n'+colors.RED +
                  'Error: Project not found in Server' + colors.ENDC+'\n')

    else:
        print('\n'+colors.RED + 'Error: Unable to Authenticate' + colors.ENDC+'\n')


elif(generateConf and generateConf['type'] == 4):
    if(authenticateClient()):
        projectStatus = checkIfProjectExist()
        if(projectStatus):
            try:
                url = f'{setupInfo["serverName"]}/remove'
                req = requests.post(url, json=generateConf)
                print(req.text)
            except:
                print(
                    '\n'+colors.RED+'ServerError: Unable to communicate with Server!'+colors.ENDC+'\n')

        else:
            print('\n'+colors.RED +
                  'Error: Project not found in Server' + colors.ENDC+'\n')

    else:
        print('\n'+colors.RED + 'Error: Unable to Authenticate' + colors.ENDC+'\n')
