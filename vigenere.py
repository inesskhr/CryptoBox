"""TP2 : Vigenère et casseur par fréquence de la lettre E."""
import unicodedata
from collections import Counter

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def normaliser(texte):
    """Mettre en majuscules et retirer les accents."""
    return ''.join(c for c in unicodedata.normalize('NFD', texte.upper())
                   if unicodedata.category(c) != 'Mn')


def lettres_seules(texte):
    return ''.join(c for c in normaliser(texte) if c in ALPHABET)


def verifier_cle(cle):
    cle = normaliser(cle)
    if not cle or any(c not in ALPHABET for c in cle):
        raise ValueError('La clé doit contenir uniquement des lettres A-Z.')
    return cle


def transformer(texte, cle, sens):
    cle = verifier_cle(cle)
    resultat = []
    j = 0
    for c in normaliser(texte):
        if c in ALPHABET:
            m = ALPHABET.index(c)
            k = ALPHABET.index(cle[j % len(cle)])
            resultat.append(ALPHABET[(m + sens * k) % 26])
            j += 1
        else:
            # Les espaces, chiffres et signes ne consomment pas la clé.
            resultat.append(c)
    return ''.join(resultat)


def vigenere_chiffrer(texte, cle):
    return transformer(texte, cle, 1)


def vigenere_dechiffrer(texte, cle):
    return transformer(texte, cle, -1)


def colonnes(texte, longueur):
    lettres = lettres_seules(texte)
    if not isinstance(longueur, int) or not 1 <= longueur <= len(lettres):
        raise ValueError('Longueur invalide ou texte trop court.')
    return [lettres[i::longueur] for i in range(longueur)]


def casser_vigenere(texte, longueur):
    """Supposer que la lettre la plus fréquente de chaque colonne est E."""
    cle = ''
    for colonne in colonnes(texte, longueur):
        frequente = Counter(colonne).most_common(1)[0][0]
        decalage = (ALPHABET.index(frequente) - ALPHABET.index('E')) % 26
        cle += ALPHABET[decalage]
    return cle


def casser_longueur_inconnue(texte):
    """Tester 2 à 10 dans l'ordre ; retenir le premier texte lisible."""
    candidats = []
    for longueur in range(2, min(10, len(lettres_seules(texte))) + 1):
        cle = casser_vigenere(texte, longueur)
        candidats.append((longueur, cle, vigenere_dechiffrer(texte, cle)))
    if not candidats:
        raise ValueError('Le texte doit contenir au moins deux lettres.')
    return candidats
