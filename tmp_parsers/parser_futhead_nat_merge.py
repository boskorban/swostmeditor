import pandas as pd
import unicodedata
import sys
import smtplib
import os
import glob
import requests
import re
from bs4 import BeautifulSoup
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

year = sys.argv[1]
location = sys.argv[2]

tiers = [
	'gold', 
	'silver',
	'bronze'
]

sum_TotalPages = 0
for tier in tiers:
	FutHead = requests.get('https://www.futhead.com/{}/players/?level={}_nif&bin_platform=pc'.format(year, tier))
	bs = BeautifulSoup(FutHead.text, 'html.parser')
	TotalPages = int(re.sub('\s +', '', str(bs.find('span', {'class': 'font-12 font-bold margin-l-r-10'}).get_text())).split(' ')[1])
	print("Tier {} has {} pages".format(tier, TotalPages))
	sum_TotalPages += TotalPages

print("\n")

i_tier = 0
for ti in range(i_tier, 3):
	i = 0
	for file in os.listdir("{}\\files_{}".format(location, year)):
		if file.startswith('players_futhead_{}_{}'.format(year, ti + 1)):
			i += 1
	print("Tier {} has {} files".format(tiers[ti], i))

onlyfiles = next(os.walk("{}\\files_{}".format(location, year)))[2]
sum_Files = len(onlyfiles)

print("\n")
print("Must be {} files".format(sum_TotalPages))
print("It's {} files".format(sum_Files))

if sum_TotalPages == len(onlyfiles):
	print("Merging CSVs")

	os.chdir("{}\\files_{}".format(location, year))

	extension = 'csv'
	all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

	combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])

	combined_csv.to_csv("{}\\players_futhead_{}.csv".format(location, year), index=False, encoding='utf-8')

	print("Merging completed")

	print("Preparing email")

	port = 587
	smtp_server = "" # fill
	sender_email = "" # fill
	receiver_email = [] # fill  
	password = "" # fill
	sporocilo = """<html>
	<head></head>
	<body>Futhead data in attachment</body>
	</html>"""

	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Futhead data - year 20{}".format(year)
	msg['From'] = "" # fill
	msg['To'] = "" # fill

	part = MIMEText(sporocilo, 'html')

	msg.attach(part)

	print("Attaching CSV")

	with open("{}\\players_futhead_{}.csv".format(location, year), "rb") as fil:
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
else:
	print("It's missing {} files".format(sum_TotalPages - sum_Files))