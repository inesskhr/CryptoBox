# CryptoBox – TP1 et TP2

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

---

## TP2 : Vigenère et casseur automatique

### Objectif et lancement

On complète CryptoBox avec Vigenère. Les options 1 à 7 du TP1 restent disponibles.
Il n'y a rien à installer en plus de Python 3.

```bash
python cryptobox.py
```

Nouvelles options :

- 8 : chiffrer avec Vigenère ;
- 9 : déchiffrer avec Vigenère ;
- 10 : retrouver une clé de longueur connue ;
- 11 : essayer les longueurs de 2 à 10.

Pour les longs textes, répondre `o` à la question « Lire un fichier texte ? » et saisir le nom du fichier (par exemple `challenge2.txt`). Pour les messages courts, répondre `n` puis saisir le texte.

### Partie A : principe du chiffrement

On normalise le message avec `normaliser` : majuscules et accents retirés grâce à `unicodedata` (bibliothèque standard de Python). Les lettres sont numérotées de 0 à 25. Pour chaque lettre, on utilise la lettre de la clé à la position `j % len(cle)`.

- Chiffrement : C = (M + K) mod 26.
- Déchiffrement : M = (C - K) mod 26.

Le compteur `j` n'avance que sur les lettres A-Z. Les espaces, retours à la ligne, chiffres et signes de ponctuation sont recopiés. La clé doit être non vide et composée uniquement de lettres après normalisation.

Exemples du sujet :

| Message | Clé | Chiffrement |
| --- | --- | --- |
| ATTAQUE A L’AUBE | CLE | CEXCBYG L P’CFFG |
| LA CLE, 14H | TP | EP VAX, 14W |

### Partie B : principe du casseur

1. On garde seulement les lettres du texte chiffré.
2. Pour une longueur L, on construit L colonnes : `lettres[i::L]`.
3. Dans chaque colonne, `Counter` compte les lettres. On récupère la plus fréquente.
4. On suppose que cette lettre correspond au E du français (rang 4). Le décalage vaut `(rang_lettre - 4) % 26`.
5. On convertit chaque décalage en lettre puis on assemble la clé. On vérifie le résultat avec le déchiffrement de la partie A.

Cette méthode statistique fonctionne si E domine dans chaque colonne. Elle peut se tromper sur un texte trop court ou atypique. La clé n'est pas codée en dur dans le casseur.

### Bonus : longueur inconnue

On applique le même casseur pour toutes les longueurs de 2 à 10, dans l'ordre croissant. Le programme affiche chaque clé candidate avec un extrait du texte déchiffré. On choisit la plus petite longueur qui donne du français lisible, car un multiple de la longueur peut aussi fonctionner. On affiche ensuite le texte complet et la clé. Conformément à la dernière consigne, seule la clé est à saisir sur la plateforme pour le bonus.

### Résolution des trois challenges

```bash
python challenge_tp2.py
```

Le script utilise les fonctions générales de `vigenere.py`. Pour le premier challenge, il utilise la clé donnée. Pour le deuxième, il lit `challenge2.txt` et applique le casseur avec L = 9. Pour le bonus, il lit `bonus_tp2.txt`, affiche les neuf essais, puis demande la plus petite longueur lisible. Le script vérifie également le rechiffrement des résultats.

### Tests du TP1 et du TP2

```bash
python -m unittest -v
```

Les tests couvrent les deux exemples du sujet, les accents, la ponctuation, les chiffres, les clés invalides, les aller-retour, la division en colonnes et le casseur. Les neuf tests du TP1 restent inchangés.

Extrait de la sortie obtenue lors des tests :

```text
Ran 18 tests

OK
```

### Fichiers ajoutés pour le TP2

- `vigenere.py` : chiffrement, déchiffrement et casseur fréquentiel.
- `challenge_tp2.py` : résolution des trois challenges.
- `challenge2.txt` : texte chiffré du challenge 2.
- `bonus_tp2.txt` : texte chiffré du bonus.
- `test_vigenere.py` : tests automatiques du TP2.

Le fichier `cryptobox.py` a été complété par les nouvelles options du menu. `challenge.py` et `test_cryptobox.py` du TP1 sont conservés.
