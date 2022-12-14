import time, os, shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from PyPDF2 import PdfFileWriter, PdfFileReader

class FournisseurTotalEnergies:

    # provider : url du fournisseur
    def energy_login(provider, user, processId):
        global wait, browser, Link
        try:
            # On créer un dossier unique par fournisseur par utilisateur où les factures seront téléchargées.
            folderPath = user.getDownloadFolder(processId)
            if not os.path.exists(folderPath):
                os.mkdir(folderPath)
            # Options pour permettre l'utilisation du driver sur le serveur.
            options = webdriver.ChromeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            prefs = {"download.default_directory":folderPath}
            options.add_experimental_option("prefs", prefs)
            browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            wait = WebDriverWait(browser, 600)
            browser.get(provider)

            try:
                time.sleep(1)
                input_identifiant = browser.find_element("xpath", '//*[@id="tx_deauthentification_login"]')
                input_pwd = browser.find_element("xpath", '//*[@id="tx_deauthentification_password"]')
                input_submit = browser.find_element("xpath", '//*[@id="tx_deauthentification_mdp_oublie"]')

                input_identifiant.click()
                input_identifiant.send_keys(user.getUsername())
                time.sleep(1)
                input_pwd.click()
                input_pwd.send_keys(user.getPassword())
                time.sleep(1)
                input_submit.click()

                try:
                    button_factures = browser.find_element("xpath", '//*[@id="header"]/div[4]/div/ul/li[2]/a')
                except NoSuchElementException:
                    return False
                
            except Exception as e:
                return False

        except Exception as e:
            return False
        return True



    def access_factures():
        try:
            button_factures = browser.find_element("xpath", '//*[@id="header"]/div[4]/div/ul/li[2]/a')
            button_factures.click()
        except Exception as e:
            browser.quit()
            print(str(e))

    def download_factures():
        try:
            time.sleep(2)
            nb_pages = browser.find_element("xpath", '// *[ @ id = "table_facture_paginate"] / span / a[6]')
            # on transforme le nombre de pages en nombre pour pouvoir le loop
            local_pages = int(nb_pages.text)
            print("Nombre de pages détectées : ", str(local_pages))
        except Exception as e:
            browser.quit()
            print(str(e))
            return False

        try:
            #on scroll toutes les pages où il y a des factures
            for i in range(1,local_pages):
                #on scroll les 10 factures sur chaque page
                for y in range(1,11):
                    time.sleep(1)
                    download_bill = browser.find_element("xpath", '//*[@id="table_facture"]/tbody/tr['+str(y)+']/td[8]/a')
                    download_bill.click()
                time.sleep(1)
                print(">>> Page "+str(i)+" téléchargée")
                next_button = browser.find_element("xpath", '//*[@id="table_facture_next"]')
                next_button.click()
                return True
        except Exception as e:
            browser.quit()
            print(str(e))
            return False
        browser.quit()
        return True

    def decoupage(user, processId):
        directory = user.getDownloadFolder(processId)
        outputFolderPath = user.getDecoupageFolder(processId)
        if not os.path.exists(outputFolderPath):
            os.mkdir(outputFolderPath)
        for file in os.listdir(directory):
            if not file.endswith(".pdf"):
                continue
            with open(os.path.join(directory,file), 'rb') as pdfFileObj:  # Changes here
                pdfReader = PdfFileReader(pdfFileObj)
                if pdfReader.numPages<3:
                    shutil.copyfile(os.path.join(directory,file), outputFolderPath + file)
                else:
                    for i in range(1, pdfReader.numPages - 1):
                        output = PdfFileWriter()
                        output.addPage(pdfReader.getPage(0))
                        output.addPage(pdfReader.getPage(i + 1))

                        export_filename = '{} - {}.pdf'.format(os.path.splitext(file)[0], i)
                        with open(outputFolderPath + export_filename, "wb") as outputStream:
                            output.write(outputStream)
        return True
