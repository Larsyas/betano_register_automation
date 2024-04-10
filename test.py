import pyautogui
from pathlib import Path
from time import sleep
from selenium.webdriver.firefox.service import Service as FirefoxService
# from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver
from utils.commands import profile_path

ROOT_DIR = Path(__file__).parent
CAPTCHA_IMG = f'{ROOT_DIR}\\images\\betano_vpn_captcha_indicator.png'


def verifica_se_email_existe():
    try:
        global email_already_exists
        email_already_exists = pyautogui.locateOnScreen(
            EMAIL_ALREADY_EXISTS,
            4, confidence=0.9
        )

        while email_already_exists:
            tentativas_de_email = 0
            print(
                f'"{conta.email}" está oficialmente repleto de câncer, é realmente uma pena, tão jovem...')
            print(
                f'Passando para o proximo, ainda restam {account_num} contas na DB.')
            try:
                # Se a imagem foi encontrada, passa para a próxima conta
                conta = iterator.next_account()

                # Apaga o e-mail em uso e tenta com o próximo
                pyautogui.click(1193, 380, duration=.2, clicks=3, interval=.2)
                bind.type(conta.email)
                sleep(2)

                # Tenta localizar a imagem EMAIL_ALREADY_EXISTS na tela novamente
                pyautogui.locateOnScreen(
                    EMAIL_ALREADY_EXISTS, 4, confidence=0.9)

                print()
                print('Email ja existe, tentando com o proximo.')
                print(account_num, 'contas restantes.')
                print()

                tentativas_de_email += 1

                if tentativas_de_email == 3:
                    print('Muitas tentativas de email. Verifique a DB.')
                    exit()

            except pyautogui.ImageNotFoundException:
                # Se a imagem não foi encontrada, significa que o e-mail não existe na Betano.
                email_already_exists = False

    # Se a imagem não foi encontrada, significa que o e-mail não existe na Betano.
    except pyautogui.ImageNotFoundException:
        email_already_exists = False
        pass
