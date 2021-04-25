

class Player():

    def __init__(self,nimi):
        self.nimi = nimi
        self.kasi = []
        self.pisteet = 0
        self.saadut_kortit = 0
        self.mokit = 0
        self.padat = 0
        self.assat =0
        self.erikoiskortit = 0
        self.pelattu = False #false jos ei ole vielä pelannut vuoroa

    def lisaaassa(self):
        self.assat+=1

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

    def lisaa_mokki(self):
        self.mokit+=1

    def nollaa_mokit(self):
        self.mokit=0

    def get_kasi(self):
        return self.kasi

    def pelaa_kortti(self,kortti):

        self.kasi.remove(kortti)

    def return_name(self):
        return self.nimi