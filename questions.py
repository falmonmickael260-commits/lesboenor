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


livret=("Family Feud · livret de sondages, édition américaine 2008","https://content.cmpl.org/bg/FamilyFeud.pdf")
six_boards=[
board("Votre voisin frappe à la porte. Que pourrait-il vouloir vous emprunter ?",livret,[
("Du sucre",26,"sucre en poudre"),("Une tondeuse",18,"tondeuse a gazon"),("Une échelle",13,"echelle"),("Une pelle",10,"pelle"),("Des outils",8,"outillage|boite a outils"),("Un marteau",7,"marteau")]),
board("Sur la route, quelle habitude des autres conducteurs vous agace ?",livret,[
("Oublier le clignotant",31,"pas de clignotant|sans clignotant|ne pas mettre son clignotant|oubli du clignotant"),("Couper la route",30,"queue de poisson|faire une queue de poisson|il me coupe la route"),("Rouler trop lentement",13,"rouler lentement|lenteur|rouler doucement"),("Coller la voiture devant",10,"coller|coller au pare chocs|suivre de trop pres"),("Téléphoner au volant",7,"telephone|telephoner|portable"),("Rouler trop vite",4,"vitesse|exces de vitesse|aller trop vite")]),
board("Dans une grande demeure luxueuse, que remarquez-vous en entrant ?",livret,[
("Un lustre",25,"grand lustre|lustre en cristal"),("Des tableaux",10,"peintures|tableau|oeuvres d art"),("Un escalier",8,"grand escalier|escalier monumental"),("Des antiquités",6,"antiquite|objets anciens"),("De beaux meubles",6,"mobilier|meubles de luxe|meubles"),("Du personnel de maison",5,"domestiques|majordome|serviteurs|domestique")]),
board("Que met-on dans une grande salade composée façon « salade du chef » ?",livret,[
("De la laitue",36,"salade|salade verte|feuilles de salade"),("Du jambon",22,"des de jambon"),("Des œufs durs",10,"oeuf|oeufs|oeuf dur"),("De la tomate",9,"tomates|tomates cerises"),("Du fromage",7,"des de fromage|gruyere|emmental"),("Du poulet",5,"blanc de poulet|poulet grille")]),
board("Au téléphone, quel service vous attendez-vous à voir vous mettre en attente ?",livret,[
("Un cabinet médical",30,"docteur|medecin|cabinet du medecin"),("Un opérateur téléphonique",18,"operateur|compagnie de telephone|service client telephonique"),("Une banque",13,"banquier|ma banque"),("Une assurance",12,"assureur|compagnie d assurance"),("Un grand magasin",9,"magasin|grande surface"),("Un restaurant",6,"resto|restaurant")]),
board("Qu’est-ce qui donne envie de choisir l’été plutôt que l’hiver ?",livret,[
("La chaleur",39,"il fait chaud|temps chaud|beau temps|soleil"),("Les vêtements légers",17,"vetements plus legers|short|tenue legere"),("Plus d’activités",10,"activites|activites dehors|activites en plein air"),("La plage",10,"aller a la plage|plages"),("On s’amuse davantage",6,"amusement|s amuser|plus amusant"),("L’absence de neige",4,"pas de neige|il ne neige pas")])]
