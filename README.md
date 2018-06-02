# SpireLogsUploader
SpireLogUploader is a tool to automate uploading Slay the Spire runs to [SpireLogs](http://spirelogs.com/).

Currently for the GUI wxPython is used, due to issues with cross-platform
installation that will be changing when I can get around to it. There is also no CLI implemented yet
but there are plans to add it.

## Installation
### Windows
1. Open command prompt as admin and run **pip install -r requirements,txt**
2. Edit the config file with the directory to the base folder of Slay the Spire as shown below.
3. cd to the downloaded folder and run **python .\spire_log_gui.py**
````
[DEFAULT]
GameDirectory = E:\Program Files (x86)\Steam\steamapps\common\SlayTheSpire\
````
### Linux
Same as windows except you will need to download and install wxPython following instructions [here](https://wxpython.org/pages/downloads/)
### Mac
I can't be bothered to check on proper installation for Macs at the moment