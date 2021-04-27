
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QTableView, QTableWidget, QTableWidgetItem, QApplication
from PyQt5.QtGui import QPixmap
from pelikentta import Pelikentta
from Pelaaja import Player

class Qui_pisteet(QWidget):

    def __init__(self, peli):
        super(Qui_pisteet, self).__init__()

        self.peli = peli
        self.setWindowTitle("Pistetaulukko")
        self.vbox = QtWidgets.QVBoxLayout()
        self.setGeometry(400,200,800,700)

        self.setLayout(self.vbox)
        self.tulosta_tilanne()
        self.show()

    def tulosta_tilanne(self):
        pelaajat = self.peli.return_pelaajat()
        self.taulukko = QGridLayout()
        self.taulukko.addWidget(QLabel(),0,0)
        pituus = len(pelaajat)

        self.taulukko.addWidget(QLabel("Kortit"),1,1)
        self.taulukko.addWidget(QLabel("Padat"),1,2)
        self.taulukko.addWidget(QLabel("Ässät"), 1, 2)
        self.taulukko.addWidget(QLabel("Mökit"), 1, 3)

        for j in range(pituus):
            self.taulukko.addWidget(QLabel(pelaajat[j].return_name()),j+1,0)


        self.vbox.addLayout(self.taulukko)


