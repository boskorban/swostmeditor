# FORMATIONS
# 4 4 2
# 5 4 1
# 4 5 1
# 5 3 2
# 3 5 2
# 4 3 3
# 4 2 4
# 3 4 3
# 5 2 3

from bs4 import BeautifulSoup
import csv, requests, sys, numpy as np, pandas, unicodedata, os, webbrowser, random, math

def returnSkillArray(n):
	array = []
	polje = 0
	min_value = math.trunc(n/7)

	for i in range(7):
		num = random.randint(min_value, 7)
		array.append(num)

	while sum(array) != n:
		if polje > 6:
			polje = 0
		if sum(array) < n:
			if array[polje] < 7:
				array[polje] += 1
			polje += 1
			continue
		if sum(array) > n:
			if array[polje] > 0:
				array[polje] -= 1
			polje += 1
			continue

	return array

def VrniFile(pozicija):
	if pozicija == 'RB' or pozicija == 'LB':
		return 'RBLB.csv'
	elif pozicija == 'RW' or pozicija == 'LW':
		return 'RWLW.csv'		
	else:
		return pozicija + '.csv'

def VrniDrzavo(drzava):
	with open('countries.csv', "r") as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=';')
		for row in csv_reader:
			if row[0] == drzava:
				return row[1]

def VrniPozicijo(pozicija):
	with open('roles.csv', "r") as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=';')
		for row in csv_reader:
			if row[1] == pozicija:
				return row[0]

def VrniCeno(pozicija, cena):
	with open(VrniFile(pozicija), "r") as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=';')
		for row in csv_reader:
			if float(row[2]) <= float(cena) and float(row[1]) >= float(cena):
				return row[0]

def VrniCenoSkill(pozicija, skill):
	with open(VrniFile(pozicija), "r") as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=';')
		for row in csv_reader:
			if int(row[3]) == int(skill):
				return row[0]

def VrniSkill(pozicija, cena):
	with open(VrniFile(pozicija), "r") as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=';')
		for row in csv_reader:
			if float(row[2]) <= float(cena) and float(row[1]) >= float(cena):
				return row[3]

team_name_tm = sys.argv[1]
team_id_tm = sys.argv[2]
team = sys.argv[3]
league = sys.argv[4]
defence = sys.argv[5]
midfield = sys.argv[6]
attack = sys.argv[7]
folder = sys.argv[8]

formation = "{}-{}-{}".format(defence, midfield, attack)

open_browser = input("Open page in browser (y/n)? ")
while not (open_browser == 'y' or open_browser == 'n'):
	open_browser = input("Open page in browser (y/n)? ")
if open_browser == 'y':
	webbrowser.open("https://www.transfermarkt.com/{}/startseite/verein/{}".format(team_name_tm, team_id_tm))

headers = {"User-Agent":"Mozilla/5.0"}
r = requests.get("https://www.transfermarkt.com/{}/startseite/verein/{}".format(team_name_tm, team_id_tm), headers=headers) #sys.argv[1]
r.encoding = r.apparent_encoding

soup = BeautifulSoup(r.text, 'html.parser')
zapisi = soup.find("table", {"class": "items"}).find("tbody").findAll("tr")

ekipa = soup.find("h1", {"itemprop": "name"}).span.text
ekipa = unicodedata.normalize('NFD', ekipa).encode('ascii', 'ignore').decode('utf8')
ekipa = ekipa.upper()

while len(ekipa) > 16:
	ekipa = input("Team name (" + ekipa + ") is too long. Enter new team name (max 16): ")
	ekipa = ekipa.upper()

trener = soup.find("div", {"class": "container-hauptinfo", "itemprop": "name"}).find("a").text
trener = unicodedata.normalize('NFD', trener).encode('ascii', 'ignore').decode('utf8')
trener = trener.upper()

while len(trener) > 24:
	trener = raw_input("Coach name (" + trener + ") is too long. Enter new coach name (max 24): ", trener)
	trener = trener.upper()

csv_file = ''
csv_file_formation = ''
csv_file_formation_full = ''

full_int = 1
full_arr = []

gk_arr = []
rb_arr = []
lb_arr = []
d_arr = []
m_arr = []
rw_arr = []
lw_arr = []
a_arr = []
r_arr = []

