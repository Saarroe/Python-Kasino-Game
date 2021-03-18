from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from pelikentta import Pelikentta


class Qui_card():

    def __init__(self, card):
        super(Qui_card, self).__init__()
        self.card = card
        self.auki = True
        self.init_card()


    def init_card(self):
        teksti=""
        sanakirja = {"Ruutu": 'D', "Hertta": 'H', "Risti": 'C', "Pata": 'S'}
        self.qp= QtGui.QPainter
        if self.auki == True:
            teksti = str(self.card.get_arvo()) + sanakirja[self.card.get_maa()]

            self.pixmap = QtGui.QPixmap("teksti.jpg")
            self.qp.drawPixmap(self.pixmap)





    def set_visibility(self,boolean):
        self.auki = boolean

    def get_visibility(self):
        return self.auki



