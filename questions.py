# Classements fondés uniquement sur des enquêtes YouGov menées en France.
# Les points reprennent les pourcentages publiés, sans extrapolation à 100.
# Les formulations des questions ont été simplifiées pour être lues à voix haute.
def study(title, slug):
    return (title, "https://yougov.com/fr-fr/articles/" + slug)

def board(question, source, rows):
    return dict(question=question, source=source, rows=rows)

glaces = study("YouGov France · glaces · juillet 2021", "37025-les-francais-et-les-glaces")
glaces20 = study("YouGov France · glaces · juillet 2020", "30987-les-francais-sont-ils-des-adeptes-de-glaces")
noel = study("YouGov France · Noël · décembre 2021", "39859-noel-sapin-artificiel")
plein_air = study("YouGov France · loisirs de plein air · juillet 2020", "31002-francais-rapport-activites-de-plein-air")
sport = study("YouGov France · sport · mai 2018", "20865-24-des-francais-font-du-sport-une-deux-fois-par-se")
fromage = study("YouGov France · fromages · juin 2015", "12592-les-fromages-preferes-des-francais-le-top10-decouv")
crepes = study("YouGov France · crêpes · janvier 2021", "33824-les-francais-sont-ils-des-fans-de-crepes")
amour = study("YouGov France · Saint-Valentin · février 2022", "40964-budget-moyen-des-francais-saint-valentin")

# Banque principale : chaque question et ses réponses sont françaises et vérifiables.
# Les entrées entre | correspondent aux formulations orales alternatives acceptées.
six_boards = [
    board("Quels parfums de glace les Français préfèrent-ils ?", glaces, [
        ("Vanille",15,"glace vanille|vanilla"),
        ("Chocolat",12,"choco|glace chocolat"),
        ("Caramel",9,"caramel beurre salé|caramel beurre sale"),
        ("Pistache",7,"pistaches"),
        ("Café",7,"cafe|glace au cafe"),
        ("Citron",5,"citron jaune|glace citron")]),
    board("Quels fromages les Français aiment-ils le plus ?", fromage, [
        ("Camembert",41,"camember"),
        ("Fromage de chèvre",36,"chevre|fromage de chevre|buche de chevre"),
        ("Comté",32,"comte"),
        ("Roquefort",29,"roquefort"),
        ("Emmental",21,"emmenthal|emmental"),
        ("Gruyère",20,"gruyere")]),
    board("Que font les Français d'un cadeau qui ne leur plaît pas ?", noel, [
        ("Ils l'utilisent quand même",41,"l utiliser|utiliser|s en servir|ils le gardent et l utilisent"),
        ("Ils le rangent au placard",21,"le ranger|ranger|placard|le garder dans un placard"),
        ("Ils le revendent sur Internet",13,"revendre|vendre|revendre en ligne|le vendre"),
        ("Ils le donnent à un proche",10,"donner|l offrir|offrir a un proche|le donner a la famille"),
        ("Ils le donnent à une association",4,"association|donner a une association|charite")]),
    board("Quel cadeau les Français aimeraient-ils recevoir à Noël ?", noel, [
        ("Un voyage",33,"vacances|un sejour|partir en voyage"),
        ("Une voiture",19,"automobile|auto|bagnole"),
        ("Un ordinateur",14,"pc|ordinateur portable|ordi")]),
    board("Quels cadeaux offrent les Français à la Saint-Valentin ?", amour, [
        ("Des fleurs",22,"fleur|rose|roses|bouquet"),
        ("Du parfum",19,"parfum|eau de parfum"),
        ("Des chocolats",13,"chocolat|boite de chocolats"),
        ("Des bijoux",12,"bijou|collier|bague"),
        ("Des vêtements",11,"vetement|habits|habit")]),
    board("Quels types de camping les Français connaissent-ils ?", plein_air, [
        ("Le camping traditionnel",62,"camping classique|camping"),
        ("Le camping sauvage",48,"sauvage|bivouac"),
        ("Le camping à la ferme",45,"a la ferme|ferme"),
        ("Le camping chez l'habitant",24,"chez l habitant|chez quelqu un")]),
    board("Quelles marques de farine les Français connaissent-ils ?", crepes, [
        ("Francine",86,"francine"),
        ("Cœur de Blé",36,"coeur de ble|cœur de blé"),
        ("Gruau d'Or",24,"gruau d or|gruau dor"),
        ("Ebly Farine",20,"ebly|ebly farine"),
        ("Markal",4,"markal")]),
    board("Quelles garnitures les Français préfèrent-ils sur les crêpes sucrées ?", crepes, [
        ("Sucre",23,"sucre en poudre|du sucre"),
        ("Pâte à tartiner",16,"nutella|pate a tartiner|chocolat a tartiner"),
        ("Confiture",15,"confiture de fraise|confiture de fruits")]),
    board("Quelles activités de plein air les Français aiment-ils pratiquer ?", plein_air, [
        ("Randonnée",58,"rando|marche|marcher"),
        ("Vélo",58,"cyclisme|vtt|bicyclette"),
        ("Natation",43,"nage|nager|piscine")]),
    board("Quels sports sont les plus pratiqués par les Français ?", sport, [
        ("Randonnée",20,"marche|rando|marcher"),
        ("Course à pied",14,"running|jogging|footing|courir"),
        ("Fitness",13,"gym|musculation|crossfit|gymnastique")]),
    board("Quelles marques de glace les Français préfèrent-ils ?", glaces, [
        ("Häagen-Dazs",24,"haagen dazs|hagen daz|hagen dazs"),
        ("Magnum",18,"magnums"),
        ("Carte d'Or",14,"carte d or|carte dor")]),
    board("Dans quels pays les Français aimeraient-ils vivre un séjour romantique ?", amour, [
        ("Italie",50,"italien|rome|venise"),
        ("France",30,"francais|paris"),
        ("Espagne",6,"espagnol|barcelone|madrid")]),
    board("Quels parfums de glace les Français préféraient-ils en 2020 ?", glaces20, [
        ("Vanille",14,"glace vanille"),
        ("Chocolat",13,"choco|glace chocolat"),
        ("Pistache",8,"pistaches"),
        ("Citron",8,"glace citron"),
        ("Caramel",7,"caramel beurre sale"),
        ("Café",6,"cafe")])
]

# Anciennes références éventuelles conservées pour compatibilité d'import.
boards = six_boards
