#!/usr/bin/env ruby
# frozen_string_literal: true

# Validateur des fichiers de traduction JSON.
#
#   depuis le dépôt public  : ruby outils/check_trad.rb trad/dialogues/E0_004.json
#   depuis le dépôt privé   : ruby game/tools/check_trad.rb game/scripts/dialogues/E0_004.json
#
# Ne modifie rien, ne touche à aucun fichier de jeu : il lit du JSON et
# signale. Six contrôles, du plus grave au moins grave :
#
#   1. STRUCTURE — les codes de contrôle du français doivent être identiques
#      à ceux de l'anglais, en nombre et en ordre. Un code perdu, et le moteur
#      lit la suite de travers.
#   2. ENCODAGE  — chaque caractère doit exister dans la table du jeu, ET son
#      glyphe doit être réellement dessiné dans la police. Les deux, parce que
#      ce n'est pas la même chose : les accents français ont tous un code dans
#      la table, mais leur case est vide ou ne contient qu'une marque isolée
#      dans `pack/sys.bin`. Encodable ≠ affichable — c'est précisément le genre
#      de fausse assurance qui a laissé passer la troncature pendant des mois.
#   3. CANARI    — la colonne anglaise doit être identique à l'extraction.
#      Un contributeur qui écrase une lettre de l'anglais en tapant sa
#      traduction fabrique une divergence que plus rien ne rattrape : le
#      moteur cherche la ligne d'origine et ne la retrouve pas.
#   4. LARGEUR   — chaque ligne affichée doit tenir dans la boîte, jugée PAR
#      RAPPORT à la ligne anglaise correspondante. Le script original compte
#      42 lignes au-delà de 43 caractères : refuser dans l'absolu reviendrait à
#      signaler un traducteur pour une largeur qu'il n'a pas créée. Erreur donc
#      seulement si le français est à la fois plus large que l'anglais ET
#      au-delà de 43 ; avertissement entre 40 et 43.
#
# Puis trois AVERTISSEMENTS, qui ne font jamais échouer :
#
#   5. OCTETS    — ce que la traduction ajoute au fichier de données, multiplié
#      par ses occurrences. Un bloc qui franchit sa frontière de 2 048 octets
#      renvoie tout le fichier en anglais, sans erreur.
#   6. TERMINO   — un terme validé au dictionnaire qui apparaît dans l'anglais
#      devrait se retrouver dans le français. Ce n'est pas une faute : le
#      français fléchit, et reformuler est souvent le bon choix. Mais sur
#      8 572 textes et des dizaines de traducteurs, c'est le seul défaut
#      qu'aucun relecteur humain ne verra.
#   7. BUDGET    — une entrée EBOOT plus longue que son `max`. Le moteur la
#      redirige vers un code cave : ça marche, c'est prouvé en jeu, mais c'est
#      plus fragile que de tenir dans la place d'origine. Les dialogues n'ont
#      pas de `max`, ce contrôle ne s'y déclenche donc jamais.
#
# Aucune dépendance au moteur p1es : la table de caractères est lue directement
# depuis le .tbl. C'est ce qui permet de publier ce fichier tel quel dans le
# dépôt communautaire, où le moteur, lui, n'a pas sa place.

require 'json'
require 'set'
require 'digest'

AQUI = File.dirname(File.expand_path(__FILE__)) unless defined?(AQUI)

