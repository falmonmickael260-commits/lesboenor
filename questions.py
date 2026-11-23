"""Chaque ligne associe un libellé, le pourcentage publié et les variantes acceptées."""
def study(title, slug):
    return (title, "https://yougov.com/fr-fr/articles/" + slug)

ice = study("YouGov France · juillet 2021", "37025-les-francais-et-les-glaces")
xmas = study("YouGov France · Noël 2021 · 1 017 adultes", "39859-noel-sapin-artificiel")
air = study("YouGov France · juillet 2020", "31002-francais-rapport-activites-de-plein-air")
sport = study("YouGov France · mai 2018", "20865-24-des-francais-font-du-sport-une-deux-fois-par-se")
def board(question, source, rows):
    return dict(question=question, source=source, rows=rows)

boards = [
board("Quel cadeau les Français rêvaient-ils de recevoir à Noël en 2021 ?", xmas, [
("Un voyage",33,"voyager|vacances|sejour|partir en voyage|un billet de voyage"),("Une voiture",19,"auto|automobile|bagnole"),("Un ordinateur",14,"ordi|ordinateur portable|pc|pc portable")]),
board("Quel parfum de glace figurait parmi les cinq préférés des Français en 2021 ?", ice, [
("Vanille",15,"vanilla"),("Chocolat",12,"choco"),("Caramel",9,"caramel beurre sale|caramel au beurre sale"),("Pistache",7,"pistaches"),("Café",7,"cafe")]),
board("Quelle activité de plein air les Français citaient-ils le plus en 2020 ?", air, [
("Randonnée",58,"rando|marche|faire de la randonnee"),("Vélo",58,"bicyclette|cyclisme|vtt|faire du velo"),("Natation",43,"nager|nage")]),
board("Que faisaient les Français d’un cadeau de Noël qui ne leur plaisait pas ?", xmas, [
("S’en servir quand même",41,"utiliser|utiliser quand meme|je l utilise|je m en sers|s en servir|ils l utilisent"),("Le ranger",21,"ranger|le mettre au placard|mettre au placard|au fond du placard|le cacher dans un placard"),("Le revendre en ligne",13,"vendre|revendre|le vendre|le revendre|vente en ligne|le vendre sur internet"),("Le donner à un proche",10,"donner a un proche|offrir a quelqu un de la famille|donner a ma famille|donner a un ami"),("Le donner à une association",4,"donner a une association|don a une association|association|donner a une oeuvre caritative")]),
board("Quelle marque de glace les Français préféraient-ils en 2021 ?", ice, [
("Häagen-Dazs",24,"haagen dazs|hagen daz|haagen daaz"),("Magnum",18,"magnums"),("Carte d’Or",14,"carte dor|carte d or")]),
board("Quelle activité sportive arrivait en tête des pratiques en France en 2018 ? Trouvez le trio.", sport, [
("Randonnée",20,"rando|marche|faire de la randonnee"),("Course à pied",14,"running|jogging|footing|courir"),("Fitness",13,"gym|gymnastique|crossfit|remise en forme")])]
