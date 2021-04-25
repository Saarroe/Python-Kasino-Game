from korttipakka import Korttipakka
from Pelaaja import Player

class Pelikentta():

    def __init__(self):
        self.pakka = Korttipakka()  #sekoitetun korttipakka pituus 52
        self.pelaajaa_lista = []
        self.turn = 0 #kenen vuoro
        self.poyta = []
        self.x=0 #on nolla jos pakassa on vielä kortteja
        self.qkortit_kasi = []
        self.qkortit_poyta = []


    def lisaaqkorttipoyta(self,kortti):
        self.qkortit_poyta.append(kortti)

    def poistaqkorttipoyta(self,kortti):
        if kortti in self.qkortit_poyta:
            self.qkortit_poyta.remove(kortti)
        else:
            print("debuggaus poista qkortti kasi")

    def getqkortit_poyta(self):
        return self.qkortit_poyta


    def lisaaqkortti(self,kortti):
        self.qkortit_kasi.append(kortti)

    def poistaqkortti(self,kortti):
        if kortti in self.qkortit_kasi:
            self.qkortit_kasi.remove(kortti)
        else:
            print("debuggaus poista qkortti kasi")

    def getqkortit_kasi(self):
        return self.qkortit_kasi

    def get_poyta(self):
        return self.poyta

    def get_vuoro(self):
        return self.turn

    def lisaa_pelaaja(self, nimi):
        self.pelaajaa_lista.append(Player(nimi))

    def lisaa_kortti_poytaan(self,kortti):
        self.poyta.append(kortti)

    def return_pelaajat(self):
        return self.pelaajaa_lista

    def get_turn_pelaaja(self):
        return self.pelaajaa_lista[self.turn]

    def otakortti_poydasta(self,kortti):
        self.poyta.remove(kortti)


    def get_pakka(self):
        return self.pakka

    def aloita_peli(self):
        for x in range(0,4):
            for pelaaja in self.return_pelaajat():
                kortti = self.pakka.nosta_kortti()
                pelaaja.lisaa_kortti_kateen(kortti)
                pelaaja.nollaa_mokit()
        #for i in range(0,4):
            kortti = self.pakka.nosta_kortti()
            self.lisaa_kortti_poytaan(kortti)

    def lisaakorttipelaajalle(self):
        pelaaja = self.pelaajaa_lista[self.turn]
        kortti = self.pakka.nosta_kortti()
        pelaaja.lisaa_kortti_kateen(kortti)

    def laske_oikein(self, poyta, kasi):
        #False jos määrä ei täsmää muuten True jos siirto ok
        summa1=0
        arvo2=kasi[0].get_arvo()

        if kasi[0].get_maa() == "Ruutu" and arvo2 == 10:
            arvo2 = 16
        elif kasi[0].get_maa()== "Pata" and arvo2 == 2:
            arvo2 = 15

        for kortti in poyta:
            arvo=kortti.get_arvo()
            if arvo == 14:
                arvo = 1
            if arvo != arvo2:
                summa1 += arvo
        print(summa1)
        print(arvo2)
        if summa1 != arvo2:
            return False
        else:
            return True



    def seuraava_vuoro(self):
        if self.turn > len(self.pelaajaa_lista):
            self.turn = 0
        else:
            self.turn += 1


    def pelaa_kortin_poytaan(self, kortti):

        pelaaja = self.pelaajaa_lista[self.turn]
        pelaaja.pelaa_kortti(kortti)
        self.poyta.append(kortti)

        if len(self.pakka.kortit) == 0:
            print("pakka loppui")
            pass
        else:
            kortti = self.pakka.nosta_kortti()
            pelaaja.lisaa_kortti_kateen(kortti)


    def klikkaus(self,qkortti):
        if qkortti.getvisibility() is True:
            if qkortti.returnpaikka() == True:  #True jos kortti pöydässä, kädessä False
                if qkortti.getklikattu() == 1:
                    qkortti.setklikattu0()
                else:
                    qkortti.setklikattu1()

            else:
                if qkortti.getklikattu() == 1:
                    for kortti in self.qkortit_kasi:
                        kortti.setklikattu0()
                else:
                    for kortti in self.qkortit_kasi:
                        kortti.setklikattu0()
                    qkortti.setklikattu1()
        else:
            print("ei näin")