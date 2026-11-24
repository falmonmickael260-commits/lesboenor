"""14 manches variées pour l'édition du 24 novembre 2026.
Chaque réponse provient d'un tableau de sondage réellement publié et conserve
son pourcentage d'origine. La formulation affichée tient en un seul mot.
Certaines études sont anciennes : l'année et le public interrogé sont indiqués
dans la source. Le classement n'est PAS présenté comme une tendance actuelle.

Le panneau de régie reste la solution pour accepter une formulation voisine
qui n'est pas reconnue automatiquement.
"""
BANK_VERSION = "2026-11-24-v5"

def board(question, source, rows):
    if len(rows) != 6:
        raise ValueError("Six réponses exactement par manche")
    if len(set(label.casefold() for label, _, _ in rows)) != 6:
        raise ValueError("Les six réponses doivent être différentes")
    if any(len(label.split()) != 1 for label, _, _ in rows):
        raise ValueError("Réponses en un mot")
    if any(type(points) is not int or not 1 <= points <= 100 for _,points,_ in rows):
        raise ValueError("Les points doivent être des pourcentages")
    if any(rows[i][1] < rows[i+1][1] for i in range(5)):
        raise ValueError("Classement décroissant obligatoire")
    return dict(question=question,source=source,rows=rows)

lecture_2025 = (
    "Ipsos / Centre national du livre · janvier 2025 · 1 001 personnes · p. 34, 48, 70",
    "https://www.ipsos.com/sites/default/files/ct/news/documents/2025-04/ipsos-cnl-francais-lecture-2025-rapport-complet.pdf"
)
sorties_2024 = (
    "Ipsos pour Maxi · janvier 2024 · femmes interrogées · p. 22",
    "https://www.ipsos.com/sites/default/files/ct/news/documents/2024-02/Ipsos-Maxi-ce-que-veulent-vraiment-les-francaises-janvier-2024-web.pdf"
)
alimentation_1989 = (
    "Ipsos · habitudes alimentaires · 1989 · 1 000 adultes",
    "https://www.ipsos.com/fr-fr/les-habitudes-alimentaires-des-francais"
)
voisinage_2000 = (
    "CSA pour Zurban · 2000 · 500 adultes parisiens · sous-total souvent/de temps en temps",
    "https://www.ipsos.com/fr-fr/les-relations-de-voisinage"
)
dimanche_1999 = (
    "Sofres pour Pèlerin · décembre 1999 · 1 000 adultes · sans les visites aux proches",
    "https://www.ipsos.com/fr-fr/la-perception-de-la-journee-du-dimanche"
)
loisirs_1987 = (
    "Ipsos · temps libre et loisirs · janvier 1987 · 300 foyers",
    "https://www.ipsos.com/fr-fr/temps-libre-sport-et-loisirs"
)
jeunes_1990 = (
    "Ipsos · goûts des jeunes · juillet 1990 · modes de transport, question 25",
    "https://www.ipsos.com/fr-fr/les-gouts-des-jeunes"
)