a_tmp_arr = []
m_tmp_arr = []

formation_arr = []

# general skin type
general_skin = ''
general_skin_type = input("Enter general skin type (1-White,2-Black,3-Blonde): ")
while not (general_skin_type == '1' or general_skin_type == '2' or general_skin_type == '3'):
	general_skin_type = input("Enter general skin type (1-White,2-Black,3-Blonde): ")
general_skin_type = int(general_skin_type)

if general_skin_type == 1:
	general_skin = 'White'
elif general_skin_type == 2:
	general_skin = 'Black'
elif general_skin_type == 3:
	general_skin = 'Blonde'

for zapis in zapisi:
	if zapis.find("td", {"class": "posrela"}) != None:
		igralec = zapis.find("td", {"class": "posrela"}).find("table", {"class": "inline-table"}).find("tr").find("td", {"class": "hauptlink"}).find("a").text
		igralec = unicodedata.normalize('NFD', igralec).encode('ascii', 'ignore').decode('utf8')
		igralec = igralec.upper()
		pozicija = zapis.find("td", {"class": "posrela"}).find("table", {"class": "inline-table"}).findAll("tr")[1].find("td").text
		drzavljanstvo = zapis.findAll("td")[7].find("img")["title"]
		cena = zapis.findAll("td")[8].text
		cena_div = int(cena.replace("€", "").replace("k", "000").replace("m", "0000").replace(".", "")) / 1000000
		posi = VrniPozicijo(pozicija)
		cena_swos = VrniCeno(posi, cena_div)

		_sum = int(VrniSkill(posi, cena_div))

		rnd_array = returnSkillArray(_sum)
		
		if posi == 'GK':
			pa = 0
			ve = 0
			he = 0
			ta = 0
			co = 0
			sp = 0
			fi = 0
		else:
			pa = rnd_array[0]
			ve = rnd_array[1]
			he = rnd_array[2]
			ta = rnd_array[3]
			co = rnd_array[4]
			sp = rnd_array[5]
			fi = rnd_array[6]

		#print("Player: {}, position: {}, nation: {}, price: {}".format(igralec, pozicija, drzavljanstvo, cena))
		#csv_file = csv_file + "{},,{},{},White,{},{},{},{},{},{},{},{}\n".format(VrniDrzavo(drzavljanstvo), igralec, posi, pa, ve, he, ta, co, sp, fi, cena_swos)
		# napolni skupni array
		full_arr.append([full_int, VrniDrzavo(drzavljanstvo), igralec, posi, general_skin, pa, ve, he, ta, co, sp, fi, cena_swos, _sum, cena_div, 0])
		full_int += 1

headers = {"User-Agent":"Mozilla/5.0"}
r = requests.get("https://www.transfermarkt.com/{}/leistungsdaten/verein/{}".format(team_name_tm, team_id_tm), headers=headers)
r.encoding = r.apparent_encoding

soup = BeautifulSoup(r.text, 'html.parser')
zapisi_minute = soup.find("table", {"class": "items"}).find("tbody").findAll("tr")

for zapis in zapisi_minute:
	if zapis.find("td", {"class": "posrela"}) != None:
		igralec = zapis.find("td", {"class": "posrela"}).find("table", {"class": "inline-table"}).find("tr").find("td", {"class": "hauptlink"}).find("a").text
		igralec = unicodedata.normalize('NFD', igralec).encode('ascii', 'ignore').decode('utf8')
		igralec = igralec.upper()
		minute = zapis.find("td", {"class": "rechts"}).text
		minute = minute.replace(".", "").replace("'", "").replace("-", "0")
		minute = int(minute)

		for igrac in full_arr:
			if igrac[2] == igralec:
				igrac[15] = minute
				continue

# kontrola dolžine imena igralca
for igralec in full_arr:
	igralec_name = igralec[2]
	while len(igralec_name) > 22:
		igralec_name = input("Player name (" + igralec_name + ") is too long. Enter new player name (max 22): ")
		igralec_name = igralec_name.upper()
	igralec[2] = igralec_name
	continue


