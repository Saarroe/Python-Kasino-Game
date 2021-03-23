from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtGui import QPixmap
from pelikentta import Pelikentta


class Qui_card():

    def __init__(self):
        super(Qui_card, self).__init__()
        self.card_back = QPixmap("kuvat/purple_back.jpg")
        self.init_cards()


    def init_cards(self):
        maat = ['D','H','C','S']
        for maa in maat: #luodaan korttikuvat kaikille korteille
            for arvo in range(2,15):
                teksti=""
                teksti="{}{}".format(arvo,maa)
                self.teksti = QPixmap("{}.jpg".format(teksti))


    def get_kiinni(self):
        return self.card_back

    def get_auki(self,kortti):
        maat={"Ruutu":'D',"Hertta":'H',"Risti":'C',"Pata":'S'}
        teksti=""
        teksti="{}{}".format(kortti.get_arvo(), maat[kortti.get_maa()])
        return self.teksti



