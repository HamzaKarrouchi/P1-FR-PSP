<img src="assets/persona-psp.jpg" align="right" width="200" alt="Shin Megami Tensei: Persona (PSP)">

# Persona 1 FR

**Traduction française de *Shin Megami Tensei: Persona*** (PSP, version
américaine `ULUS-10432`). Le jeu n'est jamais sorti en français ; ce projet
vise une version complète, jouable, et écrite en vrai français — accents
compris.

![avancement](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/HamzaKarrouchi/P1-FR-PSP/main/.github/badge.json)
![licence](https://img.shields.io/badge/licence-CC%20BY--NC--SA%204.0-lightgrey)

**On cherche des traducteurs.** Rien à installer : tu ouvres un fichier dans
ton navigateur, tu écris, tu proposes. Un robot vérifie la technique à ta
place.

👉 **[Comment aider](CONTRIBUTING.md)** · **[Avancement](SUIVI.md)** · **[FAQ](docs/FAQ.md)**

<br clear="right">

---

## À quoi ça ressemble

| Anglais d'origine | Français |
|---|---|
| <img src="assets/captures/ouverture-en.png" width="400" alt="citation d'ouverture en anglais"> | <img src="assets/captures/ouverture-fr.png" width="400" alt="citation d'ouverture en français"> |
| <img src="assets/captures/menu-en.png" width="400" alt="menu du titre en anglais"> | <img src="assets/captures/menu-fr.png" width="400" alt="menu du titre en français"> |
| <img src="assets/captures/dialogue-en.png" width="400" alt="dialogue en anglais"> | <img src="assets/captures/dialogue-fr.png" width="400" alt="dialogue en français"> |

> Colonne de gauche : le jeu d'origine. Colonne de droite : la traduction, avec
> le **pack HD** de Ryuubu par-dessus — voir [plus bas](#le-rendu-hd-recommandé).
> La netteté vient de lui ; le français vient de nous.

Les accents ont demandé le plus gros du travail technique : le jeu américain
n'a **aucun glyphe accentué** — les cases correspondantes de sa police sont
vides. Il a fallu les dessiner un par un dans les atlas de textures, puis
régler leurs métriques. Vingt-cinq caractères, validés en jeu.

<p align="center">
  <img src="assets/captures/accents.png" width="700" alt="texte français accentué en jeu">
</p>

---

## Le rendu HD, recommandé

Un pack de textures haute définition existe pour ce jeu, et **la traduction est
faite pour fonctionner avec**. Ce n'est pas notre travail — c'est celui de
**Ryuubu**, publié sur les forums PPSSPP puis porté sur GameBanana :

**<https://gamebanana.com/mods/309876>** · 207 Mo · 793 textures

Il remplace les polices, l'interface, les cartes de Persona, les portraits, les
cartes du monde, l'interface de combat, les crédits et les mini-jeux du casino.
Nous n'avons pas le droit de le redistribuer : il se télécharge chez lui.

### L'installer avec la traduction

Le pack et la traduction touchent **les mêmes textures** — les trois atlas de
police et quatre écrans. PPSSPP ne lit qu'un seul `textures.ini` par jeu, il
faut donc les fusionner :

```bash
python outils/installer_hd.py --source "<dossier HD UI décompressé>"
```

Le script copie son pack, puis redirige vers nos fichiers français les sept
textures qui nous concernent — celles-ci sont fournies avec le correctif. Les
accents sont recomposés sur ses planches HD : elles sont les nôtres à l'échelle
**×5 exacte**, même grille de 16 colonnes, ce qui rend l'opération possible.

Un fichier français absent laisse la texture anglaise HD en place plutôt que de
pointer vers le vide — vous ne risquez pas de vous retrouver avec un trou à
l'écran.

Dans PPSSPP, **fenêtre fermée** : `Remplacement de textures` **ON**,
`Enregistrement des nouvelles textures` **OFF**.

### Sans le pack HD

La traduction fonctionne très bien sans lui — c'est ainsi qu'elle a été
développée. Le texte est simplement en résolution d'origine.

---

## Ton premier fichier, en cinq minutes

1. Ouvre [SUIVI.md](SUIVI.md), prends un fichier marqué **libre**.
2. Clique dessus dans [`trad/`](trad/), puis sur le crayon ✏️ en haut à droite.
3. Remplis les champs `fr`. Ne touche à rien d'autre.
4. En bas : **Create a new branch**, puis **Propose changes**.
5. Le robot te répond en une minute et annote précisément ce qui cloche, s'il
   y a lieu. Tu corriges au même endroit.

Tout est détaillé dans **[CONTRIBUTING.md](CONTRIBUTING.md)**. Tu n'as pas
besoin du jeu, ni de savoir coder, ni d'avoir fini le fichier d'un coup.

---

## Ce qui est ouvert

| | |
|---|---|
| **Dialogues** (`trad/dialogues/`) | 8 572 textes, 104 fichiers — **ouvert** |
| **Menus et écrans** (`trad/eboot/`) | 1 518 textes, 17 fichiers — **ouvert** |
| **Donjons** (`trad/donjons/`) | 130 textes, 2 fichiers — **ouvert** |
| Noms de démons, de Personas et sorts signature | **gardés en anglais** : Pixie reste Pixie, Bufu reste Bufu, comme dans toute la série |
| Négociations de démons | leur texte n'est pas encodé comme le reste du jeu, et on n'a pas encore percé comment. On ne fait pas traduire 17 408 lignes qu'on ne saurait pas réinjecter |

Le jeu répète énormément : 17 685 lignes de dialogue pour 8 572 textes
distincts. Trois répliques de l'Arbre Agastya reviennent près de 570 fois
chacune. Tu ne traduis chaque texte **qu'une fois** — la propagation vers
toutes ses occurrences est automatique.

## La suite

- [x] chaîne technique refaite, du JSON jusqu'à l'ISO
- [x] accents dessinés et validés en jeu
- [x] introduction traduite, images de l'écran-titre traduites
- [x] validation automatique des contributions
- [x] menus, écrans et donjons cartographiés et ouverts à la traduction
- [ ] **les dialogues** — c'est là qu'on a besoin de monde
- [ ] **les menus et les écrans** — plus courts, parfaits pour commencer
- [ ] percer l'encodage du texte des négociations, puis les ouvrir
- [ ] reporter les 1 427 noms d'objets, d'armes et de sorts déjà arbitrés
- [ ] retrouver les noms de lieux — le bandeau `1F Empty Classroom` de la
      capture ci-dessus n'apparaît dans aucune extraction : ce texte vit
      ailleurs, et on ne sait pas encore où
- [ ] première version publique du correctif

Pas de date : c'est un projet de loisir. L'avancement réel est dans
[SUIVI.md](SUIVI.md), recalculé à chaque contribution.

## Comment on teste

Les traductions fusionnées ici sont réinjectées dans le jeu par les
mainteneurs, qui publient un correctif `.xdelta` de temps à autre. Tu n'as pas
besoin du jeu pour contribuer, mais si tu l'as :

1. il faut **posséder une copie légale** du jeu ;
2. le correctif s'applique sur l'ISO américaine avec [xdelta](https://www.romhacking.net/utilities/598/) ;
3. les accents demandent l'option **Remplacement de textures** de PPSSPP — la
   marche à suivre accompagne chaque version.

**Aucune ISO n'est distribuée ici, et il n'en sera jamais distribué.**

## Structure

```text
trad/dialogues/   l'histoire et les personnages
trad/eboot/       menus, écrans, noms de lieux, tutoriels
trad/donjons/     messages de couloir, portes fermées
docs/             le guide, les règles de style, le dictionnaire
outils/           le validateur, qu'on peut lancer chez soi (Ruby)
SUIVI.md          généré, jamais édité à la main
```

## Remerciements

- **Zenshou** (`@xrize._`) — sa chaîne d'outils et ses réponses sont à
  l'origine de tout ce qui marche ici. Rien de ce projet n'existerait sans lui.
- **GarekMallen** — éditeur PT-BR, table d'accents confirmée par recoupement,
  et une interface française écrite pour nous.
- **Ryuubu** — le pack de textures haute définition, dont vient tout ce que les
  captures de cette page ont de net. Publié sur les forums PPSSPP, porté sur
  [GameBanana](https://gamebanana.com/mods/309876).
- **chenetulipe et l'équipe [P2-FR-IS-PSP](https://github.com/chenetulipe/P2-FR-IS-PSP)** —
  modèle d'organisation.
- **Atlus / SEGA** — ayants droit du jeu.

## Position juridique

Projet de fans, sans but lucratif, sans aucun lien avec Atlus ou SEGA. Aucune
donnée du jeu n'est redistribuée : uniquement un correctif, qui exige de
posséder le jeu. Le script anglais est publié en clair parce que c'est la seule
façon de traduire à plusieurs — c'est un choix assumé. À la première demande
d'un ayant droit, le dépôt est retiré.

L'illustration de couverture et les captures d'écran appartiennent à
Atlus / SEGA ; elles ne sont reproduites qu'à titre d'identification du jeu.
La traduction française, elle, est publiée sous
[CC BY-NC-SA 4.0](LICENSE). Le texte anglais d'origine appartient à Atlus.
