"""Questions basées sur des enquêtes françaises publiées ; les points sont les pourcentages cités."""
def study(title, url):
    return title, url
def board(question, source, rows):
    return dict(question=question, source=source, rows=rows)

ice=study("YouGov France · glaces · 2021","https://yougov.com/fr-fr/articles/37025-les-francais-et-les-glaces")
noel=study("YouGov France · Noël · 2021","https://yougov.com/fr-fr/articles/39859-noel-sapin-artificiel")
air=study("YouGov France · plein air · 2020","https://yougov.com/fr-fr/articles/31002-francais-rapport-activites-de-plein-air")
sport=study("YouGov France · sport · 2018","https://yougov.com/fr-fr/articles/20865-24-des-francais-font-du-sport-une-deux-fois-par-se")
cheese=study("YouGov France · fromages · 2015","https://yougov.com/fr-fr/articles/12592-les-fromages-preferes-des-francais-le-top10-decouv")
crepes=study("YouGov France · crêpes · 2021","https://yougov.com/fr-fr/articles/33824-les-francais-sont-ils-des-fans-de-crepes")

six_boards=[
board("Quels parfums de glace les Français préfèrent-ils ?",ice,[
("Vanille",15,"vanilla|glace vanille"),("Chocolat",12,"choco|glace chocolat"),("Caramel",9,"caramel au beurre sale"),("Pistache",7,"pistaches"),("Café",7,"cafe")]),
board("Quels cadeaux les Français rêvent-ils de recevoir à Noël ?",noel,[
("Un voyage",33,"vacances|voyager|sejour"),("Une voiture",19,"auto|automobile"),("Un ordinateur",14,"ordi|pc|ordinateur portable")]),
board("Quelles activités de plein air les Français pratiquent-ils ?",air,[
("La randonnée",58,"randonnee|rando|marche"),("Le vélo",58,"velo|vtt|cyclisme"),("La natation",43,"natation|nage|nager")]),
board("Que font les Français d'un cadeau de Noël qui ne leur plaît pas ?",noel,[
("Ils l'utilisent quand même",41,"utiliser|garder et utiliser|s en servir"),("Ils le rangent",21,"ranger|placard|le mettre au placard"),("Ils le revendent sur Internet",13,"revendre|vendre|revente en ligne"),("Ils le donnent à un proche",10,"donner a un proche|offrir a un proche|donner a la famille"),("Ils le donnent à une association",4,"association|donner a une association")]),
board("Quelles marques de glace les Français préfèrent-ils ?",ice,[
("Häagen-Dazs",24,"haagen dazs|hagen daz"),("Magnum",18,"magnums"),("Carte d'Or",14,"carte dor|carte d or")]),
board("Quels sports les Français pratiquent-ils le plus ?",sport,[
("La randonnée",20,"randonnee|rando|marche"),("La course à pied",14,"running|jogging|footing|courir"),("Le fitness",13,"fitness|gym|gymnastique")]),
board("Quels sont les fromages préférés des Français ?",cheese,[
("Le camembert",41,"camembert"),("Le fromage de chèvre",36,"chevre|fromage de chevre"),("Le comté",32,"comte"),("Le roquefort",29,"roquefort"),("L'emmental",21,"emmental|emmenthal"),("Le gruyère",20,"gruyere")]),
board("Que mettent les Français sur leurs crêpes sucrées ?",crepes,[
("Du sucre",23,"sucre|sucre en poudre"),("De la pâte à tartiner",16,"nutella|pate a tartiner|chocolat a tartiner"),("De la confiture",15,"confiture|confiture de fraise")])
]
boards=six_boards
