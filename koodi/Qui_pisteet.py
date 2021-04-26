
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QTableView, QTableWidget, QTableWidgetItem, QApplication
from PyQt5.QtGui import QPixmap
from pelikentta import Pelikentta
from Pelaaja import Player

class Qui_pisteet(QWidget):

    def __init__(self, peli):
        super(Qui_pisteet, self).__init__()
        self.kesken = x #False jos kierros kesken, muuten True
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
        for j in range(pituus):
            self.taulukko.addWidget(QLabel(pelaajat[j].return_name()),0,j+1)
        self.taulukko.addWidget(QLabel("Kortit"),1,0)
        for j in range(pituus):
            pelaaja = pelaajat[j]
            self.taulukko.addWidget(QLabel(str(pelaaja.getkortit())),1,j+1)
        self.taulukko.addWidget(QLabel("Padat"),2,0)
        for j in range(pituus):
            pelaaja = pelaajat[j]
            self.taulukko.addWidget(QLabel(str(pelaaja.getpadat())),2,j+1)
        self.taulukko.addWidget(QLabel("Ässät"), 3, 0)
        for j in range(pituus):
            pelaaja = pelaajat[j]
            self.taulukko.addWidget(QLabel(str(pelaaja.getassat())),3,j+1)

        self.vbox.addLayout(self.taulukko)


