from django.shortcuts import render
import os
from rest_framework.views import APIView
from rest_framework.response import Response

from scraping.forms import LoginForm
from scraping.services.fournisseurs.totalenergies import FournisseurTotalEnergies as totalEnergies
from scraping.services.constantes.constantes import Constantes as const
from scraping.models import User

def launcher(request):
    if request.method == 'POST':
        global wait, browser, Link
        form = LoginForm(request.POST)
        
        if form.is_valid():
            print("Les logs sont : " + form.cleaned_data['website'], form.cleaned_data['identifier'], form.cleaned_data['password'])
            totalEnergies.energy_login("https://clientsgc.totalenergies.fr/connexion-clients-collectivites/", form.cleaned_data['identifier'], form.cleaned_data['password'])
            totalEnergies.access_factures()
            totalEnergies.download_factures()
            return render(request, 'scraping/succes.html')
    else :
        form = LoginForm()
    return render(request, 'scraping/launcher.html', {'form': form})


class UserView(APIView) :

    def get(self, *args, **kwargs) :
        success = False
        provider = ""
        username = ""
        password = ""
        try:
            provider = const.FOURNISSEURS[self.request.GET.get("provider")]
            username = self.request.GET.get("username")
            password = self.request.GET.get("password")
            success = totalEnergies.energy_login(provider, username, password)
            return Response({
                    "success" : success,
                    "provider" : self.request.GET.get("provider"),
                    "username" : username,
                    "password" : password,
                })
        except Exception as e :
            return Response({'error' : e.args})

class FactureView(APIView) : 

    def get(self, *args, **kwargs) :
        success = False
        message = ""
        provider = ""
        user = User("", "")
        filenames = ""
        try :
            provider = const.FOURNISSEURS[self.request.GET.get("provider")]
            user.setUsername(self.request.GET.get("username"))
            user.setPassword(self.request.GET.get("password"))
            totalEnergies.energy_login(provider, user)
            totalEnergies.access_factures()
            success = totalEnergies.download_factures()
        except Exception as e :
            message = e
        if success:
            folderName = user.getDownloadFolder(provider)
            filenames = os.listdir(folderName)
        return Response({
                "success" : success,
                "message" : message,
                "filenames" : filenames,
                "provider" : provider,
                "username" : user.getUsername(),
                "password" : user.getPassword()
            })
            