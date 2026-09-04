# Contribuer à la traduction

Tu veux aider ? Il te faut un compte GitHub et rien d'autre. Pas de jeu à
installer, pas d'outil à télécharger, aucune ligne de code.

---

## En deux minutes

1. Ouvre [SUIVI.md](SUIVI.md) et prends un fichier marqué **libre**. S'il y a
   une section **« À corriger »** en haut, commence plutôt par là : réparer une
   erreur vaut mieux que traduire un fichier de plus, parce qu'une erreur
   laissée en place fait rester la ligne **en anglais** dans le jeu.
2. Clique dessus dans [`trad/dialogues/`](trad/dialogues/), puis sur le crayon
   ✏️ pour l'éditer directement dans ton navigateur.
3. Remplis le champ `fr` de chaque réplique. Laisse tout le reste tel quel.
4. En bas de page, choisis **Create a new branch** et propose ta modification.
5. Un robot vérifie ton travail en une minute et te dit précisément ce qui
   cloche, s'il y a lieu. Tu corriges dans la même proposition.

**Un fichier = une proposition.** Ça évite que deux personnes traduisent la
même chose.

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
accentuées. Les guillemets français `« »`, les apostrophes, les points de
suspension aussi. **La ponctuation aussi** : `?`, `!`, `…` se tapent
normalement. Écris du français, tout simplement.

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
