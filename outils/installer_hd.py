#!/usr/bin/env python3
"""Installe le pack HD de Ryuubu/PPSSPP en gardant nos textures francaises.

    python game/tools/installer_hd.py --source <dossier "HD UI"> [--textures <dossier PPSSPP>]

Le pack HD remplace 574 textures, dont les trois atlas de police et quatre
ecrans que nous avons deja traduits. PPSSPP ne lit qu'un seul textures.ini par
jeu : il faut donc fusionner, pas juxtaposer.

Deux details rendent la fusion possible :

  - Leur ini utilise `hash = xxh64` avec `reduceHash`, le notre `hash = quick`.
    L'algorithme est GLOBAL au jeu : nos empreintes deviennent invalides. Mais
    le segment central de l'empreinte est le meme dans les deux -- c'est par lui
    qu'on apparie, et on reprend ensuite LEUR empreinte pour designer NOS
    fichiers.
  - Leurs atlas sont nos atlas en x5 exactement, meme grille de 16 colonnes.

Ce que le script fait : copie leur pack, puis repointe les entrees qui nous
concernent vers nos fichiers francais. Ce qui n'est pas encore traduit en HD
reste donc en francais basse resolution plutot que de repasser en anglais HD.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

# segment central de notre empreinte -> notre fichier francais
#
# `19881115` (les phases de lune) n'y est PLUS, et c'est voulu. Cette texture
# ne porte que les icones ; leur version HD est meilleure que la notre et n'a
# aucun texte a traduire. Les libelles (NEW / FULL MOON / HALF) vivent dans une
# texture SEPAREE, `UI/MoonStatus.png` -- que nous n'avions jamais touchee : le
# bas de notre phases_lune_fr.png etait du travail invisible, le jeu n'en
# affichait rien. C'est elle qu'il faut traduire.
NOS = {
    "8327c4ac": "police_menu.png",
    "8327c5ac": "police_dlg_p0.png",
    "2b4f00c4": "police_dlg_p1.png",
    "ada68967": "press_any_button_fr.png",
    "2b4f0ecb": "menu_titre_fr.png",
    "4455fdfd": "mise_en_garde_fr.png",
    "2b4f0bc4": "phases_lune_texte_fr.png",  # MoonStatus, a produire
}

LIGNE = re.compile(r"^\s*([0-9a-f]{16,32})\s*=\s*(\S.*?)\s*$")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source", required=True, type=Path, help='le dossier "HD UI" decompresse')
    ap.add_argument(
        "--textures",
        type=Path,
        default=Path.home() / "Documents" / "PPSSPP" / "PSP" / "TEXTURES" / "ULUS10432",
    )
    ap.add_argument("--simuler", action="store_true", help="ne rien copier, seulement dire")
    ap.add_argument(
        "--anglais",
        action="store_true",
        help="laisser le pack HD en anglais : sert a photographier l'avant/apres "
        "dans des conditions IDENTIQUES, seule la langue changeant",
    )
    args = ap.parse_args(argv)

    src, dst = args.source, args.textures
    if not (src / "textures.ini").exists():
        print(f"  {src}/textures.ini introuvable", file=sys.stderr)
        return 1

    ini = (src / "textures.ini").read_text(encoding="utf-8", errors="replace")

    # Repointage : on garde LEUR empreinte, on change le fichier vise.
    #
    # Un fichier francais absent laisse l'entree HD intacte. Repointer vers le
    # vide afficherait un trou a la place de la texture -- pire que de l'anglais
    # en HD, et sans rien pour le signaler.
    remplaces, sorties, pas_prets = [], [], []
    for ligne in ini.splitlines():
        m = LIGNE.match(ligne)
        if m:
            empreinte, cible = m.groups()
            notre = None if args.anglais else next((f for seg, f in NOS.items() if seg in empreinte), None)
            if notre:
                if (dst / notre).exists() or (Path.cwd() / notre).exists():
                    sorties.append(f"{empreinte} = {notre}")
                    remplaces.append((cible, notre))
                    continue
                pas_prets.append((cible, notre))
        sorties.append(ligne)

    if args.anglais:
        print("  mode ANGLAIS : le pack HD reste intact, aucun fichier francais utilise.")
        print("  Sert a photographier l'avant/apres a conditions egales — repasser")
        print("  au francais en relancant ce script SANS --anglais.")
    else:
        print(f"  {len(remplaces)} texture(s) repointee(s) vers nos fichiers francais :")
        for leur, notre in remplaces:
            print(f"    {leur:<28} -> {notre}")

        for leur, notre in pas_prets:
            print(f"    {leur:<28} reste en anglais HD : {notre} n'existe pas encore")

        vises = {n for _, n in remplaces} | {n for _, n in pas_prets}
        for f in sorted(set(NOS.values()) - vises):
            print(f"    ATTENTION : {f} n'a trouve aucune entree dans leur ini", file=sys.stderr)

    if args.simuler:
        print("\n  (simulation, rien n'a ete ecrit)")
        return 0

    dst.mkdir(parents=True, exist_ok=True)

    # Nos fichiers francais doivent survivre a la copie : on les met de cote.
    a_garder = {}
    for f in set(NOS.values()) | {"mappings_images.txt"}:
        p = dst / f
        if p.exists():
            a_garder[f] = p.read_bytes()

    copies = 0
    for p in sorted(src.rglob("*")):
        if p.is_file() and p.name != "textures.ini":
            cible = dst / p.relative_to(src)
            cible.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, cible)
            copies += 1

    for f, contenu in a_garder.items():
        (dst / f).write_bytes(contenu)

    (dst / "textures.ini").write_text("\n".join(sorties) + "\n", encoding="utf-8")

    print(f"\n  {copies} textures HD copiees, {len(a_garder)} fichiers francais preserves")
    print(f"  -> {dst}")
    print("\n  Dans PPSSPP : Graphismes > Textures > Remplacement de textures = ON,")
    print("  et Enregistrement des nouvelles textures = OFF. Fenetre fermee.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
