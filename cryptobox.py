"""CryptoBox - TP1 et TP2."""
from vigenere import (vigenere_chiffrer, vigenere_dechiffrer,
                      casser_vigenere, casser_longueur_inconnue)

from pathlib import Path

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def verifier_message(message):
    if any(lettre not in ALPHABET for lettre in message):
        raise ValueError("Le message doit contenir uniquement des lettres A à Z.")


def verifier_cle_substitution(cle):
    if len(cle) != 26 or set(cle) != set(ALPHABET):
        raise ValueError("La clé doit contenir les 26 lettres de A à Z, une seule fois.")


def ordre_colonnes(mot_cle):
    verifier_message(mot_cle)
    if not mot_cle:
        raise ValueError("Le mot-clé ne doit pas être vide.")
    # En cas de lettres identiques, la colonne de gauche passe en premier.
    return sorted(range(len(mot_cle)), key=lambda i: (mot_cle[i], i))


# 1. Chiffrement de César

def cesar_chiffrer(message, k):
    verifier_message(message)
    resultat = ""
    for lettre in message:
        position = ALPHABET.index(lettre)
        resultat += ALPHABET[(position + k) % 26]
    return resultat


def cesar_dechiffrer(message, k):
    return cesar_chiffrer(message, -k)


def cesar_force_brute(message):
    return [(k, cesar_dechiffrer(message, k)) for k in range(1, 26)]


# 2. Chiffrement par substitution

def substitution_chiffrer(message, cle):
    verifier_message(message)
    verifier_cle_substitution(cle)
    resultat = ""
    for lettre in message:
        resultat += cle[ALPHABET.index(lettre)]
    return resultat


def substitution_dechiffrer(message, cle):
    verifier_message(message)
    verifier_cle_substitution(cle)
    resultat = ""
    for lettre in message:
        resultat += ALPHABET[cle.index(lettre)]
    return resultat


# 3. Transposition par colonnes

def transposition_chiffrer(message, mot_cle):
    verifier_message(message)
    ordre = ordre_colonnes(mot_cle)
    n = len(mot_cle)
    # Compléter la dernière ligne avec des X si nécessaire.
    message += "X" * ((-len(message)) % n)
    resultat = ""
    for colonne in ordre:
        resultat += message[colonne::n]
    return resultat


def transposition_dechiffrer(message, mot_cle):
    verifier_message(message)
    ordre = ordre_colonnes(mot_cle)
    n = len(mot_cle)
    if len(message) % n != 0:
        raise ValueError("La longueur du message chiffré doit être un multiple de celle du mot-clé.")
    lignes = len(message) // n
    colonnes = [""] * n
    # Replacer chaque colonne dans sa position d'origine.
    for j, colonne in enumerate(ordre):
        colonnes[colonne] = message[j * lignes:(j + 1) * lignes]
    resultat = ""
    for i in range(lignes):
        for j in range(n):
            resultat += colonnes[j][i]
    # On garde les X : ils peuvent aussi faire partie du message original.
    return resultat


def main():
    while True:
        print("\n--- CryptoBox ---")
        print("1. César : chiffrer")
        print("2. César : déchiffrer")
        print("3. César : force brute")
        print("4. Substitution : chiffrer")
        print("5. Substitution : déchiffrer")
        print("6. Transposition : chiffrer")
        print("7. Transposition : déchiffrer")
        print("8. Vigenère : chiffrer")
        print("9. Vigenère : déchiffrer")
        print("10. Vigenère : casser (longueur connue)")
        print("11. Vigenère : casser (longueur inconnue)")
        print("0. Quitter")
        choix = input("Votre choix : ").strip()
        if choix == "0":
            break
        if choix not in tuple(str(i) for i in range(1, 12)):
            print("Choix invalide.")
            continue
        try:
            if choix in ("8", "9", "10", "11"):
                mode = input("Lire un fichier texte ? (o/n) : ").strip().lower()
                if mode == "o":
                    message = Path(input("Chemin du fichier : ").strip()).read_text(encoding="utf-8")
                else:
                    message = input("Message : ")
            else:
                message = input("Message (A-Z) : ").strip().upper()
            if choix in ("1", "2"):
                k = int(input("Clé César (entier) : "))
                if choix == "1":
                    resultat = cesar_chiffrer(message, k)
                else:
                    resultat = cesar_dechiffrer(message, k)
            elif choix == "3":
                for k, texte in cesar_force_brute(message):
                    print(f"k = {k:2d} : {texte}")
                continue
            elif choix in ("4", "5"):
                cle = input("Clé de substitution (26 lettres) : ").strip().upper()
                if choix == "4":
                    resultat = substitution_chiffrer(message, cle)
                else:
                    resultat = substitution_dechiffrer(message, cle)
            elif choix in ("6", "7"):
                mot_cle = input("Mot-clé : ").strip().upper()
                if choix == "6":
                    resultat = transposition_chiffrer(message, mot_cle)
                else:
                    resultat = transposition_dechiffrer(message, mot_cle)
            elif choix in ("8", "9"):
                cle = input("Clé Vigenère : ").strip().upper()
                if choix == "8":
                    resultat = vigenere_chiffrer(message, cle)
                else:
                    resultat = vigenere_dechiffrer(message, cle)
            elif choix == "10":
                longueur = int(input("Longueur de la clé : "))
                cle = casser_vigenere(message, longueur)
                print("Clé candidate :", cle)
                resultat = vigenere_dechiffrer(message, cle)
            else:
                candidats = casser_longueur_inconnue(message)
                for longueur, cle, texte in candidats:
                    print(f"L = {longueur} | clé = {cle} | {texte[:160]}")
                longueur = int(input("Plus petite longueur donnant un texte lisible : "))
                choix_candidat = next((c for c in candidats if c[0] == longueur), None)
                if choix_candidat is None:
                    raise ValueError("Longueur non testée.")
                _, cle, resultat = choix_candidat
                print("Clé candidate :", cle)
            print("Résultat :", resultat)
        except (ValueError, OSError) as erreur:
            print("Erreur :", erreur)


if __name__ == "__main__":
    main()
