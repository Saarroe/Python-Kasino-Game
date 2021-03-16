from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from pelikentta import Pelikentta
class Qui_card():
    def __init__(self, card):
        super(Qui_card, self).__init__()
        self.card = card