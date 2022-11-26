import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager



def energy_login(identifiant, pwd):
    global wait, browser, Link

    try:
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        wait = WebDriverWait(browser, 600)
        browser.get("https://clientsgc.totalenergies.fr/connexion-clients-collectivites/")
        #browser.maximize_window()
        print("page ouverte")

        try:
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
        except Exception as e:
            print(e)

    except Exception as e:
        print(e)



def access_factures():
    try:
        button_factures = browser.find_element("xpath", '//*[@id="header"]/div[4]/div/ul/li[2]/a')
        button_factures.click()
    except Exception as e:
        print(e)

def download_factures():
    try:
        time.sleep(5)
        nb_pages = browser.find_element("xpath", '// *[ @ id = "table_facture_paginate"] / span / a[6]')
        # on transforme le nombre de pages en nombre pour pouvoir le loop
        local_pages = int(nb_pages.text)
        print("Nombre de pages détectées : ", str(local_pages))
    except Exception as e:
        print(e)

    try:
        #on scroll toutes les pages où il y a des factures
        for i in range(1,local_pages):
            time.sleep(4)
            #on scroll les 10 factures sur chaque page
            for y in range(1,11):
                time.sleep(1)
                download_bill = browser.find_element("xpath", '//*[@id="table_facture"]/tbody/tr['+str(y)+']/td[8]/a')
                download_bill.click()
            time.sleep(2)
            print(">>> Page "+str(i)+" téléchargée")
            next_button = browser.find_element("xpath", '//*[@id="table_facture_next"]')
            next_button.click()
    except Exception as e:
        print(e)

