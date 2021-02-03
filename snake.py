import numpy as np
from time import sleep
from PySide2.QtCore import QTimer
from pynput import keyboard
import os
import snakes_graphic
import snakes_imgs
import sys
import cv2
import socket
import xml.etree.ElementTree as ET
import json


class Window(snakes_graphic.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = snakes_graphic.Ui_Snakes()
        self.ui.setupUi(self)
        self.snek_timer = QTimer(self)
        self.replay_timer = QTimer(self)
        self.sneks = SnekGejm()
        self.snek_timer.timeout.connect(self.sneks.biegnij)
        self.replay_timer.timeout.connect(self.sneks.run_replay)
        self.multiplayer = False
        self.client_socket = None
        self.ip = ""
        self.port = ""
        self.trzymaj = None
        self.replay_happening = False

        self.ui.exitButton.clicked.connect(self.exit_button)
        self.ui.onePlayer.clicked.connect(self.one_player_button)
        self.ui.twoPlayers.clicked.connect(self.two_players_button)
        self.ui.startButton.clicked.connect(self.start_button)
        self.ui.resetButton.clicked.connect(self.reset_button)
        self.ui.pauseButton.clicked.connect(self.pause_button)
        self.ui.button_multiplayer.clicked.connect(self.start_multiplayer_game)
        self.ui.replayButton.clicked.connect(self.replay_button)
        self.ui.readjsonButton.clicked.connect(self.read_json)
        self.ui.savejsonButton.clicked.connect(self.save_json)
        self.ui.lineEdit.textChanged.connect(self.first_line_edit)
        self.ui.lineEdit_2.textChanged.connect(self.second_line_edit)
        self.ui.botButton.clicked.connect(self.bot_game)

    def run(self):
        self.sneks.blank()

    def exit_button(self):
        sys.exit()

    def one_player_button(self):
        if not self.replay_happening: self.sneks.number_of_players = 1

    def two_players_button(self):
        if not self.replay_happening and not self.sneks.ai_game: self.sneks.number_of_players = 2

    def start_button(self):
        if not self.sneks.game_on and not self.replay_happening:
            self.sneks.game_on = True
            self.snek_timer.start(400)
            self.sneks.new_game()

    def reset_button(self):
        self.replay_happening = False
        self.replay_timer.stop()
        self.sneks.game_on = True
        self.snek_timer.start(400)
        if self.multiplayer:
            self.multiplayer = False
            self.client_socket.close()
        self.sneks.new_game()

    def pause_button(self):
        if not self.replay_happening:
            if self.sneks.game_on and not self.multiplayer:
                self.snek_timer.stop()
                self.sneks.game_on = False
            elif not self.sneks.game_on and not self.multiplayer:
                self.snek_timer.start(400)
                self.sneks.game_on = True

    def bot_game(self):
        if not self.replay_happening:
            self.sneks.ai_game = True

    def replay_button(self):
        if not self.replay_happening:
            jest_plik = self.sneks.wczytaj_xml()
            if jest_plik:
                self.snek_timer.stop()
                self.sneks.game_on = False
                self.replay_happening = True
                self.trzymaj = self.sneks.plansza
                self.replay_timer.start(400)

    def resume_game(self):
        self.replay_timer.stop()
        self.replay_happening = False
        self.sneks.plansza = self.trzymaj
        self.snek_timer.start(400)
        self.sneks.game_on = True

    def save_json(self):
        data = {}
        data['configuration'] = []
        data['configuration'].append({
            'ip': self.ip,
            'port': self.port
        })

        with open('json_configuration.json', 'w') as f:
            json.dump(data, f)

    def read_json(self):
        try:
            with open('json_configuration.json') as f:
                data = json.load(f)
                for conf in data['configuration']:
                    self.ui.lineEdit.setText(conf['ip'])
                    self.ui.lineEdit_2.setText(conf['port'])
        except FileNotFoundError:
            return

    def first_line_edit(self):
        self.ip = self.ui.lineEdit.text()

    def second_line_edit(self):
        self.port = self.ui.lineEdit_2.text()

    def start_multiplayer_game(self):
        porcik = -1
        try:
            porcik = int(self.port)
        except ValueError:
            self.ui.textEdit.setText("Wrong server port.")
            self.multiplayer = False
            return
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.ip, porcik))
            self.ui.textEdit.setText("Connected to server {}:{}.".format(self.ip, porcik))
            #self.multiplayer = True
            self.sneks.game_on = True
            self.snek_timer.start(400)
        except socket.error:
            self.ui.textEdit.setText("Couldn't connect to the server.")
            self.multiplayer = False
            return

    def send_data(self, str_data):
        data_out = bytes("&^&" + str_data + "&^&", "utf-8")
        try:
            self.client_socket.sendall(data_out)
        except socket.error:
            pass


