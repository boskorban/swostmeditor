import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
import unicodedata
import sqlite3
from sqlite3 import Error

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
        tmp_name = Names[i].get_text().upper()
        tmp_name = tmp_name.replace("...", "").replace("'", " ")
        tmp_name = unicodedata.normalize('NFD', tmp_name).encode('ascii', 'ignore').decode('utf8')
        p.append(tmp_name)
        strong = Information[i].strong.extract()
        try:
            p.append(re.sub('\s +', '', str(Information[i].get_text())).split('| ')[1].upper())
        except IndexError:
            p.append('')
        try:
            p.append(re.sub('\s +', '', str(Information[i].get_text())).split('| ')[2].upper())
        except IndexError:
            p.append('')
        p.append(strong.get_text().upper())
        p.append(Ratings[i].get_text().upper())
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