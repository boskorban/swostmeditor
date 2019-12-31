# SWOS Transfermarkt Editor

Download data from Transfermarkt.com and import in Amiga SWOS - https://sensiblesoccer.de/faq<br/><br/>
Software for import<br/>
**AG-SWSEdt** https://github.com/anoxic83/AG_SWSEdt

# Thanks to SensibleSoccer.de community 
Armandojimenez, Gatifun

# Changelog
|Version | Date | Changes |
|--|--|--|
|1.0| 30.12.2019 | First version - SWOS TM Editor v1.0 |
|1.0.1| 31.12.2019 | New data folder structure<br/>Issue  #1 closed |


# Requirements
**Modules**<br/>
requests<br/>
bs4<br/>
numpy<br/>
pandas<br/>
pyqt5

# How to install
1. Install Python - https://www.python.org/downloads/

2. Install requirements module
    ```
    pip install requests
    pip install bs4
    pip install numpy
    pip install pandas
    pip install pyqt5

# How to run
    py gui.py

# How to use it
1. Search for you team on Transfermarkt.com 

2. Get team shortname and ID from URL - https://www.transfermarkt.com/nd-lendava-1903/startseite/verein/9233
    Example shortname: **nd-lendava-1903** and ID: **9233**

3. Enter shortname and ID

![Step 1](https://i.ibb.co/pPBRywk/python-QPXv-Ly-I5-W6.png)

4. Click **Get data from TM**

![Step 2](https://i.ibb.co/FH1708G/python-Zt-JNGd-Dwfr.png)

5. You will get all data you need

6. Right click on row (delete player, change skin, change skin, ...)

![Step 3](https://i.ibb.co/Xzn1rjH/python-0oy-Gpc26-Bo.png)

7. Click **Generate formation** and get formation to import

![Step 4](https://i.ibb.co/tZ5sfYW/python-GNY9h-Hwxa-I.png)

8. Change players in formation

![Step 5](https://i.ibb.co/F0dBnmB/python-Qkp2-L7hbmq.png)

9. Save to CSV file and import to SWOS Editors (e.g. AG-SWSEdt, SWOES2, ...)

![Step 6](https://i.ibb.co/02Zg3px/python-07a9vbrvp-M.png) 

# Download latest standalone version
https://github.com/boskorban/swostmeditor/releases
