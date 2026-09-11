#!/usr/bin/env python3
"""Recompte l'avancement et reecrit SUIVI.md.

    python outils/stats.py                      depuis la racine du depot public
    python outils/stats.py --racine <chemin>
    python outils/stats.py --reservations pr.json

Personne ne met le suivi a jour a la main : c'est la seule facon qu'il soit
juste. L'action `suivi.yml` lance ce script apres chaque fusion et committe le
resultat.

Avec --reservations, un JSON produit par `gh pr list --json number,title,author,
headRefName,files` alimente le tableau « qui est sur quoi », pour que deux
personnes ne prennent pas le meme fichier.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

LARGEUR_BARRE = 24

# Les sections du suivi, dans l'ordre d'affichage. Le total attendu sert a
# montrer ce qui reste ferme : annoncer « 0 / 17 408 » pour les negociations
# est plus honnete que de les taire.
SECTIONS = [
    ("Dialogues", "trad/dialogues", None),
    ("EBOOT", "trad/eboot", 5771),
    ("Donjons", "trad/donjons", 204),
    ("Négociations", "trad/negociations", 17408),
]


def barre(fait, total):
    if total <= 0:
        return "░" * LARGEUR_BARRE
    plein = round(LARGEUR_BARRE * fait / total)
    return "█" * plein + "░" * (LARGEUR_BARRE - plein)


def compter(dossier: Path):
    """Rend (par fichier, total, traduits). Les fichiers en _ sont techniques."""
    par_fichier = []
    total = traduits = 0

    for chemin in sorted(dossier.glob("*.json")) if dossier.is_dir() else []:
        if chemin.name.startswith("_"):
            continue
        try:
            entrees = json.loads(chemin.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as e:
            print(f"  {chemin.name} illisible : {e}", file=sys.stderr)
            continue
        n = len(entrees)
        f = sum(1 for e in entrees if e.get("fr"))
        par_fichier.append((chemin.name, n, f))
        total += n
        traduits += f

    return par_fichier, total, traduits


def lire_reservations(chemin: Path):
    """{ nom de fichier => 'auteur (#numero)' } a partir de la sortie de gh."""
    reserve = {}
    try:
        for pr in json.loads(chemin.read_text(encoding="utf-8")):
            qui = nettoyer(pr.get("author", {}).get("login", "?"))
            marque = f"@{qui} (#{int(pr['number'])})"
            for f in pr.get("files", []):
                reserve[Path(f["path"]).name] = marque
    except (json.JSONDecodeError, OSError, KeyError, TypeError, ValueError) as e:
        print(f"  reservations ignorees : {e}", file=sys.stderr)
    return reserve


def valider(racine: Path, sous_dossier: str):
    """Lance le validateur et rend { chemin => (erreurs, avertissements) }.

    Sans cette passe, le suivi ne mesure que la QUANTITE de lignes remplies :
    un fichier « termine » avec cinq erreurs y ressemble trait pour trait a un
    fichier impeccable, et personne ne sait quoi reprendre. Le validateur est
    en Ruby ; s'il n'est pas installe, on s'en passe plutot que d'echouer.

    La cle est le chemin `trad/<zone>/<fichier>`, pas le seul nom de fichier :
    depuis que plusieurs zones sont ouvertes, c'est lui qui dit vers laquelle
    pointer, et deux zones ont le droit de nommer un fichier pareil.
    """
    dossier = racine / sous_dossier
    outil = racine / "outils" / "check_trad.rb"
    fichiers = sorted(p for p in dossier.glob("*.json") if not p.name.startswith("_"))
    if not outil.exists() or not fichiers or shutil.which("ruby") is None:
        return {}

    try:
        r = subprocess.run(
            ["ruby", str(outil), "--json", *[str(p) for p in fichiers]],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=300,
        )
        rapport = json.loads(r.stdout.strip().splitlines()[-1])
    except (OSError, ValueError, IndexError, subprocess.SubprocessError) as e:
        print(f"  validation ignoree : {e}", file=sys.stderr)
        return {}

    return {f"{sous_dossier}/{e['fichier']}": e for e in rapport}


def compte(entree):
    """(erreurs, avertissements) d'une entree du rapport de validation."""
    if not entree:
        return (0, 0)
    return (len(entree["soucis"]), len(entree["avertissements"]))


