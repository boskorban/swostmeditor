from sqlite3 import Error
from bs4 import BeautifulSoup
import re
import requests
import pandas as pd
import unicodedata
import sqlite3
import ftplib
import os
from zipfile import ZipFile

def cleanText(text):
    tmp_name = text
    tmp_name = tmp_name.upper().replace("...", "").replace("'", " ")
    tmp_name = unicodedata.normalize('NFD', tmp_name).encode('ascii', 'ignore').decode('utf8')
    return tmp_name

# List Intializations
tiers = [
    'gold',
    'silver',
    'bronze'
]

players = []
attributes = []
extra_attributes = []

# Looping through all pages to retrieve players stats and information
for tier in tiers:
    FutHead = requests.get('https://www.futhead.com/20/players/?level={}_nif&bin_platform=pc'.format(tier))
    bs = BeautifulSoup(FutHead.text, 'html.parser')
    TotalPages = int(re.sub('\s +', '', str(bs.find('span', {'class': 'font-12 font-bold margin-l-r-10'}).get_text())).split(' ')[1])
    print('Number of pages to be parsed for FIFA {} players: {}'.format(tier, str(TotalPages)))
    for page in range(1, TotalPages + 1):
        FutHead = requests.get('https://www.futhead.com/20/players/?level={}_nif&page={}&bin_platform=pc'.format(tier, str(page)))
        bs = BeautifulSoup(FutHead.text, 'html.parser')
        Stats = bs.findAll('span', {'class': 'player-stat stream-col-60 hidden-md hidden-sm'})
        Names = bs.findAll('span', {'class': 'player-name'})
        Information = bs.findAll('span', {'class': 'player-club-league-name'})
        Ratings = bs.findAll('span', {'class': re.compile('revision-gradient shadowed font-12')})
        num = len(bs.findAll('li', {'class': 'list-group-item list-group-table-row player-group-item dark-hover'}))
        url_pages = bs.findAll('a', {'class': 'display-block padding-0'})

        # Parsing all players information
        tmp_name = ''
        for i in range(num):
            p = ['', '', '', 0, 0]
            p[0] = cleanText(Names[i].get_text())
            strong = Information[i].strong.extract()
            try:
                p[1] = cleanText(re.sub('\s +', '', str(Information[i].get_text())).split('| ')[1])
            except IndexError:
                p[1] = ''
            try:
                p[2] = cleanText(re.sub('\s +', '', str(Information[i].get_text())).split('| ')[2])
            except IndexError:
                p[2] = ''
            p[3] = cleanText(strong.get_text())
            p[4] = Ratings[i].get_text()
            players.append(p)

        # Parsing all players stats
        temp = [0, 0, 0, 0, 0, 0]
        i = 0
        for stat in Stats:
            if stat.find('span', {'class': 'value'}) is None:
                pass
            else:
                temp[i] = stat.find('span', {'class': 'value'}).get_text()
                i += 1

            if i == 6:
                attributes.append(temp)
                temp = [0, 0, 0, 0, 0, 0]
                i = 0

        for url in url_pages:
            temp = [0, 0]
            while int(temp[0]) == 0 and int(temp[1]) == 0:
                FutHead_detail = requests.get('https://www.futhead.com/{}'.format(url['href']))
                bs = BeautifulSoup(FutHead_detail.text, 'html.parser')
                Extra_Attr = bs.findAll('div', {'class': 'divided-row player-stat-row sm'})
                
                for attr in Extra_Attr:
                    tmp_skill = attr.find('span', {'class': 'player-stat-title'}).get_text()
                    if tmp_skill == 'Finishing':
                        tmp_value = attr.find('span', {'class': 'player-stat-title'}).findNext('span').get_text()
                        temp[0] = tmp_value
                    if tmp_skill == 'Heading':
                        tmp_value = attr.find('span', {'class': 'player-stat-title'}).findNext('span').get_text()
                        temp[1] = tmp_value

                if int(temp[0]) > 0 or int(temp[1]) > 0:
                    extra_attributes.append(temp)

            print('URL ' + url['href'] + ' is done!')

        print('Page {} ({}) is done!'.format(str(page), tier))

print("Preparing data")

# Inserting data into its specific table
tmp = 'NAME;CLUB;LEAGUE;POSITION;RATING;PACE;SHOOTING;PASSING;DRIBBLING;DEFENDING;PHYSICAL;FINISHING;HEADING\n'
tmp_sql = ''
for i in range(len(players)):
    try:
        tmp = tmp + "{};{};{};{};{};{};{};{};{};{};{};{};{}\n".format(players[i][0], players[i][1], players[i][2], players[i][3], players[i][4], attributes[i][0], attributes[i][1], attributes[i][2], attributes[i][3], attributes[i][4], attributes[i][5], extra_attributes[i][0], extra_attributes[i][1])
        tmp_sql = tmp_sql + "INSERT INTO players (name, club, league, position, rating, pace, shooting, passing, dribbling, defending, physical, finishing, heading) VALUES ('{}','{}','{}','{}',{},{},{},{},{},{},{},{},{});\n".format(players[i][0], players[i][1], players[i][2], players[i][3], players[i][4], attributes[i][0], attributes[i][1], attributes[i][2], attributes[i][3], attributes[i][4], attributes[i][5], extra_attributes[i][0], extra_attributes[i][1])
    except Error as e:
        print("Error: " + e + " - " + str(i))

print("Saving files")

with open("players_futhead.csv", "w") as text_file:
    text_file.write(tmp)
    
with open("players_futhead.sql", "w") as text_file:
    text_file.write(tmp_sql)

print("Files saved")

print("Preparing database")

sql_create_table = """CREATE TABLE IF NOT EXISTS players (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    club text,
                                    league text,
                                    position text,
                                    rating integer NOT NULL,
                                    pace integer NOT NULL,
                                    shooting integer NOT NULL,
                                    passing integer NOT NULL,
                                    dribbling integer NOT NULL,
                                    defending integer NOT NULL,
                                    physical integer NOT NULL,
                                    finishing integer NOT NULL,
                                    heading integer NOT NULL
                                );"""

conn = None
try:
    conn = sqlite3.connect('players_futhead.db')

    if conn:
        c = conn.cursor()
        c.execute(sql_create_table)
        c.executescript(tmp_sql)
        conn.commit()
except Error as e:
    print("Error: " + e)
finally:
    if conn:
        conn.close()

print("Databased saved")

print("Preparing for FTP upload")

if os.path.exists("players_futhead.db"):
    with ZipFile('players_futhead.zip','w') as zip: 
        zip.write('players_futhead.db') 

    session = ftplib.FTP('host', 'user', 'pass')
    file = open('players_futhead.zip','rb')                  
    session.storbinary('STOR players_futhead.zip', file)     
    file.close()                                    
    session.quit()

    os.remove("players_futhead.zip")
else:
    print("The file does not exist")

print("FTP upload completed")