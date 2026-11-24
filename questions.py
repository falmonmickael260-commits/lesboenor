"""Nouvelle série de 8 questions (24/11/2026).
Six TOP réponses courtes, score = pourcentage explicitement publié dans l'enquête.
Des réponses formulées plus simplement à l'oral restent acceptées via les alias.
Les questions anciennes ne sont pas réutilisées dans ce catalogue.
"""
BANK_VERSION = "2026-11-24-v2"

def board(question, source, rows):
    if len(rows) != 6 or len({r[0].lower() for r in rows}) != 6:
        raise ValueError("Chaque manche exige six réponses distinctes")
    if any(len(label.split()) != 1 for label, _, _ in rows):
        raise ValueError("Les réponses affichées doivent tenir en un mot")
    if any(type(pts) is not int or not (1 <= pts <= 100) for _, pts, _ in rows):
        raise ValueError("Chaque réponse doit avoir un pourcentage publié")
    if any(rows[i][1] < rows[i + 1][1] for i in range(5)):
        raise ValueError("Les scores doivent être triés")
    return {"question": question, "source": source, "rows": rows}

snacking=("Speak Snacking · Strateg'eat · 2025 · ensemble des répondants",
"https://www.snackshow.com/content/dam/sitebuilder/ref/sandwich-and-parizza/pdf/2025/Speak-Snacking-2025.pdf.coredownload.425688328.pdf")
gastronomie=("Ipsos · Les Français et la gastronomie · 2025",
"https://www.ipsos.com/sites/default/files/ct/news/documents/2025-03/ipsos-les-francais-et-la-gastronomie-rapport-complet.pdf")
produits=("Ipsos · Les Français à table · août 1988",
"https://www.ipsos.com/fr-fr/les-francais-table-pratiques-compor-tements-et-gouts")
vacances_1990=("Ipsos · Les vacances · enquête de juin 1990",
"https://www.ipsos.com/fr-fr/les-vacances-0")
vacances_1996=("Ipsos · Les Français et leurs vacances · 1996",
"https://www.ipsos.com/fr-fr/les-francais-et-leurs-vacances")
pain=("Ifop / Confédération de la boulangerie · 2023 · total des citations",
"https://boulangerie.org/wp-content/uploads/sites/2/2023/12/PJ-1-a-la-Circulaire-n%C2%B0100-Image-du-pain-et-de-la-boulangerie-aupres-des-Francais.pdf")

six_boards=[
    board("Quels plats salés les Français achètent-ils pour manger dehors ?",snacking,[
        ("Pizza",46,"pizzas|une pizza"),
        ("Burger",31,"hamburger|hamburgers|burgers"),
        ("Sandwich",28,"sandwiches|sandwichs"),
        ("Traditionnel",27,"plat traditionnel|cuisine traditionnelle|repas traditionnel"),
        ("Kebab",24,"grec|kebabs"),
        ("Salade",23,"salades|salade composee|salade composée"),
    ]),
    board("Quelles gourmandises les Français achètent-ils à l'extérieur ?",snacking,[
        ("Chocolatine",33,"pain au chocolat|pains au chocolat|petit pain au chocolat|chocolatines"),
        ("Croissant",31,"croissants"),
        ("Crêpe",22,"crepe|crepes|crêpes"),
        ("Cookie",21,"cookies"),
        ("Fruit",21,"fruits|un fruit"),
        ("Flan",21,"flan patissier|flans|flan pâtissier"),
    ]),
    board("Quelles régions françaises sont réputées pour leur gastronomie ?",gastronomie,[
        ("Sud-Ouest",41,"sud ouest|sud-ouest|sud ouest de la france"),
        ("Lyonnais",33,"lyon|region lyonnaise|région lyonnaise|lyonnais"),
        ("Bretagne",26,"breton|bretons"),
        ("Alsace",25,"alsacien|alsacienne"),
        ("Bourgogne",18,"bourguignon|bourguignonne"),
        ("Provence",16,"provençal|provencal|provençale"),
    ]),
    board("Où les Français cherchent-ils des avis sur les restaurants ?",gastronomie,[
        ("Google",53,"google maps|maps|avis google"),
        ("Tripadvisor",45,"trip advisor|trip-advisor"),
        ("Entourage",42,"amis|famille|proches|bouche a oreille|bouche à oreille"),
        ("Routard",14,"le routard|guide du routard"),
        ("Michelin",14,"guide michelin|etoiles michelin|étoiles michelin"),
        ("Influenceurs",8,"influenceur|instagrammeurs|influenceuse"),
    ]),
    board("Quels produits alimentaires manqueraient aux Français ?",produits,[
        ("Pain",66,"baguette|baguettes"),
        ("Légumes",40,"legumes|legume|légume"),
        ("Viande",28,"viande rouge|boeuf|bœuf|steak"),
        ("Fromage",27,"fromages"),
        ("Fruits",24,"fruit"),
        ("Café",20,"cafe|coffee"),
    ]),
    board("Quels mots font penser aux vacances d'été ?",vacances_1990,[
        ("Détente",70,"detente|relaxation|se detendre|repos"),
        ("Évasion",43,"evasion|s evader|voyager|voyage"),
        ("Famille",39,"enfants|parents|avec la famille"),
        ("Plage",27,"plages|bord de mer"),
        ("Amis",26,"copains|potes|avec les amis"),
        ("Chaleur",26,"chaud|il fait chaud|soleil"),
    ]),
    board("Que font les Français pendant leurs vacances ?",vacances_1996,[
        ("Promenade",54,"marcher|marche|randonnée|randonnee|promenades|balade|balades"),
        ("Famille",50,"enfants|parents|moments en famille"),
        ("Plage",48,"plages|aller a la plage"),
        ("Visites",47,"visite|monuments|tourisme|visiter"),
        ("Lecture",33,"lire|livre|livres"),
        ("Repos",32,"se reposer|dormir|rien faire|farniente|paresser|detente"),
    ]),
    board("Quels types de pain les Français aiment-ils acheter ?",pain,[
        ("Tradition",67,"baguette tradition|tradition|baguette de tradition"),
        ("Baguette",50,"baguettes|baguette classique|baguette ordinaire"),
        ("Céréales",41,"cereales|pain aux cereales|pain complet|complet|seigle"),
        ("Campagne",24,"pain de campagne|campagnard"),
        ("Spéciaux",13,"speciaux|pain special|pain aux noix|pain aux fruits|pain aux lardons"),
        ("Mie",5,"pain de mie|mie de pain"),
    ]),
]
boards=six_boards
