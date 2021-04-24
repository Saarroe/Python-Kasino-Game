from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QInputDialog, QListWidgetItem, QListWidget
from pelikentta import Pelikentta
from Pelaaja import Player
from kortti import Kortti
from Qui_card import Qui_card
from Qui_korttiabstract import Qui_kortti
class Qui_board(QWidget):

    def __init__(self):
        super(Qui_board,self).__init__()
        self.setFixedHeight(200)
        self.setFixedWidth(600)
        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)
        self.next_turn = QPushButton("Start new game")
        #self.initboard()
        self.setStyleSheet("background-image: url(kuvat/board.jpg)")
    def initboard(self):
        card = Qui_card()
        for i in range(3): #alustaa gridin koon
            for j in range(4):

                self.grid.addWidget(card, i, j)
