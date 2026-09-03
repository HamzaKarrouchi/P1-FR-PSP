# Persona 1 FR — traduction française de *Shin Megami Tensei: Persona* (PSP)

![avancement](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/OWNER/P1-FR-PSP/main/.github/badge.json)
![licence](https://img.shields.io/badge/licence-CC%20BY--NC--SA%204.0-lightgrey)

Traduction **amateur et non lucrative** de la version PSP américaine
(`ULUS-10432`). Le jeu n'est jamais sorti en français ; ce projet vise une
version complète, jouable, et écrite en vrai français — accents compris.

**On cherche des traducteurs.** Il n'y a rien à installer : tu ouvres un
fichier dans ton navigateur, tu écris, tu proposes. Un robot vérifie la
technique à ta place.

👉 **[Comment aider](CONTRIBUTING.md)** · **[Avancement](SUIVI.md)**

---

## Où ça en est

Voir [SUIVI.md](SUIVI.md), recalculé automatiquement à chaque contribution.

L'introduction est traduite, testée en jeu et validée : dialogues, écran-titre,
écran de mise en garde, phases de lune. C'est la démonstration que la chaîne
fonctionne de bout en bout, du fichier JSON jusqu'à l'ISO.

## Ce qui est ouvert

| | |
|---|---|
| **Dialogues** | 8 572 textes, 104 fichiers — **ouvert** |
| Négociations | bloqué : l'extracteur perd 535 chaînes, on ne fait pas traduire sur une source trouée |
| Menus, objets, sorts | pas encore cartographiés dans l'EBOOT |

Le jeu répète énormément : 17 685 lignes de dialogue pour 8 572 textes
distincts. Trois répliques de l'Arbre Agastya reviennent près de 570 fois
chacune. Tu ne traduis chaque texte **qu'une fois** — la propagation vers
toutes ses occurrences est automatique.

## Comment on teste

Les traductions fusionnées ici sont réinjectées dans le jeu par les
mainteneurs, qui publient un correctif `.xdelta` de temps à autre. Tu n'as pas
besoin du jeu pour contribuer, mais si tu l'as :

1. il faut **posséder une copie légale** du jeu ;
2. le correctif s'applique sur l'ISO américaine avec [xdelta](https://www.romhacking.net/utilities/598/) ;
3. les accents demandent l'option **Remplacement de textures** de PPSSPP —
   la marche à suivre est fournie avec chaque version.

**Aucune ISO n'est distribuée ici, et il n'en sera jamais distribué.**

## Structure

```text
trad/dialogues/   les fichiers à traduire
docs/             le guide, les règles de style, le dictionnaire
outils/           le validateur, qu'on peut lancer chez soi (Ruby)
SUIVI.md          généré, jamais édité à la main
```

## Remerciements

- **Zenshou** (`@xrize._`) — sa chaîne d'outils et ses réponses sont à
  l'origine de tout ce qui marche ici. Rien de ce projet n'existerait sans lui.
- **GarekMallen** — éditeur PT-BR, table d'accents confirmée par recoupement,
  et une interface française écrite pour nous.
- **chenetulipe et l'équipe [P2-FR-IS-PSP](https://github.com/chenetulipe/P2-FR-IS-PSP)** —
  modèle d'organisation.
- **Atlus / SEGA** — ayants droit du jeu.

## Position juridique

Projet de fans, sans but lucratif, sans aucun lien avec Atlus ou SEGA. Aucune
donnée du jeu n'est redistribuée : uniquement un correctif, qui exige de
posséder le jeu. Le script anglais est publié en clair parce que c'est la seule
façon de traduire à plusieurs — c'est un choix assumé. À la première demande
d'un ayant droit, le dépôt est retiré.

La traduction française est publiée sous [CC BY-NC-SA 4.0](LICENSE). Le texte
anglais d'origine appartient à Atlus.
