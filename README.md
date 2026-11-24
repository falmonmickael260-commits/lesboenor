# Le Grand Tableau
Régie privée pour deux animateurs. Les joueurs restent dans votre salon vocal. Le même code ouvre la même partie sur téléphone et ordinateur.

## Mettre le site sur Railway
1. Décompressez l’archive. Dans un dépôt GitHub, placez le contenu du dossier plateau à la racine. Le Dockerfile doit être visible à côté de server.py.
2. Dans Railway, créez un projet depuis ce dépôt GitHub. Le Dockerfile démarre le site.
3. Dans Variables, créez HOST_KEY avec un code privé de votre choix de 12 caractères ou plus. Gardez-le en dehors du dépôt.
4. Attachez un volume au service, monté sur /data, et conservez une seule réplique. Le site utilise automatiquement RAILWAY_VOLUME_MOUNT_PATH pour sauvegarder la partie.
5. Déployez, puis ouvrez Settings → Networking → Generate Domain. Envoyez ce lien et le code à votre coanimatrice. Chacun saisit le code sur son appareil.

## Pendant la soirée
Sélectionnez l’équipe qui a obtenu la main dans votre vocal. Lisez la question et saisissez une réponse à la fois. Chaque appareil reçoit les changements en environ une seconde. Le même nombre de points donne le même rang. Une case déjà trouvée ne marque rien. Si le jeu hésite, faites préciser ou confirmez une erreur. Après trois erreurs, l’autre équipe a une tentative. Un vol réussi ajoute la valeur de la dernière case à la cagnotte et attribue le total à l’autre équipe. Un vol raté laisse la cagnotte à l’équipe initiale. Une fois toutes les cases trouvées, l’attribution est automatique. La quatorzième manche termine la partie. Le bouton Nouvelle partie réinitialise le tableau après confirmation.

## Les enquêtes
Les questions adaptées de plusieurs publications YouGov France, datées de 2018 à 2021. Les rangs portent sur les réponses retenues pour chaque manche. Les points correspondent aux pourcentages publiés, sans ajustement à 100. Plusieurs citations ou une sélection limitée peuvent conduire à un total différent de 100. La question sur les cadeaux indésirables reprend les cinq comportements chiffrés dans l’article. Le lien de chaque source est disponible à la fin de la manche, dans l’historique. Les libellés oraux, variantes et sources sont dans questions.py côté serveur.

## Essai local
Python 3.10 ou supérieur, aucune dépendance. Dans un terminal ouvert dans le dossier du projet, exécutez la commande suivante en remplaçant le code.
    
    HOST_KEY='votre-code-prive' python3 server.py

Ouvrez http://localhost:8080. La sauvegarde locale se trouve dans data/. Le serveur accepte les variables PORT et DATA_DIR. Une adresse localhost est accessible uniquement depuis votre appareil.

## Appel au buzzer
Avant la manche, ouvrez Composition des équipes. Saisissez un prénom par ligne dans chaque couleur et enregistrez. Le premier duo est appelé à la première manche, le deuxième à la suivante. Chaque équipe recommence indépendamment au début de sa liste. Les listes sont partagées et conservées pour la prochaine partie.

## Formats et 8 contre 8
Dans **Composition des équipes**, choisissez **6 contre 6**, **7 contre 7**, **8 contre 8** (16 joueurs) ou le format libre. Le formulaire prépare automatiquement 6, 7 ou 8 cases par équipe ; en format fixe, il faut enregistrer exactement le nombre de joueurs annoncé dans chacune des deux équipes avant de jouer. La régie tire au sort un joueur bleu et un joueur rouge au buzzer, sans rappel tant que les joueurs de chaque équipe ne sont pas tous passés. Les 14 manches permettent ainsi à chacun des 8 joueurs de participer au buzzer en 8 contre 8. Le mode est conservé si vous relancez une partie avec les mêmes joueurs ou avec de nouveaux joueurs.

## Édition 14 manches
Le jeu propose 14 manches de six réponses chacune. La finale comprend désormais quatre questions, posées séparément à deux finalistes. Les doublons entre les deux réponses ne marquent qu’une fois et l’objectif commun reste à 100 points. Les résultats des enquêtes historiques comportent leurs sources dans la régie.
