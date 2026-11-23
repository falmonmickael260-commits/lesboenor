"""Huit manches : 6 réponses d'un seul mot, issues de sondages de Français.
Les scores sont les pourcentages publiés, arrondis à l'entier pour les enquêtes
Toluna/LSA de 2015 ; des choix multiples peuvent totaliser plus de 100 %.
Chaque réponse a ses synonymes habituels pour faciliter la saisie en régie.
"""
def board(question, source, rows):
    if len(rows) != 6:
        raise ValueError("Il faut exactement six réponses pour chaque question.")
    if any(" " in label.strip() for label, _, _ in rows):
        raise ValueError("Chaque réponse affichée doit être un seul mot.")
    if len({label.casefold() for label, _, _ in rows}) != 6:
        raise ValueError("Les réponses affichées doivent être distinctes.")
    if any(rows[i][1] < rows[i + 1][1] for i in range(5)):
        raise ValueError("Les réponses doivent être classées par score décroissant.")
    return {"question": question, "source": source, "rows": rows}

six_boards = [
    board("Quels sont les animaux préférés des Français ?",
          ("Ipsos · 30 Millions d'amis · 2005", "https://www.ipsos.com/fr-fr/les-animaux-preferes-des-francais"), [
        ("Chien", 56, "chiens|toutou"),
        ("Chat", 44, "chats|minou"),
        ("Cheval", 33, "chevaux"),
        ("Dauphin", 25, "dauphins"),
        ("Écureuil", 12, "ecureuil|ecureuils"),
        ("Lapin", 11, "lapins"),
    ]),
    board("Quels sont les parfums de glace préférés des Français ?",
          ("YouGov France · juillet 2021", "https://yougov.com/fr-fr/articles/37025-les-francais-et-les-glaces"), [
        ("Vanille", 15, "vanilla|glace a la vanille"),
        ("Chocolat", 12, "choco|chocolats"),
        ("Caramel", 9, "caramel beurre sale|caramel au beurre sale"),
        ("Pistache", 7, "pistaches"),
        ("Café", 7, "cafe|glace au cafe"),
        ("Citron", 5, "citrons|glace citron|citron jaune"),
    ]),
    board("Quels sont les fromages préférés des Français ?",
          ("YouGov France · juin 2015", "https://yougov.com/fr-fr/articles/12592-les-fromages-preferes-des-francais-le-top10-decouv"), [
        ("Camembert", 41, "camember"),
        ("Chèvre", 36, "chevre|fromage de chevre|buche de chevre"),
        ("Comté", 32, "comte"),
        ("Roquefort", 29, "roqueforts"),
        ("Emmental", 21, "emmenthal"),
        ("Gruyère", 20, "gruyere"),
    ]),
    board("Quels fruits manqueraient le plus aux Français ?",
          ("Toluna pour LSA · mai 2015 · points arrondis", "https://www.consoglobe.com/hommes-femmes-fruits-legumes-cg"), [
        ("Fraise", 49, "fraises"),
        ("Pomme", 43, "pommes"),
        ("Banane", 41, "bananes"),
        ("Melon", 36, "melons"),
        ("Pêche", 35, "peche|peches|nectarine|nectarines"),
        ("Cerise", 34, "cerises"),
    ]),
    board("Quels légumes manqueraient le plus aux Français ?",
          ("Toluna pour LSA · mai 2015 · points arrondis", "https://www.consoglobe.com/hommes-femmes-fruits-legumes-cg"), [
        ("Patate", 65, "patates|pomme de terre|pommes de terre"),
        ("Tomate", 61, "tomates"),
        ("Carotte", 43, "carottes"),
        ("Haricot", 40, "haricots|haricots verts|haricot vert"),
        ("Laitue", 35, "salade|salade verte"),
        ("Champignon", 34, "champignons"),
    ]),
    board("Quels plats représentent le mieux la France ?",
          ("Ipsos · gastronomie française · mars 2025", "https://www.ladepeche.fr/2025/03/31/le-boeuf-bourguignon-reste-le-plat-prefere-des-francais-en-2025-12605466.php"), [
        ("Bourguignon", 39, "boeuf bourguignon|bœuf bourguignon|bourguignonne"),
        ("Cassoulet", 31, "cassoulets"),
        ("Blanquette", 22, "blanquette de veau"),
        ("Confit", 20, "confit de canard|canard confit"),
        ("Choucroute", 17, "choucroute garnie"),
        ("Crêpes", 17, "crepes|crepe|galettes|galette"),
    ]),
    board("Quels chefs cuisiniers les Français préfèrent-ils ?",
          ("Ipsos · gastronomie française · mars 2025", "https://www.aufeminin.com/tendance/ce-plat-traditionnel-de-la-gastronomie-est-le-prefere-des-francais-39-le-preferent-au-cassoulet-ou-la-blanquette-s4109910.html"), [
        ("Lignac", 43, "cyril lignac|cyril"),
        ("Etchebest", 41, "philippe etchebest|philippe"),
        ("Ducasse", 25, "alain ducasse"),
        ("Pic", 19, "anne sophie pic|anne-sophie pic"),
        ("Marx", 17, "thierry marx"),
        ("Darroze", 14, "helene darroze|hélène darroze"),
    ]),
    board("Quelles familles de sports pratiquent les Français ?",
          ("Baromètre national des pratiques sportives 2025 · catégories", "https://conseilsport.decathlon.fr/top-10-des-sports-les-plus-pratiques-en-france-en-2021"), [
        ("Marche", 49, "marche|course|running|jogging|footing|randonnee|randonnée"),
        ("Fitness", 26, "gym|gymnastique|musculation|halterophilie"),
        ("Natation", 21, "piscine|nage|nager|aquatique|plongee|plongée"),
        ("Cyclisme", 19, "velo|vélo|vtt|moto|bmx|cycle"),
        ("Raquettes", 14, "tennis|badminton|padel|raquette"),
        ("Montagne", 10, "ski|ski alpin|alpinisme|sports d hiver"),
    ]),
]
boards = six_boards
