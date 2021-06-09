"""
    Fichier : gestion_films_genres_crud.py
    Auteur : OM 2021.05.01
    Gestions des "routes" FLASK et des données pour l'association entre les films et les genres.
"""
import sys

import pymysql
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from APP_FILMS import obj_mon_application
from APP_FILMS.database.connect_db_context_manager import MaBaseDeDonnee
from APP_FILMS.erreurs.exceptions import *
from APP_FILMS.erreurs.msg_erreurs import *
from APP_FILMS.films_genres.gestion_email_wtf_forms import FormWTFAjouterGenres
from APP_FILMS.films_genres.gestion_email_wtf_forms import FormWTFUpdateGenre


"""
    Nom : films_genres_afficher
    Auteur : OM 2021.05.01
    Définition d'une "route" /films_genres_afficher

    But : Afficher les films avec les genres associés pour chaque film.

    Paramètres : id_genre_sel = 0 >> tous les films.
                 id_genre_sel = "n" affiche le film dont l'id est "n"

"""


@obj_mon_application.route("/films_genres_afficher/<int:id_film_sel>", methods=['GET', 'POST'])
def films_genres_afficher(id_film_sel):
    if request.method == "GET":
        try:
            try:
                # Renvoie une erreur si la connexion est perdue.
                MaBaseDeDonnee().connexion_bd.ping(False)
            except Exception as Exception_init_films_genres_afficher:
                code, msg = Exception_init_films_genres_afficher.args
                flash(f"{error_codes.get(code, msg)} ", "danger")
                flash(f"Exception _init_films_genres_afficher problème de connexion BD : {sys.exc_info()[0]} "
                      f"{Exception_init_films_genres_afficher.args[0]} , "
                      f"{Exception_init_films_genres_afficher}", "danger")
                raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")

            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                strsql_genres_films_afficher_data = """SELECT id_user , nom_user,
                                                               GROUP_CONCAT(email) as GenresFilms FROM t_user_email
                                                               RIGHT JOIN t_user ON t_user.id_user = t_user_email.fk_user
                                                               LEFT JOIN t_email ON t_email.id_email = t_user_email.fk_email
                                                              GROUP BY id_user"""
                if id_film_sel == 0:
                    # le paramètre 0 permet d'afficher tous les films
                    # Sinon le paramètre représente la valeur de l'id du film
                    mc_afficher.execute(strsql_genres_films_afficher_data)
                else:
                    # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
                    valeur_id_film_selected_dictionnaire = {"value_id_film_selected": id_film_sel}
                    # En MySql l'instruction HAVING fonctionne comme un WHERE... mais doit être associée à un GROUP BY
                    # L'opérateur += permet de concaténer une nouvelle valeur à la valeur de gauche préalablement définie.
                    strsql_genres_films_afficher_data += """ HAVING id_user= %(value_id_film_selected)s"""

                    mc_afficher.execute(strsql_genres_films_afficher_data, valeur_id_film_selected_dictionnaire)

                # Récupère les données de la requête.
                data_genres_films_afficher = mc_afficher.fetchall()
                print("data_genres ", data_genres_films_afficher, " Type : ", type(data_genres_films_afficher))

                # Différencier les messages.
                if not data_genres_films_afficher and id_film_sel == 0:
                    flash("""La table "t_film" est vide. !""", "warning")
                elif not data_genres_films_afficher and id_film_sel > 0:
                    # Si l'utilisateur change l'id_film dans l'URL et qu'il ne correspond à aucun film
                    flash(f"Le film {id_film_sel} demandé n'existe pas !!", "warning")
                else:
                    flash(f"Données films et genres affichés !!", "success")

        except Exception as Exception_films_genres_afficher:
            code, msg = Exception_films_genres_afficher.args
            flash(f"{error_codes.get(code, msg)} ", "danger")
            flash(f"Exception films_genres_afficher : {sys.exc_info()[0]} "
                  f"{Exception_films_genres_afficher.args[0]} , "
                  f"{Exception_films_genres_afficher}", "danger")

    # Envoie la page "HTML" au serveur.
    return render_template("films_genres/films_genres_afficher.html", data=data_genres_films_afficher)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /genres_ajouter

    Test : ex : http://127.0.0.1:5005/genres_ajouter

    Paramètres : sans

    But : Ajouter un genre pour un film

    Remarque :  Dans le champ "name_genre_html" du formulaire "genres/genres_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@obj_mon_application.route("/email_ajouter", methods=['GET', 'POST'])