header = " - TEAM: {}, COACH: {}, FORMATION: {}".format(ekipa, trener, formation)
print("ALL PLAYERS" + header)
for igralec in full_arr:
	print(igralec)


sprememba_delete_minute = input("\nDo you want to delete players without minutes (y/n)? ")
while sprememba_delete_minute != 'y' and sprememba_delete_minute != 'n':
	sprememba_delete_minute = input("\nDo you want to delete players without minutes (y/n)? ")

if sprememba_delete_minute == 'y':
	delete_minute = input("\nHow many minutes? ")
	while not delete_minute.isdigit():
		delete_minute = input("How many minutes? ")
	while int(delete_minute) < 0:
		delete_minute = input("How many minutes? ")
	delete_minute = int(delete_minute)

	for igralec in full_arr:
		if igralec[15] <= delete_minute:
			print(igralec)

	delete_it = input("\nDo you want to delete these players (y/n)? ")
	while delete_it != 'y' and sprememba_delete_minute != 'n':
		delete_it = input("\nDo you want to delete these players (y/n)? ")

	if delete_it == 'y':
		tmp_full_arr = []
		for igralec in full_arr:
			if igralec[15] > delete_minute:
				tmp_full_arr.append(igralec)

		int_id = 1
		for igralec in tmp_full_arr:
			igralec[0] = int_id
			int_id += 1
			
		full_arr = []
		full_arr = tmp_full_arr.copy()

print("ALL PLAYERS" + header)
for igralec in full_arr:
	print(igralec)

sprememba_delete = input("\nDo you want to delete players (y/n)? ")
while sprememba_delete != 'y' and sprememba_delete != 'n':
	sprememba_delete = input("\nDo you want to delete players (y/n)? ")

while sprememba_delete == 'y':
	delete_row = input("Enter player ID to delete: ")
	while not delete_row.isdigit():
		delete_row = input("Enter player ID to delete: ")
	while int(delete_row) < 1 or int(delete_row) > len(full_arr):
		delete_row = input("Enter player ID to delete: ")
	delete_row = int(delete_row) - 1

	i = 1
	delete_player = full_arr[delete_row][2]
	delete_position = full_arr[delete_row][3]

	full_arr.pop(delete_row)

	for igralec in full_arr:
		igralec[0] = i
		i += 1

	print("\nPlayer {} ({}), position {} was deleted".format(delete_player, delete_position, delete_row + 1))

	print("\nALL PLAYERS" + header)
	for igralec in full_arr:
		print(igralec)

	sprememba_delete = input("\nDo you want to delete more players (y/n)? ")
	while sprememba_delete != 'y' and sprememba_delete != 'n':
		sprememba_delete = input("\nDo you want to delete more players (y/n)? ")

# position
sprememba_position = input("\nDo you want to change players position (y/n)? ")
while sprememba_position != 'y' and sprememba_position != 'n':
	sprememba_position = input("\nDo you want to change players position (y/n)? ")

while sprememba_position == 'y':
	position_row = input('Enter player ID for position change: ')
	while not position_row.isdigit():
		position_row = input('Enter player ID for position change: ')
	while int(position_row) < 1 or int(position_row) > len(full_arr):
		position_row = input('Enter player ID for position change: ')
	position_row = int(position_row) - 1

	position_new = input("Enter new position (GK, RB, D, LB, RW, M, LW, A): ").upper()
	while not (position_new == 'GK' or position_new == 'RB' or position_new == 'D' or position_new == 'LB' or position_new == 'RW' or position_new == 'M' or position_new == 'LW' or position_new == 'A'):
		position_new = input("Enter new position (GK, RB, D, LB, RW, M, LW, A): ").upper()

	position_player = full_arr[position_row][2]
	position_old = full_arr[position_row][3]

	cena_swos_tmp = VrniCeno(position_new, full_arr[position_row][14])

	_sum_tmp = int(VrniSkill(position_new, full_arr[position_row][14]))

	rnd_array_tmp = returnSkillArray(_sum)
	if position_new == 'GK':
		pa_tmp = 0
		ve_tmp = 0
		he_tmp = 0
		ta_tmp = 0
		co_tmp = 0
		sp_tmp = 0
		fi_tmp = 0
	else:
		pa_tmp = rnd_array[0]
		ve_tmp = rnd_array[1]
		he_tmp = rnd_array[2]
		ta_tmp = rnd_array[3]
		co_tmp = rnd_array[4]
		sp_tmp = rnd_array[5]
		fi_tmp = rnd_array[6]

	full_arr[position_row][3] = position_new
	full_arr[position_row][5] = pa_tmp
	full_arr[position_row][6] = ve_tmp
	full_arr[position_row][7] = he_tmp
	full_arr[position_row][8] = ta_tmp
	full_arr[position_row][9] = co_tmp
	full_arr[position_row][10] = sp_tmp
	full_arr[position_row][11] = fi_tmp
	full_arr[position_row][12] = cena_swos_tmp
	full_arr[position_row][13] = _sum_tmp

	print("\nPlayer {} position was changed from {} to {}".format(position_player, position_old, position_new))

	print("\nALL PLAYERS" + header)
	for igralec in full_arr:
		print(igralec)

	sprememba_position = input("\nDo you want to change more players position (y/n)? ")
	while sprememba_position != 'y' and sprememba_position != 'n':
		sprememba_position = input("\nDo you want to change more players position (y/n)? ")