def rapport_markdown(sante, depot, plafond=250):
    """Corps de l'issue « Lignes a corriger ».

    Le compte seul ne suffit pas : quelqu'un qui veut aider doit pouvoir
    cliquer sur la ligne fautive. On ecrit donc chaque souci avec un lien
    permanent vers sa ligne dans le fichier.
    """
    fautifs = sorted((f, e) for f, e in sante.items() if e["soucis"])
    total = sum(len(e["soucis"]) for _, e in fautifs)

    lignes = [
        f"**{total} erreur{'s' if total > 1 else ''}** dans "
        f"{len(fautifs)} fichier{'s' if len(fautifs) > 1 else ''}.",
        "",
        "Cette issue est **tenue à jour automatiquement** : elle se réécrit à "
        "chaque contribution et se ferme toute seule quand il ne reste rien. "
        "Inutile de la commenter pour signaler une correction — corrige le "
        "fichier, elle suivra.",
        "",
        "Une erreur laissée en place fait rester la ligne **en anglais** dans le "
        "jeu. La réparer vaut donc mieux que traduire un fichier de plus.",
        "",
    ]

    écrites = 0
    for chemin, entree in fautifs:
        lignes += [f"### `{chemin}`", ""]
        for s in entree["soucis"]:
            if écrites >= plafond:
                break
            lien = f"{depot}/blob/main/{chemin}#L{s['ligne']}"
            # Le message commence par l'identifiant : on ne le repete pas, on
            # le transforme en lien vers la ligne.
            texte = s["message"][len(s["id"]) :].strip()
            lignes.append(f"- [`{s['id']}`]({lien}) {texte}")
            écrites += 1
        lignes.append("")
        if écrites >= plafond:
            lignes.append(f"*…et {total - écrites} autre(s), non listées ici.*")
            break

    return "\n".join(lignes) + "\n"


def mention(sante):
    """« 5 à vérifier », « 2 termes »… selon ce que le fichier a vraiment.

    « à relire » sur un dépassement de budget envoyait relire un français qui
    n'avait rien à se reprocher : c'est l'écran qu'il faut regarder, pas le
    texte. On nomme donc la nature de l'avertissement, et on prend la plus
    urgente quand il y en a plusieurs.
    """
    if not sante:
        return ""
    tags = [etiquette(a) for a in sante["avertissements"]]
    if not tags:
        return ""
    for tag, mot in (("OCTETS", "à alléger"), ("TERMINO", "terme"),
                     ("LARGEUR", "trop large"), ("BUDGET", "à vérifier")):
        n = tags.count(tag)
        if not n:
            continue
        if tag == "TERMINO":
            return f"{n} terme{'s' if n > 1 else ''}"
        return f"{n} {mot}"
    # Nature inconnue : on le dit quand meme plutot que de rendre "".
    return f"{len(tags)} à relire"


def etat(n, f, reserve, sante=None):
    erreurs, _ = compte(sante)

    # Une erreur passe devant tout le reste : c'est la seule chose qui demande
    # une action precise, sur une ligne precise.
    if erreurs:
        quoi = "erreur" if erreurs == 1 else "erreurs"
        return f"**à corriger** — {erreurs} {quoi}"

    note = mention(sante)
    if f == 0:
        return f"en cours par {reserve}" if reserve else "libre"
    if f == n:
        return f"terminé · {note}" if note else "terminé"
    suite = f"en cours par {reserve}" if reserve else "commencé"
    return f"{suite} · {note}" if note else suite


def milliers(n):
    """8572 -> « 8 572 ». Espace insecable : le nombre ne se coupe pas en fin de ligne."""
    return f"{n:,}".replace(",", " ")


def nettoyer(texte):
    """Un pseudo GitHub arrive d'une proposition exterieure et finit dans un
    tableau Markdown : on ne laisse passer que ce qu'un pseudo peut contenir."""
    return "".join(c for c in str(texte) if c.isalnum() or c in "-_[]#@() ")[:48]