def emails_ajouter_wtf():
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
                email_wtf = form.email_wtf.data

                valeurs_insertion_dictionnaire = {"value_email": email_wtf}

                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_user = """INSERT INTO t_email (id_email,email) VALUES (NULL,%(value_email)s)"""
                with MaBaseDeDonnee() as mconn_bd:
                    mconn_bd.mabd_execute(strsql_insert_user, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('films_genres_afficher', order_by='DESC', id_film_sel=0))

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

    return render_template("films_genres/emails_ajouter_wtf.html", form=form)


"""
    nom: edit_genre_film_selected
    On obtient un objet "objet_dumpbd"

    Récupère la liste de tous les genres du film sélectionné par le bouton "MODIFIER" de "films_genres_afficher.html"

    Dans une liste déroulante particulière (tags-selector-tagselect), on voit :
    1) Tous les genres contenus dans la "t_genre".
    2) Les genres attribués au film selectionné.
    3) Les genres non-attribués au film sélectionné.

    On signale les erreurs importantes

"""


@obj_mon_application.route("/edit_genre_film_selected", methods=['GET', 'POST'])
def edit_genre_film_selected():
    if request.method == "GET":
        try:
            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                strsql_genres_afficher = """SELECT id_email, email FROM t_email ORDER BY id_email ASC"""
                mc_afficher.execute(strsql_genres_afficher)
            data_genres_all = mc_afficher.fetchall()
            print("dans edit_genre_film_selected ---> data_genres_all", data_genres_all)

            # Récupère la valeur de "id_film" du formulaire html "films_genres_afficher.html"
            # l'utilisateur clique sur le bouton "Modifier" et on récupère la valeur de "id_film"
            # grâce à la variable "id_film_genres_edit_html" dans le fichier "films_genres_afficher.html"
            # href="{{ url_for('edit_genre_film_selected', id_film_genres_edit_html=row.id_film) }}"
            id_film_genres_edit = request.values['id_film_genres_edit_html']

            # Mémorise l'id du film dans une variable de session
            # (ici la sécurité de l'application n'est pas engagée)
            # il faut éviter de stocker des données sensibles dans des variables de sessions.
            session['session_id_film_genres_edit'] = id_film_genres_edit

            # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
            valeur_id_film_selected_dictionnaire = {"value_id_film_selected": id_film_genres_edit}

            # Récupère les données grâce à 3 requêtes MySql définie dans la fonction genres_films_afficher_data
            # 1) Sélection du film choisi
            # 2) Sélection des genres "déjà" attribués pour le film.
            # 3) Sélection des genres "pas encore" attribués pour le film choisi.
            # ATTENTION à l'ordre d'assignation des variables retournées par la fonction "genres_films_afficher_data"
            data_genre_film_selected, data_genres_films_non_attribues, data_genres_films_attribues = \
                genres_films_afficher_data(valeur_id_film_selected_dictionnaire)

            print(data_genre_film_selected)
            lst_data_film_selected = [item['id_user'] for item in data_genre_film_selected]
            print("lst_data_film_selected  ", lst_data_film_selected,
                  type(lst_data_film_selected))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les genres qui ne sont pas encore sélectionnés.
            lst_data_genres_films_non_attribues = [item['id_email'] for item in data_genres_films_non_attribues]
            session['session_lst_data_genres_films_non_attribues'] = lst_data_genres_films_non_attribues
            print("lst_data_genres_films_non_attribues  ", lst_data_genres_films_non_attribues,
                  type(lst_data_genres_films_non_attribues))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les genres qui sont déjà sélectionnés.
            lst_data_genres_films_old_attribues = [item['id_email'] for item in data_genres_films_attribues]
            session['session_lst_data_genres_films_old_attribues'] = lst_data_genres_films_old_attribues
            print("lst_data_genres_films_old_attribues  ", lst_data_genres_films_old_attribues,
                  type(lst_data_genres_films_old_attribues))

            print(" data data_genre_film_selected", data_genre_film_selected, "type ", type(data_genre_film_selected))
            print(" data data_genres_films_non_attribues ", data_genres_films_non_attribues, "type ",
                  type(data_genres_films_non_attribues))
            print(" data_genres_films_attribues ", data_genres_films_attribues, "type ",
                  type(data_genres_films_attribues))

            # Extrait les valeurs contenues dans la table "t_genres", colonne "intitule_genre"
            # Le composant javascript "tagify" pour afficher les tags n'a pas besoin de l'id_genre
            lst_data_genres_films_non_attribues = [item['email'] for item in data_genres_films_non_attribues]
            print("lst_all_genres gf_edit_genre_film_selected ", lst_data_genres_films_non_attribues,
                  type(lst_data_genres_films_non_attribues))

        except Exception as Exception_edit_genre_film_selected:
            code, msg = Exception_edit_genre_film_selected.args
            flash(f"{error_codes.get(code, msg)} ", "danger")
            flash(f"Exception edit_genre_film_selected : {sys.exc_info()[0]} "
                  f"{Exception_edit_genre_film_selected.args[0]} , "
                  f"{Exception_edit_genre_film_selected}", "danger")

    return render_template("films_genres/films_genres_modifier_tags_dropbox.html",
                           data_genres=data_genres_all,
                           data_film_selected=data_genre_film_selected,
                           data_genres_attribues=data_genres_films_attribues,
                           data_genres_non_attribues=data_genres_films_non_attribues)


