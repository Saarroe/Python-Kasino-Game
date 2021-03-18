import unittest
from pelikentta import Pelikentta
from korttipakka import Korttipakka
from Pelaaja import Player
class Test(unittest.TestCase):

    def test_alustus(self):
        uusi=Pelikentta()
        self.assertEqual(52, len(uusi.pakka.kortit))

    def test_nosta_kortti(self):
        uusi = Pelikentta()
        uusi.lisaa_pelaaja("matti")
        uusi.aloita_peli()
        matti = uusi.get_turn_pelaaja()
        self.assertEqual(1, len(uusi.return_pelaajat()))
        nimi = uusi.pelaajaa_lista[0].nimi
        self.assertEqual("matti", nimi)
        self.assertEqual(44, len(uusi.pakka.kortit))
        self.assertEqual(4, len(uusi.poyta))
        self.assertEqual(4, len(matti.kasi))
    def test_pelaa_kortti_poytaan(self):
        uusi = Pelikentta()
        uusi.lisaa_pelaaja("matti")
        uusi.aloita_peli()
        matti = uusi.get_turn_pelaaja()
        uusi.pelaa_kortin_poytaan()
        self.assertEqual(4,len(matti.kasi))
        self.assertEqual(5, len(uusi.poyta))
        self.assertEqual(43, len(uusi.pakka.kortit))

if __name__ == "__main__":
    unittest.main()