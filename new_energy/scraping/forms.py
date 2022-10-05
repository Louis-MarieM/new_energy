from django import forms

class LoginForm(forms.Form):
    identifier = forms.CharField(initial="0107303952_facturation")
    password = forms.CharField(initial="gBhnGurgJX")
    website = forms.CharField(initial="https://clientsgc.totalenergies.fr/connexion-clients-collectivites/")