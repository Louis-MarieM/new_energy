from django.shortcuts import render
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from scraping.forms import LoginForm
from scraping.services.fournisseurs.totalenergies import FournisseurTotalEnergies as totalEnergies

def launcher(request):
    if request.method == 'POST':
        global wait, browser, Link
        form = LoginForm(request.POST)
        
        if form.is_valid():
            if (totalEnergies.energy_login(form.cleaned_data['identifier'], form.cleaned_data['password'], form.cleaned_data['website'])):
                return render(request, 'scraping/launcher.html', {'form': form})
            else:
                form = LoginForm()
    else :
        form = LoginForm()
    return render(request, 'scraping/launcher.html', {'form': form})