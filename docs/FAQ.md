# Questions fréquentes

## Sur la contribution

**Je ne sais pas coder. Je peux quand même aider ?**
Oui, et c'est le but. Tu remplis un champ dans une page web et tu cliques sur un
bouton vert. Aucune ligne de code, aucun logiciel.

**Il me faut le jeu ?**
Non. Le texte anglais est dans les fichiers, tu traduis en le lisant. Avoir joué
aide pour le contexte, mais ce n'est pas obligatoire — et si tu bloques sur une
scène, demande dans ta proposition.

**Combien de temps prend un fichier ?**
Une centaine de répliques, soit deux à quatre heures selon la densité. Tu n'es
pas obligé de le finir d'un coup : propose ce que tu as, indique que c'est en
cours, complète ensuite.

**Est-ce que je peux réserver plusieurs fichiers ?**
Prends-en un. Quand il est fusionné, prends le suivant. Un fichier réservé
depuis trois semaines et jamais rendu bloque tout le monde.

**Quelqu'un travaille déjà sur mon fichier ?**
[SUIVI.md](../SUIVI.md) indique qui est sur quoi, à partir des propositions
ouvertes. Il est recalculé automatiquement.

---

## Sur les refus du robot

**`[STRUCTURE] codes attendus [...], obtenus [...]`**
Un code entre accolades a été perdu, ajouté ou déplacé. Compare ta ligne à
l'anglais : ta traduction doit contenir exactement les mêmes, dans le même
ordre. Le plus fréquent : un `{SAUT}` oublié en reformulant.

**`[LARGEUR] 47 car. (debordement certain)`**
Une ligne dépasse la boîte de dialogue. Coupe-la avec un `{SAUT}` ou raccourcis.
La mesure porte sur le texte **entre deux codes**, pas sur la réplique entière.

**`[ENCODAGE] X absent(s) de la table`**
Un caractère n'existe pas dans le jeu. Neuf fois sur dix, c'est un guillemet ou
une apostrophe recopiés depuis Word ou un site web. Retape-les.

**`[GLYPHE] X sans dessin dans la police`**
Le caractère existe dans le jeu mais sa case est vide : il s'afficherait comme
un blanc. Remplace-le.

**`[CANARI] l'anglais d'origine a été modifié`**
Tu as tapé dans `en` ou `locuteur` au lieu de `fr` ou `locuteur_fr`. Restaure
le champ tel qu'il était. Si tu ne sais plus, l'onglet **Files changed** de ta
proposition montre exactement ce qui a bougé.

**Le robot refuse une ligne que je trouve correcte.**
Ça arrive. Dis-le dans ta proposition ; si l'outil a tort, on le corrige. Il
n'est pas sacré, il est juste plus rapide que nous.

---

## Sur le jeu

**Pourquoi les accents ont-ils été un problème ?**
Le jeu américain n'a pas de glyphes accentués : les cases correspondantes de sa
police sont vides. Il a fallu les dessiner, un par un, dans les atlas de
textures, puis régler leurs métriques. C'est fait — vingt-cinq caractères,
validés en jeu. C'est aussi pour ça qu'on ne les brade pas : écris un vrai
français.

**Pourquoi certaines choses ne sont-elles pas ouvertes à la traduction ?**
Les négociations avec les démons représentent 17 400 lignes, mais l'extracteur
en perd 535. Traduire sur une source trouée, c'est du travail à refaire. Pareil
pour les objets et les sorts, dont on n'a pas encore cartographié les zones
dans l'exécutable. Ça viendra.

**Comment je teste ma traduction en jeu ?**
Tu n'as pas à le faire. Les mainteneurs réinjectent et publient un correctif de
temps en temps. Si tu veux y jouer : il faut posséder le jeu, appliquer le
`.xdelta` sur l'ISO américaine, et activer le remplacement de textures dans
PPSSPP pour les accents.

**Vous distribuez le jeu ?**
Non, jamais. Uniquement un correctif, qui ne sert à rien sans une copie légale.

---

## Sur le projet

**C'est légal ?**
C'est une zone grise, comme toute traduction amateur. Le projet est non
lucratif, ne redistribue aucune donnée du jeu, et sera retiré à la première
demande d'un ayant droit. Atlus et SEGA restent propriétaires du jeu et du
texte anglais.

**Pourquoi le script anglais est-il publié ?**
Parce que c'est la seule façon de traduire à plusieurs sans que chacun
installe une chaîne d'outils complète. C'est la pratique du milieu, et c'est un
choix assumé.

**Qui est derrière ?**
Un projet de fans francophones. La chaîne technique repose largement sur le
travail de **Zenshou**, qui l'a partagée, et de **GarekMallen**. Ils sont
crédités dans le README, et ils le méritent : sans eux, rien de tout ceci
n'existerait.
