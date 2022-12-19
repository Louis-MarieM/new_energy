from django.db import models
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from scraping.services.constantes.constantes import Constantes as const

class Facture(models.Model):
    name = models.fields.CharField(max_length=100)
    path = models.fields.CharField(max_length=100)

    def launch():
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        wait = WebDriverWait(browser, 600)
        return browser

class User():

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def getUsername(self):
        return self.username

    def setUsername(self, username):
        self.username = username

    def getPassword(self):
        return self.password

    def setPassword(self, password):
        self.password = password

    # Pour chaque utilisateur, il y a un dossier de téléchargement par fournisseur, dont le nom est donné lors de l'appel.
    def getDownloadFolder(self, processId):
        return const.DOWNLOAD_PATH + processId
    
    # Pour chaque utilisateur, il y a un dossier output de découpage par fournisseur, dont le nom est donné lors de l'appel.
    def getDecoupageFolder(self, processId):
        return const.OUTPUT_DECOUPAGE_PATH + processId + '_cut\\'