print("\nALL PLAYERS" + header)
for igralec in full_arr:
	print(igralec)

# skill
sprememba_skill = input("\nDo you want to change players skill value (y/n)? ")
while sprememba_skill != 'y' and sprememba_skill != 'n':
	sprememba_skill = input("\nDo you want to change players skill value (y/n)? ")

while sprememba_skill == 'y':
	skill_row = input('Enter player ID for skills value change: ')
	while not skill_row.isdigit():
		skill_row = input('Enter player ID for skill value change: ')
	while int(skill_row) < 1 or int(skill_row) > len(full_arr):
		skill_row = input("Enter player ID for skill value change: ")
	skill_row = int(skill_row) - 1

	skill_new = input("Enter new skill value: ")
	while not skill_new.isdigit():
		while not int(skill_new) <= 49 and int(skill_new) >= 0:
			position_new = input("Enter new skill value: ").upper()
	skill_new = int(skill_new)

	skill_player = full_arr[skill_row][2]
	skill_old = full_arr[skill_row][13]

	cena_swos_tmp_skill = VrniCenoSkill(full_arr[skill_row][3], skill_new) # vrni ceno na podlagi skilla

	rnd_array_tmp_skill = returnSkillArray(skill_new)
	if full_arr[skill_row][3] == 'GK':
		pa_tmp_skill = 0
		ve_tmp_skill = 0
		he_tmp_skill = 0
		ta_tmp_skill = 0
		co_tmp_skill = 0
		sp_tmp_skill = 0
		fi_tmp_skill = 0
	else:
		pa_tmp_skill = rnd_array_tmp_skill[0]
		ve_tmp_skill = rnd_array_tmp_skill[1]
		he_tmp_skill = rnd_array_tmp_skill[2]
		ta_tmp_skill = rnd_array_tmp_skill[3]
		co_tmp_skill = rnd_array_tmp_skill[4]
		sp_tmp_skill = rnd_array_tmp_skill[5]
		fi_tmp_skill = rnd_array_tmp_skill[6]

	full_arr[skill_row][5] = pa_tmp_skill
	full_arr[skill_row][6] = ve_tmp_skill
	full_arr[skill_row][7] = he_tmp_skill
	full_arr[skill_row][8] = ta_tmp_skill
	full_arr[skill_row][9] = co_tmp_skill
	full_arr[skill_row][10] = sp_tmp_skill
	full_arr[skill_row][11] = fi_tmp_skill
	full_arr[skill_row][12] = cena_swos_tmp_skill
	full_arr[skill_row][13] = skill_new

	print("\nPlayer {} skill value was changed from {} to {}".format(skill_player, skill_old, skill_new))

	print("\nALL PLAYERS" + header)
	for igralec in full_arr:
		print(igralec)

	sprememba_skill = input("\nDo you want to change more players skill values (y/n)? ")
	while sprememba_skill != 'y' and sprememba_skill != 'n':
		sprememba_skill = input("\nDo you want to change more players skill values (y/n)? ")


