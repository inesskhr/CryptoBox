"""CryptoBox - TP1 : César, substitution et transposition."""

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
        print("0. Quitter")
        choix = input("Votre choix : ").strip()
        if choix == "0":
            break
        if choix not in ("1", "2", "3", "4", "5", "6", "7"):
            print("Choix invalide.")
            continue
        try:
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
            else:
                mot_cle = input("Mot-clé : ").strip().upper()
                if choix == "6":
                    resultat = transposition_chiffrer(message, mot_cle)
                else:
                    resultat = transposition_dechiffrer(message, mot_cle)
            print("Résultat :", resultat)
        except ValueError as erreur:
            print("Erreur :", erreur)


if __name__ == "__main__":
    main()
