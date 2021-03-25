from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QInputDialog, QListWidgetItem, QListWidget
from pelikentta import Pelikentta
from Pelaaja import Player
from Qui_card import Qui_card

class Qui_board(QListWidget):

    def __init__(self):
        super(Qui_board, self).__init__()
        self.list = QListWidget()
        self.setStyleSheet("background-image: url(board.jpg);")
