from django.shortcuts import render
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from scraping.forms import LoginForm

def launcher(request):
    if request.method == 'POST':
        global wait, browser, Link
        form = LoginForm(request.POST)
        if form.is_valid():
            options = webdriver.ChromeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            wait = WebDriverWait(browser, 600)
            print("URL: ",form.cleaned_data['website'])
            browser.get(form.cleaned_data['website'])
            browser.maximize_window()
            print("page ouverte")
            time.sleep(2)
            input_identifiant = browser.find_element("xpath", '//*[@id="tx_deauthentification_login"]')
            input_pwd = browser.find_element("xpath", '//*[@id="tx_deauthentification_password"]')
            input_submit = browser.find_element("xpath", '//*[@id="tx_deauthentification_mdp_oublie"]')

            input_identifiant.click()
            input_identifiant.send_keys(form.cleaned_data['identifier'])
            time.sleep(1)
            input_pwd.click()
            input_pwd.send_keys(form.cleaned_data['password'])
            time.sleep(1)
            input_submit.click()
    else :
        form = LoginForm()
    return render(request, 'scraping/launcher.html', {'form': form})