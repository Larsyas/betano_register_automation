import pyautogui
from pathlib import Path
from time import sleep
from selenium.webdriver.firefox.service import Service as FirefoxService
# from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver
from utils.commands import profile_path

ROOT_DIR = Path(__file__).parent
CAPTCHA_IMG = f'{ROOT_DIR}\\images\\betano_vpn_captcha_indicator.png'


def procura_captcha(firefoxDriver: webdriver.Firefox, firefoxOptions: webdriver.FirefoxOptions):

    def _procedimento_captcha(firefoxDriver: webdriver.Firefox, firefoxOptions: webdriver.FirefoxOptions):
        firefoxDriver.quit()
        # Verifica se o driver está usando abas anônimas
        if '--private' in firefoxOptions.arguments:
            print("O driver estava usando abas anônimas. Mudando para abas normais.")
            # Remova a opção '--private' para usar abas normais
            firefoxOptions.arguments.remove('--private')
            sleep(1)

            # firefoxDriver = webdriver.Firefox(
            #     service=service, options=firefoxOptions)
            # firefoxDriver.maximize_window()
        else:
            print("O driver não estava usando abas anônimas. Mudando para abas anônimas.")
            # Adicione a opção '--private' para usar abas anônimas
            firefoxOptions.arguments.append('--private')
            sleep(1)

        # firefoxDriver = webdriver.Firefox(
        #     service=service, options=firefoxOptions)
        # firefoxDriver.maximize_window()

        return firefoxOptions

    try:
        captcha = pyautogui.locateOnScreen(CAPTCHA_IMG, 10)

        if captcha:
            print('MEU DEUS O GUSTAVO LIMA SOCORRO')
            sleep(1)
            _procedimento_captcha(firefoxDriver=driver, firefoxOptions=options)

    except pyautogui.ImageNotFoundException:
        print('N consegui achar a imagem, continuaria o processo daqui.')
        sleep(3)
        firefoxDriver.quit()


def instancia_driver():
    global driver
    driver = webdriver.Firefox(service=service, options=options)
    driver.maximize_window()


options = webdriver.FirefoxOptions()
options.add_argument('--private')
options.add_argument("--disable-blink-features=AutomationControlled")
options.set_preference("dom.webdriver.enabled", False)
options.set_preference('useAutomationExtension', False)
options.set_preference("dom.webnotifications.enabled", False)
options.set_preference("geo.enabled", False)
options.set_preference("geo.provider.use_corelocation", False)
options.set_preference("geo.prompt.testing", False)
options.set_preference("geo.prompt.testing.allow", False)
options.set_preference("dom.push.enabled", False)
options.set_preference("media.navigator.enabled", False)
options.set_preference("media.navigator.permission.disabled", True)
options.set_preference("media.navigator.streams.fake", True)
options.set_preference("media.peerconnection.enabled", False)
options.set_preference("media.peerconnection.identity.timeout", 1)
options.set_preference("media.peerconnection.turn.disable", True)
options.set_preference("media.peerconnection.use_document_iceservers", False)
options.set_preference("media.peerconnection.video.enabled", False)
options.profile = profile_path

service = FirefoxService()


x = 1
for _ in range(3):
    instancia_driver()
    print('iter: ', x)
    print('Firefox Options Arguments: ', options.arguments)
    procura_captcha(firefoxDriver=driver, firefoxOptions=options)
    x += 1