# Chaque nature d'avertissement demande une action differente : les melanger
# sous un titre unique fait mentir le suivi. L'ordre est celui de l'urgence.
CATEGORIES = {
    "OCTETS": (
        "Poids à surveiller",
        "Ces entrées alourdissent leur fichier. Un bloc qui franchit sa frontière "
        "fait rester **tout le fichier en anglais** dans le jeu, sans erreur au "
        "build : c'est le plus sournois des avertissements.",
        "entrée",
    ),
    "TERMINO": (
        "À relire",
        "Terminologie à confirmer — un terme du dictionnaire apparaît dans "
        "l'anglais sans sa traduction officielle dans le français. Ce n'est "
        "pas forcément une faute, mais ça mérite un avis.",
        "terme",
    ),
    "LARGEUR": (
        "Largeur à surveiller",
        "Ces lignes sont plus larges que l'anglaise et approchent de la limite de "
        "la boîte. Elles ne débordent pas à coup sûr, mais un `{SAUT}` de plus "
        "serait plus sage.",
        "ligne",
    ),
    "BUDGET": (
        "À vérifier en jeu",
        "Ces lignes dépassent la place que l'anglais occupe dans l'exécutable. Le "
        "moteur les redirige vers un espace libre et ça marche — « Charger une "
        "partie » le fait déjà — mais c'est plus fragile que de tenir dans le "
        "budget. Un coup d'œil à l'écran suffit à confirmer.",
        "ligne",
    ),
    # Repli obligatoire : sans lui, un avertissement d'une nature que le
    # validateur apprendrait demain disparaitrait du suivi sans bruit — le
    # defaut meme qu'on est en train de corriger.
    "AUTRE": (
        "Autres avertissements",
        "Le validateur signale ces lignes sans que le suivi sache encore les "
        "classer. À regarder dans sa sortie : `ruby outils/check_trad.rb <fichier>`.",
        "ligne",
    ),
}

ETIQUETTE = re.compile(r"\[([A-Z]+)\]")


def etiquette(avertissement):
    """« BUDGET », « TERMINO »… ou « AUTRE » si le message n'en porte pas."""
    m = ETIQUETTE.search(avertissement.get("message", ""))
    return m.group(1) if m else "AUTRE"


def grouper_avertissements(sante):
    """{ categorie => [(chemin, nombre), ...] }, trie par chemin.

    Un meme fichier peut apparaitre dans plusieurs categories : un fichier qui
    depasse son budget ET dont un terme manque a deux choses a reprendre, pas
    une. On ne compte donc pas les fichiers mais les avertissements.
    """
    groupes = {}
    for chemin, entree in sante.items():
        if entree["soucis"]:
            continue  # deja liste sous « À corriger », le plus urgent d'abord
        compte_par_tag = {}
        for a in entree["avertissements"]:
            tag = etiquette(a)
            compte_par_tag[tag] = compte_par_tag.get(tag, 0) + 1
        for tag, n in compte_par_tag.items():
            groupes.setdefault(tag, []).append((chemin, n))
    for liste in groupes.values():
        liste.sort()
    return groupes


