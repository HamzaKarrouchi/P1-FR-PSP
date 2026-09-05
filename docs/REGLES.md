# Règles de style

[CONTRIBUTING.md](../CONTRIBUTING.md) dit comment contribuer, [GUIDE.md](GUIDE.md)
explique le format. Ce document-ci parle de la seule chose qui compte vraiment :
**que le français sonne juste.**

---

## Le principe

*Persona* est un jeu de 1996 sur des lycéens ordinaires à qui il arrive quelque
chose d'extraordinaire. Le texte anglais est vivant, souvent drôle, parfois
maladroit. **Traduis l'intention, pas les mots.**

Une réplique réussie est une réplique qu'un ado francophone pourrait dire.
Si tu la relis à voix haute et qu'elle sonne comme une notice, recommence.

## Le tutoiement

Par défaut, **tout le monde se tutoie** : ce sont des camarades de classe.

Trois exceptions :

- **Nanjo vouvoie**, presque tout le monde, tout le temps. Ce n'est pas de la
  politesse, c'est de la distance : il est riche, il le sait, et il tient les
  autres à un mètre. Ne le corrige pas vers le tutoiement même quand ça
  s'adoucit — c'est un arc de personnage. C'est aussi la voix la plus présente
  du jeu (1 011 répliques) : une erreur de registre sur lui se voit partout.
- **Les adultes** (professeurs, personnel, inconnus) vouvoient les élèves et
  sont vouvoyés en retour.
- **Philémon, Igor et les entités** parlent un français soutenu et vouvoient.
  Registre solennel, phrases amples.

## Les voix

Les noms ci-dessous sont ceux que porte le champ `locuteur` **dans les
fichiers** — le jeu emploie les surnoms, pas les patronymes. Le nombre de
répliques donne une idée du poids de chaque voix.

| Locuteur | Répliques | Registre |
|---|---:|---|
| **Nanjo** (Kei Nanjo) | 1 011 | soutenu, sec, phrases complètes. Il ne contracte rien et vouvoie. |
| **Mark** (Masao Inaba) | 685 | familier, énergique, argot léger. « Mec », « ouais ». Jamais vulgaire. |
| **Ayase** (Yuka Ayase) | 685 | bavarde, directe, s'intéresse de près au héros. |
| **Elly** (Eriko Kirishima) | 674 | assurée, un rien théâtrale, cultivée. |
| **Brown** (Hidehiko Uesugi) | 664 | le blagueur ; il en fait trop, et c'est le but. |
| **Maki** (Maki Sonomura) | 571 | douce, hésitante ; beaucoup de points de suspension dans l'original — garde-les. |
| **Yukino** (Yukino Mayuzumi) | 549 | directe, un peu dure, ancienne rebelle. Elle coupe court. |
| **Reiji** (Reiji Kido) | 179 | fermé, hostile au début. Répliques courtes. |
| **Le héros** | — | muet. Ses répliques sont des choix du joueur : courtes et neutres. |

> ⚠️ **Ces descriptions de voix demandent validation.** Elles ont été écrites
> d'après la connaissance générale du jeu, pas d'après une relecture du script
> complet. Si tu connais le jeu et qu'une ligne te paraît fausse, ouvre une
> issue : ces quelques mots orientent 8 572 traductions, ils méritent d'être
> justes.

Quand un personnage nomme le héros, l'anglais emploie `(*APELLIDO_HEROE*)`
(300 fois) ou `(*APODO_HEROE*)` pour son surnom. Ces jetons portent le nom
choisi par le joueur : place-les où le français les veut, mais ne les supprime
jamais.

**Les surnoms restent-ils ?** « Mark » pour Masao, « Brown » pour Hidehiko,
« Elly » pour Eriko — le jeu les présente lui-même (« Masao Inaba (Nickname:
Mark) »). La question n'est pas tranchée : voir le
[Dictionnaire](Dictionnaire.md), et discuter avant de décider seul.

## La typographie du projet

Le jeu accepte `« »`, `’`, `…`. **On ne s'en sert pas.** La convention retenue
est celle des traductions déjà en jeu — elle a été relevée sur les lignes
validées, pas décidée en théorie :

| | On écrit | On n'écrit pas |
|---|---|---|
| Avant `!` et `?` | `blague!` `déjà?` | ~~`blague !`~~ |
| Guillemets | `"comme ça"` | ~~`« comme ça »`~~ |
| Apostrophe | `qu'une` | ~~`qu’une`~~ |
| Points de suspension | `Héhéhé...` | ~~`Héhéhé…`~~ |

Ce n'est pas la typographie française idéale, et c'est assumé : **la cohérence
d'un bout à l'autre du jeu vaut mieux que la perfection par endroits.** Une
espace avant chaque `!` coûterait aussi de la place dans des boîtes déjà
étroites, et l'apostrophe droite se distingue mal de la courbe à l'écran.

**Tirets de dialogue** : le jeu n'en utilise pas. Ne pas en ajouter.

**Les accents, eux, s'écrivent normalement** — `é è ê à â ù û ô î ï ç`, et les
majuscules accentuées `É À Ê Î Ô Ç`. Elles sont dessinées et validées en jeu.

## Ce qui ne s'invente pas

- **Les noms propres, Personas, sorts, objets et lieux** passent par le
  [Dictionnaire](Dictionnaire.md). Un terme s'y trouve : tu l'emploies. Il ne
  s'y trouve pas : tu ouvres une issue, on tranche, on l'inscrit. Un terme
  traduit de deux façons dans le jeu, c'est un bug de traduction.
- **Les onomatopées et les cris** : demande plutôt que d'improviser. « Whoa! »
  n'a pas une seule bonne traduction, et il revient des centaines de fois.
- **Les jeux de mots intraduisibles** : signale-les dans ta proposition. On en
  discute, on trouve mieux à plusieurs.

## Les répliques qui reviennent

Le champ `_occurrences` te dit combien de fois un texte apparaît. Au-delà de
quelques dizaines, la réplique est **générique** : elle sert dans des contextes
que tu ne vois pas. Traduis-la de façon neutre, qui marche partout.

Exemple : « Whoa! » revient dans une scène comique et dans une scène d'horreur.
« Waouh ! » ne marche que dans la première.

## En cas de doute

Ouvre une issue. Une question posée coûte cinq minutes ; une incohérence
découverte trois mois plus tard coûte une relecture complète.
