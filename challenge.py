"""Résolution du challenge du binôme 46 avec les fonctions de CryptoBox."""
from cryptobox import (substitution_dechiffrer, cesar_force_brute,
                       transposition_dechiffrer)


def main():
    message = "MDDRHRCRPWUR"
    cle_substitution = "FNGIWDCLJBRYSMVOTHAZPXEQKU"
    mot_cle = "MANCHE"

    # Couche 3 : retirer la substitution.
    apres_substitution = substitution_dechiffrer(message, cle_substitution)
    print("Après substitution inverse :", apres_substitution)

    # Couche 2 : essayer toutes les clés César.
    # Couche 1 : retirer la transposition pour chaque essai.
    candidats = {}
    for k, texte in cesar_force_brute(apres_substitution):
        clair = transposition_dechiffrer(texte, mot_cle)
        candidats[k] = clair
        print(f"k = {k:2d} : {clair}")

    # On choisit la clé qui donne un message lisible dans les 25 résultats.
    while True:
        try:
            k = int(input("Clé du message lisible : "))
            if k in candidats:
                break
        except ValueError:
            pass
        print("Choisissez une clé entre 1 et 25.")
    clair = candidats[k]
    print("Message final :", clair)
    print("Flag : BSD{" + clair[:8] + "}")


if __name__ == "__main__":
    main()
