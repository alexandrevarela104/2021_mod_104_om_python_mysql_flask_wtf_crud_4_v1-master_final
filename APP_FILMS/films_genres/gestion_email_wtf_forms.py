"""
    Fichier : gestion_destinataires_wtf_forms.py
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
        Dans le formulaire "destinataire_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    email_regexp = "^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$"
    email_wtf = StringField("Clavioter l'adresse mail ",
                            validators=[Length(min=2, max=50, message="min 2 max 20"),
                                        Regexp(email_regexp,
                                               message="N'oubliez pas le @, "
                                                       "le domaine (gmail,hotmail etc...), "
                                                       "pas d'espace, "
                                                       "l'extension (.com, .ch etc...)")
                                        ])

    submit = SubmitField("Enregistrer genre")


class FormWTFUpdateGenre(FlaskForm):
    """
        Dans le formulaire "destinataire_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    email_regexp = "^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$"
    email_update_wtf = StringField("Clavioter l'adresse mail ",
                            validators=[Length(min=2, max=50, message="min 2 max 20"),
                                        Regexp(email_regexp,
                                               message="N'oubliez pas le @, "
                                                       "le domaine (gmail,hotmail etc...), "
                                                       "pas d'espace, "
                                                       "l'extension (.com, .ch etc...)")
                                        ])

    submit = SubmitField("Enregistrer genre")

class FormWTFDeleteGenre(FlaskForm):
    """
        Dans le formulaire "destinataire_update_wtf.html"

        nom_user_delete_wtf : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "genre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_user".
    """
    nom_user_delete_wtf = StringField("Effacer cet email")
    submit_btn_del = SubmitField("Effacer email")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