"""
    nom: update_genre_film_selected

    Récupère la liste de tous les genres du film sélectionné par le bouton "MODIFIER" de "films_genres_afficher.html"

    Dans une liste déroulante particulière (tags-selector-tagselect), on voit :
    1) Tous les genres contenus dans la "t_genre".
    2) Les genres attribués au film selectionné.
    3) Les genres non-attribués au film sélectionné.

    On signale les erreurs importantes
"""


@obj_mon_application.route("/email_update", methods=['GET', 'POST'])
def emails_update_wtf():

    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_facture"
    id_email_update = request.values['id_email_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateGenre()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "destinataire_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            email_update = form_update.email_update_wtf.data

            email_update = email_update.lower()



            valeur_update_dictionnaire = {"value_id_email": id_email_update, "value_email": email_update,}
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_intitulegenre = """UPDATE t_email SET email = %(value_email)s WHERE id_email = %(value_id_email)s"""
            with MaBaseDeDonnee() as mconn_bd:
                mconn_bd.mabd_execute(str_sql_update_intitulegenre, valeur_update_dictionnaire)



            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_facture_update"
            return redirect(url_for('genres_afficher', order_by="ASC", id_genre_sel=id_email_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_facture" et "numero_facture" de la "t_facture"
            str_sql_id_facture = "SELECT id_email, email, FROM t_email WHERE id_email = %(value_id_email)s"
            valeur_select_dictionnaire = {"value_id_facture": id_email_update}
            mybd_curseur = MaBaseDeDonnee().connexion_bd.cursor()
            mybd_curseur.execute(str_sql_id_facture, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom genre" pour l'UPDATE
            data_nom_genre = mybd_curseur.fetchone()
            print("data_nom_genre ", data_nom_genre, " type ", type(data_nom_genre), " genre ",
                  data_nom_genre["email"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "destinataire_update_wtf.html"
            form_update.numero_facture_update_wtf.data = data_nom_genre["email"]

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

    return render_template("films_genres/emails_update_wtf.html", form_update=form_update)


@obj_mon_application.route("/update_genre_film_selected", methods=['GET', 'POST'])
def update_genre_film_selected():
    if request.method == "POST":
        try:
            # Récupère l'id du film sélectionné
            id_film_selected = session['session_id_film_genres_edit']
            print("session['session_id_film_genres_edit'] ", session['session_id_film_genres_edit'])

            # Récupère la liste des genres qui ne sont pas associés au film sélectionné.
            old_lst_data_genres_films_non_attribues = session['session_lst_data_genres_films_non_attribues']
            print("old_lst_data_genres_films_non_attribues ", old_lst_data_genres_films_non_attribues)

            # Récupère la liste des genres qui sont associés au film sélectionné.
            old_lst_data_genres_films_attribues = session['session_lst_data_genres_films_old_attribues']
            print("old_lst_data_genres_films_old_attribues ", old_lst_data_genres_films_attribues)

            # Effacer toutes les variables de session.
            session.clear()

            # Récupère ce que l'utilisateur veut modifier comme genres dans le composant "tags-selector-tagselect"
            # dans le fichier "genres_films_modifier_tags_dropbox.html"
            new_lst_str_genres_films = request.form.getlist('name_select_tags')
            print("new_lst_str_genres_films ", new_lst_str_genres_films)

            # OM 2021.05.02 Exemple : Dans "name_select_tags" il y a ['4','65','2']
            # On transforme en une liste de valeurs numériques. [4,65,2]
            new_lst_int_genre_film_old = list(map(int, new_lst_str_genres_films))
            print("new_lst_genre_film ", new_lst_int_genre_film_old, "type new_lst_genre_film ",
                  type(new_lst_int_genre_film_old))

            # Pour apprécier la facilité de la vie en Python... "les ensembles en Python"
            # https://fr.wikibooks.org/wiki/Programmation_Python/Ensembles
            # OM 2021.05.02 Une liste de "id_genre" qui doivent être effacés de la table intermédiaire "t_genre_film".
            lst_diff_genres_delete_b = list(
                set(old_lst_data_genres_films_attribues) - set(new_lst_int_genre_film_old))
            print("lst_diff_genres_delete_b ", lst_diff_genres_delete_b)

            # Une liste de "id_genre" qui doivent être ajoutés à la "t_genre_film"
            lst_diff_genres_insert_a = list(
                set(new_lst_int_genre_film_old) - set(old_lst_data_genres_films_attribues))
            print("lst_diff_genres_insert_a ", lst_diff_genres_insert_a)

            # SQL pour insérer une nouvelle association entre
            # "fk_film"/"id_film" et "fk_genre"/"id_genre" dans la "t_genre_film"
            strsql_insert_genre_film = """INSERT INTO t_user_email (id_user_email, fk_email, fk_user)
                                                    VALUES (NULL, %(value_fk_email)s, %(value_fk_user)s)"""

            # SQL pour effacer une (des) association(s) existantes entre "id_film" et "id_genre" dans la "t_genre_film"
            strsql_delete_genre_film = """DELETE FROM t_user_email WHERE fk_email = %(value_fk_email)s AND fk_user = %(value_fk_user)s"""

            with MaBaseDeDonnee() as mconn_bd:
                # Pour le film sélectionné, parcourir la liste des genres à INSÉRER dans la "t_genre_film".
                # Si la liste est vide, la boucle n'est pas parcourue.
                for id_genre_ins in lst_diff_genres_insert_a:
                    # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
                    # et "id_genre_ins" (l'id du genre dans la liste) associé à une variable.
                    valeurs_film_sel_genre_sel_dictionnaire = {"value_fk_user": id_film_selected,
                                                               "value_fk_email": id_genre_ins}

                    mconn_bd.mabd_execute(strsql_insert_genre_film, valeurs_film_sel_genre_sel_dictionnaire)

                # Pour le film sélectionné, parcourir la liste des genres à EFFACER dans la "t_genre_film".
                # Si la liste est vide, la boucle n'est pas parcourue.
                for id_genre_del in lst_diff_genres_delete_b:
                    # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
                    # et "id_genre_del" (l'id du genre dans la liste) associé à une variable.
                    valeurs_film_sel_genre_sel_dictionnaire = {"value_fk_user": id_film_selected,
                                                               "value_fk_email": id_genre_del}

                    # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
                    # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
                    # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
                    # sera interprété, ainsi on fera automatiquement un commit
                    mconn_bd.mabd_execute(strsql_delete_genre_film, valeurs_film_sel_genre_sel_dictionnaire)

        except Exception as Exception_update_genre_film_selected:
            code, msg = Exception_update_genre_film_selected.args
            flash(f"{error_codes.get(code, msg)} ", "danger")
            flash(f"Exception update_genre_film_selected : {sys.exc_info()[0]} "
                  f"{Exception_update_genre_film_selected.args[0]} , "
                  f"{Exception_update_genre_film_selected}", "danger")

    # Après cette mise à jour de la table intermédiaire "t_genre_film",
    # on affiche les films et le(urs) genre(s) associé(s).
    return redirect(url_for('films_genres_afficher', id_film_sel=id_film_selected))


"""
    nom: genres_films_afficher_data

    Récupère la liste de tous les genres du film sélectionné par le bouton "MODIFIER" de "films_genres_afficher.html"
    Nécessaire pour afficher tous les "TAGS" des genres, ainsi l'utilisateur voit les genres à disposition

    On signale les erreurs importantes
"""


def genres_films_afficher_data(valeur_id_film_selected_dict):
    print("valeur_id_film_selected_dict...", valeur_id_film_selected_dict)
    try:

        strsql_film_selected = """SELECT id_user, nom_user, GROUP_CONCAT(id_email) as GenresFilms FROM t_user_email
                                        INNER JOIN t_user ON t_user.id_user = t_user_email.fk_user
                                        INNER JOIN t_email ON t_email.id_email = t_user_email.fk_email
                                        WHERE id_user = %(value_id_film_selected)s"""

        strsql_genres_films_non_attribues = """SELECT id_email, email FROM t_email WHERE id_email not in(SELECT id_email as idGenresFilms FROM t_user_email
                                                    INNER JOIN t_user ON t_user.id_user = t_user_email.fk_user
                                                     INNER JOIN t_email ON t_email.id_email = t_user_email.fk_email
                                                    WHERE id_user = %(value_id_film_selected)s)"""

        strsql_genres_films_attribues = """SELECT id_user,id_email, email FROM t_user_email
											INNER JOIN t_user ON t_user.id_user = t_user_email.fk_user
                                            INNER JOIN t_email ON t_email.id_email = t_user_email.fk_email
                                            WHERE id_user = %(value_id_film_selected)s"""

        # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
        with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
            # Envoi de la commande MySql
            mc_afficher.execute(strsql_genres_films_non_attribues, valeur_id_film_selected_dict)
            # Récupère les données de la requête.
            data_genres_films_non_attribues = mc_afficher.fetchall()
            # Affichage dans la console
            print("genres_films_afficher_data ----> data_genres_films_non_attribues ", data_genres_films_non_attribues,
                  " Type : ",
                  type(data_genres_films_non_attribues))

            # Envoi de la commande MySql
            mc_afficher.execute(strsql_film_selected, valeur_id_film_selected_dict)
            # Récupère les données de la requête.
            data_film_selected = mc_afficher.fetchall()
            # Affichage dans la console
            print("data_film_selected  ", data_film_selected, " Type : ", type(data_film_selected))

            # Envoi de la commande MySql
            mc_afficher.execute(strsql_genres_films_attribues, valeur_id_film_selected_dict)
            # Récupère les données de la requête.
            data_genres_films_attribues = mc_afficher.fetchall()
            # Affichage dans la console
            print("data_genres_films_attribues ", data_genres_films_attribues, " Type : ",
                  type(data_genres_films_attribues))

            # Retourne les données des "SELECT"
            return data_film_selected, data_genres_films_non_attribues, data_genres_films_attribues
    except pymysql.Error as pymysql_erreur:
        code, msg = pymysql_erreur.args
        flash(f"{error_codes.get(code, msg)} ", "danger")
        flash(f"pymysql.Error Erreur dans genres_films_afficher_data : {sys.exc_info()[0]} "
              f"{pymysql_erreur.args[0]} , "
              f"{pymysql_erreur}", "danger")
    except Exception as exception_erreur:
        code, msg = exception_erreur.args
        flash(f"{error_codes.get(code, msg)} ", "danger")
        flash(f"Exception Erreur dans genres_films_afficher_data : {sys.exc_info()[0]} "
              f"{exception_erreur.args[0]} , "
              f"{exception_erreur}", "danger")
    except pymysql.err.IntegrityError as IntegrityError_genres_films_afficher_data:
        code, msg = IntegrityError_genres_films_afficher_data.args
        flash(f"{error_codes.get(code, msg)} ", "danger")
        flash(f"pymysql.err.IntegrityError Erreur dans genres_films_afficher_data : {sys.exc_info()[0]} "
              f"{IntegrityError_genres_films_afficher_data.args[0]} , "
              f"{IntegrityError_genres_films_afficher_data}", "danger")