six_boards = [
    board("Quand on a du temps libre, que fait-on le plus souvent ?", lecture_2025, [
        ("Musique", 91, "ecouter de la musique|écouter musique|chansons|chanson"),
        ("Messages", 88, "appels|appel|telephone|téléphone|sms|whatsapp|messenger|discuter a distance|contacter des proches"),
        ("Sorties", 81, "sortie|amis|sortir avec des amis|sortir"),
        ("Internet", 80, "web|surfer sur internet|navigation internet|naviguer"),
        ("Séries", 72, "serie|series|streaming|netflix|films|film|plateformes"),
        ("Télévision", 70, "tele|télé|tv|televiseur|regarder la tele"),
    ]),
    board("Quelles cuisines du monde sont appréciées ?", alimentation_1989, [
        ("Italienne", 66, "italien|italie|cuisine italienne"),
        ("Marocaine", 51, "marocain|maroc|cuisine marocaine"),
        ("Chinoise", 35, "chinois|chine|cuisine chinoise"),
        ("Vietnamienne", 32, "vietnamien|vietnam|cuisine vietnamienne"),
        ("Grecque", 20, "grec|grece|grèce|cuisine grecque"),
        ("Indienne", 17, "indien|inde|cuisine indienne"),
    ]),
    board("Quels aliments ou boissons cherche-t-on parfois à limiter ?", alimentation_1989, [
        ("Sauce", 44, "sauces|plats en sauce|plat en sauce"),
        ("Vin", 43, "vins|alcool de raisin"),
        ("Sucre", 42, "sucres|produits sucres|sucré"),
        ("Conserves", 28, "conserve|boites de conserve|boîtes"),
        ("Beurre", 28, "matiere grasse|beurres"),
        ("Frites", 27, "frite|friture|pommes frites"),
    ]),
    board("Quelles choses fait-on parfois avec ses voisins ?", voisinage_2000, [
        ("Discuter", 60, "parler|conversation|papoter|discuter sur le palier|bavarder"),
        ("Dépanner", 27, "depanner|prêter|preter|emprunter|du sucre|echanger des produits"),
        ("Arroser", 16, "arroser plantes|plantes|garder animaux|animaux|surveiller animaux"),
        ("Apéro", 16, "apero|apéro|aperitif|apéritif|boire un verre"),
        ("Dîner", 10, "diner|manger|repas|dejeuner chez les voisins"),
        ("Enfants", 9, "garder les enfants|garde enfants|baby sitting|baby-sitting"),
    ]),
    board("Quelles sorties font le plus plaisir aux femmes interrogées ?", sorties_2024, [
        ("Restaurant", 58, "resto|aller au restaurant|restaurant"),
        ("Balade", 58, "promenade|se promener|marcher|promener|balades"),
        ("Shopping", 31, "magasins|boutiques|courses en ville|faire les boutiques"),
        ("Cinéma", 27, "cinema|cine|ciné|film en salle"),
        ("Sport", 26, "sport en plein air|velo|vélo|randonnée|randonnee"),
        ("Spectacle", 22, "theatre|théâtre|comedie musicale|comédie musicale|spectacles"),
    ]),
    board("Qu'est-ce qui donne envie d'acheter un livre ?", lecture_2025, [
        ("Proches", 87, "proche|ami|amis|recommandation|conseil d un ami|avis d un proche"),
        ("Résumé", 85, "resume|quatrieme de couverture|4e de couverture|synopsis"),
        ("Auteur", 84, "ecrivain|écrivain|auteur connu|auteur favori"),
        ("Libraire", 64, "libraires|conseil du libraire|vendeur en librairie"),
        ("Critique", 62, "journaliste|critique litteraire|presse|article de journal|radio"),
        ("Titre", 59, "nom du livre|titre du livre"),
    ]),
    board("Quels types de livres lit-on ?", lecture_2025, [
        ("Pratique", 52, "loisirs|livre pratique|livres pratiques|cuisine|bricolage|jardinage"),
        ("Histoire", 46, "historique|livres d histoire|livre sur l histoire"),
        ("BD", 43, "bande dessinee|bande dessinée|bandes dessinées|bd|album"),
        ("Policier", 37, "polars|polar|enquete|enquête|espionnage|thriller"),
        ("Art", 35, "beaux livres|photographie|livre d art|livre sur l art"),
        ("Science", 35, "scientifique|sciences|technique|professionnel"),
    ]),
    board("Quels moyens de transport les jeunes citaient-ils en 1990 ?", jeunes_1990, [
        ("Voiture", 49, "auto|automobile|en voiture"),
        ("Moto", 8, "motocyclette|motocycle"),
        ("Bus", 8, "autobus|en bus"),
        ("Train", 6, "sncf|tgv|en train"),
        ("Mobylette", 6, "cyclomoteur|mob|50cc"),
        ("Métro", 5, "metro|en metro|subway"),
    ]),
    board("Le dimanche, que fait-on à part rendre visite à des proches ?", dimanche_1999, [
        ("Promenade", 55, "balade|se promener|marcher|sortir marcher"),
        ("Télévision", 43, "tele|télé|tv|regarder la tele"),
        ("Cuisine", 38, "cuisiner|manger|restaurant|preparer un repas"),
        ("Jardinage", 36, "jardiner|jardin|bricoler|bricolage"),
        ("Lecture", 36, "lire|livres|musique|ecouter de la musique"),
        ("Flâner", 35, "flaner|rester chez soi|trainer a la maison|traîner|ne rien faire"),
    ]),
    board("Avec plus de temps libre, que voudrait-on faire ?", loisirs_1987, [
        ("Voyager", 42, "voyage|vacances|partir en voyage"),
        ("Sport", 21, "faire du sport|exercice|sportif"),
        ("Culture", 18, "se cultiver|apprendre|culture generale|lire pour apprendre"),
        ("Art", 12, "artistique|peinture|dessin|musique artistique"),
        ("Artisanat", 5, "manuel|travail manuel|artisan|atelier"),
        ("Technologie", 3, "technologies|informatique|technique nouvelle|nouvelles technologies"),
    ]),
    # Ipsos, octobre 1989 : préférences de destination pour les vacances d'été
    # Question 2, classement des citations, choix multiple.
    board("Dans quels endroits rêvait-on de passer ses vacances d'été en 1989 ?",
          ("Ipsos · octobre 1989 · destinations estivales, Q2, total des citations",
           "https://www.ipsos.com/fr-fr/les-vacances-dete-et-dhiver"), [
        ("États-Unis", 26, "etats unis|etats-unis|usa|amerique|amérique"),
        ("Grèce", 24, "grece|grecque|grêce"),
        ("France", 22, "francais|française"),
        ("Italie", 18, "italien|italienne"),
        ("Espagne", 16, "espagnol|espagnole"),
        ("Antilles", 12, "antille|caraibes|caraïbes"),
    ]),
    # Ipsos, avril 1987 : raisons pour lesquelles on va voir un film
    # Question 5, six premières réponses citées.
    board("Qu'est-ce qui donne envie d'aller voir un film au cinéma ?",
          ("Ipsos · avril 1987 · raisons de voir un film, Q5",
           "https://www.ipsos.com/fr-fr/le-cinema-pourquoi-y-va-t"), [
        ("Histoire", 69, "sujet|scenario|scénario|synopsis|intrigue|histoire du film"),
        ("Acteurs", 45, "acteur|actrice|vedettes|star|stars|casting"),
        ("Amis", 37, "ami|proches|bouche a oreille|conseil|conversation"),
        ("Télévision", 28, "tv|tele|télé|emission tv|émission télé|emissions tele"),
        ("Critiques", 23, "critique|presse|journaux|avis des critiques"),
        ("Récompenses", 17, "recompenses|recompense|prix|oscar|césar|cesar|palmares|palmarès"),
    ]),
    # Ipsos, octobre 1986 : instruments pratiqués par les jeunes interrogés,
    # parmi ceux qui déclaraient jouer d'un instrument, Q11.
    board("Quels instruments jouaient les jeunes interrogés ?",
          ("Ipsos · octobre 1986 · musiciens parmi les jeunes interrogés, Q11",
           "https://www.ipsos.com/fr-fr/musique-ce-que-les-jeunes-ecoutent-et-pratiquent"), [
        ("Piano", 30, "pianoforte|clavier"),
        ("Flûte", 27, "flute|flute a bec|flûte traversière"),
        ("Guitare", 13, "guitares|basse|guitare basse"),
        ("Synthétiseur", 6, "synthetiseur|synthé|synthe|synthesizer"),
        ("Violon", 5, "violons"),
        ("Saxophone", 3, "saxo|saxophones"),
    ]),
    # Ipsos, nov. 1990 : inventions et évolutions techniques jugées
    # importantes sur les vingt années précédentes, Q3.
    board("En 1990, quelles innovations techniques étaient jugées importantes ?",
          ("Ipsos · novembre 1990 · inventions et technologies, Q3",
           "https://www.ipsos.com/fr-fr/les-evenements-les-plus-importants-des-20-dernieres-annees"), [
        ("Ordinateur", 64, "pc|ordinateur personnel|micro ordinateur|micro-ordinateur|ordinateur de bureau"),
        ("Minitel", 43, "3615|minitels"),
        ("Téléphone", 41, "telephone|telephones|tel|téléphones"),
        ("Micro-ondes", 35, "micro ondes|microonde|four micro ondes|four micro-ondes"),
        ("Calculatrice", 27, "calculette|calculatrice de poche|calculatrices"),
        ("Magnétoscope", 27, "magnetoscope|vhs|video|vidéo"),
    ]),

]
boards = six_boards
