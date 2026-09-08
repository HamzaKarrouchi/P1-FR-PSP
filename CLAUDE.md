# Instructions pour une IA qui traduit ce dépôt

Si tu utilises Claude, ChatGPT ou un autre assistant pour t'aider, donne-lui ce
fichier. Il évite les erreurs que les modèles commettent systématiquement ici.

---

## Le contexte

*Shin Megami Tensei: Persona* (PSP, version américaine, 1996/2009). Des lycéens
japonais, un jeu qui devient réel, des démons à négocier. Traduction amateur
anglais → français.

## Les erreurs que les modèles font ici

### 1. Réécrire les codes entre accolades

`{SAUT}`, `{PAGE}`, `{ATTENTE}`, `(*SCENE_INIT*)`, `[0300]` sont des ordres
pour le moteur du jeu. Un modèle a tendance à les « nettoyer », les traduire, ou
les redistribuer harmonieusement. **Ils se recopient à l'identique, en même
nombre et même ordre.** Seuls `(*APELLIDO_HEROE*)` et `(*APODO_HEROE*)` — le
nom et le surnom choisis par le joueur — peuvent se déplacer si la syntaxe
française l'exige ; rien d'autre ne bouge.

En revanche la ponctuation s'écrit normalement : `?`, `!`, `…`, `« »`. Un
modèle entraîné sur d'anciennes consignes de ce projet pourrait proposer
`[0008]` pour un point d'interrogation — **ces codes n'existent pas** dans les
fichiers actuels.

### 2. Toucher aux champs anglais

Seuls `fr` et `locuteur_fr` se remplissent. `id`, `en`, `locuteur` sont figés,
et une empreinte les surveille : les modifier fait échouer la validation.

### 3. Traduire trop long

La ligne anglaise médiane fait **33 caractères** ; au-delà de 43, la boîte
déborde. Un modèle produit naturellement du français ample, et le français est
déjà 20 à 30 % plus long que l'anglais. Ici, la contrainte fait partie du
travail : reformule court, ou redécoupe avec `{SAUT}`.

Une consigne qui marche bien : « donne-moi trois versions de cette réplique
sous 40 caractères, registre lycéen », puis choisis toi-même.

### 4. Uniformiser le registre

Chaque personnage a une voix, décrite dans [docs/REGLES.md](docs/REGLES.md).
Nanjo vouvoie et ne contracte rien — et c'est la voix la plus présente du jeu,
1 011 répliques : une erreur de registre sur lui se voit partout. Mark parle
comme un lycéen. Un modèle lisse tout vers un français scolaire moyen — c'est
la mort d'un dialogue.

Le champ `locuteur` donne le nom **tel que le jeu l'affiche** : `Mark`,
`Brown`, `Elly`, `Ayase`, et non les patronymes.

### 5. « Corriger » la typographie

Un modèle veut mettre une espace avant `!` et `?`, des guillemets `« »` et des
points de suspension `…`, parce que c'est le bon français. **Le projet fait
l'inverse** : `blague!`, `"comme ça"`, `Héhéhé...`. C'est la convention des
lignes déjà en jeu, et la cohérence d'un bout à l'autre vaut mieux que la
perfection par endroits. Détail dans [docs/REGLES.md](docs/REGLES.md).

### 6. Inventer la terminologie

Les noms propres, Personas, sorts et lieux sont fixés dans
[docs/Dictionnaire.md](docs/Dictionnaire.md). Un modèle traduira « Velvet Room »
de trois façons différentes dans le même fichier. **Le dictionnaire fait
autorité.** Un terme absent : ouvrir une issue, ne pas trancher seul.

### 7. Ignorer le champ `max` de `trad/eboot/`

Les lignes des menus et des écrans portent un `max` : un nombre de caractères à
ne pas dépasser, parce que le texte s'écrit par-dessus l'anglais à un
emplacement de taille fixe. **Un modèle l'ignore et rend une phrase ample.**
La ligne resterait alors en anglais dans le jeu, sans erreur au build.

Donne-lui la contrainte explicitement : « traduis ceci en 30 caractères
maximum, jetons non comptés ». Et vérifie le compte toi-même — les modèles
comptent mal les caractères.

## La bonne façon de s'en servir

Un modèle est excellent pour **proposer** et pour **raccourcir** : « donne-moi
trois versions de cette réplique sous 40 caractères, registre lycéen ». Il est
mauvais pour décider seul du ton, de la terminologie, et de ce qui sonne juste
en français.

**Relis tout ce qu'il produit.** Une traduction automatique non relue se voit
immédiatement, et coûte plus de temps à réparer qu'à faire.

## Vérifier

```bash
ruby outils/check_trad.rb trad/dialogues/E0_004.json
```

Il attrape les codes perdus, les lignes trop longues, les caractères
impossibles et l'anglais abîmé. Il n'attrape pas une traduction plate : ça,
c'est ton travail.
