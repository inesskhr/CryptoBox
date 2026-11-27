"""Tests TP2 : exemples du sujet, conventions et casseur générique."""
import unittest
from vigenere import (normaliser, vigenere_chiffrer, vigenere_dechiffrer,
                      casser_vigenere, casser_longueur_inconnue, colonnes)


class TestVigenere(unittest.TestCase):
    def test_exemple_1(self):
        self.assertEqual(vigenere_chiffrer('ATTAQUE A L’AUBE', 'CLE'), 'CEXCBYG L P’CFFG')
        self.assertEqual(vigenere_dechiffrer('CEXCBYG L P’CFFG', 'CLE'), 'ATTAQUE A L’AUBE')

    def test_exemple_2(self):
        self.assertEqual(vigenere_chiffrer('LA CLE, 14H', 'TP'), 'EP VAX, 14W')
        self.assertEqual(vigenere_dechiffrer('EP VAX, 14W', 'TP'), 'LA CLE, 14H')

    def test_accents(self):
        self.assertEqual(normaliser('Clé à l’école'), 'CLE A L’ECOLE')
        self.assertEqual(vigenere_chiffrer('é, à 3!', 'BC'), 'F, C 3!')

    def test_ponctuation(self):
        self.assertEqual(vigenere_chiffrer('A 1, A\nA!', 'BC'), 'B 1, C\nB!')
        self.assertEqual(vigenere_chiffrer('  A  ', 'B'), '  B  ')

    def test_aller_retour(self):
        for message in ('', 'Été à Paris, 14h.', 'BONJOUR\nMONDE', 'XYZ'):
            for cle in ('A', 'Z', 'CLE', 'MAMAN'):
                chiffre = vigenere_chiffrer(message, cle)
                self.assertEqual(vigenere_dechiffrer(chiffre, cle), normaliser(message))

    def test_colonnes(self):
        self.assertEqual(colonnes('AB, CD 12 EF', 2), ['ACE', 'BDF'])

    def test_casseur(self):
        # Chaque colonne du texte artificiel a E comme lettre dominante.
        message = ('EEEEEEEEEEEE ABCDEFGHIJK ' * 100)
        for cle in ('LUNE', 'SOLEIL', 'Z'):
            chiffre = vigenere_chiffrer(message, cle)
            self.assertEqual(casser_vigenere(chiffre, len(cle)), cle)

    def test_bonus(self):
        message = 'EEEEEEEEEE ABCDEFGHIJKLM ' * 100
        chiffre = vigenere_chiffrer(message, 'CLE')
        candidats = casser_longueur_inconnue(chiffre)
        self.assertEqual([c[0] for c in candidats], list(range(2, 11)))
        self.assertEqual(candidats[1], (3, 'CLE', message))

    def test_entrees_invalides(self):
        for cle in ('', 'A2', 'A B'):
            with self.assertRaises(ValueError):
                vigenere_chiffrer('ABC', cle)
        for longueur in (0, -1, 10):
            with self.assertRaises(ValueError):
                casser_vigenere('ABC', longueur)
        with self.assertRaises(ValueError):
            casser_longueur_inconnue('!')


if __name__ == '__main__':
    unittest.main()
