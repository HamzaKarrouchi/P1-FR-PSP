# Guide technique du format

[CONTRIBUTING.md](../CONTRIBUTING.md) suffit pour traduire. Ce guide est là
pour quand une ligne résiste : il explique *pourquoi* les contraintes existent,
ce qui permet de les contourner intelligemment plutôt que de buter dessus.

---

## 1. Les trois zones, et l'identifiant

Le texte du jeu vit à trois endroits, et `trad/` a un dossier pour chacun.

| Dossier | Contenu | Ce qui change pour toi |
|---|---|---|
| `trad/dialogues/` | l'histoire, les personnages qui parlent | un champ `locuteur` à traduire aussi |
| `trad/eboot/` | menus, écrans, noms de lieux, tutoriels | un champ **`max`** à respecter (§3) |
| `trad/donjons/` | messages de couloir, portes fermées | rien de particulier |

L'identifiant dit d'où vient la ligne :

```text
E0.BIN:012:0007            un dialogue
│      │   └── la réplique dans le bloc
│      └────── le bloc de dialogue (une scène, en gros)
└───────────── le fichier de données du jeu

EBOOT.BIN:BE:OFF_2D7B4C    une ligne d'interface, à son adresse dans l'exécutable
DNG:d00/d00.bin:0000       une ligne de donjon
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

### `(*NOM*)` — la mise en scène

Ceux-là ne s'affichent pas : ils pilotent la scène. Les plus fréquents, comptés
sur les 8 572 textes :

| Code | Occurrences | Rôle |
|---|---:|---|
| `(*SCENE_INIT*)` `(*SCENE_LOAD*)` | 5 331 | montage de la scène |
| `(*WAIT_INPUT*)` | 1 781 | attend le joueur |
| `(*SET_ANIM_LAYER*)` | 1 472 | animation d'un personnage |
| `(*SHOW_MSG*)` `(*HIDE_MSG*)` | 1 238 | ouvre ou ferme la boîte |
| `(*TEXTBOX_PARAM,0700*)` | 342 | couleur du texte |
| `(*APELLIDO_HEROE*)` | 300 | le nom choisi par le joueur |
| `(*CHECK_FLAG*)` | 292 | un embranchement du scénario |

**Recopie-les tels quels.** `(*APELLIDO_HEROE*)` et `(*APODO_HEROE*)` (son
surnom) peuvent se **déplacer** si la syntaxe française l'exige — « Alors,
(*APELLIDO_HEROE*) ? » plutôt que « (*APELLIDO_HEROE*), alors ? » — mais jamais
disparaître.

Le reste est de la machinerie : on n'y touche pas, on la transporte.

### `[1A2B]` — les caractères bruts

Quatre chiffres hexadécimaux : un caractère que l'extracteur n'a pas su nommer.
Il y en a **6 932 dans le jeu, pour 1 842 codes distincts** — `[0300]` et
`[1E00]` en tête. Ils ne se traduisent pas : **recopie-les à l'identique**.

`[0000]` est un espace de remplissage dans certaines zones de l'exécutable ;
celui-là, le validateur l'ignore.

> **La ponctuation n'est pas concernée.** `?`, `!`, `…`, `«` `»` s'écrivent
> normalement. Si tu as lu ailleurs qu'il fallait taper `[0008]` pour un point
> d'interrogation, c'est une consigne périmée de l'ancienne chaîne d'outils —
> ces codes n'existent nulle part dans les fichiers actuels.

## 3. La largeur

La police est à chasse variable — un `i` prend moins de place qu'un `M` — donc
la limite exacte dépend de la phrase. Repères mesurés sur les 14 572 lignes du
script anglais :

| | |
|---|---|
| **33 caractères** | la ligne anglaise médiane |
| 40 caractères | le 95ᵉ centile — au-delà, on sort de l'ordinaire |
| 43 caractères | débordement certain dans la plupart des boîtes |

**La largeur se juge par rapport à l'anglais**, pas dans l'absolu : 42 lignes
du script original dépassent déjà 43 caractères, et te refuser pour une largeur
que tu n'as pas créée n'aurait aucun sens. Le validateur ne bloque donc que
si ta ligne est **à la fois** plus large que l'anglaise **et** au-delà de 43.
Entre 40 et 43, il avertit.

Il compte **entre deux codes**, ce qui correspond à une ligne affichée.

### Le champ `max` — seulement dans `trad/eboot/`

Les lignes de l'EBOOT portent un champ en plus :

```json
{ "id": "EBOOT.BIN:BE:OFF_2D7B4C", "en": "Do you want Normal?", "fr": "", "max": 30 }
```

`max` est le **nombre de caractères de l'anglais**. Ces textes ne vivent pas
dans un fichier de données mais dans l'exécutable, où chaque chaîne occupe un
emplacement de taille fixe : le moteur écrit ta traduction par-dessus l'anglaise
et complète avec des espaces.

**Dépasser n'est pas interdit.** Le moteur redirige alors la chaîne trop longue
vers un espace libre de l'exécutable. C'est vérifié en jeu : « Charger une
partie », 18 caractères pour un `max` de 17, s'affiche entier sur l'écran-titre.

Mais c'est plus fragile que de tenir dans la place d'origine, alors le
validateur te le signale — **en jaune, sans bloquer** — sous `[BUDGET]`, avec le
compte exact. Les jetons (`{SAUT}`, `[0000]`…) ne comptent pas, les accents
comptent pour un.

Vise le budget quand tu peux. Ne massacre pas le français quand tu ne peux
pas : certains `max` sont intenables — `No` en fait deux, « Non » en fait
trois.

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

> **Ce qui passe n'est pas ce qu'on écrit.** Le projet emploie les guillemets
> droits `"`, l'apostrophe droite `'`, `...` en trois points, et **aucune
> espace avant `!` et `?`**. C'est la convention des lignes déjà validées en
> jeu — voir [REGLES.md](REGLES.md#la-typographie-du-projet). S'en écarter
> passe la validation mais produit un jeu typographiquement bancal.

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

## 6. Le budget d'octets — le piège invisible

Le jeu ne cherche pas ses fichiers de données par leur nom : il lit à une
**adresse fixe** sur le disque. Un fichier qui grossit est réécrit ailleurs, et
le jeu continue de lire l'ancien. Résultat : **tout le fichier redevient
anglais, sans le moindre message d'erreur.**

Chaque caractère coûte **2 octets**, et le contenu est découpé en blocs alignés
sur 2 048 octets. Un bloc qui franchit sa frontière coûte un secteur entier.

Trois choses multiplient l'addition :

- **Les répétitions.** Un texte marqué `_occurrences: 9` se paie neuf fois.
  C'est arrivé : l'aide d'un mini-jeu, plus longue de 26 caractères, a fait
  déborder **trois fichiers de données d'un coup**.
- **Le nom du personnage.** `locuteur_fr` est encodé avec *chaque* réplique.
  Rallonger un nom de cinq lettres pour quelqu'un qui parle mille fois coûte
  10 000 octets.
- **Les accents ne coûtent rien de plus** — un `é` pèse autant qu'un `e`.

**La règle simple :** pour un texte répété, reste **sous la longueur de
l'anglais**. Le validateur t'avertit quand une entrée dépasse 48 octets de
surplus, mais il ne connaît pas la marge réelle du bloc — la prudence reste
la meilleure méthode.

## 7. Le canari

Un fichier `_canari.json` contient l'empreinte de chaque texte anglais. Si tu
modifies `en` ou `locuteur` — même d'une lettre, même par accident en tapant
dans le mauvais champ — le validateur le voit et te le dit.

C'est une protection, pas une méfiance : sans elle, une lettre écrasée rendrait
la réplique introuvable au moment d'assembler le jeu, des semaines plus tard.

## 8. La terminologie

Le validateur lit le [dictionnaire](Dictionnaire.md) et signale, **en
avertissement**, un terme validé (✅) présent dans l'anglais dont la traduction
officielle manque dans ton français.

Les termes marqués 🔶 ne sont **pas** contrôlés : ce sont des propositions,
pas encore tranchées. Les figer reviendrait à décider à la place de l'équipe.

**Un terme peut avoir deux rendus légitimes**, séparés par ` / ` dans la colonne
française : `Arbre Agastya / Agastya`. N'importe lequel satisfait le contrôle.
C'est fait pour les étiquettes trop étroites — la forme longue vit dans la
légende de la carte, l'abrégée sur une étiquette de onze caractères — et non
pour laisser flotter un terme : la règle qui dit *laquelle employer où* se met
dans la même case, entre parenthèses.

L'avertissement se trompe régulièrement, et c'est voulu : « Nanjo la regarde »
ne répète pas son nom si l'anglais disait « Nanjo looks at her ». Il vaut mieux
une question de trop qu'un jeu où la Chambre de Velours change de nom trois
fois.

## 9. Vérifier chez soi (facultatif)

Le robot le fait pour toi à chaque proposition. Mais si tu veux la réponse tout
de suite, il te faut [Ruby](https://www.ruby-lang.org/fr/downloads/) :

```bash
ruby outils/check_trad.rb trad/dialogues/E0_004.json
```

```text
✅  trad/dialogues/E0_004.json — 92/92 traduites
```

Aucune dépendance à installer, et le script ne touche à rien : il lit et il
signale.
