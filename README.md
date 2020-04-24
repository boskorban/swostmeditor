# SWOS Transfermarkt Editor

Download data from Transfermarkt.com and import in Amiga SWOS - https://sensiblesoccer.de/faq<br/><br/>
Software for import to Amiga SWOS<br/>
**AG-SWSEdt** https://github.com/anoxic83/AG_SWSEdt

# Requirements
**Python**

**Modules**<br/>
requests<br/>
bs4<br/>
numpy<br/>
pandas<br/>
pyqt5

# How to install
1. Install Python - https://www.python.org/downloads/

2. Install required modules
```
    pip install requests
    pip install bs4
    pip install numpy
    pip install pandas
    pip install pyqt5
```
# How to run
```
    py gui.py
```
# How to use it
1. Search for team on Transfermarkt.com 

2. Get team shortname and ID from URL - https://www.transfermarkt.com/nd-lendava-1903/startseite/verein/9233
    Example shortname: **nd-lendava-1903** and ID: **9233**

3. Enter shortname and ID into software - first two textboxes

![Step 1](https://i.ibb.co/pPBRywk/python-QPXv-Ly-I5-W6.png)

4. Click button **Get data from TM**

![Step 2](https://i.ibb.co/FH1708G/python-Zt-JNGd-Dwfr.png)

5. You will get all data you need

6. Right click on row (delete player, change skin, change position, ...)

![Step 3](https://i.ibb.co/Xzn1rjH/python-0oy-Gpc26-Bo.png)

7. Click button **Generate formation** and get formation for import - tab **SWOS csv**

![Step 4](https://i.ibb.co/tZ5sfYW/python-GNY9h-Hwxa-I.png)

8. Change first team (first 11 players) and bench players (from 12-16) in formation

![Step 5](https://i.ibb.co/F0dBnmB/python-Qkp2-L7hbmq.png)

9. Save to CSV file and import to SWOS Editors (e.g. **AG-SWSEdt**, SWOES2, ...)

![Step 6](https://i.ibb.co/02Zg3px/python-07a9vbrvp-M.png) 

# Changelog
| Version | Date | Changes |
|--|--|--|
| 1.0 | 30.12.2019 | **Release v1.0**<br/>First version SWOS TM Editor v1.0 |
| 1.0.1 | 31.12.2019 | New data folder structure<br/>Issue  #1 closed |
| 1.0.2 | 31.12.2019 | Check if URL exists<br/>Removed print's<br/>Other small changes |
| 1.1 | 3.1.2020 | **New minor version v1.1**<br/>Start application maximized<br/>Download and show player images<br/>Save image as data in array<br/>Added number of appearances, in squad and goals |
| 1.2 | 5.1.2020 | **New minor version v1.2**<br/>Summary of players position on the right side (tab Transfermarkt)<br/>In team must be at least 16 players (tab Transfermarkt)<br/>There must be at least 2 GK and minimum field players depending on the formation<br/>Position 1 and 12 is reserved for GK (tab SWOS csv)<br/>Fills Leagues ID SWOS and Team ID SWOS with 1<br/>Sorting by skill and minutes if sum of skills is same<br/>Bold rows for first 16 players in formation (export to csv)<br/>Fixed issues<br/>Other small changes |
| 1.3 | 20.1.2020 | **New minor version v1.3**<br/>Importing data from Futhead for skills calculation<br/>Downloading SQLite database with Futhead data<br/>Futhead parser (extra .py file)<br/>Fixed issues<br/>Other small changes |
| 1.3.1 | 10.2.2020 | URL correction to download Futhead skills database |
| 1.3.2 | 17.2.2020 | Possibility to change players country<br/>Control number players position based on formation<br/>URL trim whitespace on start or end of URL |
| 1.4 | 20.4.2020 | **New minor version v1.4**<br/>Editing data in table (no more need for right-click menu)<br/>Fixed issues<br/>Other small changes |
| 1.4.1 | 22.4.2020 | Bug fixed - national teams import<br/>Other small changes |
| 1.4.2 | 22.4.2020 | Prices CSV's corrected<br/>Quicker player deleting |
| 1.4.3 | 24.4.2020 | Fixed bug - if there is no coach<br/>Other changes |

# To-Do
| Version | Planned | Description | Done |
|--|--|--|--|
| 1.1.x | Q1 2020 | Summary of players position on the right side (tab Transfermarkt) | ![#c5f015](https://placehold.it/15/c5f015/000000?text=+) |
| 1.2 | Q1 2020 | In team must be at least 16 players (tab Transfermarkt) | ![#c5f015](https://placehold.it/15/c5f015/000000?text=+) |
| 1.2 | Q1 2020 | There must be at least 2 GK and minimum field players depending on the formation | ![#c5f015](https://placehold.it/15/c5f015/000000?text=+) |
| 1.2 | Q1 2020 | Position 1 and 12 is reserved for GK (tab SWOS csv) | ![#c5f015](https://placehold.it/15/c5f015/000000?text=+) |

# Download latest standalone version
https://github.com/boskorban/swostmeditor/releases

# Donations
http://paypal.me/boskorban

# Thanks to SensibleSoccer.de community 
Armandojimenez, Gatifun