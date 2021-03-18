from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from pelikentta import Pelikentta

class Qui_card():

    def __init__(self, card):
        super(Qui_card, self).__init__()
        self.card = card
        self.init_card()
        self.auki = True

    def init_cards(self):
        teksti=""
        sanakirja = {"Ruutu": 'D', "Hertta": 'H', "Risti": 'C', "Pata": 'S'}
        if self.auki == True:
            teksti = ""
            sanakirja = {"Ruutu": 'D', "Hertta": 'H', "Risti": 'C', "Pata": 'S'}
            teksti = str(self.card.get_arvo()) + sanakirja[self.card.get_maa()]
            self.pixmap = Gpixmap("teksti.jpg")





    def set_visibility(self,boolean):
        self.auki = boolean

    def get_visibility(self):
        return self.auki



