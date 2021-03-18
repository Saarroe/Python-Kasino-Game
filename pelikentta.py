from korttipakka import Korttipakka
from Pelaaja import Player
class Pelikentta():

    def __init__(self):
        self.pakka = Korttipakka()  #sekoitettu korttipakka pituus 52
        self.pelaajaa_lista = []
        self.turn = 0 #kenen vuoro
        self.poyta = []
        self.x=0 #on nolla jos pakassa on vielä kortteja

    def lisaa_pelaaja(self, nimi):
        self.pelaajaa_lista.append(Player(nimi))

    def lisaa_kortti_poytaan(self,kortti):
        self.poyta.append(kortti)

    def return_pelaajat(self):
        return self.pelaajaa_lista

    def get_turn_pelaaja(self):
        return self.pelaajaa_lista[self.turn]
    def otakortti_poydasta(self,i):
        if i < len(self.poyta):
            kortti = self.poyta[i]
            self.poyta.remove(kortti)
            return kortti
    def get_pakka(self):
        return self.pakka

    def aloita_peli(self):
        for x in range(0,4):
            for pelaaja in self.return_pelaajat():
                kortti = self.pakka.nosta_kortti()
                pelaaja.lisaa_kortti_kateen(kortti)
                pelaaja.nollaa_mokit()
        for i in range(0,4):
            kortti = self.pakka.nosta_kortti()
            self.lisaa_kortti_poytaan(kortti)


    def laske_oikein(self, plr_kortti, pöyt_kortit):
        if plr_kortti.get_maa()=="Ruutu" and plr_kortti_arvo == 10:
            arvo = 16
        elif plr_kortti_get_maa()== "Pata" and plr_kortti_arvo == 14:
            arvo = 15
        else:
            arvo = kortti.arvo


    def seuraava_vuoro(self):
        if self.turn > len(self.pelaajaa_lista):
            self.turn = 0
        else:
            self.turn += 1


    def pelaa_kortin_poytaan(self):
        pelaaja = self.pelaajaa_lista[self.turn]
        kortti = pelaaja.pelaa_kortti(1)
        self.poyta.append(kortti)
        if len(self.pakka.kortit) == 0:
            print("pakka loppui")
        else:
            kortti = self.pakka.nosta_kortti()
            pelaaja.lisaa_kortti_kateen(kortti)
            self.seuraava_vuoro()

    def saa_kortin_pöydästä(self):
        halutut = []
        pelaaja = self.pelaajaa_lista[self.turn]
        halutut.append(self.poyta[1])
        kortti = pelaaja.pelaa_kortti(1)
