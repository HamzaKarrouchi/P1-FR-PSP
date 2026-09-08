# Contribuer à la traduction

Tu veux aider ? Il te faut un compte GitHub et rien d'autre. Pas de jeu à
installer, pas d'outil à télécharger, aucune ligne de code.

---

## En deux minutes

1. Ouvre [SUIVI.md](SUIVI.md) et prends un fichier marqué **libre**. S'il y a
   une section **« À corriger »** en haut, commence plutôt par là : réparer une
   erreur vaut mieux que traduire un fichier de plus, parce qu'une erreur
   laissée en place fait rester la ligne **en anglais** dans le jeu.
2. Clique dessus dans [`trad/`](trad/), puis sur le crayon ✏️ pour l'éditer
   directement dans ton navigateur.
3. Remplis le champ `fr` de chaque réplique. Laisse tout le reste tel quel.
4. En bas de page, choisis **Create a new branch** et propose ta modification.
5. Un robot vérifie ton travail en une minute et te dit précisément ce qui
   cloche, s'il y a lieu. Tu corriges dans la même proposition.

**Un fichier = une proposition.** Ça évite que deux personnes traduisent la
même chose.

---

## Les trois dossiers

| Dossier | Contenu | Bon pour |
|---|---|---|
| [`trad/dialogues/`](trad/dialogues/) | l'histoire, les personnages qui parlent | qui aime écrire du dialogue vivant |
| [`trad/eboot/`](trad/eboot/) | menus, écrans, noms de lieux, tutoriels | **commencer** : lignes courtes, contexte évident |
| [`trad/donjons/`](trad/donjons/) | messages de couloir, portes fermées | une soirée, c'est tout petit |

Les lignes de `trad/eboot/` portent un champ **`max`** en plus : le nombre de
caractères à ne pas dépasser. Ces textes vivent dans l'exécutable du jeu, à un
emplacement de taille fixe. **Dépasser fait rester la ligne en anglais.** Le
robot te le dit sous `[BUDGET]`, avec le compte exact.

Quand un `max` rend le français impossible — `No` fait deux caractères, « Non »
en fait trois — **dis-le dans ta proposition** au lieu d'écorcher la langue.
Ces cas-là se règlent côté moteur.

---

## Ce que tu vois

```json
{
  "id": "E0.BIN:012:0007",
  "locuteur": "Nanjo",
  "en": "You sure you ain't got the brain rot,{SAUT}Hidehiko?{ATTENTE}",
  "locuteur_fr": "",
  "fr": ""
}
```

| Champ | |
|---|---|
| `id` | l'adresse de la réplique dans le jeu — **ne jamais toucher** |
| `locuteur` | qui parle, en anglais — **ne jamais toucher** |
| `en` | la réplique d'origine — **ne jamais toucher** |
| `locuteur_fr` | le nom du personnage en français — à remplir |
| `fr` | **ta traduction** |

Certaines entrées portent un `_occurrences`. Il indique combien de fois cette
réplique revient dans le jeu — parfois plusieurs centaines. Tu ne la traduis
qu'une fois : la propagation est automatique.

---

## Les trois règles qui comptent

### 1. Garde les codes entre accolades

`{SAUT}`, `{PAGE}`, `{ATTENTE}`, `{FERME}`… ce sont les ordres du moteur :
saut de ligne, changement de page, attente d'une touche. Ta traduction doit en
contenir **exactement les mêmes, dans le même ordre** que l'anglais.

```text
en : "You sure you ain't got the brain rot,{SAUT}Hidehiko?{ATTENTE}"
fr : "T'es sûr que t'as pas le cerveau qui{SAUT}fond, Hidehiko ?{ATTENTE}"
```

Même chose pour les codes en `(*MAJUSCULES*)` et `[1A2B]` : recopie-les à
l'identique. `(*APELLIDO_HEROE*)` porte le nom que le joueur a choisi ; tu peux
le **déplacer** si le français l'exige, mais il ne disparaît pas.

### 2. Environ 40 caractères par ligne affichée

La boîte de dialogue est étroite et ne va pas à la ligne toute seule : c'est
`{SAUT}` qui décide. Compte **entre deux codes**, pas sur la phrase entière.
Au-delà de 43 caractères, le texte sort de la boîte.

