"""
    Fichier : gestion_destinataires_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.html5 import DateField
from wtforms import SelectField
from wtforms import SubmitField
from wtforms.validators import Length, DataRequired
from wtforms.validators import Regexp


class FormWTFAjouterGenres(FlaskForm):
    """
        Dans le formulaire "destinataire_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    numero_facture_regexp = "^-?[0-9][0-9,\.]+$"
    numero_facture_wtf = StringField("Clavioter le numero de votre facture, Vous ne pourrez pas ajouter un numéro de facture qui existe déjà ",
                                            validators=[Length(min=2, max=11, message="min 2 max 11"),
                                                        Regexp(numero_facture_regexp,
                                                               message="Veuillez entrer un numéro de facture correct")
                                                        ])
    somme_regexp = "^-?[0-9][0-9,\.]+$"
    somme_wtf = StringField("Clavioter le montant de la facture ",
                                   validators=[Length(min=2, max=50, message="min 2 max 50"),
                                               Regexp(somme_regexp,
                                                      message="Veuillez entrer une somme correcte")
                                               ])
    delai_regexp = "^-?[0-9][0-9,\.]+$"
    delai_wtf = DateField("Clavioter le jour du délai de payement", format="%Y-%m-%d")

    payement_wtf = DateField("Clavioter la date de payement. ",  format="%Y-%m-%d")

    submit = SubmitField("Enregistrer genre")


class FormWTFUpdateGenre(FlaskForm):
    """
        Dans le formulaire "destinataire_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    numero_facture_regexp = "^-?[0-9][0-9,\.]+$"
    numero_facture_update_wtf = StringField("Clavioter le numero de votre facture ",
                                      validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                  Regexp(numero_facture_regexp,
                                                         message="pas d'espace",)
                                                  ])
    somme_regexp = "^-?[0-9][0-9,\.]+$"
    somme_update_wtf = StringField("Clavioter le montant de la facture ",
                            validators=[Length(min=2, max=50, message="min 2 max 20"),
                                        Regexp(somme_regexp,
                                               message="N'oubliez pas le @, "
                                                       "le domaine (gmail,hotmail etc...), "
                                                       "pas d'espace, "
                                                       "l'extension (.com, .ch etc...)")
                                        ])
    delai_regexp = "^-?[0-9][0-9,\.]+$"
    delai_update_wtf = StringField("Clavioter le delai. Exemple = yyyy-mm-dd ",
                                   validators=[Length(min=2, max=20, message="min 2 max 20")
                                               ])
    payement_regexp = "^-?[0-9][0-9,\.]+$"
    payement_update_wtf = StringField("Clavioter la date de payement. Exemple = yyyy-mm-dd",
                                   validators=[Length(min=2, max=20, message="min 2 max 20")
                                               ])
    submit = SubmitField("Enregistrer genre")

class FormWTFDeleteGenre(FlaskForm):
    """
        Dans le formulaire "destinataire_delete_wtf.html"

        numero_facture_delete_wtf : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "genre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_user".
    """
    numero_facture_delete_wtf = StringField("Effacer cet utilisateur")
    submit_btn_del = SubmitField("Effacer genre")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
