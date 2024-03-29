from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLabel
from PyQt5.QtGui import QPixmap
from pelikentta import Pelikentta

#olio luo pelikorteille qlabelin ja asettaa sille pixmapin, joko kiinni tai auki

class Qui_card(QLabel):

    def __init__(self, kortti, peli):
        super(Qui_card, self).__init__()
        self.klikattu = 0 # jos klikattu arvo on 1
        self.card_back = QPixmap("kuvat/purple_back.jpg")
        self.kortti = kortti
        self.visible = False  #false kiinni, true oikein
        self.pixmap2 = QPixmap(self.teksti())
        self.kuva()
        self.paikka = None# True jos pöytä, false niin kädessä
        self.peli = peli

    def setpixmapnone(self):
        self.setStyleSheet("background:transparent")

    def getkortti(self):
        return self.kortti

    def setklikattu1(self):
        self.klikattu = 1

    def setklikattu0(self):
        self.klikattu = 0

    def getklikattu(self):
        return self.klikattu

    def kuva(self):
        if self.visible is False:
            self.setPixmap(self.card_back.scaled(100,150))

    def getvisibility(self):
        return self.visible

    def suljekortti(self):
        self.visible = False
        self.setPixmap(self.card_back.scaled(100,150))

    def avaakortti(self):
        self.visible = True
        self.setPixmap(self.pixmap2.scaled(100,150))

    def teksti(self):
        maat = {"Ruutu": 'D', "Hertta": 'H', "Risti": 'C', "Pata": 'S'}
        arvot ={"11": 'J', "12": "Q", "13": 'K', "14":'A'}
        arvo=str(self.kortti.get_arvo())
        if arvo in arvot:
            arvo = arvot[arvo]
        teksti = "kuvat/{}{}.jpg".format(arvo, maat[self.kortti.get_maa()])
        return teksti

    def mousePressEvent(self,*args, **kwargs):
        self.peli.klikkaus(self)

