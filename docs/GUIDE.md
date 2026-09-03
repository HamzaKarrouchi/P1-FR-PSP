# Guide technique du format

[CONTRIBUTING.md](../CONTRIBUTING.md) suffit pour traduire. Ce guide est là
pour quand une ligne résiste : il explique *pourquoi* les contraintes existent,
ce qui permet de les contourner intelligemment plutôt que de buter dessus.

---

## 1. L'identifiant

```
E0.BIN:012:0007
│      │   └── la réplique dans le bloc
│      └────── le bloc de dialogue (une scène, en gros)
└───────────── le fichier de données du jeu
```

Il n'a aucune valeur pour la traduction, mais c'est par lui que ta ligne
retrouve sa place dans le jeu. S'il change, la réplique est perdue.

## 2. Les codes de contrôle

Le texte du jeu n'est pas du texte pur : il est parsemé d'ordres pour le
moteur. Ils apparaissent sous trois formes.

### `{NOM}` — les ordres courants

| Code | Effet |
|---|---|
| `{SAUT}` | passe à la ligne suivante **dans la même boîte** |
| `{PAGE}` | vide la boîte et continue dessus |
| `{ATTENTE}` | attend que le joueur appuie |
| `{FERME}` | ferme la boîte de dialogue |
| `{PAUSE}` | marque un temps |

**La boîte ne va pas à la ligne toute seule.** Sans `{SAUT}`, le texte continue
tout droit et sort de l'écran. C'est toi qui découpes.

### `(*NOM*)` — les ordres rares

`(*PLAYER_NAME*)` insère le prénom choisi par le joueur, `(*APELLIDO_HEROE*)`
son nom de famille, `(*TEXTBOX_PARAM,0700*)` change la couleur du texte.

Recopie-les tels quels. Tu peux les **déplacer** si la syntaxe française
l'exige — « (*PLAYER_NAME*), viens ! » plutôt que « Viens, (*PLAYER_NAME*) ! »
— mais jamais en supprimer ni en ajouter.

### `[1A2B]` — les caractères bruts

Quatre chiffres hexadécimaux : un caractère que l'extracteur n'a pas su nommer.
Les plus fréquents sont `[0008]` pour `?` et `[0009]` pour `!`. **Recopie-les**
au lieu de taper le signe : c'est ainsi que le jeu les encode.

`[0000]` est un espace de remplissage dans certaines zones ; celui-là, tu peux
l'ignorer.

## 3. La largeur

La police est à chasse variable — un `i` prend moins de place qu'un `M` — donc
la limite exacte dépend de la phrase. Repères mesurés sur le script anglais :

| | |
|---|---|
| **40 caractères** | confortable, aucun risque |
| 43 caractères | plafond observé dans le jeu original |
| au-delà | débordement certain, le texte sort de la boîte |

Le validateur avertit à 40 et refuse à 43. Il compte **entre deux codes**, ce
qui correspond à une ligne affichée.

### Le français est plus long

De 20 à 30 %. Trois réflexes :

- **couper les béquilles** : « il est en train de » → « il », « c'est pour ça
  que » → « donc »
- **préférer le mot court** : « rencontrer » → « voir », « posséder » → « avoir »
- **redécouper avec `{SAUT}`** quand la phrase ne peut pas raccourcir — deux
  lignes courtes valent mieux qu'une longue coupée par le moteur

Si rien ne passe, c'est le signe qu'il faut reformuler la réplique, pas la
compresser. Une traduction lisible et libre bat une traduction fidèle et
illisible.

## 4. Les caractères

**Les accents fonctionnent.** Ils ont demandé du travail — les glyphes
accentués n'existaient pas dans la police du jeu et ont dû être dessinés — mais
c'est réglé et validé en jeu. Écris `déjà`, `être`, `ça`, `À`, `Ê`.

Ce qui passe : lettres accentuées et majuscules accentuées, `« »`, `’`, `…`,
`—`, la ponctuation courante.

Ce qui ne passe pas : les caractères collés depuis un traitement de texte
exotique, les emoji, les symboles rares. Le validateur les attrape sous
`[ENCODAGE]` ou `[GLYPHE]`.

> `[ENCODAGE]` : le caractère n'existe pas dans le jeu.
> `[GLYPHE]` : il existe mais sa case est vide dans la police — il s'afficherait
> blanc. C'est plus vicieux, parce que rien ne planterait.

## 5. Les doublons

Chaque texte n'apparaît **qu'une fois** dans les fichiers. Le champ
`_occurrences` te dit combien de fois il revient en jeu.

Conséquence importante : une réplique qui revient 570 fois est forcément
générique. Traduis-la de façon à ce qu'elle marche **dans tous les contextes**,
pas seulement dans celui que tu imagines.

## 6. Le canari

Un fichier `_canari.json` contient l'empreinte de chaque texte anglais. Si tu
modifies `en` ou `locuteur` — même d'une lettre, même par accident en tapant
dans le mauvais champ — le validateur le voit et te le dit.

C'est une protection, pas une méfiance : sans elle, une lettre écrasée rendrait
la réplique introuvable au moment d'assembler le jeu, des semaines plus tard.

## 7. Vérifier chez soi (facultatif)

Le robot le fait pour toi à chaque proposition. Mais si tu veux la réponse tout
de suite, il te faut [Ruby](https://www.ruby-lang.org/fr/downloads/) :

```bash
ruby outils/check_trad.rb trad/dialogues/E0_004.json
```

```
✅  trad/dialogues/E0_004.json — 92/92 traduites
```

Aucune dépendance à installer, et le script ne touche à rien : il lit et il
signale.
