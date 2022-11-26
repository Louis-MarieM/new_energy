import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager



def energy_login(identifiant, pwd):
    global wait, browser, Link

    try:
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        wait = WebDriverWait(browser, 600)
        browser.get("https://backoffice.unergie.com/b2g-home-v2")
        #browser.maximize_window()
        print("Page ouverte")

        try:
            time.sleep(2)
            input_identifiant = browser.find_element("xpath", '//*[@id="iptLogin"]')
            input_pwd = browser.find_element("xpath", '//*[@id="iptPassword"]')
            input_submit = browser.find_element("xpath", '//*[@id="btnLogin"]')

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
        time.sleep(2)
        deploy_menu = browser.find_element("xpath", '//*[@id="menu_billing"]')
        deploy_menu.click()
        time.sleep(1)
        button_factures = browser.find_element("xpath", '//*[@id="submenu_myMetaInvoicesB2G"]')
        button_factures.click()
    except Exception as e:
        print(e)

def download_factures():
    try:
        time.sleep(5)
        nb_pages = browser.find_element("xpath", '/html/body/ui-view/div[2]/div/div[2]/ui-view/div/div[1]/div[2]/h4')
        # on transforme le nombre de pages en nombre pour pouvoir le loop
        local_pages = int(re.sub("[^0-9]", "", nb_pages.text))
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
                download_bill = browser.find_element("xpath", '/html/body/ui-view/div[2]/div/div[2]/ui-view/div/div[3]/table/tbody/tr[1]/td[2]/span/a')
                download_bill.click()
            time.sleep(2)
            print(">>> Page "+str(i)+" téléchargée")
            next_button = browser.find_element("xpath", '/html/body/ui-view/div[2]/div/div[2]/ui-view/div/div[3]/div/div/div/ul/li[4]/a')
            next_button.click()
    except Exception as e:
        print(e)

