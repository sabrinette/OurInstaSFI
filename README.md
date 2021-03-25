# OurInsta
OurInsta est un système d'information comparable au service Instagram

## Contributeurs:
###### Fatima Afilal
###### Sabrine Ben Alaya
###### Ilyes Mohammed


## Tech
Ce projet fonctionne avec:
- [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Backend
- [Sqlalchemy](https://www.sqlalchemy.org/) - Backend
- [XAMPP](https://www.apachefriends.org/fr/index.html) - Backend
- [Html](https://fr.wikipedia.org/wiki/Hypertext_Markup_Language) - Frontend
- [Css](https://fr.wikipedia.org/wiki/Feuilles_de_style_en_cascade) - Frontend
- [Bootstrap](https://getbootstrap.com/) - Frontend
- [Ajax/jQuery](https://api.jquery.com/jquery.ajax/) - Frontend


## Arbre du projet : 
* static dans lequel on a six dossiers:

    - css: la feuille de style du projet 
    - fonts:ou se trouve les icones 
    - js: Code JavaScript du projet dans main.js
    - post_images: les images a poster sur Instagram
    - profile_image: les images utilisées pour les photos de profile de chaque utilisateurs (+ une photo par défaut si l'utilisateur ne mit pas sa photo)
    - vendor: dans lequel on trouve le Jquery,qui nous permet de modifier le DOM(Html en général)
    - Les différents images qu'on a utilisés pour le design de l'application
    
* templates: dans lequel il y a tous les codes HTML des pages de l'application:

    - addPost.html: pour ajouter une image
    - base.html: fichier html de base pour les pages avant l'authentification, ou se trouve les imports deJquery, de Bootsrap...
    - dashboard.html:affiche le nombre total des images dans l'application, la volumétrie correspondante en terme d'octets et le nombre d'images partagé par chaque utilisateur et sa volumétrie.
    - editProfile.html: ou l'utilisateur peut modifier ses informations
    - home.html : 
        - code html de la page d'accueil 
        - Boucle sur tous les posts pour qu'ils soient affichés
        - Tous ce qu'on récupère de serveur en html c'est avec jinja
    - layout.html: code html de base pour les pages aprés l'authentification
    - login.html: view de la page login 
    - post.html: code html pour poster une image
    - profile.html: code html pour la page du profile
    - register.html:code html pour créer un compte
    - updatePost/deletePost.html: code pour modifier/supprimer une telle image
    - \__init__.py: ou on trouve: 
    	- les configurations de l'application,
	- le lancement de l'application,
  	-  les configuration de l'application:
	```bash
 	app = Flask(__name__)
 	app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqldb://root:@127.0.0.1:3306/ourinsta"
	```
* models.py: les classes utilisé pour sqlalchemy(ORM), il reflète la conception de la base de données, On a cinq classes/tables: Users, Post, Reaction,Comment, followers:

    -  classe Users:   on trouve les attributs décrivant les informations personnelle des utilisateurs(user-id, name,email...) et on les stoque dans la base de donnée. 
        - l'attribut is-authenticated: nécessaire pour la gestion de session utilisateur et l'authentification(savoir si user est connecté ou non),
    
    - classe Post: contient les attributs nécessaire pour un tel post(post_id, user_id, post_description...)
    
    - classe Reaction: on trouve ses attributs: 
	    - user_id, post_id: les deux clés étrangers construisent ensemble une clé primaire
        -  reaction_type: un boolean, soit 0 (unlike) ou 1(like).
	        
	 -  classe Comment: on trouve ses attributs: 
	       - comment_id, post_id: sans une clé primaire, pour qu'un utilisateur peut faire plusieurs commentaire sur un post
	       - l'attribut content: le contenu du commentaire.

	  -  classe followers: ou se trouve id des abonnées et l'id des abonnements

* routes.py: ou se trouve tous les routes des fonctionnalités de l'application:

    - route vers home: récupération de tous les post de tous les abonnées et les envoyés à HTML,
    - route vers addPost: Ajouter une image(enregistrer sous static/post_images) et sa description , et l'enregistré dans la base de donnée,
    - route vers login: Vérification de l'état de l'utilisateur: s'il est authentifié, on le redirige vers Home, sinon, il fait l'authentification,
    - route vers register:Même chose que la route de login, avec le chargement de l'image(sous static/profile_images),
    - route vers logout: fermeture de la session actuelle de l'utilisateur,
    - route vers profile: récupération de tous les post de l'utilisateur actuelle,
    - route post/id: récupération du post de id=id,
    - route vers editProfile: Mettre à jour les informations personnelles de l'utilisateur actuelle,
    - route pour deletePost:un dropdown à côté de chaque image, si on clique sur, il supprime l'image de la base de donnée
    - route pour updatePost: un dropdown à côté de chaque image, si on clique sur, il nous redirige vers une autre page pour faire les modifications sur le post
    - route de AddReaction: 
	    - lorsqu'on clique sur l'un des boutons de réaction, le JS récupère dès le code en home.html l'id du post et le type de réaction, puis il teste, si data=like/dislike alors data du réaction_ type reçoit 1/0,
	    - si on met dislike/Like, automatiquement le Like/Dislike se supprime, et si on clique deux fois sur un bouton, ça supprime aussi,
	    - Le nombre de Like/Dislike est mis à jour en temps réel automatiquement grâce au ajax/Jquery,
    - route de addComment: Même principe de AddReaction, 
    - route vers deleteComment: Supression du commentaire possédant comment_id et post_id actuelle, 
    - route vers results: faire des recherches des images en fonction des mots clé dans la description.

* run.py: Lancement de l'application.


