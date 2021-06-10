"""
    Fichier : gestion_destinataires_crud.py
    Auteur : OM 2021.03.16
    Gestions des "routes" FLASK et des données pour les genres.
"""
import sys

import pymysql
from flask import flash, request
from flask import redirect
from flask import render_template

from flask import session
from flask import url_for

from APP_FILMS import obj_mon_application
from APP_FILMS.database.connect_db_context_manager import MaBaseDeDonnee
from APP_FILMS.erreurs.exceptions import *
from APP_FILMS.erreurs.msg_erreurs import *
from APP_FILMS.factures.gestion_factures_wtf_forms import FormWTFAjouterGenres
from APP_FILMS.factures.gestion_factures_wtf_forms import FormWTFDeleteGenre
from APP_FILMS.factures.gestion_factures_wtf_forms import FormWTFUpdateGenre
from APP_FILMS.essais_wtf_forms.wtf_forms_demo_select import DemoFormSelectWTF

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /genres_afficher
    
    Test : ex : http://127.0.0.1:5005/genres_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_genre_sel = 0 >> tous les genres.
                id_genre_sel = "n" affiche le genre dont l'id est "n"
"""


@obj_mon_application.route("/factures_afficher/<string:order_by>/<int:id_genre_sel>", methods=['GET', 'POST'])
def factures_afficher(order_by, id_genre_sel):
    if request.method == "GET":

        with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
            destinataire = """SELECT id_destinataire, destinataire FROM t_destinataire ORDER BY id_destinataire ASC"""

            mc_afficher.execute(destinataire)

        with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
            motif = """SELECT id_motif, motif FROM t_motif ORDER BY id_motif ASC"""

            mc_afficher.execute(motif)

        try:
            try:
                # Renvoie une erreur si la connexion est perdue.
                MaBaseDeDonnee().connexion_bd.ping(False)
            except Exception as erreur:
                flash(f"Dans Gestion genres ...terrible erreur, il faut connecter une base de donnée", "danger")
                print(f"Exception grave Classe constructeur GestionGenres {erreur.args[0]}")
                raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")




            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                if order_by == "ASC" and id_genre_sel == 0:
                    strsql_genres_afficher = """ SELECT `t_facture`.*, `t_destinataire`.`destinataire`, `t_motif`.`motif`
                                                                FROM `t_facture`
                                                                    LEFT JOIN `t_avoir_destinataire` ON `t_avoir_destinataire`.`fk_facture` = `t_facture`.`id_facture`
                                                                    LEFT JOIN `t_destinataire` ON `t_avoir_destinataire`.`fk_destinataire` = `t_destinataire`.`id_destinataire`
                                                                    LEFT JOIN `t_avoir_motif` ON `t_avoir_motif`.`fk_facture` = `t_facture`.`id_facture`
                                                                    LEFT JOIN `t_motif` ON `t_avoir_motif`.`fk_motif` = `t_motif`.`id_motif` ORDER BY id_facture"""
                    mc_afficher.execute(strsql_genres_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_facture"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du genre sélectionné avec un nom de variable
                    valeur_id_genre_selected_dictionnaire = {"value_id_genre_selected": id_genre_sel}
                    strsql_genres_afficher = """SELECT `t_facture`.*, `t_destinataire`.`destinataire`, `t_motif`.`motif`
                                                                FROM `t_facture`
                                                                    LEFT JOIN `t_avoir_destinataire` ON `t_avoir_destinataire`.`fk_facture` = `t_facture`.`id_facture`
                                                                    LEFT JOIN `t_destinataire` ON `t_avoir_destinataire`.`fk_destinataire` = `t_destinataire`.`id_destinataire`
                                                                    LEFT JOIN `t_avoir_motif` ON `t_avoir_motif`.`fk_facture` = `t_facture`.`id_facture`
                                                                    LEFT JOIN `t_motif` ON `t_avoir_motif`.`fk_motif` = `t_motif`.`id_motif` WHERE id_facture = %(value_id_genre_selected)s"""

                    mc_afficher.execute(strsql_genres_afficher, valeur_id_genre_selected_dictionnaire)
                else:
                    strsql_genres_afficher = """SELECT `t_facture`.*, `t_destinataire`.`destinataire`, `t_motif`.`motif`
                                                                FROM `t_facture`
                                                                    LEFT JOIN `t_avoir_destinataire` ON `t_avoir_destinataire`.`fk_facture` = `t_facture`.`id_facture`
                                                                    LEFT JOIN `t_destinataire` ON `t_avoir_destinataire`.`fk_destinataire` = `t_destinataire`.`id_destinataire`
                                                                    LEFT JOIN `t_avoir_motif` ON `t_avoir_motif`.`fk_facture` = `t_facture`.`id_facture`
                                                                    LEFT JOIN `t_motif` ON `t_avoir_motif`.`fk_motif` = `t_motif`.`id_motif` ORDER BY id_facture DESC"""

                    mc_afficher.execute(strsql_genres_afficher)



                data_genres = mc_afficher.fetchall()

                print("data_genres ", data_genres, " Type : ", type(data_genres))

                # Différencier les messages si la table est vide.
                if not data_genres and id_genre_sel == 0:
                    flash("""La table "t_facture" est vide. !!""", "warning")
                elif not data_genres and id_genre_sel > 0:
                    # Si l'utilisateur change l'id_facture dans l'URL et que le genre n'existe pas,
                    flash(f"Le genre demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_facture" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données genres affichés !!", "success")

        except Exception as erreur:
            print(f"RGG Erreur générale. genres_afficher")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)"
            # fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            flash(f"RGG Exception {erreur} genres_afficher", "danger")
            raise Exception(f"RGG Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")


    # Envoie la page "HTML" au serveur.
    return render_template("factures/factures_afficher.html", data=data_genres)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /factures_ajouter
    
    Test : ex : http://127.0.0.1:5005/factures_ajouter
    
    Paramètres : sans
    
    But : Ajouter un genre pour un film
    
    Remarque :  Dans le champ "name_genre_html" du formulaire "genres/factures_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@obj_mon_application.route("/factures_ajouter", methods=['GET', 'POST'])
def factures_ajouter_wtf():
    form = FormWTFAjouterGenres()
    if request.method == "POST":
        try:
            try:
                # Renvoie une erreur si la connexion est perdue.
                MaBaseDeDonnee().connexion_bd.ping(False)
            except Exception as erreur:
                flash(f"Dans Gestion genres ...terrible erreur, il faut connecter une base de donnée", "danger")
                print(f"Exception grave Classe constructeur GestionGenres {erreur.args[0]}")
                raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")

            if form.validate_on_submit():
                numero_facture_wtf = form.numero_facture_wtf.data
                somme_wtf = form.somme_wtf.data
                delai_wtf = form.delai_wtf.data
                payement_wtf = form.payement_wtf.data
                destinataire_wtf = request.form.get('destinataire')
                motif_wtf = request.form.get('motif')


                valeurs_insertion_dictionnaire = {"value_numerous_facture": numero_facture_wtf,
                                                  "value_somme": somme_wtf,
                                                  "value_delai": delai_wtf,
                                                  "value_payement": payement_wtf,
                                                  "value_destinataire": destinataire_wtf,
                                                  "value_motif": motif_wtf}
                print("-------------------------------------------------------------------")
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)
                print("-------------------------------------------------------------------")

                # Création de la facture dans la table facture
                strsql_insert_facture = """INSERT INTO t_facture (id_facture,numero_facture,somme,delai,payement) VALUES (NULL,%(value_numerous_facture)s,%(value_somme)s,%(value_delai)s,%(value_payement)s)"""
                with MaBaseDeDonnee().connexion_bd.cursor() as mconn_bd:
                    mconn_bd.execute(strsql_insert_facture, valeurs_insertion_dictionnaire)

                # Ici, j'essaie de récuperer l'id de la facture que je viens de créer, pour l'associer au destinataire/motif
                strsql_insert_fac = """SELECT `id_facture` FROM `t_facture` ORDER BY `id_facture` DESC LIMIT 1"""
                with MaBaseDeDonnee().connexion_bd.cursor() as mconn_bd:
                    mconn_bd.execute(strsql_insert_fac, valeurs_insertion_dictionnaire)
                    id_facture = mconn_bd.fetchall()[0]
                print(id_facture)

                # Ici, j'essaie de faire la liason de la fk facture et fk destinataire en récuperant la dernière id crée
                strsql_insert_fk = """INSERT INTO t_avoir_destinataire (id_avoir_destinataire,fk_facture,fk_destinataire) VALUES (NULL,%(id_facture)s,%(value_destinataire)s)"""
                with MaBaseDeDonnee().connexion_bd.cursor() as mconn_bd:
                    mconn_bd.execute(strsql_insert_fk, valeurs_insertion_dictionnaire)




                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")



                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('factures_afficher', order_by='DESC', id_genre_sel=0))

        # ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
        except pymysql.err.IntegrityError as erreur_genre_doublon:
            # Dérive "pymysql.err.IntegrityError" dans "MaBdErreurDoublon" fichier "erreurs/exceptions.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            code, msg = erreur_genre_doublon.args

            flash(f"{error_codes.get(code, msg)} ", "warning")

        # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
        except (pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                TypeError) as erreur_gest_genr_crud:
            code, msg = erreur_gest_genr_crud.args

            flash(f"{error_codes.get(code, msg)} ", "danger")
            flash(f"Erreur dans Gestion genres CRUD : {sys.exc_info()[0]} "
                  f"{erreur_gest_genr_crud.args[0]} , "
                  f"{erreur_gest_genr_crud}", "danger")

    strsql_insert_contenu = """SELECT t_destinataire.destinataire, t_destinataire.id_destinataire FROM t_destinataire """
    with MaBaseDeDonnee().connexion_bd.cursor() as mconn_bd:
        mconn_bd.execute(strsql_insert_contenu)
        destinataire = mconn_bd.fetchall()



        strsql_insert_contenu = """SELECT t_motif.motif, t_motif.id_motif FROM t_motif """
        with MaBaseDeDonnee().connexion_bd.cursor() as mconn_bd:
            mconn_bd.execute(strsql_insert_contenu)
            motif = mconn_bd.fetchall()



    return render_template("factures/factures_ajouter_wtf.html", form=form, destinataire=destinataire, motif=motif)







"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /facure_update
    
    Test : ex cliquer sur le menu "genres" puis cliquer sur le bouton "EDIT" d'un "genre"
    
    Paramètres : sans
    
    But : Editer(update) un genre qui a été sélectionné dans le formulaire "factures_afficher.html"
    
    Remarque :  Dans le champ "numero_facture_update_wtf" du formulaire "genres/destinataire_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@obj_mon_application.route("/facture_update", methods=['GET', 'POST'])
def facture_update_wtf():

    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_facture"
    id_facture_update = request.values['id_facture_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateGenre()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "destinataire_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            numero_facture_update = form_update.numero_facture_update_wtf.data
            somme_update = form_update.somme_update_wtf.data
            delai_update = form_update.delai_update_wtf.data
            payement_update = form_update.payement_update_wtf.data

            numero_facture_update = numero_facture_update.lower()
            somme_update = somme_update.lower()
            delai_update = delai_update.lower()
            payement_update = payement_update.lower()


            valeur_update_dictionnaire = {"value_id_facture": id_facture_update, "value_numerous_facture": numero_facture_update,"value_somme": somme_update,"value_delai": delai_update, "value_payement":payement_update}
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_intitulegenre = """UPDATE t_facture SET numero_facture = %(value_numerous_facture)s WHERE id_facture = %(value_id_facture)s"""
            with MaBaseDeDonnee() as mconn_bd:
                mconn_bd.mabd_execute(str_sql_update_intitulegenre, valeur_update_dictionnaire)

            str_sql_update_intitulegenre = """UPDATE t_facture SET somme = %(value_somme)s WHERE id_facture = %(value_id_facture)s"""
            with MaBaseDeDonnee() as mconn_bd:
                mconn_bd.mabd_execute(str_sql_update_intitulegenre, valeur_update_dictionnaire)

            str_sql_update_intitulegenre = """UPDATE t_facture SET delai = %(value_delai)s WHERE id_facture = %(value_id_facture)s"""
            with MaBaseDeDonnee() as mconn_bd:
                mconn_bd.mabd_execute(str_sql_update_intitulegenre, valeur_update_dictionnaire)

            str_sql_update_intitulegenre = """UPDATE t_facture SET payement = %(value_payement)s WHERE id_facture = %(value_id_facture)s"""
            with MaBaseDeDonnee() as mconn_bd:
                mconn_bd.mabd_execute(str_sql_update_intitulegenre, valeur_update_dictionnaire)


            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_facture_update"
            return redirect(url_for('factures_afficher', order_by="ASC", id_genre_sel=id_facture_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_facture" et "numero_facture" de la "t_facture"
            str_sql_id_facture = "SELECT id_facture, numero_facture, somme, delai, payement FROM t_facture WHERE id_facture = %(value_id_facture)s"
            valeur_select_dictionnaire = {"value_id_facture": id_facture_update}
            mybd_curseur = MaBaseDeDonnee().connexion_bd.cursor()
            mybd_curseur.execute(str_sql_id_facture, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom genre" pour l'UPDATE
            data_nom_genre = mybd_curseur.fetchone()
            print("data_nom_genre ", data_nom_genre, " type ", type(data_nom_genre), " genre ",
                  data_nom_genre["numero_facture"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "destinataire_update_wtf.html"
            form_update.numero_facture_update_wtf.data = data_nom_genre["numero_facture"]
            form_update.somme_update_wtf.data = data_nom_genre["somme"]
            form_update.delai_update_wtf.data = data_nom_genre["delai"]
            form_update.payement_update_wtf.data = data_nom_genre["payement"]

    # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
    except KeyError:
        flash(f"__KeyError dans facture_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")
    except ValueError:
        flash(f"Erreur dans facture_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]}", "danger")
    except (pymysql.err.OperationalError,
            pymysql.ProgrammingError,
            pymysql.InternalError,
            pymysql.err.IntegrityError,
            TypeError) as erreur_gest_genr_crud:
        code, msg = erreur_gest_genr_crud.args
        flash(f"attention : {error_codes.get(code, msg)} {erreur_gest_genr_crud} ", "danger")
        flash(f"Erreur dans facture_update_wtf : {sys.exc_info()[0]} "
              f"{erreur_gest_genr_crud.args[0]} , "
              f"{erreur_gest_genr_crud}", "danger")
        flash(f"__KeyError dans facture_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")



    return render_template("factures/facture_update_wtf.html", form_update=form_update)


"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /genre_delete
    
    Test : ex. cliquer sur le menu "genres" puis cliquer sur le bouton "DELETE" d'un "genre"
    
    Paramètres : sans
    
    But : Effacer(delete) un genre qui a été sélectionné dans le formulaire "factures_afficher.html"
    
    Remarque :  Dans le champ "numero_facture_delete_wtf" du formulaire "genres/destinataire_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@obj_mon_application.route("/facture_delete", methods=['GET', 'POST'])
def facture_delete_wtf():
    data_films_attribue_genre_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_facture"
    id_facture_delete = request.values['id_facture_btn_delete_html']

    # Objet formulaire pour effacer le genre sélectionné.
    form_delete = FormWTFDeleteGenre()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("factures_afficher", order_by="ASC", id_genre_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "genres/destinataire_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_films_attribue_genre_delete = session['data_films_attribue_genre_delete']
                print("data_films_attribue_genre_delete ", data_films_attribue_genre_delete)

                flash(f"Effacer le genre de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_facture": id_facture_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_destinataire = """DELETE FROM t_avoir_destinataire WHERE fk_facture = %(value_id_facture)s"""
                str_sql_delete_motif= """DELETE FROM  t_avoir_motif WHERE fk_facture = %(value_id_facture)s"""
                str_sql_delete_user = """DELETE FROM  t_user_facture WHERE fk_facture = %(value_id_facture)s"""

                str_sql_delete_idgenre = """DELETE FROM t_facture WHERE id_facture = %(value_id_facture)s"""
                # Manière brutale d'effacer d'abord la "fk_facture", même si elle n'existe pas dans la "t_destinataire"
                # Ensuite on peut effacer le genre vu qu'il n'est plus "lié" (INNODB) dans la "t_destinataire"
                with MaBaseDeDonnee() as mconn_bd:
                    mconn_bd.mabd_execute(str_sql_delete_destinataire, valeur_delete_dictionnaire)
                    mconn_bd.mabd_execute(str_sql_delete_motif, valeur_delete_dictionnaire)
                    mconn_bd.mabd_execute(str_sql_delete_user, valeur_delete_dictionnaire)
                    mconn_bd.mabd_execute(str_sql_delete_idgenre, valeur_delete_dictionnaire)


                flash(f"Genre définitivement effacé !!", "success")
                print(f"Genre définitivement effacé !!")

                # afficher les données
                return redirect(url_for('factures_afficher', order_by="ASC", id_genre_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_facture": id_facture_delete}
            print(id_facture_delete, type(id_facture_delete))

            # Requête qui affiche tous les films qui ont le genre que l'utilisateur veut effacer
            str_sql_genres_films_delete = """SELECT id_user, nom_user, id_facture, numero_facture FROM t_user_facture
                                            INNER JOIN t_user ON t_user_facture.fk_user = t_user.id_user 
                                            INNER JOIN t_facture ON t_user_facture.fk_facture = t_facture.id_facture
                                            WHERE fk_facture = %(value_id_facture)s"""

            mybd_curseur = MaBaseDeDonnee().connexion_bd.cursor()

            mybd_curseur.execute(str_sql_genres_films_delete, valeur_select_dictionnaire)
            data_films_attribue_genre_delete = mybd_curseur.fetchall()
            print("data_films_attribue_genre_delete...", data_films_attribue_genre_delete)

            # Nécessaire pour mémoriser les données afin d'afficher à nouveau
            # le formulaire "genres/destinataire_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
            session['data_films_attribue_genre_delete'] = data_films_attribue_genre_delete

            # Opération sur la BD pour récupérer "id_facture" et "numero_facture" de la "t_facture"
            str_sql_id_facture = "SELECT id_facture, numero_facture, somme, delai, payement FROM t_facture WHERE id_facture = %(value_id_facture)s"

            mybd_curseur.execute(str_sql_id_facture, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()",
            # vu qu'il n'y a qu'un seul champ "nom genre" pour l'action DELETE
            data_nom_genre = mybd_curseur.fetchone()
            print("data_nom_genre ", data_nom_genre, " type ", type(data_nom_genre), " genre ",
                  data_nom_genre["numero_facture"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "destinataire_delete_wtf.html"
            form_delete.numero_facture_delete_wtf.data = data_nom_genre["numero_facture"]


            # Le bouton pour l'action "DELETE" dans le form. "destinataire_delete_wtf.html" est caché.
            btn_submit_del = False

    # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
    except KeyError:
        flash(f"__KeyError dans facture_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")
    except ValueError:
        flash(f"Erreur dans facture_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]}", "danger")
    except (pymysql.err.OperationalError,
            pymysql.ProgrammingError,
            pymysql.InternalError,
            pymysql.err.IntegrityError,
            TypeError) as erreur_gest_genr_crud:
        code, msg = erreur_gest_genr_crud.args
        flash(f"attention : {error_codes.get(code, msg)} {erreur_gest_genr_crud} ", "danger")

        flash(f"Erreur dans facture_update_wtf : {sys.exc_info()[0]} "
              f"{erreur_gest_genr_crud.args[0]} , "
              f"{erreur_gest_genr_crud}", "danger")

        flash(f"__KeyError dans facture_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")

    return render_template("factures/facture_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_films_associes=data_films_attribue_genre_delete)
