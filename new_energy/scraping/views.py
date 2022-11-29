from django.shortcuts import render
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from rest_framework.views import APIView
from rest_framework.response import Response

from scraping.forms import LoginForm
from scraping.services.fournisseurs.totalenergies import FournisseurTotalEnergies as totalEnergies
from scraping.services.constantes.constantes import Constantes as const
from scraping.models import Facture
from scraping.serializers import FactureSerializer

def launcher(request):
    if request.method == 'POST':
        global wait, browser, Link
        form = LoginForm(request.POST)
        
        if form.is_valid():
            if (totalEnergies.energy_login(form.cleaned_data['identifier'], form.cleaned_data['password'], form.cleaned_data['website'])):
                return render(request, 'scraping/succes.html')
    else :
        form = LoginForm()
    return render(request, 'scraping/launcher.html', {'form': form})


class FactureView(APIView) :

    def get(self, *args, **kwargs) :
        success = False
        provider = ""
        username = ""
        password = ""
        provider = const.FOURNISSEURS[self.request.GET.get("provider")]
        username = self.request.GET.get("username")
        password = self.request.GET.get("password")
        print (provider, username, password)
        success = totalEnergies.energy_login(provider, username, password)
        return Response({
                "success" : success,
                "provider" : self.request.GET.get("provider"),
                "username" : username,
                "password" : password,
            })