from kortti import Kortti
import random
class Korttipakka():


    def __init__(self):
        self.kortit=[]
        self.set_kortit()

    def sekoita(self):
        random.shuffle(self.kortit)


    def set_kortit(self):
        maat = { "Hertta": Kortti.Hertta,"Ruutu": Kortti.Ruutu, "Pata": Kortti.Pata, "Risti": Kortti.Risti}
        for maa in maat:
            for arvo in range(2, 15):
                kortti = Kortti(maat[maa], arvo)
                self.kortit.append(kortti)
        #sekoita
        self.sekoita()

    def nosta_kortti(self):
       return self.kortit.pop()
