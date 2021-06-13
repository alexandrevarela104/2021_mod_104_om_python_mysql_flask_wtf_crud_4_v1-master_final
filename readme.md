Module 104 Rendu final gestionaire de factures 13.01.2021
---


# Faire fonctionner mon projet Gestionaire de factures :
##### BUT : CRUD (Create Read Update Delete) complet sur la "t_user" et la table intermédiaire "t_motif"
* Démarrer le serveur MySql (uwamp ou xamp ou mamp, etc)
* Si cela est déjà fait, passez au point suivant. Dans PyCharm, importer la BD grâce à un "run" du fichier "zzzdemos/1_ImportationDumpSql.py".
  * En cas d'erreurs : ouvrir le fichier ".env" à la racine du projet, contrôler les indications de connexion pour la bd.
* Puis dans le répertoire racine du projet, ouvrir le fichier "1_run_server_flask.py" et faire un "run".
  * Indispensable, car la BD à changé depuis le dernier exercice.



# Onglet Utilisateurs:
Dans cette onglet, vous allez pouvoir créer votre compte utilisateur pour faciliter la recherche de vos factures

#Onglet Factures:
Cet onglet Factures va vous permettre de insérer toutes les factures que vous pouvez avoir pour pouvoir faciliter votre gestion de vos factures

#Onglets Destinataire/Motif:

Comme leur noms l'indique, ces deux tables vous permettrons de ajouter/editer ou suppriemr un motif ou un destintaire qui ne serait pas présent sur la liste déroulante au moment de la création de votre facture 

#Onglets Utilisateurs/factures Utilisateurs/emails:

Ces deux pages vous permettront de associer vos factures/emails, sur votre compte

#Onglet Email:

Page crud qui vous fournit si vous le souhaitez, un email