print("\nALL PLAYERS" + header)
for igralec in full_arr:
	print(igralec)


sprememba_skin = input("\nDo you want to change skins (y/n)? ")
while sprememba_skin != 'y' and sprememba_skin != 'n':
	sprememba_skin = input("\nDo you want to change skins (y/n)? ")

while sprememba_skin == 'y':
	skin_row = input('Enter player ID for skin change: ')
	while not skin_row.isdigit():
		skin_row = input('Enter player ID for skin change: ')
	while int(skin_row) < 1 or int(skin_row) > len(full_arr):
		skin_row = input("Enter player ID for skin change: ")
	skin_row = int(skin_row) - 1

	skin_type = input("Enter skin type (1-White,2-Black,3-Blonde): ")
	while not (skin_type == '1' or skin_type == '2' or skin_type == '3'):
		skin_type = input("Enter skin type (1-White,2-Black,3-Blonde): ")
	skin_type = int(skin_type)

	skin_player = full_arr[skin_row][2]
	skin_old = full_arr[skin_row][4]

	if skin_type == 1:
		full_arr[skin_row][4] = 'White'
	elif skin_type == 2:
		full_arr[skin_row][4] = 'Black'
	elif skin_type == 3:
		full_arr[skin_row][4] = 'Blonde'

	skin_new = full_arr[skin_row][4]

	print("\nSkin of {} was changed from {} to {}".format(skin_player, skin_old, skin_new))

	print("\nALL PLAYERS" + header)
	for igralec in full_arr:
		print(igralec)

	sprememba_skin = input("\nDo you want to change more skins (y/n)? ")
	while sprememba_skin != 'y' and sprememba_skin != 'n':
		sprememba_skin = input("\nDo you want to change more skins (y/n)? ")


print("Sorting players ...")

for igralec in full_arr:
	if igralec[3] == 'GK':
		gk_arr.append([igralec[1], igralec[2], igralec[3], igralec[4], igralec[5], igralec[6], igralec[7], igralec[8], igralec[9], igralec[10], igralec[11], igralec[12], igralec[13], igralec[15]])
	elif igralec[3] == 'RB':
		rb_arr.append([igralec[1], igralec[2], igralec[3], igralec[4], igralec[5], igralec[6], igralec[7], igralec[8], igralec[9], igralec[10], igralec[11], igralec[12], igralec[13], igralec[15]])
	elif igralec[3] == 'LB':
		lb_arr.append([igralec[1], igralec[2], igralec[3], igralec[4], igralec[5], igralec[6], igralec[7], igralec[8], igralec[9], igralec[10], igralec[11], igralec[12], igralec[13], igralec[15]])
	elif igralec[3] == 'D':
		d_arr.append([igralec[1], igralec[2], igralec[3], igralec[4], igralec[5], igralec[6], igralec[7], igralec[8], igralec[9], igralec[10], igralec[11], igralec[12], igralec[13], igralec[15]])
	elif igralec[3] == 'M':
		m_arr.append([igralec[1], igralec[2], igralec[3], igralec[4], igralec[5], igralec[6], igralec[7], igralec[8], igralec[9], igralec[10], igralec[11], igralec[12], igralec[13], igralec[15]])
	elif igralec[3] == 'RW':
		rw_arr.append([igralec[1], igralec[2], igralec[3], igralec[4], igralec[5], igralec[6], igralec[7], igralec[8], igralec[9], igralec[10], igralec[11], igralec[12], igralec[13], igralec[15]])
	elif igralec[3] == 'LW':
		lw_arr.append([igralec[1], igralec[2], igralec[3], igralec[4], igralec[5], igralec[6], igralec[7], igralec[8], igralec[9], igralec[10], igralec[11], igralec[12], igralec[13], igralec[15]])
	elif igralec[3] == 'A':
		a_arr.append([igralec[1], igralec[2], igralec[3], igralec[4], igralec[5], igralec[6], igralec[7], igralec[8], igralec[9], igralec[10], igralec[11], igralec[12], igralec[13], igralec[15]])

print("OK")

print("Creating formation ...")

