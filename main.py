import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


Link = "https://clientsgc.totalenergies.fr/connexion-clients-collectivites/"
identifiant = "0107303952_facturation"
pwd = "gBhnGurgJX"




def energy_login():
    global wait, browser, Link

    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    wait = WebDriverWait(browser, 600)
    browser.get(Link)
    browser.maximize_window()
    print("page ouverte")
    time.sleep(2)
    input_identifiant = browser.find_element("xpath", '//*[@id="tx_deauthentification_login"]')
    input_pwd = browser.find_element("xpath", '//*[@id="tx_deauthentification_password"]')
    input_submit = browser.find_element("xpath", '//*[@id="tx_deauthentification_mdp_oublie"]')

    input_identifiant.click()
    input_identifiant.send_keys(identifiant)
    time.sleep(1)
    input_pwd.click()
    input_pwd.send_keys(pwd)
    time.sleep(1)
    input_submit.click()

def access_factures():
    button_factures = browser.find_element("xpath", '//*[@id="header"]/div[4]/div/ul/li[2]/a')
    button_factures.click()

def download_factures():
    time.sleep(1)
    nb_pages = browser.find_element("xpath", '//*[@id="table_facture_paginate"]/span/a[6]')
    # on transforme le nombre de pages en nombre pour pouvoir le loop
    local_pages = int(nb_pages.text)
    print("Nombre de pages détectées : ", str(local_pages))
    for i in range(local_pages-2):
        download_csv = browser.find_element("xpath", '//*[@id="btn_export"]')
        download_csv.click()
        time.sleep(1)
        next_button = browser.find_element("xpath", '//*[@id="table_facture_next"]')
        next_button.click()

##############################################################################
##############################################################################
##############################################################################

if __name__ == "__main__":
    print("Je démarre le navigateur")

    energy_login()

    access_factures()

    download_factures()
    print("Téléchargement terminé")