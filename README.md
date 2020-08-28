![navbar_purbeurre](products/static/products/img/HomePurBeurreReadme.png)

### 1. Objet du projet 11 :

Amélioration du projet 8 : "PurBeurre - Trouvez un produit de substitution à ceux que vous consommez tous les jours".

### 2. Fonctionnalités ajoutées :
- Intégration à l'application "users" de l'envoi d'email avec un lien à cliquer pour confirmer la création du compte utilisateur.
- Ajout de l'application "comments" qui permet aux utilisateurs connectés de saisir un commentaire sur les fiches produits.
- Refactoring de la base de données avec l'enregistrement de 5000 produits.

### 3. Bug
- Ajout par le mentor T. Chappuis de l'application "pending_favorites" incluant un bug à détecter qui empêche son fonctionnement. Cette application permet de sauvegarder des produits dans la session utilisateur sans qu'il soit connecté et de les enregistrer dans son espace automatiquement dès qu'il se connecte.

### 4. Installation des dépendances
- pip install -r requirements.txt

### 5. Tests
- Lancer les tests : **_coverage run manage.py test_**
- Editer le rapport du coverage : **_coverage report -m_**

### 6. Lancement en local
- Créer et remplir la base de données : **_python manage.py populatedb_**
- Lancer l'application : **_python manage.py runserver_**

