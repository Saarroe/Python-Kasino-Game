import unittest
from pelikentta import Pelikentta
from korttipakka import Korttipakka
from Pelaaja import Player
from kortti import Kortti
from Qui_card import Qui_card
from Qui import GUI_aloitus
class Test(unittest.TestCase):

    def test_alustus(self):
        uusi=Pelikentta(True)
        self.assertEqual(52, len(uusi.pakka.kortit))

    def test_nosta_kortti(self):
        uusi = Pelikentta(True)

        uusi.lisaa_pelaaja("matti")
        uusi.lisaa_pelaaja("Juho")
        uusi.aloita_peli()
        self.assertEqual(2, len(uusi.return_pelaajat()))
        pelaajat = uusi.return_pelaajat()
        nimi = pelaajat[0].return_name()
        self.assertEqual("matti", nimi)
        self.assertEqual(40, len(uusi.pakka.getkortit()))
        self.assertEqual(4, len(uusi.get_poyta()))
        self.assertEqual(4, len(pelaajat[0].get_kasi()))

    def test_pelaa_kortti_poytaan(self): #aloita_peli funktion testaus
        uusi = Pelikentta(True)
        uusi.lisaa_pelaaja("matti")
        uusi.lisaa_pelaaja("Juho")
        uusi.aloita_peli()
        matti = uusi.get_turn_pelaaja()
        kortit_kasi = matti.get_kasi()
        uusi.pelaa_kortin_poytaan(kortit_kasi[0])
        self.assertEqual(39, len(uusi.pakka.getkortit()))
        self.assertEqual(4, len(matti.get_kasi()))
        self.assertEqual(5, len(uusi.get_poyta()))


    def test_kortti(self):
        kortti = Kortti("Ruutu", 10)
        self.assertEqual("Ruutu", kortti.get_maa())
        self.assertEqual(10, kortti.get_arvo())

    def test_laskeoikein(self):  #testaa pelin laske oikein funktion erikoiskorteilla
        uusi = Pelikentta(True)

        poyta=[]
        poyta.append(Kortti("Pata", 14))
        poyta.append(Kortti("Ruutu", 10))
        poyta.append(Kortti("Ruutu", 4))
        kasi = Kortti("Pata", 2)
        self.assertTrue(uusi.laske_oikein(poyta,kasi))
        poyta.append(Kortti("Pata", 5))
        self.assertFalse(uusi.laske_oikein(poyta,kasi))  #Palauttaa false kun menee väärin

    def test_laskepisteet(self):  #katsotaan meneekö pistelasku oikein
        uusi = Pelikentta(True)
        uusi.lisaa_pelaaja("eka")
        uusi.lisaa_pelaaja("voittaja")
        pelaajat = uusi.return_pelaajat()
        pelaajat[1].lisaakortit(8)
        pelaajat[1].lisaapadat(6)
        pelaajat[1].lisaaassat(4)
        pelaajat[1].lisaamokit(3)
        pelaajat[1].lisaaruutu10()
        pelaajat[1].lisaapata2()
        uusi.laskepisteet()
        self.assertTrue(pelaajat[1].getruutu10())
        self.assertEqual(13, pelaajat[1].getpisteet())
        pelaajat[1].lisaapiste()
        self.assertEqual(14, pelaajat[1].getpisteet())
    def test_pelattu(self):
        uusi = Player("Juho")
        uusi.setpelattufalse()
        self.assertFalse(uusi.getpelattu())

    def test_nollaapelittiedot(self):
        uusi = Pelikentta(True)
        uusi.lisaa_pelaaja("Sanni")
        uusi.lisaa_pelaaja("kanttarelli")
        kortti=uusi.pakka.nosta_kortti()
        uusi.lisaa_kortti_poytaan(kortti)
        self.assertEqual(51, len(uusi.pakka.getkortit()))
        self.assertEqual(1, len(uusi.get_poyta()))
        uusi.nollaapelitiedot()
        self.assertEqual(52, len(uusi.pakka.getkortit()))
        self.assertEqual(0, len(uusi.get_poyta()))

    def test_nollaapelajaatiedot(self):
        uusi = Pelikentta(True)
        uusi.lisaa_pelaaja("Sanni")
        uusi.lisaa_pelaaja("kanttarelli")
        pelaajat = uusi.return_pelaajat()
        pelaajat[1].lisaakortit(8)
        pelaajat[1].lisaapadat(6)
        pelaajat[1].lisaaassat(4)
        pelaajat[1].lisaamokit(3)
        pelaajat[1].lisaaruutu10()
        pelaajat[1].lisaapata2()
        uusi.laskepisteet()
        self.assertEqual(8, pelaajat[1].getkortit())
        pelaajat[1].nollaatiedot()
        self.assertEqual(13, pelaajat[1].getpisteet())
        self.assertEqual(0, pelaajat[1].getkortit())
        self.assertEqual(0, pelaajat[1].getpadat())
        self.assertEqual(0, pelaajat[1].getmokit())
        self.assertFalse(pelaajat[1].getpata2())
        self.assertFalse(pelaajat[1].getruutu10())



    def testaavuoro(self):
        uusi = Pelikentta(True)
        uusi.lisaa_pelaaja("Sanni")
        uusi.lisaa_pelaaja("kanttarelli")
        uusi.asetavuoro(1)
        self.assertEqual(1, uusi.get_vuoro())
        self.assertEqual("kanttarelli", uusi.get_turn_pelaaja().return_name())
        uusi.seuraava_vuoro()
        self.assertEqual(0, uusi.get_vuoro())
        self.assertEqual("Sanni", uusi.get_turn_pelaaja().return_name() )

if __name__ == "__main__":
    unittest.main()