module CheckTrad
  LARGEUR_MAX = 40   # visé ; le script anglais monte à 43 en chasse étroite
  LARGEUR_DURE = 43  # au-delà, débordement certain
  SEUIL_OCTETS = 48  # au-delà, une entrée pèse assez pour faire déborder un bloc

  # Repère un code de contrôle sous ses trois formes : nom lisible {SAUT},
  # balise du moteur (*TAG*) ou code brut [1234].
  JETON = /\{[A-Z]+\}|\(\*[^*]*\*\)|\[[0-9A-Fa-f]{4}\]/

  module_function

  def jetons(texte)
    texte.to_s.scan(JETON)
  end

  def lignes_affichees(texte)
    texte.to_s.split(/\{SAUT\}|\{PAGE\}|\{ATTENTE\}|\{FERME\}|\{PAUSE\}/)
         .map { |l| l.gsub(JETON, '').strip }
         .reject(&:empty?)
  end

  # Lit la table de caractères du jeu : des lignes `XXXX=c`, hexadécimal à
  # gauche, caractère à droite. Rend { caractère => code }.
  #
  # Un même caractère peut apparaître plusieurs fois ; la première occurrence
  # gagne, comme dans le moteur.
  def charger_table(chemin)
    table = {}
    File.read(chemin, encoding: 'UTF-8').each_line do |ligne|
      ligne = ligne.chomp
      next if ligne.lstrip.empty? || ligne.lstrip.start_with?('#')

      hex, car = ligne.split('=', 2)
      next if car.nil? || car.empty?
      next unless hex.to_s.strip.length == 4

      code = Integer(hex.strip, 16) rescue next
      table[car] ||= code
    end
    table
  end

  def caracteres_hors_table(texte, tabla)
    texte.to_s.gsub(JETON, '').each_char.reject do |c|
      c == ' ' || tabla.key?(c)
    end.uniq
  end

  # Caractères encodables mais dont le glyphe n'est pas dessiné : ils
  # s'écriront dans le fichier et s'afficheront comme un blanc en jeu.
  #
  # Limité aux LETTRES à dessein. La ponctuation basse (virgule 0x0003, point
  # 0x0004…) partage ses codes avec des commandes du moteur, qui les rend par
  # un chemin à lui : sa case d'atlas est vide alors que le jeu l'affiche très
  # bien. L'inclure ne produirait que du faux positif.
  def caracteres_sans_glyphe(texte, tabla, glyphes)
    return [] if glyphes.nil?

    # Le relevé des glyphes s'arrête à 0x1FF : au-delà, on n'a pas regardé.
    # Absent de la liste ne veut donc « pas dessiné » que DANS cette plage.
    #
    # Sans cette borne, `β` (0x200) faisait échouer neuf entrées. Ce n'est même
    # pas du texte : il n'apparaît jamais ailleurs qu'accolé à
    # `(*SET_ANIM_LAYER*)`, suivi d'un `[XX]` — c'est un octet de paramètre
    # d'animation que l'extracteur a rendu comme un caractère. Le recopier
    # faisait rougir le validateur ; le retirer aurait cassé l'animation, sans
    # bruit.
    plafond = glyphes.max || 0

    texte.to_s.gsub(JETON, '').each_char.reject do |c|
      next true unless c =~ /[[:alpha:]]/

      code = tabla[c]
      code.nil? || code > plafond || glyphes.include?(code)
    end.uniq
  end

  def charger_glyphes
    chemin = File.join(AQUI, 'glyphes_disponibles.json')
    return nil unless File.exist?(chemin)

    JSON.parse(File.read(chemin))['codes'].to_set
  rescue StandardError
    nil
  end

  # --- Terminologie -------------------------------------------------------
  #
  # Sur 8 572 textes traduits par des dizaines de personnes, l'incohérence de
  # terminologie est le seul défaut qu'aucun relecteur n'attrapera : personne
  # ne se souvient qu'un autre a écrit « Chambre de Velours » trois mois plus
  # tôt. Une machine, si.
  #
  # C'est un AVERTISSEMENT, jamais un refus. Le français fléchit (« à la
  # Chambre de Velours »), et un traducteur a souvent raison de reformuler
  # plutôt que de répéter un nom. Bloquer là-dessus rendrait le validateur
  # insupportable, et un validateur qu'on contourne ne sert plus à rien.
  #
  # Seuls les termes ✅ sont contrôlés : les 🔶 sont des propositions, les
  # figer reviendrait à trancher à la place de l'équipe.
  ACCENTS_NUS = {
    'à' => 'a', 'â' => 'a', 'ä' => 'a', 'ç' => 'c', 'é' => 'e', 'è' => 'e',
    'ê' => 'e', 'ë' => 'e', 'î' => 'i', 'ï' => 'i', 'ô' => 'o', 'ö' => 'o',
    'ù' => 'u', 'û' => 'u', 'ü' => 'u', 'ÿ' => 'y', 'œ' => 'oe', 'æ' => 'ae'
  }.freeze

  def aplatir(texte)
    texte.to_s.downcase.gsub(Regexp.union(ACCENTS_NUS.keys), ACCENTS_NUS)
  end

  # Lit les tableaux « | Anglais | Français | Statut | » du dictionnaire.
  # Rend [[terme anglais, terme français]] pour les seules lignes ✅.
  def charger_dictionnaire(chemin)
    return [] unless chemin && File.exist?(chemin)

    termes = []
    File.readlines(chemin, encoding: 'UTF-8').each do |ligne|
      cases = ligne.strip.split('|').map(&:strip)
      cases.shift if cases.first.to_s.empty?
      next unless cases.length >= 3 && cases[2].include?('✅')

      en = cases[0]
      fr = cases[1].sub(/\*\(.*/, '').strip # coupe la note en italique

      # Une case qui porte encore une parenthèse est une explication, pas un
      # terme : « (nom choisi par le joueur) » ne se cherche pas dans un texte.
      next if en.empty? || fr.empty? || en.include?('(') || fr.include?('(')
      next if en.include?('/') || fr.include?('/') # alternatives, trop ambigu
      next if en.length < 3

      termes << [en, fr]
    end
    termes.uniq
  rescue StandardError
    []
  end

  def chercher_dictionnaire
    ['Dictionnaire.md',
     File.join('..', 'docs', 'Dictionnaire.md'),
     File.join('..', 'scripts', 'Dictionnaire.md')]
      .map { |r| File.expand_path(r, AQUI) }
      .find { |c| File.exist?(c) }
  end

  # Un terme est signalé quand l'anglais le contient et que le français ne
  # contient pas sa traduction. Comparaison sans accents ni casse, pour que
  # « chambre de velours » et « Chambre de Velours » se valent.
  def termes_manquants(anglais, francais, termes)
    plat_en = aplatir(anglais)
    plat_fr = aplatir(francais)

    termes.select do |en, fr|
      plat_en.match?(/\b#{Regexp.escape(aplatir(en))}\b/) &&
        !plat_fr.include?(aplatir(fr))
    end
  end

  # Empreinte d'une entrée telle qu'extraite du jeu. Douze caractères
  # hexadécimaux suffisent : on cherche l'édition accidentelle, pas la fraude.
  def empreinte(anglais, locuteur)
    Digest::SHA256.hexdigest("#{locuteur} #{anglais}")[0, 12]
  end

  # Le canari se cherche à côté du fichier vérifié, puis dans le dossier
  # parent : les fichiers de travail vivent dans `trad/dialogues/`, le canari
  # à la racine de `trad/`. Absent, on ne contrôle rien — c'est le cas des
  # brouillons locaux, qui n'ont pas à en porter un.
  def charger_canari(chemin)
    dossier = File.dirname(File.expand_path(chemin))
    [dossier, File.dirname(dossier)].each do |d|
      candidat = File.join(d, '_canari.json')
      return JSON.parse(File.read(candidat, encoding: 'UTF-8')) if File.exist?(candidat)
    end
    nil
  rescue StandardError
    nil
  end

  def verifier(chemin, tabla, glyphes, canari = nil, termes = [])
    entrees = JSON.parse(File.read(chemin, encoding: 'UTF-8'))
    soucis = []
    avertis = []
    traduites = 0

    entrees.each do |e|
      id = e['id']

      if canari
        attendue = canari[id]
        if attendue.nil?
          soucis << "#{id} [CANARI] identifiant inconnu — entrée ajoutée à la main ?"
        elsif empreinte(e['en'], e['locuteur']) != attendue
          soucis << "#{id} [CANARI] l'anglais d'origine a été modifié — restaurer 'en' et 'locuteur'"
        end
      end

      # Le nom du personnage passe par la même table que le dialogue : un
      # caractère impossible s'y voit aussi peu, et s'affiche aussi blanc.
      unless e['locuteur_fr'].to_s.empty?
        hors = caracteres_hors_table(e['locuteur_fr'], tabla)
        soucis << "#{id} [ENCODAGE] locuteur : #{hors.join(' ')} absent(s) de la table" if hors.any?

        muets = caracteres_sans_glyphe(e['locuteur_fr'], tabla, glyphes)
        soucis << "#{id} [GLYPHE] locuteur : #{muets.join(' ')} sans dessin dans la police" if muets.any?
      end

      next if e['fr'].to_s.empty?

      traduites += 1

      # `[0000]` est l'espace encodé de certaines zones EBOOT, pas une
      # structure : le nombre de mots change forcément en français.
      attendus = jetons(e['en']).reject { |j| j == '[0000]' }
      obtenus  = jetons(e['fr']).reject { |j| j == '[0000]' }
      if attendus != obtenus
        soucis << "#{id} [STRUCTURE] codes attendus #{attendus.inspect}, obtenus #{obtenus.inspect}"
      end

      hors = caracteres_hors_table(e['fr'], tabla)
      soucis << "#{id} [ENCODAGE] #{hors.join(' ')} absent(s) de la table" if hors.any?

      muets = caracteres_sans_glyphe(e['fr'], tabla, glyphes)
      soucis << "#{id} [GLYPHE] #{muets.join(' ')} sans dessin dans la police" if muets.any?

      # AVERTISSEMENT, pas erreur — et c'est une correction.
      #
      # On a longtemps cru que depasser `max` faisait garder l'anglais par le
      # moteur. Une capture du 05/09/2026 (game/images/captures_jeu/) montre
      # l'inverse : « Charger une partie », 18 caracteres pour un `max` de 17,
      # s'affiche ENTIER sur l'ecran-titre. Le moteur redirige bien la chaine
      # trop longue vers un code cave, comme game/CLAUDE.md le decrivait.
      #
      # Depasser reste plus fragile que tenir dans le budget, donc on le dit.
      # Mais bloquer sur ce motif interdisait des mots que le francais n'a pas
      # plus courts : « No » fait deux caracteres, « Non » en fait trois.
      if e['max']
        # `max` est un nombre de caractères, jetons non comptés : compter pareil.
        n = e['fr'].gsub(JETON, '').length
        if n > e['max']
          avertis << "#{id} [BUDGET] #{n} caractères pour un maximum de #{e['max']} — passe par un code cave, à vérifier en jeu"
        end
      end

      # La largeur se juge PAR RAPPORT À L'ANGLAIS. 42 lignes du script
      # original dépassent déjà 43 caractères : un traducteur fidèle y serait
      # refusé pour une largeur qu'il n'a pas créée. On ne reproche donc que ce
      # que le français ajoute — et on n'avertit qu'à partir de 40, comme
      # annoncé aux contributeurs.
      anglaises = lignes_affichees(e['en'])
      lignes_affichees(e['fr']).each_with_index do |l, i|
        origine = (anglaises[i] || anglaises.max_by(&:length) || '').length
        next unless l.length > LARGEUR_MAX

        if l.length <= origine
          # Aussi large que l'original, donc pas une régression : on le dit,
          # sans bloquer.
          avertis << "#{id} [LARGEUR] #{l.length} car., comme l'anglais (#{origine}) — deja large a l'origine"
        elsif origine > LARGEUR_DURE
          # L'anglais lui-même dépasse déjà la boîte : ce n'est donc pas une
          # ligne affichée. Ce sont les blocs de mise en scène — des centaines
          # de (*SCENE_LOAD*) et (*SET_ANIM_LAYER*) dont les espaces se
          # retrouvent dans le texte — avec une phrase courte au bout. On ne
          # peut pas être plus strict que l'original.
          avertis << "#{id} [LARGEUR] #{l.length} car. contre #{origine} en anglais — " \
                     "l'anglais deborde deja, ce n'est pas une ligne affichee"
        elsif l.length > LARGEUR_DURE
          soucis << "#{id} [LARGEUR] #{l.length} car. contre #{origine} en anglais (debordement certain) : #{l.inspect}"
        else
          avertis << "#{id} [LARGEUR] #{l.length} car. contre #{origine} en anglais — a surveiller"
        end
      end

      # BUDGET D'OCTETS. Le jeu ne cherche pas ses fichiers de données par leur
      # nom : il lit à une adresse fixe. Un `.BIN` qui grossit est réécrit
      # ailleurs, et le jeu continue de lire l'ancien — tout redevient anglais,
      # sans une erreur. Chaque caractère coûte 2 octets, et un texte répété
      # coûte autant de fois qu'il apparaît. Le nom du locuteur compte aussi :
      # il est encodé avec la réplique.
      #
      # On ne mesure pas ici la marge réelle du bloc, qu'on ignore. On signale
      # ce qui s'allonge et combien ça coûte, pour que la dérive se voie tôt
      # plutôt qu'au build.
      # Le seuil existe pour que l'avertissement reste lisible : quelques
      # octets sont absorbés par la marge du bloc, et signaler chaque +8
      # noierait les cas qui comptent vraiment — un texte d'aide recopié neuf
      # fois a fait déborder trois fichiers d'un coup.
      n = e.fetch('_occurrences', 1)
      gonfle = (e['fr'].gsub(JETON, '').length - e['en'].gsub(JETON, '').length) +
               (e['locuteur_fr'].to_s.empty? ? 0 : e['locuteur_fr'].length - e['locuteur'].to_s.length)
      cout = gonfle * 2 * n
      if cout > SEUIL_OCTETS
        avertis << "#{id} [OCTETS] +#{cout} octets (#{gonfle} car. x#{n} occurrences) — " \
                   'un bloc qui deborde renvoie tout le fichier en anglais'
      end

      termes_manquants(e['en'], e['fr'], termes).each do |en, fr|
        avertis << "#{id} [TERMINO] « #{en} » se traduit « #{fr} » (dictionnaire) — " \
                   'volontaire ? sinon aligner'
      end
    end

    [entrees.length, traduites, soucis, avertis]
  end

  # Numéro de ligne de chaque entrée dans le fichier JSON, repéré sur son `id`.
  # Les fichiers sont écrits en JSON indenté : un `id` par ligne, dans l'ordre.
  # Sert aux annotations GitHub, qui se posent alors sur la bonne ligne du diff
  # — y compris pour une proposition venue d'un fork, où le robot n'a pas le
  # droit d'écrire un commentaire.
  def lignes_des_ids(chemin)
    lignes = {}
    File.readlines(chemin, encoding: 'UTF-8').each_with_index do |ligne, i|
      m = ligne.match(/"id"\s*:\s*"?([^",]+)"?/)
      lignes[m[1]] ||= i + 1 if m
    end
    lignes
  rescue StandardError
    {}
  end

  # Format attendu par GitHub Actions. Les retours à la ligne doivent être
  # échappés, sinon l'annotation est tronquée à la première.
  def annoter(chemin, ligne, message, niveau = 'error')
    propre = message.gsub('%', '%25').gsub("\r", '%0D').gsub("\n", '%0A')
    titre = niveau == 'warning' ? 'Terminologie' : 'Traduction'
    puts "::#{niveau} file=#{chemin},line=#{ligne},title=#{titre}::#{propre}"
  end

  def main(argv)
    annotations = argv.delete('--annoter')
    # `--json` sert au suivi, qui a besoin de savoir quels fichiers sont sains.
    # Une sortie machine plutôt qu'un texte à relire : reformuler un message ne
    # doit pas casser le tableau d'avancement.
    en_json = argv.delete('--json')

    if argv.empty?
      # Le chemin réellement invoqué, et non un chemin en dur : le même fichier
      # vit sous `outils/` dans le dépôt public et sous `game/tools/` dans le
      # privé, et afficher l'autre envoie le contributeur dans le mur.
      puts "usage: ruby #{$PROGRAM_NAME} [--annoter] [--json] <fichier.json> [...]"
      return 2
    end

    tbl = [File.join(AQUI, 'persona1_psp.tbl'),
           File.join(AQUI, 'p1es', 'persona1_psp.tbl')].find { |c| File.exist?(c) }
    if tbl.nil?
      warn 'erreur : persona1_psp.tbl introuvable'
      return 2
    end

    tabla = charger_table(tbl)
    glyphes = charger_glyphes
    warn 'note : glyphes_disponibles.json absent — contrôle des glyphes ignoré' if glyphes.nil?

    termes = charger_dictionnaire(chercher_dictionnaire)
    warn 'note : Dictionnaire.md introuvable — contrôle terminologique ignoré' if termes.empty?

    total_soucis = 0
    total_avertis = 0
    rapport = []

    argv.each do |chemin|
      canari = charger_canari(chemin)
      total, traduites, soucis, avertis = verifier(chemin, tabla, glyphes, canari, termes)

      if en_json
        # Le numéro de ligne accompagne chaque souci : c'est lui qui permet au
        # suivi de pointer directement dans le fichier, sans que personne ait à
        # chercher la réplique à la main.
        ou = lignes_des_ids(chemin)
        detaille = lambda do |liste|
          liste.map do |s|
            id = s.split(' ', 2).first
            { 'id' => id, 'ligne' => ou[id] || 1, 'message' => s }
          end
        end

        rapport << { 'fichier' => File.basename(chemin), 'textes' => total,
                     'traduites' => traduites,
                     'soucis' => detaille.call(soucis),
                     'avertissements' => detaille.call(avertis) }
        total_soucis += soucis.length
        next
      end

      etat = if soucis.any?
               "❌ #{soucis.length}"
             elsif avertis.any?
               "⚠ #{avertis.length}"
             else
               '✅'
             end
      puts "#{etat}  #{chemin} — #{traduites}/#{total} traduites"
      soucis.each { |s| puts "      #{s}" }
      avertis.each { |a| puts "      #{a}" }
      total_soucis += soucis.length
      total_avertis += avertis.length

      next unless annotations && (soucis.any? || avertis.any?)

      lignes = lignes_des_ids(chemin)
      soucis.each { |s| annoter(chemin, lignes[s.split(' ', 2).first] || 1, s) }
      avertis.each { |a| annoter(chemin, lignes[a.split(' ', 2).first] || 1, a, 'warning') }
    end

    if en_json
      puts JSON.generate(rapport)
      return total_soucis.zero? ? 0 : 1
    end

    # Les avertissements ne font PAS échouer : ils demandent un avis humain, ils
    # ne constatent pas une faute.
    puts "#{total_avertis} avertissement(s) — à relire, pas bloquant" if total_avertis.positive?

    total_soucis.zero? ? 0 : 1
  end
end

exit(CheckTrad.main(ARGV)) if __FILE__ == $PROGRAM_NAME