# vratar
df_gk = pandas.DataFrame(gk_arr, columns=['A','B','C','D','E','F','G','H','I','J','K','L','M','N'])
tmp = gk_arr[df_gk['M'].idxmax()]
formation_arr.append([tmp[0], 1, tmp[1], tmp[2], tmp[3], tmp[4], tmp[5], tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], tmp[12], tmp[13]])
gk_arr.pop(df_gk['M'].idxmax())

# obramba
for x in range(int(defence) - 2):
	df_d = pandas.DataFrame(d_arr, columns=['A','B','C','D','E','F','G','H','I','J','K','L','M','N'])
	tmp = d_arr[df_d['M'].idxmax()]
	formation_arr.append([tmp[0], 3 + x, tmp[1], tmp[2], tmp[3], tmp[4], tmp[5], tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], tmp[12], tmp[13]])
	d_arr.pop(df_d['M'].idxmax())

# desni back
if len(rb_arr) > 0:
	df_rb = pandas.DataFrame(rb_arr, columns=['A','B','C','D','E','F','G','H','I','J','K','L','M','N'])
	tmp = rb_arr[df_rb['M'].idxmax()]
	formation_arr.insert(1, [tmp[0], 2, tmp[1], tmp[2], tmp[3], tmp[4], tmp[5], tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], tmp[12], tmp[13]])
	rb_arr.pop(df_rb['M'].idxmax())
else:
	df_d = pandas.DataFrame(d_arr, columns=['A','B','C','D','E','F','G','H','I','J','K','L','M','N'])
	tmp = d_arr[df_d['M'].idxmax()]
	formation_arr.insert(1, [tmp[0], 2, tmp[1], tmp[2], tmp[3], tmp[4], tmp[5], tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], tmp[12], tmp[13]])
	d_arr.pop(df_d['M'].idxmax())

# levi back
if len(lb_arr) > 0:
	df_lb = pandas.DataFrame(lb_arr, columns=['A','B','C','D','E','F','G','H','I','J','K','L','M','N'])
	tmp = lb_arr[df_lb['M'].idxmax()]
	formation_arr.append([tmp[0], int(defence) + 1, tmp[1], tmp[2], tmp[3], tmp[4], tmp[5], tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], tmp[12], tmp[13]])
	lb_arr.pop(df_lb['M'].idxmax())
else:
	df_d = pandas.DataFrame(d_arr, columns=['A','B','C','D','E','F','G','H','I','J','K','L','M','N'])
	tmp = d_arr[df_d['M'].idxmax()]
	formation_arr.append([tmp[0], int(defence) + 1, tmp[1], tmp[2], tmp[3], tmp[4], tmp[5], tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], tmp[12], tmp[13]])
	d_arr.pop(df_d['M'].idxmax())

# sredina
if int(midfield) == 2:
	m_tmp_arr = m_arr + rw_arr + lw_arr
	for x in range(2):
		df_m = pandas.DataFrame(m_tmp_arr, columns=['A','B','C','D','E','F','G','H','I','J','K','L','M','N'])
		tmp = m_tmp_arr[df_m['M'].idxmax()]
		formation_arr.append([tmp[0], int(defence) + 2 + x, tmp[1], tmp[2], tmp[3], tmp[4], tmp[5], tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], tmp[12], tmp[13]])
		m_tmp_arr.pop(df_m['M'].idxmax())
