import re
import requests
import pandas as pd
import unicodedata
import sys
import smtplib
import os
from bs4 import BeautifulSoup
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

year = sys.argv[1]
tier = sys.argv[2] 
tier = int(tier) - 1
page_i = sys.argv[3]
location = sys.argv[4]

if not os.path.exists("{}\\files_{}".format(location, year)):
    os.makedirs("{}\\files_{}".format(location, year))

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
FutHead = requests.get('https://www.futhead.com/{}/players/?level={}_nif&bin_platform=pc'.format(year, tiers[tier]))
bs = BeautifulSoup(FutHead.text, 'html.parser')
TotalPages = int(re.sub('\s +', '', str(bs.find('span', {'class': 'font-12 font-bold margin-l-r-10'}).get_text())).split(' ')[1])
print('Number of pages to be parsed for FIFA {} players: {}'.format(tiers[tier], str(TotalPages)))
for page in range(int(page_i), TotalPages + 1): 
	FutHead = requests.get('https://www.futhead.com/{}/players/?level={}_nif&page={}&bin_platform=pc'.format(year, tiers[tier], str(page)))
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
		p[0] = Names[i].get_text() # not in use
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
		temp = [0, 0, '', '']
		while int(temp[0]) == 0 and int(temp[1]) == 0:
			FutHead_detail = requests.get('https://www.futhead.com/{}'.format(url['href']))
			bs = BeautifulSoup(FutHead_detail.text, 'html.parser')
			
			if temp[3] == '':
				Name = bs.find('span', {'class': 'info display-inline-block'}).find('small', {'class': 'firstname'})
				temp[3] = (Name.get_text().strip().upper() + ' ' + Name.next_sibling.strip().upper()).strip()

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

	print('Page {} of {} ({}) is done!'.format(str(page), str(TotalPages),  tiers[tier]))

	# Inserting data into its specific table
	tmp = 'NATIONAL;NAME;CLUB;LEAGUE;POSITION;RATING;PACE;SHOOTING;PASSING;DRIBBLING;DEFENDING;PHYSICAL;FINISHING;HEADING\n'
	for i in range(len(players)):
		try:
			tmp = tmp + "{};{};{};{};{};{};{};{};{};{};{};{};{};{}\n".format(extra_attributes[i][2], extra_attributes[i][3], players[i][1], players[i][2], players[i][3], players[i][4], attributes[i][0], attributes[i][1], attributes[i][2], attributes[i][3], attributes[i][4], attributes[i][5], extra_attributes[i][0], extra_attributes[i][1])
		except Error as e:
			print("Error: " + e + " - " + str(i))

	print("Saving files")

	with open("{}\\files_{}\\players_futhead_{}_{}_{}.csv".format(location, year, year, tier + 1, page), "w", encoding="utf-8") as text_file:
		text_file.write(tmp)

	players = []
	attributes = []
	extra_attributes = []

	print("File saved")

print("All done")