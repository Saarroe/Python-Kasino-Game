from korttipakka import Korttipakka
from Pelaaja import Player

class Pelikentta():

    def __init__(self,x):
        self.pakka = Korttipakka(x)  #sekoitetun korttipakka pituus 52, true kun eka init
        self.pelaajaa_lista = []
        self.turn = 0 #kenen vuoro
        self.poyta = []

        self.qkortit_poyta = []



    def asetavuoro(self, x):
        self.turn = x
    def lisaaqkorttipoyta(self,kortti):
        self.qkortit_poyta.append(kortti)

    def poistaqkorttipoyta(self,kortti):

        if kortti in self.qkortit_poyta:

            self.qkortit_poyta.remove(kortti)
        else:

            print("debuggaus poista qkortti pöytä")

    def getqkortit_poyta(self):
        return self.qkortit_poyta

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
        #for i in range(0,4):
            kortti = self.pakka.nosta_kortti()
            self.lisaa_kortti_poytaan(kortti)

    def lisaakorttipelaajalle(self):
        pelaaja = self.pelaajaa_lista[self.turn]
        if len(self.pakka.getkortit())>0:
            kortti = self.pakka.nosta_kortti()
            pelaaja.lisaa_kortti_kateen(kortti)
        else:
            pass

    def laske_oikein(self, poyta, kasi):
        #False jos määrä ei täsmää muuten True jos siirto ok
        summa1=0
        arvo2=kasi.get_arvo()

        if kasi.get_maa() == "Ruutu" and arvo2 == 10:
            arvo2 = 16
        elif kasi.get_maa()== "Pata" and arvo2 == 2:
            arvo2 = 15

        for kortti in poyta:
            arvo=kortti.get_arvo()
            if arvo == 14:
                arvo = 1

            summa1 += arvo

        if summa1%arvo2 == 0:  #kun jakojäännös 0 niin menee oikein
            return True
        else:
            return False



    def seuraava_vuoro(self):
        if self.turn == len(self.pelaajaa_lista)-1:
            self.turn = 0
        else:
            self.turn += 1


    def pelaa_kortin_poytaan(self, kortti):

        pelaaja = self.pelaajaa_lista[self.turn]
        pelaaja.pelaa_kortti(kortti)
        self.poyta.append(kortti)

        if len(self.pakka.getkortit()) == 0:
            pass

        else:
            kortti = self.pakka.nosta_kortti()
            pelaaja.lisaa_kortti_kateen(kortti)


    def klikkaus(self,qkortti):
        pelaaja = self.get_turn_pelaaja()
        qkorttikasi = pelaaja.getqkortit_kasi()


        if qkortti.getvisibility() is True and pelaaja.getpelattu() == False:
            if qkortti in self.qkortit_poyta:  #True jos kortti pöydässä, kädessä False

                if qkortti.getklikattu() == 1:

                    qkortti.setklikattu0()
                else:
                    qkortti.setklikattu1()

            else:
                if qkortti.getklikattu() == 1:

                    for kortti in pelaaja.getqkortit_kasi():
                        kortti.setklikattu0()

                else:

                    for kortti in pelaaja.getqkortit_kasi():
                        kortti.setklikattu0()
                    qkortti.setklikattu1()
        else:
            print("klikkaa avointa korttia")

    def enitenkortteja(self):  #Piste kellä eniten kortteja
        suurin = 0
        haluttu = None
        for pelaaja in self.pelaajaa_lista:
            korttimaara = pelaaja.getkortit()

            if korttimaara > suurin:
                suurin= korttimaara
                haluttu = pelaaja
            elif korttimaara == suurin:
                haluttu = None

        if haluttu != None:
            haluttu.lisaapiste()

    def enitenpatoja(self):  #kaksi pistettä kellä eniten patoja
        suurin = 0
        haluttu = None
        for pelaaja in self.pelaajaa_lista:
            padat = pelaaja.getpadat()
            if padat > suurin:
                suurin = padat
                haluttu = pelaaja

        if haluttu != None:
            haluttu.lisaapiste()
            haluttu.lisaapiste()

    def muutpisteet(self):

        for pelaaja in self.pelaajaa_lista:

            for piste in range(pelaaja.getassat()):  # pisteet ässistä

                pelaaja.lisaapiste()
            for piste in range(pelaaja.getmokit()):  # Pisteet mökeistä

                pelaaja.lisaapiste()

            if pelaaja.getpata2() is True:  # Piste pata2
                pelaaja.lisaapiste()
            if pelaaja.getruutu10() is True: # 2 pistettä ruutu10
                pelaaja.lisaapiste()
                pelaaja.lisaapiste()
            else:
                pass



    def laskepisteet(self):

        self.enitenkortteja()
        self.enitenpatoja()
        self.muutpisteet()

    def nollaapelitiedot(self):
        self.pakka = Korttipakka(True)

        self.turn = 0  # kenen vuoro

        self.poyta = []

        self.qkortit_poyta = []


    def nollaakorttiqui(self):
        for kortti in self.pakka.getkortit():
            kortti.set_guifalse()
