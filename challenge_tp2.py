"""Résolution des trois challenges du binôme 46 avec CryptoBox."""
from pathlib import Path
from vigenere import (vigenere_chiffrer, vigenere_dechiffrer,
                      casser_vigenere, casser_longueur_inconnue)

DOSSIER = Path(__file__).resolve().parent


def challenge1():
    chiffre = 'FMLGYQXC'
    cle = 'JLLJWMBO'
    clair = vigenere_dechiffrer(chiffre, cle)
    assert vigenere_chiffrer(clair, cle) == chiffre
    return clair


def challenge2():
    chiffre = (DOSSIER / 'challenge2.txt').read_text(encoding='utf-8')
    cle = casser_vigenere(chiffre, 9)
    clair = vigenere_dechiffrer(chiffre, cle)
    assert vigenere_chiffrer(clair, cle) == chiffre
    return cle, clair


def bonus():
    chiffre = (DOSSIER / 'bonus_tp2.txt').read_text(encoding='utf-8')
    return casser_longueur_inconnue(chiffre)


def main():
    print('Challenge 1 :', challenge1())
    cle, clair = challenge2()
    print('\nChallenge 2 : clé =', cle)
    print(clair)
    print('\nBonus : essais de L = 2 à 10')
    candidats = bonus()
    for longueur, cle, clair in candidats:
        print(f'L = {longueur} | clé = {cle} | {clair[:130]}')
    while True:
        try:
            l = int(input('\nPlus petite longueur donnant du français lisible : '))
            choix = next((c for c in candidats if c[0] == l), None)
            if choix is not None:
                break
        except ValueError:
            pass
        print('Choisir une longueur testée.')
    longueur, cle, clair = choix
    chiffre = (DOSSIER / 'bonus_tp2.txt').read_text(encoding='utf-8')
    assert vigenere_chiffrer(clair, cle) == chiffre
    print(clair)
    print('Bonus : clé =', cle, '| longueur =', longueur)
    print('Réponse à rendre pour le bonus :', cle)


if __name__ == '__main__':
    main()
