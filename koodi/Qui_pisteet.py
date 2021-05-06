
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QTableView, QTableWidget, QTableWidgetItem, QApplication
from PyQt5.QtGui import QPixmap
from pelikentta import Pelikentta
from Pelaaja import Player

class Qui_pisteet(QWidget):

    def __init__(self, peli, x):
        super(Qui_pisteet, self).__init__()

        self.setStyleSheet("background-image: url(kuvat/testi.jpg)")
        self.loppu = x
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

        self.taulukko.addWidget(QLabel("  Nimi"),0,0)
        self.taulukko.addWidget(QLabel("  Kortit"),0, 1)
        self.taulukko.addWidget(QLabel("  Padat"),0, 2)
        self.taulukko.addWidget(QLabel("  Ässät"), 0, 3)
        self.taulukko.addWidget(QLabel("  Mökit"), 0, 4)
        self.taulukko.addWidget(QLabel("  Pata2"),0,5)
        self.taulukko.addWidget(QLabel("  Ruutu10"), 0, 6)
        piste=QLabel("Pisteet")
        piste.setAlignment(QtCore.Qt.AlignCenter)
        piste.setFont(QtGui.QFont("Arial", 10))

        self.taulukko.addWidget(piste, 0, 7)  #Edellisiltä kierroksilta
        x=1

        for pelaaja in pelaajat:
            teksti="{}:".format(pelaaja.return_name())
            piste = QLabel(teksti)
            piste.setAlignment(QtCore.Qt.AlignCenter)
            self.taulukko.addWidget(piste, x, 0)

            piste = QLabel(str(pelaaja.getkortit()))
            piste.setAlignment(QtCore.Qt.AlignCenter)
            self.taulukko.addWidget(piste, x, 1)

            piste = QLabel(str(pelaaja.getpadat()))
            piste.setAlignment(QtCore.Qt.AlignCenter)
            self.taulukko.addWidget(piste, x, 2)

            piste = QLabel(str(pelaaja.getassat()))
            piste.setAlignment(QtCore.Qt.AlignCenter)
            self.taulukko.addWidget(piste, x, 3)

            piste = QLabel(str(pelaaja.getmokit()))
            piste.setAlignment(QtCore.Qt.AlignCenter)
            self.taulukko.addWidget(piste, x, 4)

            if pelaaja.getpata2() == False:
                piste = QLabel("0")
            else:
                piste = QLabel("1")
            piste.setAlignment(QtCore.Qt.AlignCenter)
            self.taulukko.addWidget(piste, x, 5)

            if pelaaja.getruutu10() == False:
                piste = QLabel("0")
            else:
                piste = QLabel("1")
            piste.setAlignment(QtCore.Qt.AlignCenter)
            self.taulukko.addWidget(piste, x, 6)

            piste = QLabel(str(pelaaja.getpisteet()))
            piste.setAlignment(QtCore.Qt.AlignCenter)
            piste.setFont(QtGui.QFont("Arial", 15))
            self.taulukko.addWidget(piste, x, 7)
            x+=1

        if self.loppu is True:
            teksti = QLabel("Kierros loppui, pistetilanne kierroksen jälkeen:")
            suurin =0
            lista = []
            for pelaaja in pelaajat:
                if pelaaja.getpisteet()>suurin:
                    lista = []
                    lista.append(pelaaja)
                    suurin=pelaaja.getpisteet()
                    johtaja = pelaaja
                elif pelaaja.getpisteet() == suurin:
                    lista.append(pelaaja)
            if suurin > 15 and len(lista) ==1:  #onko voittajaa vai ei
                teksti2 = "Pelaaja {} voitti, pisteitä on {}".format(johtaja.return_name(), suurin)
                voittaja = QLabel(teksti2)

                #self.setStyleSheet("background: green")
            elif len(lista) ==1:
                teksti2 ="Pelaaja {} johtaa, pisteitä on {}".format(johtaja.return_name(), suurin)
                voittaja = QLabel(teksti2)
            else:
                teksti2 =""
                for i in lista:
                    teksti2+=i.return_name()+" "
                teksti2+= "Pisteet: "+str(suurin) + " "
                if suurin > 15:
                    teksti2 += "Peli päättyi tasapeliin"
                else:
                    teksti2 += "Tilanne tasan tällä hetkellä"
            voittaja = QLabel(teksti2)
        else:
            teksti = QLabel("Pistetilanne tällä hetkellä:")
            voittaja = QLabel("Kierros vielä kesken!!")
        voittaja.setAlignment(QtCore.Qt.AlignCenter)
        teksti.setAlignment(QtCore.Qt.AlignCenter)
        self.vbox.addWidget(teksti)
        teksti.setFixedHeight(50)
        self.vbox.addLayout(self.taulukko)
        self.vbox.addWidget(voittaja)
        voittaja.setFixedHeight(100)


