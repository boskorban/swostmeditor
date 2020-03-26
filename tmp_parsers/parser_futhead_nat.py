import re
import requests
import pandas as pd
import unicodedata
import sys
import smtplib
from bs4 import BeautifulSoup
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

year = sys.argv[1]

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
    FutHead = requests.get('https://www.futhead.com/{}/players/?level={}_nif&bin_platform=pc'.format(year, tier))
    bs = BeautifulSoup(FutHead.text, 'html.parser')
    TotalPages = int(re.sub('\s +', '', str(bs.find('span', {'class': 'font-12 font-bold margin-l-r-10'}).get_text())).split(' ')[1])
    print('Number of pages to be parsed for FIFA {} players: {}'.format(tier, str(TotalPages)))
    for page in range(1, TotalPages + 1): 
        FutHead = requests.get('https://www.futhead.com/{}/players/?level={}_nif&page={}&bin_platform=pc'.format(year, tier, str(page)))
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
            p[0] = Names[i].get_text()
            strong = Information[i].strong.extract()
            try:
                p[1] = re.sub('\s +', '', str(Information[i].get_text())).split('| ')[1]
            except IndexError:
                p[1] = ''
            try:
                p[2] = re.sub('\s +', '', str(Information[i].get_text())).split('| ')[2]
            except IndexError:
                p[2] = ''
            p[3] = strong.get_text()
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
            temp = [0, 0, '']
            while int(temp[0]) == 0 and int(temp[1]) == 0:
                FutHead_detail = requests.get('https://www.futhead.com/{}'.format(url['href']))
                bs = BeautifulSoup(FutHead_detail.text, 'html.parser')
                if temp[2] == '':
                    try:
	                    Nationality = bs.find('div', {'class': 'tab in'}).findAll('div', {'class': 'col-xs-5 player-sidebar-value'})[2]
	                    temp[2] = Nationality.get_text().strip().upper()
                    except:
                        temp[2] = ''
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

        print('Page {} of {} ({}) is done!'.format(str(page), str(TotalPages), tier))

print("Preparing data")

# Inserting data into its specific table
tmp = 'NATIONAL;NAME;CLUB;LEAGUE;POSITION;RATING;PACE;SHOOTING;PASSING;DRIBBLING;DEFENDING;PHYSICAL;FINISHING;HEADING\n'
for i in range(len(players)):
    try:
        tmp = tmp + "{};{};{};{};{};{};{};{};{};{};{};{};{};{}\n".format(extra_attributes[i][2], players[i][0], players[i][1], players[i][2], players[i][3], players[i][4], attributes[i][0], attributes[i][1], attributes[i][2], attributes[i][3], attributes[i][4], attributes[i][5], extra_attributes[i][0], extra_attributes[i][1])
    except Error as e:
        print("Error: " + e + " - " + str(i))

print("Saving files")

with open("players_futhead_{}.csv".format(year), "w", encoding="utf-8") as text_file:
    text_file.write(tmp)

print("File saved")

print("Preparing email")

port = 587
smtp_server = "smtp server"
sender_email = "email"
receiver_email = ["receiver1@xy.com","receiver2@xy.com"]
password = "pwd"
sporocilo = """<html>
<head></head>
<body>Futhead data in attachment</body>
</html>"""

msg = MIMEMultipart('alternative')
msg['Subject'] = "Futhead data - year 20{}".format(year)
msg['From'] = "email"
msg['To'] = "receiver1@xy.com;receiver2@xy.com"

part = MIMEText(sporocilo, 'html')

msg.attach(part)

print("Attaching CSV")

with open("players_futhead_{}.csv".format(year), "rb") as fil:
    part_file = MIMEApplication(fil.read(), Name=basename("players_futhead_{}.csv".format(year)))
    part_file['Content-Disposition'] = 'attachment; filename="{}"'.format(basename("players_futhead_{}.csv".format(year)))
    msg.attach(part_file)

print("Start sending email")

with smtplib.SMTP(smtp_server, port) as server:
	server.starttls()
	server.login(sender_email, password)
	server.sendmail(sender_email, receiver_email, msg.as_string())
	server.quit()

print("Email sent")