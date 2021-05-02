

class Player():

    def __init__(self,nimi):
        self.vika = False
        self.jakaja = False
        self.nimi = nimi
        self.kasi = []
        self.qkasi = []
        self.pisteet = 0
        self.saadut_kortit = 0
        self.mokit = 0
        self.padat = 0
        self.assat =0
        self.pata2 = False
        self.ruutu10 = False
        self.pelattu = False #false jos ei ole vielä pelannut vuoroa

    def getjakaja(self):
        return self.jakaja

    def setjakajatrue(self):
        self.jakaja = True

    def setjakajafalse(self):
        self.jakaja = False

    def setvikatrue(self):
        self.vika = True
    def setvikafalse(self):
        self.vika = False

    def getvika(self):
        return self.vika

    def lisaapiste(self):
        self.pisteet+=1

    def lisaapisteet(self,x):
        self.pisteet=x

    def getpisteet(self):
        return self.pisteet

    def nollaatiedot(self):
        self.mokit = 0
        self.kasi = []
        self.qkasi = []
        self.saadut_kortit = 0
        self.mokit = 0
        self.padat = 0
        self.assat = 0
        self.pata2 = False
        self.ruutu10 = False
        self.pelattu = False

    def nollaaqkasi(self):
        self.qkasi = []
        self.kasi = []

    def lisaaqkortti(self,kortti):
        self.qkasi.append(kortti)

    def poistaqkortti(self,kortti):
        if kortti in self.qkasi:
            self.qkasi.remove(kortti)
        else:
            print("debuggaus poista qkortti kasi")

    def getqkortit_kasi(self):
        return self.qkasi

    def lisaaassa(self):
        self.assat+=1

    def lisaapata(self):
        self.padat+=1

    def getassat(self):
        return self.assat

    def getpadat(self):
        return self.padat

    def lisaapata2(self):
        self.pata2 = True

    def getpata2(self):
        return self.pata2

    def getruutu10(self):
        return self.ruutu10

    def lisaaruutu10(self):
        self.ruutu10 = True

    def getpelattu(self):
        return self.pelattu

    def setpelattutrue(self):
        self.pelattu=True

    def setpelattufalse(self):
        self.pelattu = False

    def lisaa_kortti_kateen(self, kortti):
        self.kasi.append(kortti)

    def lisaa_kortti(self):
        self.saadut_kortit+=1

    def getkortit(self):
        return self.saadut_kortit

    def lisaakortit(self, x):
        self.saadut_kortit = x
    def lisaaassat(self, x):
        self.assat = x
    def lisaapadat(self,x):
        self.padat = x
    def lisaamokit(self, x):
        self.mokit = x

    def lisaa_mokki(self):
        self.mokit+=1

    def getmokit(self):
        return self.mokit

    def get_kasi(self):
        return self.kasi

    def pelaa_kortti(self,kortti):

        self.kasi.remove(kortti)

    def return_name(self):
        return self.nimi