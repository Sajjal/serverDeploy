import json


class colors:  # You may need to change color settings
    RED = '\033[31m'
    ENDC = '\033[m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'


class SetupConfig:

    def __init__(self, wildCardDomain):

        self.repeat = True
        self.projectName = None
        self.domainName = None
        self.mainFile = None
        self.wildCardDomain = wildCardDomain
        self.status = None

    def promptUser(self):
        name = input('\n'+'Project Name (no space please)? ')
        domain = input('Domain Name? (empty to default as Project Name) ')
        mainFile = input('Main File (E.g. app.js/server.js)? ')

        if (' ' in name) == True:
            print('\n'+colors.RED +
                  'ERROR: Remove Space from Project Name' + colors.ENDC+'\n')
        elif (' ' in domain) == True:
            print('\n'+colors.RED +
                  'ERROR: Remove Space from Domain Name' + colors.ENDC+'\n')
        elif not name:
            print('\n'+colors.RED +
                  'ERROR: Project Name is Required' + colors.ENDC+'\n')
        elif ((' ' in mainFile) == True or not mainFile or (not '.' in mainFile) == True):
            print('\n'+colors.RED + 'ERROR: Invalid Main File' + colors.ENDC+'\n')
        else:
            self.projectName = name
            self.domainName = f"{name}.{self.wildCardDomain}" if not domain else domain
            self.mainFile = mainFile
            self.status = 'success'
            return

    def userOption(self):
        status = None

        while(self.repeat):
            try:
                option = int(input('\n'+colors.GREEN + '***** S & D serverDeploy *****' + colors.ENDC + '\n' + '\n'+'1. New Project' + '\n' +
                                   '2. Update Existing Project' + '\n' + '3. Terminate Program' + '\n\n' + colors.GREEN + '*********** OPTION ***********' + colors.ENDC + '\t'))

                if(option == 1):
                    self.status == self.projectName == self.domainName == None
                    self.promptUser()
                    if(self.status == 'success'):
                        status = {"name": self.projectName, "domain": self.domainName,
                                  "mainFile": self.mainFile, "type": 1}
                        print('\n'+'Generating Configuration...' + '\n')
                        self.repeat = False

                elif(option == 2):
                    name = input('\n' + 'Project Name (no space please)? ')
                    if ((' ' in name) == True or not name):
                        print('\n'+colors.RED +
                              'ERROR: Invalid Project Name' + colors.ENDC+'\n')
                    else:
                        status = {"name": name, "type": 2}
                        print('\n'+'Generating Configuration...' + '\n')
                        self.repeat = False

                elif(option == 3):
                    self.repeat = False
                    print(
                        '\n'+colors.YELLOW + 'Program Closed!' + colors.ENDC + '\n')

                else:
                    print(
                        '\n'+colors.RED + 'ERROR: Invalid Selection! Try Again' + colors.ENDC + '\n')
            except:
                print('\n'+colors.RED +
                      'ERROR: Invalid Selection! Try Again' + colors.ENDC + '\n')
        return status