else: # več kot 2 v sredini
	for x in range(int(midfield) - 2):
		df_m = pandas.DataFrame(m_arr, columns=['A','B','C','D','E','F','G','H','I','J','K','L','M','N'])
		tmp = m_arr[df_m['M'].idxmax()]
		formation_arr.append([tmp[0], int(defence) + 3 + x, tmp[1], tmp[2], tmp[3], tmp[4], tmp[5], tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], tmp[12], tmp[13]])
		m_arr.pop(df_m['M'].idxmax())

	# desni winger
	if len(rw_arr) > 0:
		df_rw = pandas.DataFrame(rw_arr, columns=['A','B','C','D','E','F','G','H','I','J','K','L','M','N'])
		tmp = rw_arr[df_rw['M'].idxmax()]
		formation_arr.insert(int(defence) + 1, [tmp[0], int(defence) + 2, tmp[1], tmp[2], tmp[3], tmp[4], tmp[5], tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], tmp[12], tmp[13]])
		rw_arr.pop(df_rw['M'].idxmax())
	else:
		df_m = pandas.DataFrame(m_arr, columns=['A','B','C','D','E','F','G','H','I','J','K','L','M','N'])
		tmp = m_arr[df_m['M'].idxmax()]
		formation_arr.insert(int(defence) + 1, [tmp[0], int(defence) + 2, tmp[1], tmp[2], tmp[3], tmp[4], tmp[5], tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], tmp[12], tmp[13]])
		m_arr.pop(df_m['M'].idxmax())

	# levi back
	if len(lw_arr) > 0:
		df_lw = pandas.DataFrame(lw_arr, columns=['A','B','C','D','E','F','G','H','I','J','K','L','M','N'])
		tmp = lw_arr[df_lw['M'].idxmax()]
		formation_arr.append([tmp[0], int(defence) + int(midfield) + 1, tmp[1], tmp[2], tmp[3], tmp[4], tmp[5], tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], tmp[12], tmp[13]])
		lw_arr.pop(df_lw['M'].idxmax())
	else:
		df_lw = pandas.DataFrame(m_arr, columns=['A','B','C','D','E','F','G','H','I','J','K','L','M','N'])
		tmp = m_arr[df_lw['M'].idxmax()]
		formation_arr.append([tmp[0], int(defence) + int(midfield) + 1, tmp[1], tmp[2], tmp[3], tmp[4], tmp[5], tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], tmp[12], tmp[13]])
		m_arr.pop(df_lw['M'].idxmax())	

# napad
if len(a_arr) < int(attack):
	if int(midfield) == 2:
		a_tmp_arr = a_arr + m_tmp_arr
	else:
		a_tmp_arr = a_arr + rw_arr + lw_arr
else: 
	a_tmp_arr = a_arr.copy()

for x in range(int(attack)):
	df_a = pandas.DataFrame(a_tmp_arr, columns=['A','B','C','D','E','F','G','H','I','J','K','L','M','N'])
	tmp = a_tmp_arr[df_a['M'].idxmax()]
	formation_arr.append([tmp[0], int(defence) + int(midfield) + 2 + x, tmp[1], tmp[2], tmp[3], tmp[4], tmp[5], tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], tmp[12], tmp[13]])
	a_tmp_arr.pop(df_a['M'].idxmax())

# rezerve - vratar
df_gk = pandas.DataFrame(gk_arr, columns=['A','B','C','D','E','F','G','H','I','J','K','L','M','N'])
tmp = gk_arr[df_gk['M'].idxmax()]
formation_arr.append([tmp[0], 12, tmp[1], tmp[2], tmp[3], tmp[4], tmp[5], tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], tmp[12], tmp[13]])
gk_arr.pop(df_gk['M'].idxmax())

# rezerve - ostali
if int(midfield) == 2 and len(a_arr) < int(attack):
	r_arr = rb_arr + lb_arr + d_arr + a_tmp_arr
elif int(midfield) == 2:
	r_arr = rb_arr + lb_arr + d_arr + m_tmp_arr + a_tmp_arr
elif len(a_arr) < int(attack):
	r_arr = rb_arr + lb_arr + d_arr + m_arr + a_tmp_arr
else:
	r_arr = rb_arr + lb_arr + d_arr + m_arr + rw_arr + lw_arr + a_tmp_arr

for x in range(4):
	df_r = pandas.DataFrame(r_arr, columns=['A','B','C','D','E','F','G','H','I','J','K','L','M','N'])
	tmp = r_arr[df_r['M'].idxmax()]
	formation_arr.append([tmp[0], 13 + x, tmp[1], tmp[2], tmp[3], tmp[4], tmp[5], tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], tmp[12], tmp[13]])
	r_arr.pop(df_r['M'].idxmax())

# rezerve - izven
r_arr = gk_arr + r_arr
for x in range(len(r_arr)):
	df_r = pandas.DataFrame(r_arr, columns=['A','B','C','D','E','F','G','H','I','J','K','L','M','N'])
	tmp = r_arr[df_r['M'].idxmax()]
	formation_arr.append([tmp[0], 17 + x, tmp[1], tmp[2], tmp[3], tmp[4], tmp[5], tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], tmp[12], tmp[13]])
	r_arr.pop(df_r['M'].idxmax())