class SnekGejm(snakes_graphic.QGraphicsItem):
    def __init__(self):
        super(SnekGejm, self).__init__()
        self.number_of_players = 1
        self.ai_game = False
        self.wonsz = None
        self.wonsz2 = None
        self.kierunek = int(6 * np.random.rand(1))
        self.kierunek2 = int(6 * np.random.rand(1))
        self.punkty1 = 0
        self.punkty2 = 0
        self.owoc = False
        self.owoc_pos = None
        self.wysokosc = 17
        self.szerokosc = 7
        self.game_on = False
        self.key_char = ""
        self.key_char2 = ""
        self.tile_width = 58
        self.tile_height = 44
        self.tile_img = snakes_graphic.QPixmap(":/snake_images/tile.png")
        self.snake1_img = snakes_graphic.QPixmap(":/snake_images/snake1.png")
        self.head1_img = snakes_graphic.QPixmap(":/snake_images/head1.png")
        self.snake2_img = snakes_graphic.QPixmap(":/snake_images/snake2.png")
        self.head2_img = snakes_graphic.QPixmap(":/snake_images/head2.png")
        self.cherry_img = snakes_graphic.QPixmap(":/snake_images/cherry.png")
        self.replay = []
        self.xml_replay = []
        self.plansza = self.nowa_plansza()

    def blank(self):
        self.game_on = False
        gameWindow.snek_timer.stop()
        gameWindow.ui.textEdit.setText("First player's controls: q, w, e, a, s, d\nSecond player's controls: "
                                       "i, o, p, j, k, l\nChoose number of players and press Start.")
        gameWindow.ui.lineEdit.setText("Server IP")
        gameWindow.ui.lineEdit_2.setText("Port")
        self.pusta_plansza()

    def new_game(self):
        self.plansza = self.nowa_plansza()
        self.kierunek = int(6 * np.random.rand(1))
        self.kierunek2 = int(6 * np.random.rand(1))
        self.punkty1 = 0
        self.punkty2 = 0
        self.wonsz = self.nowy_wonsz(self.kierunek, 1)
        if self.number_of_players == 2 or self.ai_game: self.wonsz2 = self.nowy_wonsz(self.kierunek2, 2)
        else: self.wonsz2 = None
        self.owoc = False
        self.biegnij()


    class Komorka():
        def __init__(self, typ, y, x):
            self.type = typ
            self.pos_y = y
            self.pos_x = x
            self.wartosc_g = 0
            self.wartosc_h = 0
            self.wartosc_f = 0
            self.wczesniejsza_pos = None


    def kolizja(self, position):
        y, x = position
        try:
            if self.plansza[y][x].type != 0:
                return True
        except IndexError:
            return True
        return False

    def uaktualnij_plansze(self):
        if self.wonsz:
            self.wonsz, self.punkty1 = self.uaktualnij_wensza(self.wonsz, self.kierunek, self.punkty1)
        if self.wonsz2 and not self.ai_game:
            self.wonsz2, self.punkty2 = self.uaktualnij_wensza(self.wonsz2, self.kierunek2, self.punkty2)
        elif self.wonsz2 and self.ai_game:
            self.wonsz2, self.punkty2 = self.inteligentny_wonsz(self.wonsz2, self.punkty2)
        self.wartosci_planszy()
        if self.wonsz and self.wonsz2:
            gameWindow.ui.textEdit.setText("Both players are alive.")
        elif self.wonsz and not self.wonsz2:
            gameWindow.ui.textEdit.setText("Only first player is alive.")
        elif not self.wonsz and self.wonsz2:
            gameWindow.ui.textEdit.setText("Only second player is alive.")
        else:
            self.blank()
        while not self.owoc:
            y1 = int(self.wysokosc*np.random.rand(1))
            x1 = int(self.szerokosc*np.random.rand(1))
            if not self.kolizja((y1, x1)):
                self.owoc_pos = (y1, x1)
                self.owoc = True
        y, x = self.owoc_pos
        self.plansza[y][x].type = 3
        gameWindow.ui.playerOnePoints.setText(str(self.punkty1))
        gameWindow.ui.playerTwoPoints.setText(str(self.punkty2))
        self.rysuj_plansze(False)

    def wartosci_planszy(self):
        for rzad in self.plansza:
            for komorka in rzad:
                komorka.type = 0
        if self.wonsz:
            for poz in self.wonsz:
                y, x = poz
                self.plansza[y][x].type = 1
            y, x = self.wonsz[0]
            self.plansza[y][x].type = 4
        if self.wonsz2:
            for poz in self.wonsz2:
                y, x = poz
                self.plansza[y][x].type = 2
            y, x = self.wonsz2[0]
            self.plansza[y][x].type = 5
        gameWindow.ui.playerOnePoints.setText(str(self.punkty1))
        gameWindow.ui.playerTwoPoints.setText(str(self.punkty2))

    def uaktualnij_wensza(self, wonsz, kierunkowy, punkciki):
        y, x = wonsz[0]
        y1, x1 = 0, 0
        if kierunkowy == 0:
            y1 = y - 2
            x1 = x
        elif kierunkowy == 1:
            if y % 2:
                y1 = y - 1
                x1 = x
            else:
                y1 = y - 1
                x1 = x - 1
        elif kierunkowy == 2:
            if y % 2:
                y1 = y + 1
                x1 = x
            else:
                y1 = y + 1
                x1 = x - 1
        elif kierunkowy == 3:
            y1 = y + 2
            x1 = x
        elif kierunkowy == 4:
            if y % 2:
                y1 = y + 1
                x1 = x + 1
            else:
                y1 = y + 1
                x1 = x
        elif kierunkowy == 5:
            if y % 2:
                y1 = y - 1
                x1 = x + 1
            else:
                y1 = y - 1
                x1 = x
        if x1 == -1: x1 = self.szerokosc - 1
        elif x1 == self.szerokosc: x1 = 0
        if y1 == -2: y1 = self.wysokosc - 2
        elif y1 == -1: y1 = self.wysokosc - 1
        elif y1 == self.wysokosc: y1 = 0
        elif y1 == self.wysokosc + 1: y1 = 1
        wonsz.insert(0, (y1, x1))
        if self.plansza[y1][x1].type == 1:
            return None, punkciki
        elif self.plansza[y1][x1].type == 2:
            return None, punkciki
        elif self.plansza[y1][x1].type == 3:
            self.owoc = False
            punkciki += 10
            return wonsz, punkciki
        elif self.plansza[y1][x1].type == 4:
            return None, punkciki
        elif self.plansza[y1][x1].type == 5:
            return None,punkciki
        wonsz.pop()
        return wonsz, punkciki

    def inteligentny_wonsz(self, wonsz, punkciki):
        y, x = wonsz[0]
        y_goal = -1
        x_goal = -1
        if self.owoc: y_goal, x_goal = self.owoc_pos
        else:
            return self.random_move(wonsz, punkciki)
        openset = []
        closedset = []

        self.plansza[y][x].wczesniejsza_pos = (y, x)
        self.plansza[y][x].wartosc_g = 0
        self.plansza[y][x].wartosc_h = np.sqrt(np.power((x_goal - x), 2) + np.power((y_goal - y), 2))
        self.plansza[y][x].wartosc_f = self.plansza[y][x].wartosc_g + self.plansza[y][x].wartosc_h

        obecne_pole = self.plansza[y][x]
        openset.append(obecne_pole)

        while len(openset) > 0:
            min_wartosc = 1000000
            index = 0
            for ind, pole in enumerate(openset):
                if pole.wartosc_f < min_wartosc:
                    index = ind
                    min_wartosc = pole.wartosc_f
                    obecne_pole = pole

            if obecne_pole.pos_x == x_goal and obecne_pole.pos_y == y_goal:
                y1, x1 = self.find_next_move(y_goal, x_goal, y, x)
                wonsz.insert(0, (y1, x1))
                if self.plansza[y1][x1].type == 3:
                    self.owoc = False
                    punkciki += 10
                    return wonsz, punkciki
                wonsz.pop()
                return wonsz, punkciki

            curr_x = obecne_pole.pos_x
            curr_y = obecne_pole.pos_y
            openset.pop(index)
            closedset.append(obecne_pole)

            neighbours = []
            if curr_y % 2:
                neigh_y = curr_y - 1
                neigh_x = curr_x
                if neigh_y < 0:
                    neigh_y += self.wysokosc
                if self.plansza[neigh_y][neigh_x].type == 0 or self.plansza[neigh_y][neigh_x].type == 3:
                    if self.plansza[neigh_y][neigh_x] not in closedset:
                        neighbours.append(self.plansza[neigh_y][neigh_x])
                neigh_y = curr_y + 1
                neigh_x = curr_x
                if neigh_y > self.wysokosc - 1:
                    neigh_y -= self.wysokosc
                if self.plansza[neigh_y][neigh_x].type == 0 or self.plansza[neigh_y][neigh_x].type == 3:
                    if self.plansza[neigh_y][neigh_x] not in closedset:
                        neighbours.append(self.plansza[neigh_y][neigh_x])
                neigh_y = curr_y - 2
                neigh_x = curr_x
                if neigh_y < 0:
                    neigh_y += self.wysokosc
                if self.plansza[neigh_y][neigh_x].type == 0 or self.plansza[neigh_y][neigh_x].type == 3:
                    if self.plansza[neigh_y][neigh_x] not in closedset:
                        neighbours.append(self.plansza[neigh_y][neigh_x])
                neigh_y = curr_y + 2
                neigh_x = curr_x
                if neigh_y > self.wysokosc - 1:
                    neigh_y -= self.wysokosc
                if self.plansza[neigh_y][neigh_x].type == 0 or self.plansza[neigh_y][neigh_x].type == 3:
                    if self.plansza[neigh_y][neigh_x] not in closedset:
                        neighbours.append(self.plansza[neigh_y][neigh_x])
                neigh_y = curr_y - 1
                neigh_x = curr_x + 1
                if neigh_y < 0:
                    neigh_y += self.wysokosc
                if neigh_x > self.szerokosc - 1:
                    neigh_x -= self.szerokosc
                if self.plansza[neigh_y][neigh_x].type == 0 or self.plansza[neigh_y][neigh_x].type == 3:
                    if self.plansza[neigh_y][neigh_x] not in closedset:
                        neighbours.append(self.plansza[neigh_y][neigh_x])
                neigh_y = curr_y + 1
                neigh_x = curr_x + 1
                if neigh_y > self.wysokosc - 1:
                    neigh_y -= self.wysokosc
                if neigh_x > self.szerokosc - 1:
                    neigh_x -= self.szerokosc
                if self.plansza[neigh_y][neigh_x].type == 0 or self.plansza[neigh_y][neigh_x].type == 3:
                    if self.plansza[neigh_y][neigh_x] not in closedset:
                        neighbours.append(self.plansza[neigh_y][neigh_x])
            else:
                neigh_y = curr_y - 1
                neigh_x = curr_x
                if neigh_y < 0:
                    neigh_y += self.wysokosc
                if self.plansza[neigh_y][neigh_x].type == 0 or self.plansza[neigh_y][neigh_x].type == 3:
                    if self.plansza[neigh_y][neigh_x] not in closedset:
                        neighbours.append(self.plansza[neigh_y][neigh_x])
                neigh_y = curr_y + 1
                neigh_x = curr_x
                if neigh_y > self.wysokosc - 1:
                    neigh_y -= self.wysokosc
                if self.plansza[neigh_y][neigh_x].type == 0 or self.plansza[neigh_y][neigh_x].type == 3:
                    if self.plansza[neigh_y][neigh_x] not in closedset:
                        neighbours.append(self.plansza[neigh_y][neigh_x])
                neigh_y = curr_y - 2
                neigh_x = curr_x
                if neigh_y < 0:
                    neigh_y += self.wysokosc
                if self.plansza[neigh_y][neigh_x].type == 0 or self.plansza[neigh_y][neigh_x].type == 3:
                    if self.plansza[neigh_y][neigh_x] not in closedset:
                        neighbours.append(self.plansza[neigh_y][neigh_x])
                neigh_y = curr_y + 2
                neigh_x = curr_x
                if neigh_y > self.wysokosc - 1:
                    neigh_y -= self.wysokosc
                if self.plansza[neigh_y][neigh_x].type == 0 or self.plansza[neigh_y][neigh_x].type == 3:
                    if self.plansza[neigh_y][neigh_x] not in closedset:
                        neighbours.append(self.plansza[neigh_y][neigh_x])
                neigh_y = curr_y - 1
                neigh_x = curr_x - 1
                if neigh_y < 0:
                    neigh_y += self.wysokosc
                if neigh_x < 0:
                    neigh_x += self.szerokosc
                if self.plansza[neigh_y][neigh_x].type == 0 or self.plansza[neigh_y][neigh_x].type == 3:
                    if self.plansza[neigh_y][neigh_x] not in closedset:
                        neighbours.append(self.plansza[neigh_y][neigh_x])
                neigh_y = curr_y + 1
                neigh_x = curr_x - 1
                if neigh_y > self.wysokosc - 1:
                    neigh_y -= self.wysokosc
                if neigh_x < 0:
                    neigh_x += self.szerokosc
                if self.plansza[neigh_y][neigh_x].type == 0 or self.plansza[neigh_y][neigh_x].type == 3:
                    if self.plansza[neigh_y][neigh_x] not in closedset:
                        neighbours.append(self.plansza[neigh_y][neigh_x])

            for ind, neighbour in enumerate(neighbours):
                neigh_y = neighbour.pos_y
                neigh_x = neighbour.pos_x
                wartosc_przewidywana = obecne_pole.wartosc_g\
                                       + np.sqrt(np.power((curr_x - neigh_x), 2)
                                                 + np.power((curr_y - neigh_y), 2))
                neighbour_in_openset = False
                if neighbour in openset: neighbour_in_openset = True
                if not neighbour_in_openset:
                    self.plansza[neigh_y][neigh_x].wczesniejsza_pos = (curr_y, curr_x)
                    self.plansza[neigh_y][neigh_x].wartosc_g = wartosc_przewidywana
                    self.plansza[neigh_y][neigh_x].wartosc_h = np.sqrt(np.power((x_goal - neigh_x), 2) +
                                                                       np.power((y_goal - neigh_y), 2))
                    self.plansza[neigh_y][neigh_x].wartosc_f = self.plansza[neigh_y][neigh_x].wartosc_g + \
                                                               self.plansza[neigh_y][neigh_x].wartosc_h
                    openset.append(self.plansza[neigh_y][neigh_x])
                elif wartosc_przewidywana < self.plansza[neigh_y][neigh_x].wartosc_g:
                    self.plansza[neigh_y][neigh_x].wczesniejsza_pos = (curr_y, curr_x)
                    self.plansza[neigh_y][neigh_x].wartosc_g = wartosc_przewidywana
                    self.plansza[neigh_y][neigh_x].wartosc_f = self.plansza[neigh_y][neigh_x].wartosc_g + \
                                                               self.plansza[neigh_y][neigh_x].wartosc_h
                    indeksior = openset.index(neighbour)
                    openset[indeksior].wczesniejsza_pos = (curr_y, curr_x)
                    openset[indeksior].wartosc_g = wartosc_przewidywana
                    openset[indeksior].wartosc_f = self.plansza[neigh_y][neigh_x].wartosc_f

        return self.random_move(wonsz, punkciki)

    def find_next_move(self, goal_y, goal_x, wonsz_y, wonsz_x):
        not_the_whole_path_yet = True
        y, x = self.plansza[goal_y][goal_x].wczesniejsza_pos
        if y == wonsz_y and x == wonsz_x:
            return goal_y, goal_x
        while not_the_whole_path_yet:
            next_y, next_x = self.plansza[y][x].wczesniejsza_pos
            if next_y == wonsz_y and next_x == wonsz_x:
                not_the_whole_path_yet = False
                return y, x
            y = next_y
            x = next_x

    def random_move(self, wonsz, punkciki):
        y, x = wonsz[0]
        y1, x1 = -1, -1
        juz_byly = []
        puste_pole = False
        while not puste_pole:
            if len(juz_byly) == 6:
                return None, punkciki
            dobry_indeks = False
            indeks_kierunkowy = -1
            while not dobry_indeks:
                indeks_kierunkowy = int(6 * np.random.rand(1))
                if indeks_kierunkowy in juz_byly:
                    dobry_indkes = False
                else:
                    dobry_indeks = True
                    juz_byly.append(indeks_kierunkowy)

            if indeks_kierunkowy == 0:
                y1 = y - 2
                x1 = x
            elif indeks_kierunkowy == 1:
                if y % 2:
                    y1 = y - 1
                    x1 = x
                else:
                    y1 = y - 1
                    x1 = x - 1
            elif indeks_kierunkowy == 2:
                if y % 2:
                    y1 = y + 1
                    x1 = x
                else:
                    y1 = y + 1
                    x1 = x - 1
            elif indeks_kierunkowy == 3:
                y1 = y + 2
                x1 = x
            elif indeks_kierunkowy == 4:
                if y % 2:
                    y1 = y + 1
                    x1 = x + 1
                else:
                    y1 = y + 1
                    x1 = x
            elif indeks_kierunkowy == 5:
                if y % 2:
                    y1 = y - 1
                    x1 = x + 1
                else:
                    y1 = y - 1
                    x1 = x
            if x1 == -1:
                x1 = self.szerokosc - 1
            elif x1 == self.szerokosc:
                x1 = 0
            if y1 == -2:
                y1 = self.wysokosc - 2
            elif y1 == -1:
                y1 = self.wysokosc - 1
            elif y1 == self.wysokosc:
                y1 = 0
            elif y1 == self.wysokosc + 1:
                y1 = 1

            if self.plansza[y1][x1].type == 0:
                wonsz.insert(0, (y1, x1))
                wonsz.pop()
                return wonsz, punkciki
            elif self.plansza[y1][x1].type == 1:
                puste_pole = False
            elif self.plansza[y1][x1].type == 2:
                puste_pole = False
            elif self.plansza[y1][x1].type == 3:
                wonsz.insert(0, (y1, x1))
                self.owoc = False
                punkciki += 10
                return wonsz, punkciki
            elif self.plansza[y1][x1].type == 4:
                puste_pole = False
            elif self.plansza[y1][x1].type == 5:
                pust_pole = False



    def rysuj_plansze(self, replay):
        scena = snakes_graphic.QGraphicsScene()
        item = None
        for i, row in enumerate(self.plansza):
            for j, val in enumerate(row):
                if self.plansza[i][j].type == 0:
                    item = snakes_graphic.QGraphicsPixmapItem(self.tile_img)
                elif self.plansza[i][j].type == 1:
                    item = snakes_graphic.QGraphicsPixmapItem(self.snake1_img)
                elif self.plansza[i][j].type == 2:
                    item = snakes_graphic.QGraphicsPixmapItem(self.snake2_img)
                elif self.plansza[i][j].type == 3:
                    item = snakes_graphic.QGraphicsPixmapItem(self.cherry_img)
                elif self.plansza[i][j].type == 4:
                    item = snakes_graphic.QGraphicsPixmapItem(self.head1_img)
                else:
                    item = snakes_graphic.QGraphicsPixmapItem(self.head2_img)
                if i % 2:
                    item.setPos((j * (self.tile_width * (3 / 2))) + (self.tile_width * (3 / 4)),
                                i * (self.tile_height) * (1 / 2))
                else:
                    item.setPos(j * (self.tile_width * (3 / 2)), i * (self.tile_height) * (1 / 2))
                scena.addItem(item)
        if replay:
            item = snakes_graphic.QGraphicsTextItem("REPLAY")
            item.setPos(198, 100)
            item.setScale(5.0)
            scena.addItem(item)
        gameWindow.ui.graphicsView.setScene(scena)

    def pusta_plansza(self):
        scena = snakes_graphic.QGraphicsScene()

        for i, row in enumerate(self.plansza):
            for j, val in enumerate(row):
                item = snakes_graphic.QGraphicsPixmapItem(self.tile_img)
                if i%2:
                    item.setPos((j * (self.tile_width * (3 / 2))) + (self.tile_width * (3/4)),
                                i * (self.tile_height) * (1/2))
                else:
                    item.setPos(j * (self.tile_width * (3 / 2)), i * (self.tile_height) * (1/2))
                scena.addItem(item)

        gameWindow.ui.graphicsView.setScene(scena)

    def nowa_plansza(self):
        komorki_pion = self.wysokosc
        komorki_poziom = self.szerokosc
        board = [[]]
        for i in range(komorki_pion):
            for j in range(komorki_poziom):
                board[i].append(self.Komorka(0, i, j))
            board.append([])
        return board

    def nowy_wonsz(self, kierunkowy, nr_wensza):
        y = int((2 + (self.wysokosc - 4)*np.random.rand(1)))
        x = int((1 + (self.szerokosc - 2)*np.random.rand(1)))
        y1 = 0
        x1 = 0
        if kierunkowy == 0:
            y1 = y + 2
            x1 = x
        elif kierunkowy == 1:
            if y % 2:
                y1 = y + 1
                x1 = x + 1
            else:
                y1 = y + 1
                x1 = x
        elif kierunkowy == 2:
            if y % 2:
                y1 = y - 1
                x1 = x + 1
            else:
                y1 = y - 1
                x1 = x
        elif kierunkowy == 3:
            y1 = y - 2
            x1 = x
        elif kierunkowy == 4:
            if y % 2:
                y1 = y - 1
                x1 = x
            else:
                y1 = y - 1
                x1 = x - 1
        elif kierunkowy == 5:
            if y % 2:
                y1 = y + 1
                x1 = x
            else:
                y1 = y + 1
                x1 = x - 1
        if self.kolizja((y, x)) or self.kolizja((y1, x1)):
            if nr_wensza == 1: self.wonsz = self.nowy_wonsz(kierunkowy, nr_wensza)
            elif nr_wensza == 2: self.wonsz2 = self.nowy_wonsz(kierunkowy, nr_wensza)
        self.plansza[y][x].type = nr_wensza
        self.plansza[y1][x1].type = nr_wensza
        return [(y, x), (y1, x1)]

    def on_press(self, key):
        try:
            self.key_char = key.char
        except AttributeError:
            pass

    def on_press2(self, key):
        try:
            self.key_char2 = key.char
        except AttributeError:
            pass

    def konwertuj_plansze(self, plansza_w_bajtach):
        komorki_pion = self.wysokosc
        komorki_poziom = self.szerokosc
        board = [[]]
        for i in range(komorki_pion):
            for j in range(komorki_poziom):
                board[i].append(self.Komorka(0, i, j))
            board.append([])
        wiadomosc = plansza_w_bajtach.decode()
        wiadomosci = wiadomosc.split("&^&")
        plansza_w_stringach = wiadomosci[-1]
        for index, character in enumerate(plansza_w_stringach):
            board[index//komorki_pion][index%komorki_pion].type = int(character)
        return board

    def dodaj_replay(self):
        komorki_pion = self.wysokosc
        komorki_poziom = self.szerokosc
        board = []
        for i in range(komorki_pion):
            for j in range(komorki_poziom):
                board.append(self.plansza[i][j].type)
        self.replay.insert(0, board)
        if len(self.replay) > 26: self.replay.pop()

    def run_replay(self):
        if len(self.xml_replay) == 1: gameWindow.resume_game()
        for index, value in enumerate(self.xml_replay[-1]):
            self.plansza[index // self.szerokosc][index % self.szerokosc].type = value
        self.xml_replay.pop()
        self.rysuj_plansze(True)

    def replay_w_stringu(self, wektor):
        plansza_w_stringach = ""
        for elem in wektor:
            plansza_w_stringach += str(elem)
        return plansza_w_stringach

    def replay_w_intach(self, wektor):
        plansza_w_intach = []
        for char in wektor:
            plansza_w_intach.append(int(char))
        return plansza_w_intach

    def zapisz_xml(self):
        replay = ET.Element('replay')
        for i in range(len(self.replay)):
            plansza = ET.SubElement(replay, 'plansza')
            plansza.set('name', 'plansza')
            plansza.text = self.replay_w_stringu(self.replay[i])

        string_replay = ET.tostring(replay).decode('ascii')
        string_replay = string_replay.replace('><', '>\n<')
        f = open("replay.xml", "w")
        f.write(string_replay)
        f.close()

    def wczytaj_xml(self):
        try:
            tree = ET.parse("replay.xml")
            root = tree.getroot()
            for child in root:
                self.xml_replay.append(self.replay_w_intach(child.text))
            return True
        except FileNotFoundError:
            return False

    def biegnij(self):
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()
        listener2 = keyboard.Listener(on_press=self.on_press2)
        listener2.start()

        if self.game_on:

            if self.key_char == "w":
                if self.kierunek != 3: self.kierunek = 0
            elif self.key_char == "q":
                if self.kierunek != 4: self.kierunek = 1
            elif self.key_char == "a":
                if self.kierunek != 5: self.kierunek = 2
            elif self.key_char == "s":
                if self.kierunek != 0: self.kierunek = 3
            elif self.key_char == "d":
                if self.kierunek != 1: self.kierunek = 4
            elif self.key_char == "e":
                if self.kierunek != 2: self.kierunek = 5

            if self.key_char2 == "o":
                if self.kierunek2 != 3: self.kierunek2 = 0
            elif self.key_char2 == "i":
                if self.kierunek2 != 4: self.kierunek2 = 1
            elif self.key_char2 == "j":
                if self.kierunek2 != 5: self.kierunek2 = 2
            elif self.key_char2 == "k":
                if self.kierunek2 != 0: self.kierunek2 = 3
            elif self.key_char2 == "l":
                if self.kierunek2 != 1: self.kierunek2 = 4
            elif self.key_char2 == "p":
                if self.kierunek2 != 2: self.kierunek2 = 5

            if gameWindow.multiplayer is True:
                data_in = b''
                while True:
                    try:
                        data_t = gameWindow.client_socket.recv(25000)
                        data_in += data_t
                        if len(data_t) < 25000:
                            break
                    except socket.error:
                        break
                if len(data_in) > 0:
                    self.plansza = self.konwertuj_plansze(data_in)
                else:
                    gameWindow.multiplayer = False
                    return
                gameWindow.send_data(str(self.kierunek))
                self.rysuj_plansze()
            else:
                self.uaktualnij_plansze()

            self.dodaj_replay()
            self.zapisz_xml()


if __name__ == "__main__":
    app = snakes_graphic.QApplication(sys.argv)
    gameWindow = Window()
    gameWindow.run()
    gameWindow.show()
    sys.exit(app.exec_())