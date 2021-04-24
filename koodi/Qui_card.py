from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget
from PyQt5.QtGui import QPixmap
from pelikentta import Pelikentta

#olio luo pelikorteille kuvakkeet

class Qui_card(QtWidgets.QAbstractButton):

    def __init__(self,parent):
        super(Qui_card, self).__init__(parent)
        self.card_back = QPixmap("kuvat/purple_back.jpg")
        self.visible = False

    def paintEvent(self, event):
        if self.visible is False:
            painter = QtGui.QPainter()
            painter.begin(self)
            painter.drawPixmap(0,0,200,100, self.card_back)
            painter.end()




