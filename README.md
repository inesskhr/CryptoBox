# CryptoBox – TP1

Binôme 46

## Objectif

CryptoBox est un outil en Python permettant de chiffrer et de déchiffrer un message avec trois méthodes : César, substitution et transposition par colonnes. Le programme ne nécessite aucune bibliothèque externe.

## Utilisation

Il faut avoir Python 3 installé. Depuis le dossier du projet, lancer :

```bash
python cryptobox.py
```

Le menu permet de choisir une méthode, de saisir un message et une clé, puis d'afficher le résultat. L'option 3 affiche les 25 possibilités de César.

Les messages sont en lettres A à Z sans espaces ni accents. Le menu convertit les minuscules en majuscules. La clé de substitution doit être une permutation de l'alphabet. Pour la transposition, les colonnes sont triées par ordre alphabétique du mot-clé. En cas de lettres identiques, on conserve leur ordre de gauche à droite. La dernière ligne est complétée par des X ; au déchiffrement, on conserve ces X car ils peuvent aussi appartenir au message original.

## Exemples de test

| Méthode | Message | Clé | Résultat du chiffrement |
| --- | --- | --- | --- |
| César | BONJOUR | 3 | ERQMRXU |
| Substitution | ATTAQUE | QWERTYUIOPASDFGHJKLZXCVBNM | QZZQJXT |
| Transposition | RENDEZVOUSAMIDI | PORTE | ESIEVMRZANOIDUD |

Pour lancer les tests automatiques :

```bash
python -m unittest -v
```

## Challenge du binôme 46

Le message intercepté est `MDDRHRCRPWUR`. L'ordre du chiffrement est : transposition (MANCHE), César (clé inconnue), substitution (FNGIWDCLJBRYSMVOTHAZPXEQKU).

Pour résoudre le challenge, lancer :

```bash
python challenge.py
```

Le programme inverse d'abord la substitution, puis teste les 25 clés de César. Pour chaque clé, il inverse aussi la transposition. Il suffit de choisir le résultat lisible ; le programme affiche le message final et le flag composé des huit premières lettres.

## Organisation du projet

- `cryptobox.py` : fonctions de chiffrement et de déchiffrement, menu principal.
- `challenge.py` : résolution du challenge avec les fonctions de CryptoBox.
- `test_cryptobox.py` : tests des trois méthodes et du challenge.
- `README.md` : présentation et mode d'emploi.

Sur certains ordinateurs, il faut utiliser `python3` au lieu de `python`.
