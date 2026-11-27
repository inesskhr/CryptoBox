"""Tests de CryptoBox, avec les exemples donnés dans le sujet."""
import unittest
from cryptobox import (cesar_chiffrer, cesar_dechiffrer, cesar_force_brute,
                       substitution_chiffrer, substitution_dechiffrer,
                       transposition_chiffrer, transposition_dechiffrer)


class TestCryptoBox(unittest.TestCase):
    def test_cesar(self):
        self.assertEqual(cesar_chiffrer("BONJOUR", 3), "ERQMRXU")
        self.assertEqual(cesar_dechiffrer("ERQMRXU", 3), "BONJOUR")
        self.assertEqual(cesar_chiffrer("XYZ", 3), "ABC")
        self.assertEqual(cesar_chiffrer("ABC", 26), "ABC")

    def test_force_brute(self):
        essais = cesar_force_brute("ERQMRXU")
        self.assertEqual(len(essais), 25)
        self.assertEqual([k for k, _ in essais], list(range(1, 26)))
        self.assertIn((3, "BONJOUR"), essais)

    def test_substitution(self):
        cle = "QWERTYUIOPASDFGHJKLZXCVBNM"
        self.assertEqual(substitution_chiffrer("ATTAQUE", cle), "QZZQJXT")
        self.assertEqual(substitution_dechiffrer("QZZQJXT", cle), "ATTAQUE")

    def test_transposition(self):
        self.assertEqual(transposition_chiffrer("RENDEZVOUSAMIDI", "PORTE"),
                         "ESIEVMRZANOIDUD")
        self.assertEqual(transposition_dechiffrer("ESIEVMRZANOIDUD", "PORTE"),
                         "RENDEZVOUSAMIDI")

    def test_remplissage(self):
        chiffre = transposition_chiffrer("BONJOUR", "MANCHE")
        self.assertEqual(len(chiffre), 12)
        self.assertEqual(transposition_dechiffrer(chiffre, "MANCHE"),
                         "BONJOURXXXXX")

    def test_mot_cle_repetitions(self):
        chiffre = transposition_chiffrer("ABCDEFGH", "MAMAN")
        self.assertEqual(chiffre, "BGDXAFCHEX")
        self.assertEqual(transposition_dechiffrer(chiffre, "MAMAN"), "ABCDEFGHXX")

    def test_cas_limites(self):
        self.assertEqual(transposition_chiffrer("", "ABC"), "")
        self.assertEqual(transposition_dechiffrer("", "ABC"), "")
        self.assertEqual(transposition_chiffrer("ABCX", "A"), "ABCX")
        self.assertEqual(transposition_dechiffrer("ABCX", "A"), "ABCX")

    def test_entrees_invalides(self):
        with self.assertRaises(ValueError):
            cesar_chiffrer("A B", 3)
        with self.assertRaises(ValueError):
            substitution_chiffrer("ABC", "A" * 26)
        with self.assertRaises(ValueError):
            transposition_chiffrer("ABC", "")
        with self.assertRaises(ValueError):
            transposition_dechiffrer("ABCD", "ABC")

    def test_challenge(self):
        cle = "FNGIWDCLJBRYSMVOTHAZPXEQKU"
        chiffre = "MDDRHRCRPWUR"
        apres_substitution = substitution_dechiffrer(chiffre, cle)
        self.assertEqual(apres_substitution, "NFFKRKGKUEZK")
        candidats = [(k, transposition_dechiffrer(t, "MANCHE"))
                     for k, t in cesar_force_brute(apres_substitution)]
        self.assertIn((13, "HAMSTERSXXXX"), candidats)
        rechiffre = substitution_chiffrer(
            cesar_chiffrer(transposition_chiffrer("HAMSTERS", "MANCHE"), 13), cle)
        self.assertEqual(rechiffre, chiffre)


if __name__ == "__main__":
    unittest.main()
