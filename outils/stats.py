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
import sys
from pathlib import Path

LARGEUR_BARRE = 24

# Les sections du suivi, dans l'ordre d'affichage. Le total attendu sert a
# montrer ce qui reste ferme : annoncer « 0 / 17 408 » pour les negociations
# est plus honnete que de les taire.
SECTIONS = [
    ("Dialogues", "trad/dialogues", None),
    ("EBOOT", "trad/eboot", 5771),
    ("Negociations", "trad/negociations", 17408),
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
            qui = pr.get("author", {}).get("login", "?")
            marque = f"@{qui} (#{pr['number']})"
            for f in pr.get("files", []):
                reserve[Path(f["path"]).name] = marque
    except (json.JSONDecodeError, OSError, KeyError, TypeError) as e:
        print(f"  reservations ignorees : {e}", file=sys.stderr)
    return reserve


def etat(n, f, reserve):
    if f == 0:
        return f"en cours par {reserve}" if reserve else "libre"
    if f == n:
        return "termine"
    return f"en cours par {reserve}" if reserve else "commence"


def rendre(sections, reservations):
    lignes = [
        "# Avancement de la traduction",
        "",
        "> Fichier **genere**. Ne pas modifier a la main : chaque fusion l'ecrase.",
        "",
        "```text",
    ]

    for nom, _, _par_fichier, total, traduits in sections:
        pct = round(100 * traduits / total) if total else 0
        lignes.append(f"{nom:<14} {barre(traduits, total)}  {pct:>3} %   " f"{traduits:>6} / {total:<6} textes")

    lignes += ["```", ""]

    for nom, _, par_fichier, _total, _traduits in sections:
        if not par_fichier:
            continue
        lignes += [
            f"## {nom}",
            "",
            "| Fichier | Textes | Traduits | % | Etat |",
            "|---|---:|---:|---:|---|",
        ]
        for fichier, n, f in par_fichier:
            pct = round(100 * f / n) if n else 0
            lignes.append(f"| `{fichier}` | {n} | {f} | {pct} % | " f"{etat(n, f, reservations.get(fichier))} |")
        lignes.append("")

    return "\n".join(lignes) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--racine", default=".", type=Path)
    ap.add_argument("--reservations", type=Path)
    ap.add_argument("--sortie", type=Path, help="defaut : <racine>/SUIVI.md")
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

    sortie = args.sortie or racine / "SUIVI.md"
    sortie.write_text(rendre(sections, reservations), encoding="utf-8")

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
    print(f"  -> {sortie}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