print("OK")

print("\n\nFORMATION" + header)
for igralec in formation_arr:
	print(igralec)

# postava
sprememba_postava = input("\nDo you want to make changes in formation (y/n)? ")
while sprememba_postava != 'y' and sprememba_postava != 'n':
	sprememba_postava = input("\nDo you want to make changes in formation (y/n)? ")

while sprememba_postava == 'y':
	player_one = input("Enter ID of first player: ")
	while not player_one.isdigit():
		player_one = input("Enter ID of first player: ")
	while int(player_one) < 1 or int(player_one) > len(full_arr):
		player_one = input("Enter ID of first player: ")
	player_one = int(player_one) - 1

	player_two = input("Enter ID of second player: ")
	while not player_two.isdigit():
		player_two = input("Enter ID of second player: ")
	while int(player_two) < 1 or int(player_two) > len(full_arr):
		player_two = input("Enter ID of second player: ")
	player_two = int(player_two) - 1

	arr_player_one = formation_arr[player_one]
	arr_player_two = formation_arr[player_two]

	formation_arr[player_one] = arr_player_two
	formation_arr[player_two] = arr_player_one
	
	formation_arr[player_one][1] = player_one + 1
	formation_arr[player_two][1] = player_two + 1

	print("\nPlayer {} was replaced with {}".format(formation_arr[player_one][2], formation_arr[player_two][2]))

	print("\nFORMATION" + header)
	for igralec in formation_arr:
		print(igralec)

	sprememba_postava = input("\nDo you want to make some more changes in formation (y/n)? ")
	while sprememba_postava != 'y' and sprememba_postava != 'n':
		sprememba_postava = input("\nDo you want to make some more changes in formation (y/n)? ")

csv_file_head = "{},{},{},{},{},,,,,,,,".format(ekipa, league, team, formation, trener)
csv_file_formation_full = csv_file_head + "\n"
for igralec in formation_arr:
	csv_file_formation_full = csv_file_formation_full + "{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(igralec[0], igralec[1], igralec[2], igralec[3], igralec[4], igralec[5], igralec[6], igralec[7], igralec[8], igralec[9], igralec[10], igralec[11], igralec[12])

csv_file_formation = csv_file_head + "\n"
for igralec in formation_arr[:16]:
	csv_file_formation = csv_file_formation + "{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(igralec[0], igralec[1], igralec[2], igralec[3], igralec[4], igralec[5], igralec[6], igralec[7], igralec[8], igralec[9], igralec[10], igralec[11], igralec[12])

print("\n\n")
#print("ALL PLAYERS - {}_manual.csv".format(ekipa))
#print(csv_file)
#print("\n")
print("FORMATION FULL{} - {}_full.csv".format(header, ekipa))
print(csv_file_formation_full)
print("\n")
print("FORMATION{} - {}.csv".format(header, ekipa))
print(csv_file_formation)

save_csv = input("Save to CSVs (y/n)? ")
while save_csv != 'y' and save_csv != 'n':
	save_csv = input("\nSave to CSVs (y/n)? ")

if save_csv == 'y':
	print("Saving files to csv files ...")

	filename = "{}\\{}\\{}.csv".format(folder, ekipa, ekipa)
#	filename_manual = "{}\\{}\\{}_manual.csv".format(folder, ekipa, ekipa)
	filename_full = "{}\\{}\\{}_full.csv".format(folder, ekipa, ekipa)
	if not os.path.exists(os.path.dirname(filename)):
	    try:
	        os.makedirs(os.path.dirname(filename))
	    except OSError as exc:
	        if exc.errno != errno.EEXIST:
	            raise

#	with open(filename_manual, "w") as text_file:
#	    text_file.write(csv_file)

#	print("Saving {}".format(filename_manual))

	with open(filename, "w") as text_file:
	    text_file.write(csv_file_formation)

	print("Saving {}".format(filename))

	with open(filename_full, "w") as text_file:
	    text_file.write(csv_file_formation_full)

	print("Saving {}".format(filename_full))

	print("All saved")