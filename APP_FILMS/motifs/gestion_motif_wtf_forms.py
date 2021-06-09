"""
    Fichier : gestion_destinataires_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import DateField
from wtforms import SelectField
from wtforms import SubmitField
from wtforms.validators import Length, DataRequired
from wtforms.validators import Regexp


class FormWTFAjouterGenres(FlaskForm):
    """
        Dans le formulaire "destinataire_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    motif_regexp = "^[A-Za-z0-9 ]*[A-Za-z0-9][A-Za-z0-9 ]*$"
    motif_wtf = StringField("Clavioter le numero de votre facture ",
                                            validators=[Length(min=2, max=80, message="min 2 max 20"),
                                                        Regexp(motif_regexp,
                                                               message="pas d'espace")
                                                        ])


    submit = SubmitField("Enregistrer genre")


class FormWTFUpdateGenre(FlaskForm):
    """
        Dans le formulaire "destinataire_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    motif_regexp = "^[A-Za-z0-9 ]*[A-Za-z0-9][A-Za-z0-9 ]*$"
    motif_update_wtf = StringField("Clavioter le motif de la facture ",
                                      validators=[Length(min=2, max=80, message="min 2 max 20"),
                                                  Regexp(motif_regexp,
                                                         message="pas d'espace")
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
    motif_delete_wtf = StringField("Effacer cet utilisateur")
    submit_btn_del = SubmitField("Effacer genre")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
