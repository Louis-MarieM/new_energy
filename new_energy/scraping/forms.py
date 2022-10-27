from django import forms
from scraping.services.constantes.constantes import Constantes as cst

class LoginForm(forms.Form):
    identifier = forms.CharField(initial="0107303952_facturation")
    password = forms.CharField(initial="gBhnGurgJX")
    # Champ vide.
    Choices = [("", "----------")]
    Choices += cst.FOURNISSEURS
    website = forms.ChoiceField(choices=Choices, required=True)