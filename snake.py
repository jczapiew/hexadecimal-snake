import numpy as np
from time import sleep
from pynput import keyboard
import os


class SnekGejm():
    def __init__(self):
        self.plansza = None
        self.wonsz = None
        self.kierunek = int(6*np.random.rand(1))
        self.owoc = False
        self.owoc_pos = None
        self.wysokosc = 0
        self.szerokosc = 0
        self.game_on = True
        self.key_char = ""
        self.new_game()

    def new_game(self):
        print("\033[1;31;40mWitaj w grze Sneak.")
        print("\033[1;31;40mSterowanie odbywa się za pomocą klawiszy:\nw - górny ruch\nq - lewy górny ruch\n"
              "a - lewy dolny ruch\ns - dolny ruch\nd - prawy dolny ruch\ne - prawy górny ruch")
        print("\033[1;31;40mNa planszy pojawiają się losowo owoce, których zbieranie wydłuża węża.")
        print("\033[1;31;40mPodaj wymiary planszy:\nWysokosc: ")
        height = int(input())
        self.wysokosc = height
        print("\033[1;31;40mSzerokosc: ")
        width = int(input())
        self.szerokosc = width
        self.plansza = self.nowa_plansza()
        self.wonsz = self.nowy_wonsz()
        self.game_on = True
        self.biegnij()

    class Komorka():
        def __init__(self, typ, y, x):
            self.type = typ
            self.pos_y = y
            self.pos_x = x

    def kolizja(self, position):
        y, x = position
        try:
            if self.plansza[y][x].type != 0:
                return True
        except IndexError:
            return True
        return False

    def uaktualnij_plansze(self):
        self.game_on = self.uaktualnij_wensza()
        if not self.game_on:
            print("\033[1;31;40m")
            print("\033[1;31;40mPrzegrales")
            self.new_game()
        for rzad in self.plansza:
            for komorka in rzad:
                komorka.type = 0
        for poz in self.wonsz:
            y, x = poz
            self.plansza[y][x].type = 1
        while not self.owoc:
            y1 = int(self.wysokosc*np.random.rand(1))
            x1 = int(self.szerokosc*np.random.rand(1))
            if not self.kolizja((y1, x1)):
                self.owoc_pos = (y1, x1)
                self.owoc = True
        y, x = self.owoc_pos
        self.plansza[y][x].type = 3
        self.rysuj_plansze()

    def uaktualnij_wensza(self):
        y, x = self.wonsz[0]
        y1, x1 = 0, 0
        if self.kierunek == 0:
            y1 = y - 2
            x1 = x
        elif self.kierunek == 1:
            if y % 2:
                y1 = y - 1
                x1 = x
            else:
                y1 = y - 1
                x1 = x - 1
        elif self.kierunek == 2:
            if y % 2:
                y1 = y + 1
                x1 = x
            else:
                y1 = y + 1
                x1 = x - 1
        elif self.kierunek == 3:
            y1 = y + 2
            x1 = x
        elif self.kierunek == 4:
            if y % 2:
                y1 = y + 1
                x1 = x + 1
            else:
                y1 = y + 1
                x1 = x
        elif self.kierunek == 5:
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
        self.wonsz.insert(0, (y1, x1))
        if self.plansza[y1][x1].type == 1:
            return False
        elif self.plansza[y1][x1].type == 3:
            self.owoc = False
            return True
        self.wonsz.pop()
        return True

    def rysuj_plansze(self):
        plansza_w_stringach = ""
        for rzad in range(self.wysokosc):
            if rzad%2: continue
            plansza_w_stringach += "\033[1;30;40m    "
            for kolumna in range(self.szerokosc):
                plansza_w_stringach += "\033[1;30;47m####"
                if not rzad: plansza_w_stringach += "\033[1;30;40m        "
                else:
                    if   self.plansza[rzad-1][kolumna].type == 0: plansza_w_stringach += "\033[1;30;40m        "
                    elif self.plansza[rzad-1][kolumna].type == 1: plansza_w_stringach += "\033[1;32;46m$$$$$$$$"
                    elif self.plansza[rzad-1][kolumna].type == 2: plansza_w_stringach += "\033[1;30;47m########"
                    elif self.plansza[rzad-1][kolumna].type == 3: plansza_w_stringach += "\033[1;33;41m********"
                if rzad and kolumna + 1 == self.szerokosc: plansza_w_stringach += "\033[1;30;47m##"
            plansza_w_stringach += "\033[1;30;40m\n\033[1;30;40m  "
            for kolumna in range(self.szerokosc):
                plansza_w_stringach += "\033[1;30;47m##"
                if   self.plansza[rzad][kolumna].type == 0: plansza_w_stringach += "\033[1;30;40m    "
                elif self.plansza[rzad][kolumna].type == 1: plansza_w_stringach += "\033[1;32;46m$$$$"
                elif self.plansza[rzad][kolumna].type == 2: plansza_w_stringach += "\033[1;30;47m####"
                elif self.plansza[rzad][kolumna].type == 3: plansza_w_stringach += "\033[1;33;41m****"
                plansza_w_stringach += "\033[1;30;47m##"
                if not rzad: plansza_w_stringach += "\033[1;30;40m    "
                else:
                    if   self.plansza[rzad-1][kolumna].type == 0: plansza_w_stringach += "\033[1;30;40m    "
                    elif self.plansza[rzad-1][kolumna].type == 1: plansza_w_stringach += "\033[1;32;46m$$$$"
                    elif self.plansza[rzad-1][kolumna].type == 2: plansza_w_stringach += "\033[1;30;47m####"
                    elif self.plansza[rzad-1][kolumna].type == 3: plansza_w_stringach += "\033[1;33;41m****"
                if rzad and kolumna + 1 == self.szerokosc: plansza_w_stringach += "\033[1;30;47m##"
            plansza_w_stringach += "\033[1;30;40m\n"
            for kolumna in range(self.szerokosc):
                plansza_w_stringach += "\033[1;30;47m##"
                if   self.plansza[rzad][kolumna].type == 0: plansza_w_stringach += "\033[1;30;40m        "
                elif self.plansza[rzad][kolumna].type == 1: plansza_w_stringach += "\033[1;32;46m$$$$$$$$"
                elif self.plansza[rzad][kolumna].type == 2: plansza_w_stringach += "\033[1;30;47m########"
                elif self.plansza[rzad][kolumna].type == 3: plansza_w_stringach += "\033[1;33;41m********"
                plansza_w_stringach += "\033[1;30;47m##"
                if kolumna + 1 == self.szerokosc: plansza_w_stringach += "\033[1;30;47m##"
            plansza_w_stringach += "\033[1;30;40m\n\033[1;30;40m  "
            for kolumna in range(self.szerokosc):
                plansza_w_stringach += "\033[1;30;47m##"
                if   self.plansza[rzad][kolumna].type == 0: plansza_w_stringach += "\033[1;30;40m    "
                elif self.plansza[rzad][kolumna].type == 1: plansza_w_stringach += "\033[1;32;46m$$$$"
                elif self.plansza[rzad][kolumna].type == 2: plansza_w_stringach += "\033[1;30;47m####"
                elif self.plansza[rzad][kolumna].type == 3: plansza_w_stringach += "\033[1;33;41m****"
                plansza_w_stringach += "\033[1;30;47m##"
                if self.wysokosc%2 and rzad + 1 == self.wysokosc: plansza_w_stringach += "\033[1;30;40m    "
                else:
                    if   self.plansza[rzad+1][kolumna].type == 0: plansza_w_stringach += "\033[1;30;40m    "
                    elif self.plansza[rzad+1][kolumna].type == 1: plansza_w_stringach += "\033[1;32;46m$$$$"
                    elif self.plansza[rzad+1][kolumna].type == 2: plansza_w_stringach += "\033[1;30;47m####"
                    elif self.plansza[rzad+1][kolumna].type == 3: plansza_w_stringach += "\033[1;33;41m****"
                    if kolumna + 1 == self.szerokosc: plansza_w_stringach += "\033[1;30;47m##"
            plansza_w_stringach += "\033[1;30;40m\n"
        if not self.wysokosc%2:
            plansza_w_stringach += "\033[1;30;40m    "
            plansza_w_stringach += "\033[1;30;47m##"
            for kolumna in range(self.szerokosc):
                plansza_w_stringach += "\033[1;30;47m##"
                if   self.plansza[self.wysokosc-1][kolumna].type == 0: plansza_w_stringach += "\033[1;30;40m        "
                elif self.plansza[self.wysokosc-1][kolumna].type == 1: plansza_w_stringach += "\033[1;32;46m$$$$$$$$"
                elif self.plansza[self.wysokosc-1][kolumna].type == 2: plansza_w_stringach += "\033[1;30;47m########"
                elif self.plansza[self.wysokosc-1][kolumna].type == 3: plansza_w_stringach += "\033[1;33;41m********"
                plansza_w_stringach += "\033[1;30;47m##"
            plansza_w_stringach += "\033[1;30;40m\n\033[1;30;40m        "
            for kolumna in range(self.szerokosc):
                plansza_w_stringach += "\033[1;30;47m##"
                if   self.plansza[self.wysokosc-1][kolumna].type == 0: plansza_w_stringach += "\033[1;30;40m    "
                elif self.plansza[self.wysokosc-1][kolumna].type == 1: plansza_w_stringach += "\033[1;32;46m$$$$"
                elif self.plansza[self.wysokosc-1][kolumna].type == 2: plansza_w_stringach += "\033[1;30;47m####"
                elif self.plansza[self.wysokosc-1][kolumna].type == 3: plansza_w_stringach += "\033[1;33;41m****"
                plansza_w_stringach += "\033[1;30;47m##"
                plansza_w_stringach += "\033[1;30;40m    "
            plansza_w_stringach += "\033[1;30;40m\n\033[1;30;40m          "
            for kolumna in range(self.szerokosc):
                plansza_w_stringach += "\033[1;30;47m####"
                plansza_w_stringach += "\033[1;30;40m        "
            plansza_w_stringach += "\033[1;30;40m\n"
        else:
            plansza_w_stringach += "\033[1;30;40m    "
            for kolumna in range(self.szerokosc):
                plansza_w_stringach += "\033[1;30;47m####"
                plansza_w_stringach += "\033[1;30;40m        "
            plansza_w_stringach += "\033[1;30;40m\n"
        print(plansza_w_stringach)

    def nowa_plansza(self):
        komorki_pion = self.wysokosc
        komorki_poziom = self.szerokosc
        board = [[]]
        for i in range(komorki_pion):
            for j in range(komorki_poziom):
                board[i].append(self.Komorka(0, i, j))
            board.append([])
        return board

    def nowy_wonsz(self):
        y = int((2 + (self.wysokosc - 4)*np.random.rand(1)))
        x = int((1 + (self.szerokosc - 2)*np.random.rand(1)))
        y1 = 0
        x1 = 0
        if self.kierunek == 0:
            y1 = y + 2
            x1 = x
        elif self.kierunek == 1:
            if y % 2:
                y1 = y + 1
                x1 = x + 1
            else:
                y1 = y + 1
                x1 = x
        elif self.kierunek == 2:
            if y % 2:
                y1 = y - 1
                x1 = x + 1
            else:
                y1 = y - 1
                x1 = x
        elif self.kierunek == 3:
            y1 = y - 2
            x1 = x
        elif self.kierunek == 4:
            if y % 2:
                y1 = y - 1
                x1 = x
            else:
                y1 = y - 1
                x1 = x - 1
        elif self.kierunek == 5:
            if y % 2:
                y1 = y + 1
                x1 = x
            else:
                y1 = y + 1
                x1 = x - 1
        return [(y, x), (y1, x1)]

    def reset(self):
        self.kierunek = int(6 * np.random.rand(1))
        self.owoc = False
        self.wonsz = self.nowy_wonsz()

    def on_press(self, key):
        try:
            self.key_char = key.char
        except AttributeError:
            pass

    def biegnij(self):
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()
        clear = lambda: os.system('cls' if os.name == "nt" else "clear")
        while self.game_on:
            self.uaktualnij_plansze()
            sleep(0.4)

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
            elif self.key_char == "r":
                self.reset()

            clear()


if __name__ == "__main__":
    snek = SnekGejm()