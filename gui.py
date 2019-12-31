# Code create by BOCo23 https://github.com/boskorban

from PyQt5.QtWidgets import *
from PyQt5 import *
from bs4 import BeautifulSoup
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
        print(ed_coach_name_tm.text())
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
                               igralec[7], igralec[8], igralec[9], igralec[10], igralec[11], int(igralec[12]), igralec[14]])
            elif igralec[2] == 'RB':
                rb_arr.append([igralec[0], igralec[1], igralec[2], igralec[3], igralec[4], igralec[5], igralec[6],
                               igralec[7], igralec[8], igralec[9], igralec[10], igralec[11], int(igralec[12]), igralec[14]])
            elif igralec[2] == 'LB':
                lb_arr.append([igralec[0], igralec[1], igralec[2], igralec[3], igralec[4], igralec[5], igralec[6],
                               igralec[7], igralec[8], igralec[9], igralec[10], igralec[11], int(igralec[12]), igralec[14]])
            elif igralec[2] == 'D':
                d_arr.append([igralec[0], igralec[1], igralec[2], igralec[3], igralec[4], igralec[5], igralec[6],
                              igralec[7], igralec[8], igralec[9], igralec[10], igralec[11], int(igralec[12]), igralec[14]])
            elif igralec[2] == 'M':
                m_arr.append([igralec[0], igralec[1], igralec[2], igralec[3], igralec[4], igralec[5], igralec[6],
                              igralec[7], igralec[8], igralec[9], igralec[10], igralec[11], int(igralec[12]), igralec[14]])
            elif igralec[2] == 'RW':
                rw_arr.append([igralec[0], igralec[1], igralec[2], igralec[3], igralec[4], igralec[5], igralec[6],
                               igralec[7], igralec[8], igralec[9], igralec[10], igralec[11], int(igralec[12]), igralec[14]])
            elif igralec[2] == 'LW':
                lw_arr.append([igralec[0], igralec[1], igralec[2], igralec[3], igralec[4], igralec[5], igralec[6],
                               igralec[7], igralec[8], igralec[9], igralec[10], igralec[11], int(igralec[12]), igralec[14]])
            elif igralec[2] == 'A':
                a_arr.append([igralec[0], igralec[1], igralec[2], igralec[3], igralec[4], igralec[5], igralec[6],
                              igralec[7], igralec[8], igralec[9], igralec[10], igralec[11], int(igralec[12]), igralec[14]])

        df_gk = pandas.DataFrame(gk_arr, columns=[
                                 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'])
        tmp = gk_arr[df_gk['M'].idxmax()]
        formation_arr.append([tmp[0], str(1), tmp[1], tmp[2], tmp[3], tmp[4], tmp[5],
                              tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], str(tmp[12]), tmp[13]])
        gk_arr.pop(df_gk['M'].idxmax())

        # goalkeepers
        for x in range(int(defence) - 2):
            df_d = pandas.DataFrame(d_arr, columns=[
                                    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'])
            tmp = d_arr[df_d['M'].idxmax()]
            formation_arr.append([tmp[0], str(3 + x), tmp[1], tmp[2], tmp[3], tmp[4], tmp[5],
                                  tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], str(tmp[12]), tmp[13]])
            d_arr.pop(df_d['M'].idxmax())

            # right back
        if len(rb_arr) > 0:
            df_rb = pandas.DataFrame(rb_arr, columns=[
                                     'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'])
            tmp = rb_arr[df_rb['M'].idxmax()]
            formation_arr.insert(1, [tmp[0], str(2), tmp[1], tmp[2], tmp[3], tmp[4], tmp[5],
                                     tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], str(tmp[12]), tmp[13]])
            rb_arr.pop(df_rb['M'].idxmax())
        else:
            df_d = pandas.DataFrame(d_arr, columns=[
                                    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'])
            tmp = d_arr[df_d['M'].idxmax()]
            formation_arr.insert(1, [tmp[0], str(2), tmp[1], tmp[2], tmp[3], tmp[4], tmp[5],
                                     tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], str(tmp[12]), tmp[13]])
            d_arr.pop(df_d['M'].idxmax())

            # left back
        if len(lb_arr) > 0:
            df_lb = pandas.DataFrame(lb_arr, columns=[
                                     'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'])
            tmp = lb_arr[df_lb['M'].idxmax()]
            formation_arr.append([tmp[0], str(int(defence) + 1), tmp[1], tmp[2], tmp[3], tmp[4],
                                  tmp[5], tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], str(tmp[12]), tmp[13]])
            lb_arr.pop(df_lb['M'].idxmax())
        else:
            df_d = pandas.DataFrame(d_arr, columns=[
                                    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'])
            tmp = d_arr[df_d['M'].idxmax()]
            formation_arr.append([tmp[0], str(int(defence) + 1), tmp[1], tmp[2], tmp[3], tmp[4],
                                  tmp[5], tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], str(tmp[12]), tmp[13]])
            d_arr.pop(df_d['M'].idxmax())

            # midfield
        if int(midfield) == 2:
            m_tmp_arr = m_arr + rw_arr + lw_arr
            for x in range(2):
                df_m = pandas.DataFrame(m_tmp_arr, columns=[
                                        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'])
                tmp = m_tmp_arr[df_m['M'].idxmax()]
                formation_arr.append([tmp[0], str(int(defence) + 2 + x), tmp[1], tmp[2], tmp[3], tmp[4],
                                      tmp[5], tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], str(tmp[12]), tmp[13]])
                m_tmp_arr.pop(df_m['M'].idxmax())
        else:  # more than 2 in midfield
            for x in range(int(midfield) - 2):
                df_m = pandas.DataFrame(m_arr, columns=[
                                        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'])
                tmp = m_arr[df_m['M'].idxmax()]
                formation_arr.append([tmp[0], str(int(defence) + 3 + x), tmp[1], tmp[2], tmp[3], tmp[4],
                                      tmp[5], tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], str(tmp[12]), tmp[13]])
                m_arr.pop(df_m['M'].idxmax())

                # right winger
            if len(rw_arr) > 0:
                df_rw = pandas.DataFrame(rw_arr, columns=[
                                         'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'])
                tmp = rw_arr[df_rw['M'].idxmax()]
                formation_arr.insert(int(defence) + 1, [tmp[0], str(int(defence) + 2), tmp[1], tmp[2], tmp[3],
                                                        tmp[4], tmp[5], tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], str(tmp[12]), tmp[13]])
                rw_arr.pop(df_rw['M'].idxmax())
            else:
                df_m = pandas.DataFrame(m_arr, columns=[
                                        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'])
                tmp = m_arr[df_m['M'].idxmax()]
                formation_arr.insert(int(defence) + 1, [tmp[0], str(int(defence) + 2), tmp[1], tmp[2], tmp[3],
                                                        tmp[4], tmp[5], tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], str(tmp[12]), tmp[13]])
                m_arr.pop(df_m['M'].idxmax())

                # left winger
            if len(lw_arr) > 0:
                df_lw = pandas.DataFrame(lw_arr, columns=[
                                         'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'])
                tmp = lw_arr[df_lw['M'].idxmax()]
                formation_arr.append([tmp[0], str(int(defence) + int(midfield) + 1), tmp[1], tmp[2], tmp[3],
                                      tmp[4], tmp[5], tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], str(tmp[12]), tmp[13]])
                lw_arr.pop(df_lw['M'].idxmax())
            else:
                df_lw = pandas.DataFrame(m_arr, columns=[
                                         'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'])
                tmp = m_arr[df_lw['M'].idxmax()]
                formation_arr.append([tmp[0], str(int(defence) + int(midfield) + 1), tmp[1], tmp[2], tmp[3],
                                      tmp[4], tmp[5], tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], str(tmp[12]), tmp[13]])
                m_arr.pop(df_lw['M'].idxmax())

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
                tmp = a_tmp_arr[df_a['M'].idxmax()]
                formation_arr.append([tmp[0], str(int(defence) + int(midfield) + 2 + x), tmp[1], tmp[2], tmp[3],
                                      tmp[4], tmp[5], tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], str(tmp[12]), tmp[13]])
                a_tmp_arr.pop(df_a['M'].idxmax())

            # reserves - goalkeeper
            df_gk = pandas.DataFrame(gk_arr, columns=[
                                     'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'])
            tmp = gk_arr[df_gk['M'].idxmax()]
            formation_arr.append([tmp[0], str(12), tmp[1], tmp[2], tmp[3], tmp[4], tmp[5],
                                  tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], str(tmp[12]), tmp[13]])
            gk_arr.pop(df_gk['M'].idxmax())

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
                tmp = r_arr[df_r['M'].idxmax()]
                formation_arr.append([tmp[0], str(13 + x), tmp[1], tmp[2], tmp[3], tmp[4], tmp[5],
                                      tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], str(tmp[12]), tmp[13]])
                r_arr.pop(df_r['M'].idxmax())

            # reserves - out of 16
            r_arr = gk_arr + r_arr
            for x in range(len(r_arr)):
                df_r = pandas.DataFrame(r_arr, columns=[
                                        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'])
                tmp = r_arr[df_r['M'].idxmax()]
                formation_arr.append([tmp[0], str(17 + x), tmp[1], tmp[2], tmp[3], tmp[4], tmp[5],
                                      tmp[6], tmp[7], tmp[8], tmp[9], tmp[10], tmp[11], str(tmp[12]), tmp[13]])
                r_arr.pop(df_r['M'].idxmax())

            fillTableCsv()

            tabs.setCurrentIndex(1)


def on_btn_get_data_clicked():
    if ed_team_name.text() != '' and ed_team_id.text() != '':
        global full_arr
        global formation_arr
        while len(full_arr) > 0:
            full_arr.pop(0)

        while len(formation_arr) > 0:
            formation_arr.pop(0)

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
                drzavljanstvo = zapis.findAll("td")[7].find("img")["title"]
                cena = zapis.findAll("td")[8].text.strip()
                cena = cena.replace("-", "")
                if cena == '':
                    cena_div = 0
                    cena_swos = 0
                    _sum = 0
                else:
                    cena_div = int(cena.replace("€", "").replace("k", "000").replace("m", "0000").replace(".", "")) / 1000000
                    cena_swos = getPrice(posi, cena_div)
                    _sum = int(getSkill(posi, cena_div))

                rnd_array = returnSkillArray(_sum)

                if posi == 'GK':
                    pa = str(0)
                    ve = str(0)
                    he = str(0)
                    ta = str(0)
                    co = str(0)
                    sp = str(0)
                    fi = str(0)
                else:
                    pa = str(rnd_array[0])
                    ve = str(rnd_array[1])
                    he = str(rnd_array[2])
                    ta = str(rnd_array[3])
                    co = str(rnd_array[4])
                    sp = str(rnd_array[5])
                    fi = str(rnd_array[6])

                full_arr.append([getCountry(drzavljanstvo), igralec, posi,
                                 general_skin, pa, ve, he, ta, co, sp, fi, cena_swos, str(_sum), str(cena_div), str(0)])

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
                minute = zapis.find("td", {"class": "rechts"}).text
                minute = minute.replace(".", "").replace(
                    "'", "").replace("-", "0")
                minute = str(minute)

                for igrac in full_arr:
                    if igrac[1] == igralec:
                        igrac[14] = minute
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
    tabela.setColumnCount(15)
    tabela.setHorizontalHeaderLabels(["National", "Name", "Position", "Player skin", "PA",
                                      "VE", "HE", "TA", "CO", "SP", "FI", "SWOS price", "Sum skills", "TM price", "Minutes"])

    for row in range(0, len(full_arr)):
        for column in range(0, 15):
            tabela.setItem(row, column, QTableWidgetItem(
                (full_arr[row][column])))

    header = tabela.horizontalHeader()
    for x in range(0, 15):
        header.setSectionResizeMode(x, QHeaderView.ResizeToContents)


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

    header = tabela_csv.horizontalHeader()
    for x in range(0, 15):
        header.setSectionResizeMode(x, QHeaderView.ResizeToContents)


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

                formation_arr[row] = igralec_new
                formation_arr[tmp_newid - 1] = igralec_old

                formation_arr[row][1] = str(row + 1)
                formation_arr[tmp_newid - 1][1] = str(tmp_newid)

                for row in range(0, len(formation_arr)):
                    for column in range(0, 15):
                        tabela_csv.setItem(row, column, QTableWidgetItem(
                            (formation_arr[row][column])))


def getPlayerID(max_len):
    num, ok = QInputDialog.getInt(
        tab_SWOS, "Player ID", "Enter player ID to change", 1, 1, max_len, 1)

    if ok:
        return num


def generateMenu():
    if tabela.selectionModel().selection().indexes():
        for i in tabela.selectionModel().selection().indexes():
            row, column = i.row(), i.column()

        global full_arr
        menu = QMenu()

        deleAction = menu.addAction("Delete this player")

        changePlayerName = menu.addAction("Change player name")

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
            full_arr.pop(row)
        elif action == changePlayerName:
            tmp_name = setName(str(full_arr[row][1]))
            if tmp_name != None:
                full_arr[row][1] = tmp_name
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


def setName(current):
    text, okPressed = QInputDialog.getText(
        tab_TM, "Player name", "Enter new name:", QLineEdit.Normal, current)

    if okPressed and text != '':
        return text


app = QApplication([])
app.setStyle('Fusion')

tabs = QTabWidget()
tab_TM = QWidget()
tab_SWOS = QWidget()
layout_tm = QVBoxLayout()
layout_swos = QVBoxLayout()
layout_1 = QHBoxLayout()
layout_2 = QHBoxLayout()
layout_3 = QHBoxLayout()
layout_4 = QHBoxLayout()
layout_5 = QHBoxLayout()
layout_6 = QHBoxLayout()
layout_7 = QHBoxLayout()

tabs.addTab(tab_TM, "Transfermarkt")
tabs.addTab(tab_SWOS, "SWOS csv")

# variables for GUI
full_arr = []
formation_arr = []

# components for GUI
lbl_team_name = QLabel('Team short name TM ')
ed_team_name = QLineEdit('nd-lendava-1903')
lbl_team_id = QLabel('Team ID TM')
ed_team_id = QLineEdit('9233')
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

tabela = QTableWidget()
tabela.setEditTriggers(QTableWidget.NoEditTriggers)
tabela.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
tabela.customContextMenuRequested.connect(generateMenu)

lbl_league_id_swoes = QLabel('League ID SWOES')
ed_league_id_swoes = QLineEdit()
lbl_team_id_swoes = QLabel('Team ID SWOES')
ed_team_id_swoes = QLineEdit()

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
lbl_team_name.setFixedWidth(100)
lbl_team_id.setFixedWidth(100)
lbl_league_id_swoes.setFixedWidth(100)
lbl_team_id_swoes.setFixedWidth(100)
lbl_team_name_tm.setFixedWidth(100)
lbl_coach_name_tm.setFixedWidth(100)
lbl_formation_tm.setFixedWidth(100)

# layout - tab TM
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
layout_tm.addLayout(layout_1)
layout_tm.addLayout(layout_2)

layout_tm.addWidget(btn_get_data)

layout_tm.addLayout(layout_3)

layout_tm.addWidget(tabela)

layout_tm.addWidget(btn_generate)

# layout - main SWOS
layout_swos.addLayout(layout_4)
layout_swos.addLayout(layout_5)
layout_swos.addLayout(layout_6)
layout_swos.addLayout(layout_7)

tab_TM.setLayout(layout_tm)
tab_SWOS.setLayout(layout_swos)
tabs.setWindowTitle("SWOS - TM Editor v1.0")
tabs.show()
app.exec_()