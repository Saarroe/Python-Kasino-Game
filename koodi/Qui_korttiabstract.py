
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QInputDialog, QListWidgetItem, QListWidget
from pelikentta import Pelikentta
from Pelaaja import Player
from kortti import Kortti
from Qui_card import Qui_card

class pixmapvarasto:

    def __init__(self):
        super(Qui_kortti,self).__init__()

        class Qui_card(QWidget):

            def __init__(self):
                super(Qui_card, self).__init__()
                self.card_back = QPixmap("kuvat/purple_back.jpg")
                self.shape = QtCore.QRectF()
                self.init_cards()  # luo kuvat ja kortit
                self.lista = []

            def init_cards(self):
                maat = ['D', 'H', 'C', 'S']
                lista = []
                for maa in maat:  # luodaan korttikuvat kaikille korteille
                    for arvo in range(2, 15):
                        teksti = ""
                        teksti = "{}{}".format(arvo, maa)
                        self.teksti = QPixmap("{}.jpg".format(teksti))
                        self.lista.append(self.teksti)


            def get_auki(self, kortti):
                maat = {"Ruutu": 'D', "Hertta": 'H', "Risti": 'C', "Pata": 'S'}
                teksti = ""
                teksti = "{}{}".format(kortti.get_arvo(), maat[kortti.get_maa()])
                return self.teksti
