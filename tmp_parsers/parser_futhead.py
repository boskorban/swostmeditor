from sqlite3 import Error
from bs4 import BeautifulSoup
import re
import requests
import pandas as pd
import unicodedata
import sqlite3
import ftplib
import os

def cleanText(text):
    tmp_name = text
    tmp_name = tmp_name.upper().replace("...", "").replace("'", " ")
    tmp_name = unicodedata.normalize('NFD', tmp_name).encode('ascii', 'ignore').decode('utf8')
    return tmp_name

# List Intializations
players = []
attributes = []

# Looping through all pages to retrieve players stats and information
FutHead = requests.get('https://www.futhead.com/20/players/?level=all_nif&bin_platform=pc')
bs = BeautifulSoup(FutHead.text, 'html.parser')
TotalPages = int(re.sub('\s +', '', str(bs.find('span', {'class': 'font-12 font-bold margin-l-r-10'}).get_text())).split(' ')[1])
print('Number of pages to be parsed for FIFA players: ' + str(TotalPages))
for page in range(1,  TotalPages + 1):
    FutHead = requests.get('https://www.futhead.com/20/players/?level=all_nif&page={}&bin_platform=pc'.format(str(page)))
    bs = BeautifulSoup(FutHead.text, 'html.parser')
    Stats = bs.findAll('span', {'class': 'player-stat stream-col-60 hidden-md hidden-sm'})
    Names = bs.findAll('span', {'class': 'player-name'})
    Information = bs.findAll('span', {'class': 'player-club-league-name'})
    Ratings = bs.findAll('span', {'class': re.compile('revision-gradient shadowed font-12')})
    num = len(bs.findAll('li', {'class': 'list-group-item list-group-table-row player-group-item dark-hover'}))

    # Parsing all players information
    tmp_name = ''
    for i in range(num):
        p = []
        p.append(cleanText(Names[i].get_text()))
        strong = Information[i].strong.extract()
        try:
            p.append(cleanText(re.sub('\s +', '', str(Information[i].get_text())).split('| ')[1]))
        except IndexError:
            p.append('')
        try:
            p.append(cleanText(re.sub('\s +', '', str(Information[i].get_text())).split('| ')[2]))
        except IndexError:
            p.append('')
        p.append(cleanText(strong.get_text()))
        p.append(Ratings[i].get_text())
        players.append(p)

    # Parsing all players stats
    temp = []
    for stat in Stats:
        if Stats.index(stat) % 6 == 0:
            if len(temp) > 0:
                attributes.append(temp)
            temp = []
        if stat.find('span', {'class': 'value'}) is None:
            pass
        else:
            temp.append(stat.find('span', {'class': 'value'}).get_text())
    print('Page ' + str(page) + ' is done!')

# Inserting data into its specific table
#tmp = 'NAME;CLUB;LEAGUE;POSITION;RATING;PACE;SHOOTING;PASSING;DRIBBLING;DEFENDING;PHYSICAL\n'
#for player, attribute in zip(players, attributes):
#    tmp = tmp + "{};{};{};{};{};{};{};{};{};{};{}\n".format(player[0], player[1], player[2], player[3], player[4], attribute[0], attribute[1], attribute[2], attribute[3], attribute[4], attribute[5])

#with open("output.csv", "w") as text_file:
#    text_file.write(tmp)

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
                                    physical integer NOT NULL
                                );"""


conn = None
try:
    conn = sqlite3.connect('players_futhead.db')

    if conn:
        c = conn.cursor()
        c.execute(sql_create_table)

        for player, attribute in zip(players, attributes):
            sql = "INSERT INTO players (name, club, league, position, rating, pace, shooting, passing, dribbling, defending, physical) VALUES ('{}','{}','{}','{}',{},{},{},{},{},{},{})".format(player[0], player[1], player[2], player[3], player[4], attribute[0], attribute[1], attribute[2], attribute[3], attribute[4], attribute[5])
            cur = conn.cursor()
            cur.execute(sql)
        conn.commit()
except Error as e:
    print(e)
finally:
    if conn:
        conn.close()

if os.path.exists("players_futhead.db"):
    session = ftplib.FTP('host', 'user', 'pass')
    file = open('players_futhead.db','rb')                  
    session.storbinary('STOR /public_html/swos_tm_db/players_futhead.db', file)     
    file.close()                                    
    session.quit()
    os.remove("players_futhead.db")
else:
    print("The file does not exist")