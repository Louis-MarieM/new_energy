from django.db import models
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

class Facture(models.Model):
    name = models.fields.CharField(max_length=100)
    path = models.fields.CharField(max_length=100)

    def launch():
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        wait = WebDriverWait(browser, 600)
        return browser