def rendre(sections, reservations, sante):
    lignes = [
        "# Avancement de la traduction",
        "",
        "> Fichier **généré**. Ne pas le modifier à la main : chaque fusion l'écrase.",
        "",
        "```text",
    ]

    a_corriger = sorted(f for f, e in sante.items() if e["soucis"])
    par_categorie = grouper_avertissements(sante)

    for nom, _, par_fichier, total, traduits in sections:
        # Une section fermee affichee « 0 % » donne l'impression d'un projet a
        # l'abandon, alors qu'elle n'est simplement pas encore ouverte. On dit
        # laquelle, et son volume, sans la compter comme un retard.
        if not par_fichier:
            lignes.append(f"{nom:<14} pas encore ouvert — environ {milliers(total)} textes")
            continue
        pct = round(100 * traduits / total) if total else 0
        lignes.append(
            f"{nom:<14} {barre(traduits, total)}  {pct:>3} %   " f"{milliers(traduits):>6} / {milliers(total)} textes"
        )

    lignes += ["```", ""]

    # Ce qui demande une action passe avant l'inventaire : quelqu'un qui vient
    # aider doit voir en premier ce qui est casse, pas defiler cent lignes.
    if a_corriger:
        lignes += [
            "## ⚠ À corriger",
            "",
            "Ces fichiers contiennent des erreurs de validation. Les corriger vaut "
            "mieux que d'en traduire un nouveau : une erreur laissée là fera rester "
            "la ligne en anglais dans le jeu.",
            "",
        ]
        for f in a_corriger:
            n = len(sante[f]["soucis"])
            lignes.append(f"- [`{Path(f).name}`]({f}) — {n} erreur{'s' if n > 1 else ''}")
        lignes += [
            "",
            "**Le détail ligne par ligne est dans "
            "[l'issue « Lignes à corriger »](../../issues?q=is%3Aissue+is%3Aopen+label%3Asuivi-auto)**, "
            "tenue à jour automatiquement. Il s'affiche aussi tout seul sur les "
            "lignes de ta proposition.",
            "",
        ]

    # Un avertissement de budget n'est pas une question de terminologie : les
    # confondre sous un seul titre envoyait relire un vocabulaire qui n'avait
    # rien à se reprocher. Une section par nature, avec le mot juste.
    for tag, (titre, explication, unite) in CATEGORIES.items():
        fichiers = par_categorie.get(tag)
        if not fichiers:
            continue
        lignes += [f"## {titre}", "", explication, ""]
        for f, n in fichiers:
            lignes.append(f"- [`{Path(f).name}`]({f}) — {n} {unite}{'s' if n > 1 else ''}")
        lignes.append("")

    for nom, sous_dossier, par_fichier, _total, _traduits in sections:
        if not par_fichier:
            continue
        lignes += [
            f"## {nom}",
            "",
            "Prends un fichier **libre**, dis-le en ouvrant ta proposition, et il "
            "passera en « en cours » dans la minute.",
            "",
            "| Fichier | Textes | Traduits | % | État |",
            "|---|---:|---:|---:|---|",
        ]
        for fichier, n, f in par_fichier:
            pct = round(100 * f / n) if n else 0
            lignes.append(
                f"| [`{fichier}`]({sous_dossier}/{fichier}) | {n} | {f} | {pct} % | "
                f"{etat(n, f, reservations.get(fichier), sante.get(f'{sous_dossier}/{fichier}'))} |"
            )
        lignes.append("")

    return "\n".join(lignes) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--racine", default=".", type=Path)
    ap.add_argument("--reservations", type=Path)
    ap.add_argument("--sortie", type=Path, help="defaut : <racine>/SUIVI.md")
    ap.add_argument(
        "--sans-valider", action="store_true", help="ne pas lancer check_trad.rb (plus rapide, etats moins precis)"
    )
    ap.add_argument("--rapport", type=Path, help="ou ecrire le detail des erreurs (corps de l'issue de suivi)")
    ap.add_argument("--depot", default="", help="URL du depot, pour les liens du rapport")
    args = ap.parse_args(argv)

    racine = args.racine
    reservations = lire_reservations(args.reservations) if args.reservations else {}

    sections = []
    for nom, sous_dossier, attendu in SECTIONS:
        par_fichier, total, traduits = compter(racine / sous_dossier)
        if total == 0 and attendu:
            total = attendu  # section pas encore ouverte : montrer la dette
        if total == 0:
            continue
        sections.append((nom, sous_dossier, par_fichier, total, traduits))

    if not sections:
        print("aucun fichier de traduction trouve", file=sys.stderr)
        return 1

    # TOUTES les zones ouvertes, pas seulement la premiere. Une zone listee au
    # suivi mais jamais relue afficherait « termine » sur un fichier casse, et
    # c'est justement l'EBOOT -- avec son budget par ligne, dont le depassement
    # laisse la ligne en anglais sans erreur au build -- qui en a le plus besoin.
    sante = {}
    if not args.sans_valider:
        for _nom, sous_dossier, par_fichier, _total, _traduits in sections:
            if par_fichier:
                sante.update(valider(racine, sous_dossier))

    sortie = args.sortie or racine / "SUIVI.md"
    sortie.write_text(rendre(sections, reservations, sante), encoding="utf-8")

    # Le badge du README : format « endpoint » de shields.io.
    principal = sections[0]
    pct = round(100 * principal[4] / principal[3]) if principal[3] else 0
    badge = {
        "schemaVersion": 1,
        "label": "traduction",
        "message": f"{pct} %",
        "color": "brightgreen" if pct >= 80 else "orange" if pct >= 20 else "red",
    }
    chemin_badge = racine / ".github" / "badge.json"
    chemin_badge.parent.mkdir(parents=True, exist_ok=True)
    chemin_badge.write_text(json.dumps(badge, indent=2) + "\n", encoding="utf-8")

    for nom, _, _, total, traduits in sections:
        print(f"  {nom:<14} {traduits} / {total}")

    casses = sum(1 for e in sante.values() if e["soucis"])
    if casses:
        print(f"  {casses} fichier(s) a corriger")

    # Le rapport détaillé va hors du dépôt : c'est le corps d'une issue, pas un
    # fichier à versionner. Vide quand tout est sain — l'action ferme alors
    # l'issue au lieu de la réécrire.
    if args.rapport:
        corps = rapport_markdown(sante, args.depot) if casses else ""
        args.rapport.write_text(corps, encoding="utf-8")

    print(f"  -> {sortie}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
