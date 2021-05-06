[![GitHub stars](https://img.shields.io/github/stars/Sajjal/serverDeploy)](https://github.com/Sajjal/serverDeploy/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/Sajjal/serverDeploy)](https://github.com/Sajjal/serverDeploy/issues)
![GitHub language count](https://img.shields.io/github/languages/count/Sajjal/serverDeploy)
![GitHub top language](https://img.shields.io/github/languages/top/Sajjal/serverDeploy)
![GitHub repo size](https://img.shields.io/github/repo-size/Sajjal/serverDeploy)

# Welcome to S & D serverDeploy!

### Thank you for exploring S & D serverDeploy.

It is a lightweight CLI application that can deploy and configure **Node.js** based web application in the remote server *(Similar to `Vercel`)*. This application is developed using Python 3 and Flask.

---

## Background (_Why this application was developed?_)

I've just started learning Python and it seems fun. Learning without doing is not effective. Therefore, I was thinking to do some project in Python but I was in short of ideas. Being a web developer myself, I need to frequently create and update web apps in remote server. The work pattern is similar in most projects and it is somewhat time consuming. So, I decided to automate this process using Python and here it is.  

## Prerequisites:

### Virtual Server:

- Setup a Virtual Server on any cloud provider of your choice `(Ubuntu 16.04+ Preferred)`
- Enable port 22, 80 and 443
- Create a SUDO user with no password, generate SSH key-pair and download the Key
- Install Apache2

### Domain Name:

- Obtain a Domain Name of your choice from any Domain name registrar
- Point the A record of your Domain to your server's public IP address
- Create a Wild-Card sub-domain (*) and Point the A record of your sub-domain to your server's public IP address
- Configure Reverse Proxy on Apache2 and forward your Domain to port 5000

### Python:

- This project works best on Python 3.8.9 (`Other versions are not tested yet!`)

### Node.js:

- Install **Node.js** on your Virtual Server

---

## Installation:

### Server Setup:

- Copy the `server` directory to your Virtual Server at `/home/SUDO_USER/serverDeploy/`
- **cd** to `/home/SUDO_USER/serverDeploy/server/config`
- Modify the value of `scpDir`, `projectsDir`, `passCode` in `serverSetup.json`

> **INFO:** The `scpDir` is generally `/home/SUDO_USER` | The `projectsDir` is where you want to store your Deployed Projects; You need to create this Directory

- **cd** to `/home/SUDO_USER/serverDeploy/server` and type:

        - npm install pm2@latest -g

        - pip3 install virtualenv
        
        - virtualenv venv

        - source venv/bin/activate

        - pip3 install -r requirements.txt

        - pm2 start pm2Config.json

- Type `http://yourDomainName` on your browser's address bar and hit Enter. **The server should be Up and Running.**

> **Important:** Replace `SUDO_USER` with the username you created earlier (`See Prerequisites`).

---
### Client Setup:

- Copy the `client` directory to `~/serverDeploy/` on your local computer
- **cd** to `~/serverDeploy/client`
- Modify the value of `sshKey`, `serverSCPInfo`, `serverName` and `wildCardDomain`
- Open terminal and type:

        - pip3 install virtualenv

        - virtualenv venv

        - source venv/bin/activate

        - pip3 install -r requirements.txt

        - chmod +x app.py

- Add the following line in your `.zshrc` or `.bash_profile`:

        alias serverDeploy=~/serverDeploy/client/app.py

- Type `source ~/.zshrc` OR `source ~/.bash_profile` in the terminal and restart the terminal

- You must have `port=process.env.PORT` in your **Node.js** based Web Application 

- **cd** to your **Node.js** based Web Application project directory and type `serverDeploy`

- Enjoy!

> **INFO:** Above mentioned Client Setup is for Linux and MacOS only.

---

## serverDeploy Flow Chart:

<img src="https://github.com/Sajjal/serverDeploy/blob/master/client/screenShots/flowChart.svg">

---

## CLI Options:

<img src="https://github.com/Sajjal/serverDeploy/blob/master/client/screenShots/CLI.png">

---

With Love,

**Sajjal**