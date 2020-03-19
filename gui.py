# Code create by BOCo23 https://github.com/boskorban

from PyQt5.QtWidgets import *
from PyQt5 import *
from PyQt5.QtGui import *
from urllib.request import urlopen
from bs4 import BeautifulSoup
from os import walk
from sqlite3 import Error
import csv
import requests
import sys
import numpy as np
import pandas
import unicodedata
import os
import webbrowser
import random
import math
import ftplib
import sqlite3
from zipfile import ZipFile


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


def getFile(position):
    if position == 'RB' or position == 'LB':
        return 'data\\RBLB.csv'
    elif position == 'RW' or position == 'LW':
        return 'data\\RWLW.csv'
    else:
        return 'data\\{}.csv'.format(position)


def getCountry(drzava):
    with open('data\\countries.csv', "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            if row[0] == drzava:
                return row[1]
    return "XYZ"


def getPosition(position):
    with open('data\\roles.csv', "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            if row[1] == position:
                return row[0]


def getPrice(position, price):
    with open(getFile(position), "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            if float(row[2]) <= float(price) and float(row[1]) >= float(price):
                return row[0]


def getPriceSkill(position, skill):
    with open(getFile(position), "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            if int(row[3]) == int(skill):
                return row[0]


def getSkill(position, price):
    with open(getFile(position), "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            if float(row[2]) <= float(price) and float(row[1]) >= float(price):
                return row[3]


def getPriceFuthead(rating):
    with open('data\\fut_swos.csv', "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            if int(row[0]) == int(rating):
                return row[1]

# function to watch same sum of skills and more minutes
def getTopPlayer(array_player, id_player):
    index_array = 0
    return_index = id_player
    arr_player = array_player[return_index]

    for igralec in array_player:
        if arr_player[12] == igralec[12]: #skills
            if arr_player[13] < igralec[13]: #minutes
                arr_player = igralec
                return_index = index_array
        index_array += 1

    return int(return_index)

def getFutheadSwosSkillArray(rating, sp, ve, pa, co, ta, fi, he):
    rtn_array = [sp, ve, pa, co, ta, fi, he]

    sum_swos = sp + ve + pa + co + ta + fi + he
    tmp_swos = int(rating / 2)
    difference_swos = tmp_swos - sum_swos

    arr_int = 0
    while difference_swos != 0:
        if arr_int > 6:
            arr_int = 0

        if rtn_array[arr_int] == 7:
            arr_int += 1
            continue

        if difference_swos > 0:
            rtn_array[arr_int] += 1
            difference_swos -= 1
            arr_int += 1
        elif difference_swos < 0:
            rtn_array[arr_int] -= 1
            difference_swos += 1
            arr_int += 1

    return rtn_array     

def getFutheadSwosSkill(skill):
    if skill <= 13:
        return 1
    elif skill >= 14 and skill <= 27:
        return 2
    elif skill >= 28 and skill <= 41:
        return 3
    elif skill >= 42 and skill <= 56:
        return 4
    elif skill >= 57 and skill <= 71:
        return 5
    elif skill >= 72 and skill <= 86:
        return 6
    elif skill >= 87:
        return 7


def alert_popup(text):
    alert = QMessageBox()
    alert.setText(text)
    alert.exec_()


def on_btn_generate_clicked():
    global full_arr
    global formation_arr

    while len(formation_arr) > 0:
        formation_arr.pop(0)

    player_long = ''

    for igralec in full_arr:
        if len(igralec[2]) > 22:
            if player_long != '':
                player_long = player_long + ', '
            player_long = player_long + igralec[2]

    if len(ed_team_name_tm.text()) > 16:
        alert_popup("Team name too long (max 16)")
    elif ed_team_name_tm.text() == '':
        alert_popup("Team name is empty")
    elif len(ed_coach_name_tm.text()) > 24:
        alert_popup("Coach name too long (max 24)")
    elif ed_coach_name_tm.text() == '':
        alert_popup("Coach name is empty")
    elif player_long != '':
        alert_popup("Players name is too long: {}".format(player_long))
    else:
        arr_formation = (ed_formation_tm.currentText()).split("-")
        defence = arr_formation[0]
        midfield = arr_formation[1]
        attack = arr_formation[2]

        gk_arr = []
        rb_arr = []
        lb_arr = []
        d_arr = []
        m_arr = []
        rw_arr = []
        lw_arr = []
        a_arr = []

        for igralec in full_arr:
            if igralec[2] == 'GK':
                gk_arr.append([igralec[0], igralec[1], igralec[2], igralec[3], igralec[4], igralec[5], igralec[6],
                               igralec[7], igralec[8], igralec[9], igralec[10], igralec[11], int(igralec[12]), int(igralec[14])])
            elif igralec[2] == 'RB':
                rb_arr.append([igralec[0], igralec[1], igralec[2], igralec[3], igralec[4], igralec[5], igralec[6],
                               igralec[7], igralec[8], igralec[9], igralec[10], igralec[11], int(igralec[12]), int(igralec[14])])
            elif igralec[2] == 'LB':
                lb_arr.append([igralec[0], igralec[1], igralec[2], igralec[3], igralec[4], igralec[5], igralec[6],
                               igralec[7], igralec[8], igralec[9], igralec[10], igralec[11], int(igralec[12]), int(igralec[14])])
            elif igralec[2] == 'D':
                d_arr.append([igralec[0], igralec[1], igralec[2], igralec[3], igralec[4], igralec[5], igralec[6],
                              igralec[7], igralec[8], igralec[9], igralec[10], igralec[11], int(igralec[12]), int(igralec[14])])
            elif igralec[2] == 'M':
                m_arr.append([igralec[0], igralec[1], igralec[2], igralec[3], igralec[4], igralec[5], igralec[6],
                              igralec[7], igralec[8], igralec[9], igralec[10], igralec[11], int(igralec[12]), int(igralec[14])])
            elif igralec[2] == 'RW':
                rw_arr.append([igralec[0], igralec[1], igralec[2], igralec[3], igralec[4], igralec[5], igralec[6],
                               igralec[7], igralec[8], igralec[9], igralec[10], igralec[11], int(igralec[12]), int(igralec[14])])
            elif igralec[2] == 'LW':
                lw_arr.append([igralec[0], igralec[1], igralec[2], igralec[3], igralec[4], igralec[5], igralec[6],
                               igralec[7], igralec[8], igralec[9], igralec[10], igralec[11], int(igralec[12]), int(igralec[14])])
            elif igralec[2] == 'A':
                a_arr.append([igralec[0], igralec[1], igralec[2], igralec[3], igralec[4], igralec[5], igralec[6],
                              igralec[7], igralec[8], igralec[9], igralec[10], igralec[11], int(igralec[12]), int(igralec[14])])

        # control number of players
        if len(gk_arr) < 2:
        	alert_popup("There is no enough GK")
        	return
        if (len(rb_arr) + len(lb_arr) + len(d_arr)) < int(defence):
        	alert_popup("There is no enough defenders")
        	return
        if (len(m_arr) + len(rw_arr) + len(lw_arr)) < int(midfield):
        	alert_popup("There is no enough midfielders")
        	return
        if (len(rw_arr) + len(lw_arr) + len(a_arr)) < int(attack):
        	alert_popup("There is no enough attackers")
        	return

        tmp_int = 0

        # goalkeepers
        df_gk = pandas.DataFrame(gk_arr, columns=[
                                 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'])
        tmp_int = getTopPlayer(gk_arr, df_gk['M'].idxmax())
        tmp = gk_arr[tmp_int]
        formation_arr.append([tmp[0], str(1), tmp[1], tmp[2], tmp[3], tmp[4], tmp[5],
                              tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], str(tmp[12]), str(tmp[13])])
        gk_arr.pop(tmp_int)

        # defenders
        for x in range(int(defence) - 2):
            df_d = pandas.DataFrame(d_arr, columns=[
                                    'A', 'B',
                                     'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'])
            tmp_int = getTopPlayer(d_arr, df_d['M'].idxmax())
            tmp = d_arr[tmp_int]
            formation_arr.append([tmp[0], str(3 + x), tmp[1], tmp[2], tmp[3], tmp[4], tmp[5],
                                  tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], str(tmp[12]), str(tmp[13])])
            d_arr.pop(tmp_int)

            # right back
        if len(rb_arr) > 0:
            df_rb = pandas.DataFrame(rb_arr, columns=[
                                     'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'])
            tmp_int = getTopPlayer(rb_arr, df_rb['M'].idxmax())
            tmp = rb_arr[tmp_int]
            formation_arr.insert(1, [tmp[0], str(2), tmp[1], tmp[2], tmp[3], tmp[4], tmp[5],
                                     tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], str(tmp[12]), str(tmp[13])])
            rb_arr.pop(tmp_int)
        else:
            df_d = pandas.DataFrame(d_arr, columns=[
                                    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'])
            tmp_int = getTopPlayer(d_arr, df_d['M'].idxmax())
            tmp = d_arr[tmp_int]
            formation_arr.insert(1, [tmp[0], str(2), tmp[1], tmp[2], tmp[3], tmp[4], tmp[5],
                                     tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], str(tmp[12]), str(tmp[13])])
            d_arr.pop(tmp_int)

            # left back
        if len(lb_arr) > 0:
            df_lb = pandas.DataFrame(lb_arr, columns=[
                                     'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'])
            tmp_int = getTopPlayer(lb_arr, df_lb['M'].idxmax())
            tmp = lb_arr[tmp_int]
            formation_arr.append([tmp[0], str(int(defence) + 1), tmp[1], tmp[2], tmp[3], tmp[4],
                                  tmp[5], tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], str(tmp[12]), str(tmp[13])])
            lb_arr.pop(tmp_int)
        else:
            df_d = pandas.DataFrame(d_arr, columns=[
                                    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'])
            tmp_int = getTopPlayer(d_arr, df_d['M'].idxmax())
            tmp = d_arr[tmp_int]
            formation_arr.append([tmp[0], str(int(defence) + 1), tmp[1], tmp[2], tmp[3], tmp[4],
                                  tmp[5], tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], str(tmp[12]), str(tmp[13])])
            d_arr.pop(tmp_int)

            # midfield
        if int(midfield) == 2:
            m_tmp_arr = m_arr + rw_arr + lw_arr
            for x in range(2):
                df_m = pandas.DataFrame(m_tmp_arr, columns=[
                                        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'])
                tmp_int = getTopPlayer(m_tmp_arr, df_m['M'].idxmax())
                tmp = m_tmp_arr[tmp_int]
                formation_arr.append([tmp[0], str(int(defence) + 2 + x), tmp[1], tmp[2], tmp[3], tmp[4],
                                      tmp[5], tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], str(tmp[12]), str(tmp[13])])
                m_tmp_arr.pop(tmp_int)
        else:  # more than 2 in midfield
            for x in range(int(midfield) - 2):
                df_m = pandas.DataFrame(m_arr, columns=[
                                        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'])
                tmp_int = getTopPlayer(m_arr, df_m['M'].idxmax())
                tmp = m_arr[tmp_int]
                formation_arr.append([tmp[0], str(int(defence) + 3 + x), tmp[1], tmp[2], tmp[3], tmp[4],
                                      tmp[5], tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], str(tmp[12]), str(tmp[13])])
                m_arr.pop(tmp_int)

                # right winger
            if len(rw_arr) > 0:
                df_rw = pandas.DataFrame(rw_arr, columns=[
                                         'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'])
                tmp_int = getTopPlayer(rw_arr, df_rw['M'].idxmax())
                tmp = rw_arr[tmp_int]
                formation_arr.insert(int(defence) + 1, [tmp[0], str(int(defence) + 2), tmp[1], tmp[2], tmp[3],
                                                        tmp[4], tmp[5], tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], str(tmp[12]), str(tmp[13])])
                rw_arr.pop(tmp_int)
            else:
                df_m = pandas.DataFrame(m_arr, columns=[
                                        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'])
                tmp_int = getTopPlayer(m_arr, df_m['M'].idxmax())
                tmp = m_arr[tmp_int]
                formation_arr.insert(int(defence) + 1, [tmp[0], str(int(defence) + 2), tmp[1], tmp[2], tmp[3],
                                                        tmp[4], tmp[5], tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], str(tmp[12]), str(tmp[13])])
                m_arr.pop(tmp_int)

                # left winger
            if len(lw_arr) > 0:
                df_lw = pandas.DataFrame(lw_arr, columns=[
                                         'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'])
                tmp_int = getTopPlayer(lw_arr, df_lw['M'].idxmax())
                tmp = lw_arr[tmp_int]
                formation_arr.append([tmp[0], str(int(defence) + int(midfield) + 1), tmp[1], tmp[2], tmp[3],
                                      tmp[4], tmp[5], tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], str(tmp[12]), str(tmp[13])])
                lw_arr.pop(tmp_int)
            else:
                df_m = pandas.DataFrame(m_arr, columns=[
                                         'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'])
                tmp_int = getTopPlayer(m_arr, df_m['M'].idxmax())
                tmp = m_arr[tmp_int]
                formation_arr.append([tmp[0], str(int(defence) + int(midfield) + 1), tmp[1], tmp[2], tmp[3],
                                      tmp[4], tmp[5], tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], str(tmp[12]), str(tmp[13])])
                m_arr.pop(tmp_int)

            # attack
            if len(a_arr) < int(attack):
                if int(midfield) == 2:
                    a_tmp_arr = a_arr + m_tmp_arr
                else:
                    a_tmp_arr = a_arr + rw_arr + lw_arr
            else:
                a_tmp_arr = a_arr.copy()

            for x in range(int(attack)):
                df_a = pandas.DataFrame(a_tmp_arr, columns=[
                    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'])
                tmp_int = getTopPlayer(a_tmp_arr, df_a['M'].idxmax())
                tmp = a_tmp_arr[tmp_int]
                formation_arr.append([tmp[0], str(int(defence) + int(midfield) + 2 + x), tmp[1], tmp[2], tmp[3],
                                      tmp[4], tmp[5], tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], str(tmp[12]), str(tmp[13])])
                a_tmp_arr.pop(tmp_int)

            # reserves - goalkeeper
            df_gk = pandas.DataFrame(gk_arr, columns=[
                                     'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'])
            tmp_int = getTopPlayer(gk_arr, df_gk['M'].idxmax())
            tmp = gk_arr[tmp_int]
            formation_arr.append([tmp[0], str(12), tmp[1], tmp[2], tmp[3], tmp[4], tmp[5],
                                  tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], str(tmp[12]), str(tmp[13])])
            gk_arr.pop(tmp_int)

            # reserves - others
            if int(midfield) == 2 and len(a_arr) < int(attack):
                r_arr = rb_arr + lb_arr + d_arr + a_tmp_arr
            elif int(midfield) == 2:
                r_arr = rb_arr + lb_arr + d_arr + m_tmp_arr + a_tmp_arr
            elif len(a_arr) < int(attack):
                r_arr = rb_arr + lb_arr + d_arr + m_arr + a_tmp_arr
            else:
                r_arr = rb_arr + lb_arr + d_arr + m_arr + rw_arr + lw_arr + a_tmp_arr

            for x in range(4):
                df_r = pandas.DataFrame(r_arr, columns=[
                                        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'])
                tmp_int = getTopPlayer(r_arr, df_r['M'].idxmax())
                tmp = r_arr[tmp_int]
                formation_arr.append([tmp[0], str(13 + x), tmp[1], tmp[2], tmp[3], tmp[4], tmp[5],
                                      tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], str(tmp[12]), str(tmp[13])])
                r_arr.pop(tmp_int)

            # reserves - out of 16
            r_arr = gk_arr + r_arr
            for x in range(len(r_arr)):
                df_r = pandas.DataFrame(r_arr, columns=[
                                        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'])
                tmp_int = getTopPlayer(r_arr, df_r['M'].idxmax())
                tmp = r_arr[tmp_int]
                formation_arr.append([tmp[0], str(17 + x), tmp[1], tmp[2], tmp[3], tmp[4], tmp[5],
                                      tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], str(tmp[12]), str(tmp[13])])
                r_arr.pop(tmp_int)

            fillTableCsv()

            tabs.setCurrentIndex(1)


def on_btn_get_data_clicked():
    if ed_team_url.text().strip() != '':
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(ed_team_url.text().strip(), headers=headers)
        if r.status_code != 200:
            alert_popup("URL does not exists")
            return None

        tmp_url = ''
        tmp_url_team_name = ''
        tmp_url_team_id = ''

        tmp_url = ed_team_url.text().strip()
        tmp_url = tmp_url.replace("https://", "").replace("http://", "")

        tmp_url_arr = tmp_url.split('/')
        tmp_url_team_name = tmp_url_arr[1]
        tmp_url_team_id = tmp_url_arr[4]

        ed_team_url.setText('')
        ed_team_name.setText(tmp_url_team_name)
        ed_team_id.setText(tmp_url_team_id)

    if ed_team_name.text() == '' or ed_team_id.text() == '':
        alert_popup("Team shortname or team ID is empty")

    if ed_team_name.text() != '' and ed_team_id.text() != '':
        global full_arr
        global formation_arr
        while len(full_arr) > 0:
            full_arr.pop(0)

        while len(formation_arr) > 0:
            formation_arr.pop(0)

        qm = QMessageBox()
        ret = qm.question(qm, '', "Fill data with skills from Futhead?", qm.Yes | qm.No)

        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get("https://www.transfermarkt.com/{}/startseite/verein/{}".format(
            ed_team_name.text(), ed_team_id.text()), headers=headers)
        r.encoding = r.apparent_encoding

        soup = BeautifulSoup(r.text, 'html.parser')
        zapisi = soup.find("table", {"class": "items"}).find(
            "tbody").findAll("tr")

        ekipa = soup.find("h1", {"itemprop": "name"}).span.text
        ekipa = unicodedata.normalize('NFD', ekipa).encode(
            'ascii', 'ignore').decode('utf8')
        ekipa = ekipa.upper()

        trener = soup.find(
            "div", {"class": "container-hauptinfo", "itemprop": "name"}).find("a").text
        trener = unicodedata.normalize('NFD', trener).encode(
            'ascii', 'ignore').decode('utf8')
        trener = trener.upper()

        general_skin = 'White'

        for zapis in zapisi:
            if zapis.find("td", {"class": "posrela"}) != None:
                igralec = zapis.find("td", {"class": "posrela"}).find("table", {
                    "class": "inline-table"}).find("tr").find("td", {"class": "hauptlink"}).find("a").text
                igralec = unicodedata.normalize('NFD', igralec).encode(
                    'ascii', 'ignore').decode('utf8')
                igralec = igralec.upper()
                pozicija = zapis.find("td", {"class": "posrela"}).find(
                    "table", {"class": "inline-table"}).findAll("tr")[1].find("td").text
                posi = getPosition(pozicija)

                slika = zapis.find("td", {"class": "posrela"}).find("table", {"class": "inline-table"}).findAll("tr")[0].find("td").find("a").find("img")["data-src"]
                image = QPixmap()
                url = slika
                data = urlopen(url).read()
                image.loadFromData(data)

                drzavljanstvo = zapis.findAll("td")[7].find("img")["title"]
                cena = zapis.findAll("td")[8].text.strip()
                cena = cena.replace("-", "")
                if cena == '':
                    cena_div = 0
                    cena_swos = 0
                    _sum = 0
                else:
                    cena_div = int(cena.replace("€", "").replace(
                        "k", "000").replace("m", "0000").replace(".", "")) / 1000000
                    cena_swos = getPrice(posi, cena_div)
                    _sum = int(getSkill(posi, cena_div))

                imported = 0
                if posi == 'GK':
                    pa = str(0)
                    ve = str(0)
                    he = str(0)
                    ta = str(0)
                    co = str(0)
                    sp = str(0)
                    fi = str(0)
                else:
                    if ret == qm.No:
                        imported = 1
                        rnd_array = returnSkillArray(_sum)

                        pa = str(rnd_array[0])
                        ve = str(rnd_array[1])
                        he = str(rnd_array[2])
                        ta = str(rnd_array[3])
                        co = str(rnd_array[4])
                        sp = str(rnd_array[5])
                        fi = str(rnd_array[6])
                    else:
                        conn = None
                        try:
                            conn = sqlite3.connect('data\\players_futhead.db')

                            if conn:
                                cur = conn.cursor()
                                cur.execute("SELECT * FROM players where name = '{}' and club = '{}' order by id asc limit 1".format(igralec, ekipa))
                             
                                rows = cur.fetchall()

                                if len(rows) > 0:
                                    for row in rows: 
                                        rating = row[5]
                                        sp = getFutheadSwosSkill(row[6])
                                        ve = getFutheadSwosSkill(row[7])
                                        pa = getFutheadSwosSkill(row[8])
                                        co = getFutheadSwosSkill(row[9])
                                        ta = getFutheadSwosSkill(row[10])
                                        fi = getFutheadSwosSkill(row[12])
                                        he = getFutheadSwosSkill(row[13])

                                        fut_array = []
                                        fut_array = getFutheadSwosSkillArray(rating, sp, ve, pa, co, ta, fi, he)

                                        _sum = fut_array[0] + fut_array[1] + fut_array[2] + fut_array[3] + fut_array[4] + fut_array[5] + fut_array[6]
                                        cena_swos = getPriceFuthead(_sum)

                                        sp = str(fut_array[0])
                                        ve = str(fut_array[1])
                                        pa = str(fut_array[2])
                                        co = str(fut_array[3])
                                        ta = str(fut_array[4])
                                        fi = str(fut_array[5])
                                        he = str(fut_array[6])

                                        imported = 1
                                else:
                                    rnd_array = returnSkillArray(_sum)

                                    pa = str(rnd_array[0])
                                    ve = str(rnd_array[1])
                                    he = str(rnd_array[2])
                                    ta = str(rnd_array[3])
                                    co = str(rnd_array[4])
                                    sp = str(rnd_array[5])
                                    fi = str(rnd_array[6])
                        except Error as e:
                            print(e)
                        finally:
                            if conn:
                                conn.close()

                

                full_arr.append([getCountry(drzavljanstvo), igralec, posi,
                                 general_skin, pa, ve, he, ta, co, sp, fi, cena_swos, str(_sum), str(cena_div), str(0), str(0), str(0), str(0), image, imported])

        r = requests.get("https://www.transfermarkt.com/{}/leistungsdaten/verein/{}".format(
            ed_team_name.text(), ed_team_id.text()), headers=headers)
        r.encoding = r.apparent_encoding

        soup = BeautifulSoup(r.text, 'html.parser')
        zapisi_minute = soup.find(
            "table", {"class": "items"}).find("tbody").findAll("tr")

        for zapis in zapisi_minute:
            if zapis.find("td", {"class": "posrela"}) != None:
                igralec = zapis.find("td", {"class": "posrela"}).find("table", {
                    "class": "inline-table"}).find("tr").find("td", {"class": "hauptlink"}).find("a").text
                igralec = unicodedata.normalize('NFD', igralec).encode(
                    'ascii', 'ignore').decode('utf8')
                igralec = igralec.upper()
                squad = zapis.findAll("td")[7].text
                squad = squad.replace("-", "0")
                appereance = zapis.findAll("td")[8].text
                appereance = appereance.replace("-", "0").replace("Not used during this season", "0").replace("Not in squad during this season", "0")
                goals = zapis.findAll("td")[9].text
                goals = goals.replace("-", "0")
                minute = zapis.find("td", {"class": "rechts"}).text
                minute = minute.replace(".", "").replace(
                    "'", "").replace("-", "0")
                minute = str(minute)

                for igrac in full_arr:
                    if igrac[1] == igralec:
                        igrac[14] = minute
                        igrac[15] = squad
                        igrac[16] = appereance
                        igrac[17] = goals
                        continue

        ed_team_name_tm.setText(ekipa)
        ed_coach_name_tm.setText(trener)

        fillTable()
        fillTableCsv()


def on_btn_savecsv_clicked():
    if ed_league_id_swoes.text() == '':
        alert_popup("Enter league ID")
    elif ed_team_id_swoes.text() == '':
        alert_popup("Enter team ID")
    else:
        csv_file_head = "{},{},{},{},{},,,,,,,,".format(ed_team_name_tm.text(), ed_league_id_swoes.text(
        ), ed_team_id_swoes.text(), ed_formation_tm.currentText(), ed_coach_name_tm.text())

        csv_file_formation = csv_file_head + "\n"
        for igralec in formation_arr[:16]:
            csv_file_formation = csv_file_formation + "{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(
                igralec[0], igralec[1], igralec[2], igralec[3], igralec[4], igralec[5], igralec[6], igralec[7], igralec[8], igralec[9], igralec[10], igralec[11], igralec[12])

        filename = "{}\\{}.csv".format(
            ed_save_csv.text(), ed_team_name_tm.text())
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:
                raise

        with open(filename, "w") as text_file:
            text_file.write(csv_file_formation)

        alert_popup("Saved to {}".format(filename))


def fillTable():
    global full_arr

    tabela.setRowCount(len(full_arr))
    tabela.setColumnCount(19)
    tabela.setHorizontalHeaderLabels(["National", "Name", "Position", "Player skin", "PA",
                                      "VE", "HE", "TA", "CO", "SP", "FI", "SWOS price", "Sum skills", "TM price", "Minutes", "In squad", "Appearances", "Goals", "Image"])

    for row in range(0, len(full_arr)):
        for column in range(0, 18):
            tabela.setItem(row, column, QTableWidgetItem((full_arr[row][column])))
            
        painter = QPainter()
        lbl = QLabel()
        image = QPixmap(full_arr[row][18])
        image = image.scaled(28, 32)

        lbl.setPixmap(image)
        tabela.setCellWidget(row, 18, lbl)

    tabela.resizeColumnsToContents()
    tabela.resizeRowsToContents()

    if len(full_arr) > 0:
        font = QFont()
        font.setItalic(True)
        for row_bold in range(0, len(full_arr)):
            for column_bold in range(0, 18):
                if full_arr[row_bold][19] == 0 and full_arr[row_bold][2] != 'GK':
                    tabela.item(row_bold, column_bold).setFont(font)

    int_gk = 0
    int_rb = 0
    int_d = 0
    int_lb = 0
    int_rw = 0
    int_m = 0
    int_lw = 0
    int_a = 0

    for igralec in full_arr:
        if igralec[2] == 'GK':
            int_gk += 1
        elif igralec[2] == 'RB':
            int_rb += 1
        elif igralec[2] == 'D':
            int_d += 1
        elif igralec[2] == 'LB':
            int_lb += 1
        elif igralec[2] == 'RW':
            int_rw += 1
        elif igralec[2] == 'M':
            int_m += 1            
        elif igralec[2] == 'LW':
            int_lw += 1      
        elif igralec[2] == 'A':
            int_a += 1

    lbl_GK_number.setText(str(int_gk))
    lbl_RB_number.setText(str(int_rb))
    lbl_D_number.setText(str(int_d))
    lbl_LB_number.setText(str(int_lb))
    lbl_RW_number.setText(str(int_rw))
    lbl_M_number.setText(str(int_m))
    lbl_LW_number.setText(str(int_lw))
    lbl_A_number.setText(str(int_a))


def fillTableCsv():
    global formation_arr

    tabela_csv.setRowCount(len(formation_arr))
    tabela_csv.setColumnCount(15)
    tabela_csv.setHorizontalHeaderLabels(["National", "Number", "Name", "Position", "Player skin",
                                          "PA", "VE", "HE", "TA", "CO", "SP", "FI", "SWOS price", "Sum skills", "Minutes"])

    for row in range(0, len(formation_arr)):
        for column in range(0, 15):
            tabela_csv.setItem(row, column, QTableWidgetItem(
                (formation_arr[row][column])))

    if len(formation_arr) > 0:
        font = QFont()
        font.setBold(True)
        for row_bold in range(0, 16):
            for column_bold in range(0, 15):
                tabela_csv.item(row_bold, column_bold).setFont(font)

    tabela_csv.resizeColumnsToContents()                


def generateMenuCSV():
    if tabela_csv.selectionModel().selection().indexes():
        for i in tabela_csv.selectionModel().selection().indexes():
            row, column = i.row(), i.column()

        global formation_arr

        menu = QMenu()
        changeAction = menu.addAction("Change this player")

        action = menu.exec_(QtGui.QCursor.pos())
        if action == changeAction:
            tmp_newid = getPlayerID(len(formation_arr))
            if tmp_newid != None:
                igralec_old = formation_arr[row]
                igralec_new = formation_arr[tmp_newid - 1]

                if (igralec_old[3] == 'GK' and igralec_new[3] == 'GK') or (igralec_old[3] != 'GK' and igralec_new[3] != 'GK'):
                    formation_arr[row] = igralec_new
                    formation_arr[tmp_newid - 1] = igralec_old

                    formation_arr[row][1] = str(row + 1)
                    formation_arr[tmp_newid - 1][1] = str(tmp_newid)

                    fillTableCsv()
                else:
                    alert_popup("Position 1 and 12 is reserved for GK")


def getPlayerID(max_len):
    num, ok = QInputDialog.getInt(
        tab_SWOS, "Player ID", "Enter player ID to change", 1, 1, max_len, 1)

    if ok:
        return num


def isEnoughPlayersFormation(formation, position):
    global full_arr

    arr_formation = (ed_formation_tm.currentText()).split("-")
    defence = int(arr_formation[0])
    midfield = int(arr_formation[1])
    attack = int(arr_formation[2])

    int_gk = 0
    int_rb = 0
    int_d = 0
    int_lb = 0
    int_rw = 0
    int_m = 0
    int_lw = 0
    int_a = 0

    for igralec in full_arr:
        if igralec[2] == 'GK':
            int_gk += 1
        elif igralec[2] == 'RB':
            int_rb += 1
        elif igralec[2] == 'D':
            int_d += 1
        elif igralec[2] == 'LB':
            int_lb += 1
        elif igralec[2] == 'RW':
            int_rw += 1
        elif igralec[2] == 'M':
            int_m += 1            
        elif igralec[2] == 'LW':
            int_lw += 1      
        elif igralec[2] == 'A':
            int_a += 1

    if position == 'GK':
        int_gk -= 1
    elif position == 'RB':
        int_rb -= 1
    elif position == 'D':
        int_d -= 1
    elif position == 'LB':
        int_lb -= 1
    elif position == 'RW':
        int_rw -= 1
    elif position == 'M':
        int_m -= 1
    elif position == 'LW':
        int_lw -= 1
    elif position == 'A':
        int_a -= 1

    if (int_gk < 2):
        return "In team must be at least 2 goalkeepers"
    elif ((int_rb + int_d + int_lb) < defence):
        return "In team must be at least {} defenders".format(str(defence))
    elif ((int_rw + int_m + int_lw) < midfield):
        return "In team must be at least {} midfielders".format(str(midfield))
    elif (int_a < attack):
        return "In team must be at least {} attackers".format(str(attack))
    else: 
        return ""


def generateMenu():
    if tabela.selectionModel().selection().indexes():
        for i in tabela.selectionModel().selection().indexes():
            row, column = i.row(), i.column()

        global full_arr
        menu = QMenu()

        str_return = ''

        deleAction = menu.addAction("Delete this player")

        changePlayerName = menu.addAction("Change player name")

        changePlayerCountry = menu.addAction("Change player country")

        changePositionAction = menu.addAction(
            "Change players position (popup)")
        changePositionMenu = menu.addMenu("Change players position to")
        changePositionGK = changePositionMenu.addAction("GK")
        changePositionRB = changePositionMenu.addAction("RB")
        changePositionD = changePositionMenu.addAction("D")
        changePositionLB = changePositionMenu.addAction("LB")
        changePositionRW = changePositionMenu.addAction("RW")
        changePositionM = changePositionMenu.addAction("M")
        changePositionLW = changePositionMenu.addAction("LW")
        changePositionA = changePositionMenu.addAction("A")

        changeSkinAction = menu.addAction("Change players skin (popup)")
        changeSkinMenu = menu.addMenu("Change players skin to")
        changeSkinWhiteAction = changeSkinMenu.addAction("White")
        changeSkinBlackAction = changeSkinMenu.addAction("Black")
        changeSkinBlondeAction = changeSkinMenu.addAction("Blonde")

        changeSumSkillAction = menu.addAction("Change SWOS skill value")
        changeSkillMenu = menu.addMenu("Change each skill")
        changeSkillPA = changeSkillMenu.addAction("PA")
        changeSkillVE = changeSkillMenu.addAction("VE")
        changeSkillHE = changeSkillMenu.addAction("HE")
        changeSkillTA = changeSkillMenu.addAction("TA")
        changeSkillCO = changeSkillMenu.addAction("CO")
        changeSkillSP = changeSkillMenu.addAction("SP")
        changeSkillFI = changeSkillMenu.addAction("FI")

        action = menu.exec_(QtGui.QCursor.pos())
        if action == deleAction:
            str_return = isEnoughPlayersFormation(ed_formation_tm.currentText(), full_arr[row][2])
            if len(full_arr) <= 16:
                alert_popup("In team must be at least 16 players")
            elif str_return != "":
                alert_popup(str_return)
            else:
                full_arr.pop(row)
        elif action == changePlayerName:
            tmp_name = setName(str(full_arr[row][1]))
            if tmp_name != None:
                full_arr[row][1] = tmp_name
        elif action == changePlayerCountry:
            tmp_country = setCountry(str(full_arr[row][0]))
            if tmp_country != None:
                full_arr[row][0] = tmp_country
        elif action == changeSkinAction:
            tmp_skin = setSkin()
            if tmp_skin != None:
                full_arr[row][3] = tmp_skin
        elif action == changeSkinWhiteAction:
            full_arr[row][3] = "White"
        elif action == changeSkinBlackAction:
            full_arr[row][3] = "Black"
        elif action == changeSkinBlondeAction:
            full_arr[row][3] = "Blonde"
        elif action == changeSumSkillAction:
            tmp_skill = setSkill(int(full_arr[row][12]))
            if tmp_skill != None:
                full_arr[row][12] = int(tmp_skill)
                recalculateSwosSkillPrice(
                    row, full_arr[row][2], int(full_arr[row][12]))
        elif action == changePositionAction:
            tmp_position = setPosition()
            if tmp_position != None:
                full_arr[row][2] = tmp_position
                recalculateSwosSkillPrice(
                    row, full_arr[row][2], int(full_arr[row][12]))
        elif action == changePositionGK:
            full_arr[row][2] = "GK"
            recalculateSwosSkillPrice(
                row, full_arr[row][2], int(full_arr[row][12]))
        elif action == changePositionRB:
            full_arr[row][2] = "RB"
            recalculateSwosSkillPrice(
                row, full_arr[row][2], int(full_arr[row][12]))
        elif action == changePositionD:
            full_arr[row][2] = "D"
            recalculateSwosSkillPrice(
                row, full_arr[row][2], int(full_arr[row][12]))
        elif action == changePositionLB:
            full_arr[row][2] = "LB"
            recalculateSwosSkillPrice(
                row, full_arr[row][2], int(full_arr[row][12]))
        elif action == changePositionLW:
            full_arr[row][2] = "LW"
            recalculateSwosSkillPrice(
                row, full_arr[row][2], int(full_arr[row][12]))
        elif action == changePositionM:
            full_arr[row][2] = "M"
            recalculateSwosSkillPrice(
                row, full_arr[row][2], int(full_arr[row][12]))
        elif action == changePositionRW:
            full_arr[row][2] = "RW"
            recalculateSwosSkillPrice(
                row, full_arr[row][2], int(full_arr[row][12]))
        elif action == changePositionA:
            full_arr[row][2] = "A"
            recalculateSwosSkillPrice(
                row, full_arr[row][2], int(full_arr[row][12]))
        elif action == changeSkillPA and full_arr[row][2] != "GK":
            tmp_sk = setSkillEach(int(full_arr[row][4]), "PA")
            if tmp_sk != None:
                full_arr[row][4] = str(tmp_sk)
                setSWOSPriceEach(row)
        elif action == changeSkillVE and full_arr[row][2] != "GK":
            tmp_sk = setSkillEach(int(full_arr[row][5]), "VE")
            if tmp_sk != None:
                full_arr[row][5] = str(tmp_sk)
                setSWOSPriceEach(row)
        elif action == changeSkillHE and full_arr[row][2] != "GK":
            tmp_sk = setSkillEach(int(full_arr[row][6]), "HE")
            if tmp_sk != None:
                full_arr[row][6] = str(tmp_sk)
                setSWOSPriceEach(row)
        elif action == changeSkillTA and full_arr[row][2] != "GK":
            tmp_sk = setSkillEach(int(full_arr[row][7]), "TA")
            if tmp_sk != None:
                full_arr[row][7] = str(tmp_sk)
                setSWOSPriceEach(row)
        elif action == changeSkillCO and full_arr[row][2] != "GK":
            tmp_sk = setSkillEach(int(full_arr[row][8]), "CO")
            if tmp_sk != None:
                full_arr[row][8] = str(tmp_sk)
                setSWOSPriceEach(row)
        elif action == changeSkillSP and full_arr[row][2] != "GK":
            tmp_sk = setSkillEach(int(full_arr[row][9]), "SP")
            if tmp_sk != None:
                full_arr[row][9] = str(tmp_sk)
                setSWOSPriceEach(row)
        elif action == changeSkillFI and full_arr[row][2] != "GK":
            tmp_sk = setSkillEach(int(full_arr[row][10]), "FI")
            if tmp_sk != None:
                full_arr[row][10] = str(tmp_sk)
                setSWOSPriceEach(row)

        fillTable()


def setSWOSPriceEach(row_id):
    global full_arr

    sum_skill = int(full_arr[row_id][4]) + int(full_arr[row_id][5]) + int(full_arr[row_id][6]) + int(
        full_arr[row_id][7]) + int(full_arr[row_id][8]) + int(full_arr[row_id][9]) + int(full_arr[row_id][10])
    full_arr[row_id][12] = str(sum_skill)
    full_arr[row_id][11] = getPrice(full_arr[row_id][2], sum_skill)


def recalculateSwosSkillPrice(poz, position, skill):
    global full_arr

    cena_swos_tmp = getPriceSkill(position, skill)

    rnd_array_tmp = returnSkillArray(skill)
    if position == 'GK':
        pa_tmp = 0
        ve_tmp = 0
        he_tmp = 0
        ta_tmp = 0
        co_tmp = 0
        sp_tmp = 0
        fi_tmp = 0
    else:
        pa_tmp = rnd_array_tmp[0]
        ve_tmp = rnd_array_tmp[1]
        he_tmp = rnd_array_tmp[2]
        ta_tmp = rnd_array_tmp[3]
        co_tmp = rnd_array_tmp[4]
        sp_tmp = rnd_array_tmp[5]
        fi_tmp = rnd_array_tmp[6]

    full_arr[poz][2] = position
    full_arr[poz][4] = str(pa_tmp)
    full_arr[poz][5] = str(ve_tmp)
    full_arr[poz][6] = str(he_tmp)
    full_arr[poz][7] = str(ta_tmp)
    full_arr[poz][8] = str(co_tmp)
    full_arr[poz][9] = str(sp_tmp)
    full_arr[poz][10] = str(fi_tmp)
    full_arr[poz][11] = cena_swos_tmp
    full_arr[poz][12] = str(skill)


def setSkin():
    items = ("White", "Black", "Blonde")

    item, ok = QInputDialog.getItem(
        tab_TM, "Players skin", "Select skin", items, 0, False)

    if ok and item:
        return item


def setPosition():
    items = ("GK", "RB", "D", "LB", "RW", "M", "LW", "A")

    item, ok = QInputDialog.getItem(
        tab_TM, "Players position", "Select position", items, 0, False)

    if ok and item:
        return item


def setSkill(current):
    num, ok = QInputDialog.getInt(
        tab_TM, "Skill value", "Enter skill value", current, 0, 49, 1)

    if ok:
        return str(num)


def setSkillEach(current, text):
    num, ok = QInputDialog.getInt(
        tab_TM, "Skill value", "Enter {} value".format(text), current, 0, 7, 1)

    if ok:
        return str(num)

def setCountry(current):
    text, okPressed = QInputDialog.getText(
        tab_TM, "Player country", "Enter new country:", QLineEdit.Normal, current)

    if okPressed and text != '':
        return text

def setName(current):
    text, okPressed = QInputDialog.getText(
        tab_TM, "Player name", "Enter new name:", QLineEdit.Normal, current)

    if okPressed and text != '':
        return text

headers = {"User-Agent": "Mozilla/5.0"}
r = requests.get("http://swos.boskorban.si/players_futhead.zip", headers=headers)

with open('data\\players_futhead.zip', 'wb') as f:
    f.write(r.content)

if os.path.exists("data\\players_futhead.db"):
    os.remove("data\\players_futhead.db")

with ZipFile("data\\players_futhead.zip", 'r') as zip:
    zip.extractall()

os.rename('players_futhead.db', 'data\\players_futhead.db')
os.remove('data\\players_futhead.zip')

app = QApplication([])
app.setStyle('Fusion')

tabs = QTabWidget()
tab_TM = QWidget()
tab_SWOS = QWidget()
layout_tm = QVBoxLayout()
layout_swos = QVBoxLayout()
layout_0 = QHBoxLayout()
layout_1 = QHBoxLayout()
layout_2 = QHBoxLayout()
layout_3 = QHBoxLayout()
layout_4 = QHBoxLayout()
layout_5 = QHBoxLayout()
layout_6 = QHBoxLayout()
layout_7 = QHBoxLayout()
layout_8 = QGridLayout()

tabs.addTab(tab_TM, "Transfermarkt")
tabs.addTab(tab_SWOS, "SWOS csv")

# variables for GUI
full_arr = []
formation_arr = []

# components for GUI
lbl_team_url = QLabel('Team URL on TM ')
ed_team_url = QLineEdit(
    'https://www.transfermarkt.com/nd-lendava-1903/startseite/verein/9233')
lbl_team_name = QLabel('Team short name TM ')
ed_team_name = QLineEdit('')
lbl_team_id = QLabel('Team ID TM')
ed_team_id = QLineEdit('')
btn_get_data = QPushButton('Get data from TM')

btn_generate = QPushButton('Generate formation')

lbl_team_name_tm = QLabel('Team name')
ed_team_name_tm = QLineEdit()
lbl_coach_name_tm = QLabel('Coach name')
ed_coach_name_tm = QLineEdit()
lbl_formation_tm = QLabel('Formation')
ed_formation_tm = QComboBox()
ed_formation_tm.addItem("4-4-2")
ed_formation_tm.addItem("5-4-1")
ed_formation_tm.addItem("4-5-1")
ed_formation_tm.addItem("5-3-2")
ed_formation_tm.addItem("3-5-2")
ed_formation_tm.addItem("4-3-3")
ed_formation_tm.addItem("4-2-4")
ed_formation_tm.addItem("3-4-3")
ed_formation_tm.addItem("5-2-3")

lbl_GK = QLabel('Goalkeepers (GK)')
lbl_GK_number = QLabel('0')
lbl_RB = QLabel('Right back (RB)')
lbl_RB_number = QLabel('0')
lbl_D = QLabel('Defender (D)')
lbl_D_number = QLabel('0')
lbl_LB = QLabel('Left back (LB)')
lbl_LB_number = QLabel('0')
lbl_RW = QLabel('Right winger (RW)')
lbl_RW_number = QLabel('0')
lbl_M = QLabel('Midfielder (M)')
lbl_M_number = QLabel('0')
lbl_LW = QLabel('Left winger (LW)')
lbl_LW_number = QLabel('0')
lbl_A = QLabel('Attacker (A)')
lbl_A_number = QLabel('0')

tabela = QTableWidget()
tabela.setEditTriggers(QTableWidget.NoEditTriggers)
tabela.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
tabela.customContextMenuRequested.connect(generateMenu)

lbl_league_id_swoes = QLabel('League ID SWOS')
ed_league_id_swoes = QLineEdit('1')
lbl_team_id_swoes = QLabel('Team ID SWOS')
ed_team_id_swoes = QLineEdit('1')

tabela_csv = QTableWidget()
tabela_csv.setEditTriggers(QTableWidget.NoEditTriggers)
tabela_csv.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
tabela_csv.customContextMenuRequested.connect(generateMenuCSV)

lbl_save_csv = QLabel("Save to")
ed_save_csv = QLineEdit("C:\\SWOS")

btn_savecsv = QPushButton('Save CSV file')

# signals / events
btn_get_data.clicked.connect(on_btn_get_data_clicked)
btn_generate.clicked.connect(on_btn_generate_clicked)
btn_savecsv.clicked.connect(on_btn_savecsv_clicked)

# length for labels
lbl_team_url.setFixedWidth(100)
lbl_team_name.setFixedWidth(100)
lbl_team_id.setFixedWidth(100)
lbl_league_id_swoes.setFixedWidth(100)
lbl_team_id_swoes.setFixedWidth(100)
lbl_team_name_tm.setFixedWidth(100)
lbl_coach_name_tm.setFixedWidth(100)
lbl_formation_tm.setFixedWidth(100)

# layout - tab TM
layout_0.addWidget(lbl_team_url)
layout_0.addWidget(ed_team_url)
layout_1.addWidget(lbl_team_name)
layout_1.addWidget(ed_team_name)
layout_2.addWidget(lbl_team_id)
layout_2.addWidget(ed_team_id)
layout_3.addWidget(lbl_team_name_tm)
layout_3.addWidget(ed_team_name_tm)
layout_3.addWidget(lbl_coach_name_tm)
layout_3.addWidget(ed_coach_name_tm)
layout_3.addWidget(lbl_formation_tm)
layout_3.addWidget(ed_formation_tm)
layout_8.addWidget(lbl_GK, 0, 0)
layout_8.addWidget(lbl_GK_number, 0, 1, 1, 10)
layout_8.addWidget(lbl_RB, 1, 0)
layout_8.addWidget(lbl_RB_number, 1, 1, 1, 10)
layout_8.addWidget(lbl_D, 2, 0)
layout_8.addWidget(lbl_D_number, 2, 1, 1, 10)
layout_8.addWidget(lbl_LB, 3, 0)
layout_8.addWidget(lbl_LB_number, 3, 1, 1, 10)
layout_8.addWidget(lbl_RW, 4, 0)
layout_8.addWidget(lbl_RW_number, 4, 1, 1, 10)
layout_8.addWidget(lbl_M, 5, 0)
layout_8.addWidget(lbl_M_number, 5, 1, 1, 10)
layout_8.addWidget(lbl_LW, 6, 0)
layout_8.addWidget(lbl_LW_number, 6, 1, 1, 10)
layout_8.addWidget(lbl_A, 7, 0)
layout_8.addWidget(lbl_A_number, 7, 1, 1, 10)

# layout - tab SWOS
layout_4.addWidget(lbl_league_id_swoes)
layout_4.addWidget(ed_league_id_swoes)
layout_5.addWidget(lbl_team_id_swoes)
layout_5.addWidget(ed_team_id_swoes)
layout_6.addWidget(tabela_csv)
layout_7.addWidget(lbl_save_csv)
layout_7.addWidget(ed_save_csv)
layout_7.addWidget(btn_savecsv)

# layout - main TM
layout_tm.addLayout(layout_0)
layout_tm.addLayout(layout_1)
layout_tm.addLayout(layout_2)

layout_tm.addWidget(btn_get_data)

layout_tm.addLayout(layout_3)

layout_tm.addWidget(tabela)

layout_tm.addLayout(layout_8)

layout_tm.addWidget(btn_generate)

# layout - main SWOS
layout_swos.addLayout(layout_4)
layout_swos.addLayout(layout_5)
layout_swos.addLayout(layout_6)
layout_swos.addLayout(layout_7)

tab_TM.setLayout(layout_tm)
tab_SWOS.setLayout(layout_swos)
tabs.setWindowTitle("SWOS - TM Editor v1.2")
tabs.showMaximized()
app.exec_()
