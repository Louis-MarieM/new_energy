import time, os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

from scraping.services.constantes.constantes import Constantes as const

class FournisseurTotalEnergies:

    def energy_login(provider, username, password):
        global wait, browser, Link
        try:
            # On récupère le libellé du fournisseur.
            # Puis on créer un dossier unique par fournisseur par utilisateur où les factures seront téléchargées.
            key_list = list(const.FOURNISSEURS.keys())
            val_list = list(const.FOURNISSEURS.values())
            position = val_list.index(provider)
            folderName = key_list[position] + username + password
            if not os.path.exists(folderName):
                os.mkdir(folderName)
            # Options pour permettre l'utilisation du driver sur le serveur.
            options = webdriver.ChromeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            prefs = {"download.default_directory":const.DOWNLOAD_PATH + folderName}
            options.add_experimental_option("prefs", prefs)
            browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            wait = WebDriverWait(browser, 600)
            browser.get(provider)

            try:
                time.sleep(2)
                input_identifiant = browser.find_element("xpath", '//*[@id="tx_deauthentification_login"]')
                input_pwd = browser.find_element("xpath", '//*[@id="tx_deauthentification_password"]')
                input_submit = browser.find_element("xpath", '//*[@id="tx_deauthentification_mdp_oublie"]')

                input_identifiant.click()
                input_identifiant.send_keys(username)
                time.sleep(1)
                input_pwd.click()
                input_pwd.send_keys(password)
                time.sleep(1)
                input_submit.click()

                try:
                    button_factures = browser.find_element("xpath", '//*[@id="header"]/div[4]/div/ul/li[2]/a')
                except NoSuchElementException:
                    return e
                
            except Exception as e:
                return e

        except Exception as e:
            return e
        return True



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
            return e

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
                return True
        except Exception as e:
            return e
        return True

