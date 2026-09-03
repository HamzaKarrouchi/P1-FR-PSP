# Instructions pour une IA qui traduit ce dépôt

Si tu utilises Claude, ChatGPT ou un autre assistant pour t'aider, donne-lui ce
fichier. Il évite les erreurs que les modèles commettent systématiquement ici.

---

## Le contexte

*Shin Megami Tensei: Persona* (PSP, version américaine, 1996/2009). Des lycéens
japonais, un jeu qui devient réel, des démons à négocier. Traduction amateur
anglais → français.

## Les cinq erreurs que les modèles font ici

### 1. Réécrire les codes entre accolades

`{SAUT}`, `{PAGE}`, `{ATTENTE}`, `(*PLAYER_NAME*)`, `[0008]` sont des ordres
pour le moteur du jeu. Un modèle a tendance à les « nettoyer », les traduire, ou
les redistribuer harmonieusement. **Ils se recopient à l'identique, en même
nombre et même ordre.** `(*PLAYER_NAME*)` peut se déplacer si la syntaxe
française l'exige ; rien d'autre ne bouge.

### 2. Toucher aux champs anglais

Seuls `fr` et `locuteur_fr` se remplissent. `id`, `en`, `locuteur` sont figés,
et une empreinte les surveille : les modifier fait échouer la validation.

### 3. Traduire trop long

Environ 40 caractères par ligne affichée, mesurés **entre deux codes**.
Un modèle produit naturellement du français ample. Ici, la contrainte fait
partie du travail : reformule court, ou redécoupe avec `{SAUT}`.

### 4. Uniformiser le registre

Chaque personnage a une voix, décrite dans [docs/REGLES.md](docs/REGLES.md).
Nanjo vouvoie et ne contracte rien ; Mark parle comme un lycéen. Un modèle
lisse tout vers un français scolaire moyen — c'est la mort d'un dialogue.

### 5. Inventer la terminologie

Les noms propres, Personas, sorts et lieux sont fixés dans
[docs/Dictionnaire.md](docs/Dictionnaire.md). Un modèle traduira « Velvet Room »
de trois façons différentes dans le même fichier. **Le dictionnaire fait
autorité.** Un terme absent : ouvrir une issue, ne pas trancher seul.

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