Le français est 20 à 30 % plus long que l'anglais. Reformuler court fait partie
du travail : c'est souvent là que la traduction devient bonne.

### 3. Écris un vrai français

Les accents fonctionnent — `é è ê à â ù û ô î ï ç` et les majuscules
accentuées `É À Ê Î Ô Ç`. Écris-les normalement.

**En revanche le projet a sa propre typographie**, et elle n'est pas celle du
français soigné. C'est celle des lignes déjà validées en jeu :

| | On écrit | Pas |
|---|---|---|
| avant `!` et `?` | `blague!` `déjà?` | ~~`blague !`~~ |
| guillemets | `"comme ça"` | ~~`« comme ça »`~~ |
| apostrophe | `qu'une` | ~~`qu’une`~~ |
| suspension | `Héhéhé...` | ~~`Héhéhé…`~~ |

La cohérence d'un bout à l'autre du jeu vaut mieux que la perfection par
endroits, et une espace avant chaque `!` coûte de la place dans des boîtes déjà
étroites. Le détail est dans [docs/REGLES.md](docs/REGLES.md#la-typographie-du-projet).

La seule chose à recopier telle quelle, ce sont les codes entre crochets —
`[0300]`, `[1E00]`… Ce sont des caractères que l'extracteur n'a pas su nommer.
Il y en a près de 7 000 dans le jeu ; ils ne se traduisent pas, ils se
transportent.

---

## Le style

- **Tutoiement entre les personnages**, sauf Nanjo, qui vouvoie presque tout le
  monde — c'est un trait de caractère, pas une politesse.
- **Registre lycéen** pour Mark et Hidehiko : familier, vivant, jamais vulgaire.
- Colle au **sens**, pas au mot-à-mot.
- Les noms propres, Personas, sorts et lieux suivent le
  [Dictionnaire](docs/Dictionnaire.md). Il fait autorité ; si un terme y manque,
  ouvre une issue plutôt que de trancher seul.

Plus de détail dans [docs/REGLES.md](docs/REGLES.md).

---

## Si le robot refuse ta proposition

Il te dit exactement quoi corriger :

```text
❌ E0.BIN:012:0034 [LARGEUR] 47 car. (debordement certain) : "..."
❌ E0.BIN:012:0041 [STRUCTURE] codes attendus ["{SAUT}", "{ATTENTE}"], obtenus ["{ATTENTE}"]
```

| Message | Ce qui s'est passé |
|---|---|
| `[STRUCTURE]` | un code `{…}` a été perdu, ajouté ou déplacé |
| `[LARGEUR]` | une ligne dépasse la boîte de dialogue |
| `[ENCODAGE]` | un caractère n'existe pas dans le jeu (souvent un guillemet exotique collé depuis un traitement de texte) |
| `[GLYPHE]` | le caractère existe mais ne se dessine pas : il apparaîtrait blanc |
| `[BUDGET]` | une ligne de `trad/eboot/` dépasse son `max` — elle resterait en anglais |
| `[CANARI]` | l'anglais d'origine a été modifié par accident — restaure `en` et `locuteur` |

Ce n'est pas un jugement sur ta traduction. **On ne relit que le français**,
jamais la technique : le robot s'en charge.

Il existe un dernier message, en **jaune** celui-là, qui ne bloque rien :

| `[TERMINO]` | un terme du [dictionnaire](docs/Dictionnaire.md) apparaît dans l'anglais mais pas sa traduction dans le français |

C'est une question, pas un reproche. Souvent tu as raison — le français
fléchit, et reformuler vaut mieux que répéter un nom. Réponds-y en un mot dans
ta proposition et on passe à la suite.

---

## Signaler une faute vue en jeu

Ouvre une [issue](../../issues/new/choose) avec la capture d'écran et, si tu
l'as, l'identifiant de la réplique. Pas besoin de savoir la corriger.

---

## Ce que tu acceptes en contribuant

Ta traduction est publiée sous [CC BY-NC-SA 4.0](LICENSE), comme le reste du
projet. Tu figures dans les remerciements. Le projet est **amateur et non
lucratif** : personne n'est payé, et personne ne vend rien.
