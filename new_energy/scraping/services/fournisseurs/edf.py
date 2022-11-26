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
        browser.get("https://auth.entreprises-collectivites.edf.fr/openam/XUI/#login/&realm=%2Ffront_office&goto=https%3A%2F%2Fauth.entreprises-collectivites.edf.fr%2Fopenam%2Foauth2%2Fauthorize%3Fresponse_type%3Dcode%26scope%3Dopenid%2520profile%2520sso_token%26client_id%3DICE%26state%3D0Oh4buG25ABf6o2gURUYMy92HtY%26redirect_uri%3Dhttps%253A%252F%252Fwww.edfcollectivites.fr%252Frest%252Foidc%252FredirectURI.html%26nonce%3DhgqfK7rG0y7rq_qZJmurVa6bYJ2mQonn6fTrSWsfTrA%26response_mode%3Dquery")
        #browser.maximize_window()
        print("page ouverte")

        try:
            time.sleep(2)
            input_identifiant = browser.find_element("xpath", '//*[@id="idToken1"]')
            input_pwd = browser.find_element("xpath", '//*[@id="idToken2"]')
            input_submit = browser.find_element("xpath", '//*[@id="loginButton_0"]')

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
        time.sleep(10)
        browser.get("https://www.edfcollectivites.fr/content/ice-pmsc/homepage.html#/accueil")
        try:
            time.sleep(15)
            browser.find_element("xpath", '//*[@id="poursuivrepopin"]').click()
        except Exception as e:
            print(e)
            pass
        try:
            time.sleep(15)
            browser.find_element("xpath", '//*[@id="carousel-site-0"]').click()
            try:
                time.sleep(15)
                button_factures = browser.find_element("xpath", '//*[@id="ice-header-menu-factures"]/a')
                button_factures.click()
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)
            pass

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

