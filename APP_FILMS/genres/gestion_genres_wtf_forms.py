"""
    Fichier : gestion_factures_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import Length
from wtforms.validators import Regexp


class FormWTFAjouterGenres(FlaskForm):
    """
        Dans le formulaire "genres_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_user_regexp = "^[a-zA-Z0-9]([._-](?![._-])|[a-zA-Z0-9]){3,18}[a-zA-Z0-9]$"
    nom_user_wtf = StringField("Clavioter le nom d'utilisateur ",
                                      validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                  Regexp(nom_user_regexp,
                                                         message="Pas de chiffres, de caractères "
                                                                 "spéciaux, "
                                                                 "d'espace à double, de double "
                                                                 "apostrophe, de double trait union")
                                                  ])
    email_regexp = "^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$"
    email_wtf = StringField("Clavioter l'adresse mail ",
                            validators=[Length(min=2, max=50, message="min 2 max 20"),
                                        Regexp(email_regexp,
                                               message="N'oubliez pas le @, "
                                                       "le domaine (gmail,hotmail etc...), "
                                                       "pas d'espace, "
                                                       "l'extension (.com, .ch etc...)")
                                        ])

    mot_de_passe_regexp = "^([A-Za-z0-9]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    mot_de_passe_wtf = StringField("Clavioter le mot de passe ",
                                   validators=[Length(min=2, max=20, message="min 2 max 20"),
                                               Regexp(mot_de_passe_regexp,
                                                      message="Pas de chiffres, de caractères "
                                                              "spéciaux, "
                                                              "d'espace à double, de double "
                                                              "apostrophe, de double trait union")
                                               ])
    submit = SubmitField("Enregistrer genre")


class FormWTFUpdateGenre(FlaskForm):
    """
        Dans le formulaire "genre_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_user_regexp = "^[a-zA-Z0-9]([._-](?![._-])|[a-zA-Z0-9]){3,18}[a-zA-Z0-9]$"
    nom_user_update_wtf = StringField("Clavioter le nom d'utilisateur ",
                                      validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                  Regexp(nom_user_regexp,
                                                         message="pas d'espace")
                                                  ])
    email_regexp = "^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$"
    email_update_wtf = StringField("Clavioter l'adresse mail ",
                            validators=[Length(min=2, max=50, message="min 2 max 50"),
                                        Regexp(email_regexp,
                                               message="N'oubliez pas le @, "
                                                       "le domaine (gmail,hotmail etc...), "
                                                       "pas d'espace, "
                                                       "l'extension (.com, .ch etc...)")
                                        ])
    mot_de_passe_regexp = "^[a-zA-Z0-9]([._-](?![._-])|[a-zA-Z0-9]){3,18}[a-zA-Z0-9]$"
    mot_de_passe_update_wtf = StringField("Clavioter le mot de passe ",
                                   validators=[Length(min=2, max=20, message="min 2 max 20")
                                               ])
    submit = SubmitField("Enregistrer genre")

class FormWTFDeleteGenre(FlaskForm):
    """
        Dans le formulaire "genre_update_wtf.html"

        nom_user_delete_wtf : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "genre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_user".
    """
    nom_user_delete_wtf = StringField("Effacer cet utilisateur")
    submit_btn_del = SubmitField("Effacer genre")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
