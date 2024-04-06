import pyautogui
from months import months
from utils.data_usage_test import AccountIterator, Conta
from pynput.keyboard import Controller, Key
from utils.commands import profile_path, DEFAULT_PASSWORD
from time import sleep
from selenium import webdriver
from utils.register_address import FakeAddress
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
import datetime
from utils.test import FakeData
from pathlib import Path

ROOT_DIR = Path(__file__).parent  # (Sou_um_ser_humano_confia)
CAPTCHA_IMG = f'{ROOT_DIR}\\images\\betano_vpn_captcha_indicator.png'

iterator = AccountIterator()
iterator.connect_to_db()

service = FirefoxService(executable_path=GeckoDriverManager().install())

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


# options = Options()
# options.add_argument("--private-window")


bind = Controller()


def procura_captcha(firefoxDriver: webdriver.Firefox, firefoxOptions: webdriver.FirefoxOptions):

    def _procedimento_captcha(firefoxDriver: webdriver.Firefox, firefoxOptions: webdriver.FirefoxOptions):
        # This function closes the driver, resets ip and change tab functioning
        firefoxDriver.quit()

        # ALTERA ENTRE ABAS PRIVATE E NORMAL
        if '--private' in firefoxOptions.arguments:
            print("O driver estava usando abas anônimas. Mudando para abas normais.")
            firefoxOptions.arguments.remove('--private')
            sleep(1)

        else:
            print("O driver não estava usando abas anônimas. Mudando para abas anônimas.")
            # Adicione a opção '--private' para usar abas anônimas
            firefoxOptions.arguments.append('--private')
            sleep(1)

        reset_vpn()

        return firefoxOptions

    try:
        captcha = pyautogui.locateOnScreen(CAPTCHA_IMG, 10)

        if captcha:
            print('Got into a captcha, now starting captcha correction process.')
            sleep(1)
            _procedimento_captcha(firefoxDriver=driver, firefoxOptions=options)

    except pyautogui.ImageNotFoundException:
        print('Did not got into the first registration captcha, continuing now.')

    captcha


def reset_vpn():

    # search for norton on windows search
    bind.tap(Key.cmd)
    sleep(2)
    pyautogui.typewrite("Norton 360", interval=0.1)
    sleep(2)

    # opens it
    bind.tap(Key.enter)
    sleep(5)

    # turns vpn off and on again
    print('clicando no vpn')
    pyautogui.click(1347, 629, duration=.2)
    sleep(20)
    pyautogui.click(1347, 629, duration=.2)
    sleep(6)

    bind.press(Key.alt_l)
    bind.tap(Key.f4)
    bind.release(Key.alt_l)


def save_info_to_db():
    conta.date_of_creation = datetime.datetime.now()


def connect_to_phone():
    # This function presumes you're in the pc desktop.

    def restart_ip():

        # clicks airplane phone mode (turn on)
        pyautogui.click(851, 583, duration=.5)
        sleep(15)

        # clicks airplane phone mode (turn off)
        pyautogui.click(851, 583, duration=.5)
        sleep(7)

        # turns phone wifi router back on
        pyautogui.click(1044, 580, duration=.5)
        sleep(5)

        # minimizes everything
        bind.press(Key.cmd)
        bind.type('d')
        bind.release(Key.cmd)

        # # clicks internet options
        # pyautogui.click(856, 294, duration=.5)
        # sleep(2)

        # # turns 4g on
        # pyautogui.click(1110, 631, duration=.5)
        # sleep(3)

        # # closes internet options
        # pyautogui.click(1096, 937, duration=.5)
        # sleep(2)

    # opens scrcpy
    bind.press(Key.cmd)
    bind.type('6')
    bind.release(Key.cmd)
    sleep(10)

    restart_ip()


def _switchTab(i):
    driver.switch_to.window(driver.window_handles[i])


def access_betano():
    global driver
    driver = webdriver.Firefox(service=service, options=options)
    driver.maximize_window()

    driver.get('https://br.betano.com/')
    sleep(2)
    bind.tap(Key.esc)
    sleep(2)


def register_betano_account():
    # Instanciando e gerando fake data class
    fake_data_income = FakeAddress()
    fake_data_income.gerar_endereco_e_phone_unicos()

    # Chamando próxima conta do iterator
    global conta
    conta = iterator.next_account()

    # driver.find_element(
    #     By.XPATH,
    #     '/html/body/main/div/div/section[2]/div[6]/div/div/div[2]/div[1]/p[1]/a'
    # ).click()

    # Selects navigator
    pyautogui.click(1505, 808, duration=.2)
    bind.tap(Key.esc)

    # clica em registar
    pyautogui.click(1778, 118, duration=.5)
    sleep(6)

    ###########################################################################
    # HERE IS WHERE THE REGISTRATION CAPTCHA POPS UP (NEED TO VERIFY) #########
    procura_captcha()

    # clica em registrar com email
    pyautogui.click(1230, 652, duration=.1)
    sleep(6)

    bind.type(conta.email)
    bind.tap(Key.tab)

    # campo da data (dia)
    day = str(conta.date_of_birth[0] + conta.date_of_birth[1])

    if day == '22':
        # that's because Betano has the bug of 22 on day field.
        bind.type('222')
        sleep(1)

    else:
        bind.type(day)
        sleep(1)

    bind.tap(Key.tab)
    sleep(1)

    # campo da data (mês)
    month = str(conta.date_of_birth[3] + conta.date_of_birth[4])

    if month in months:
        bind.type(months[f'{month}'])
        sleep(1)

    bind.tap(Key.tab)
    sleep(1)

    # campo da data (ano)
    year = str(
        conta.date_of_birth[6] +
        conta.date_of_birth[7] +
        conta.date_of_birth[8] +
        conta.date_of_birth[9]
    )

    bind.type(year)
    sleep(1)

    bind.tap(Key.tab)
    sleep(1)

    bind.type(
        conta.cpf
    )

    sleep(3)
    for x in range(5):
        bind.tap(Key.tab)
        sleep(.1)
        x += 1

    bind.tap(Key.enter)
    sleep(6)

    # select address field
    pyautogui.click(1202, 449, duration=.1)
    sleep(1)

    betano_address = f'{fake_data_income.fake_estado} \
{fake_data_income.fake_rua}\
{fake_data_income.fake_numero_casa}'

    # escreve endereço
    bind.type(betano_address)
    print(betano_address)
    print('Email usado: ', conta.email)
    fake_data_income.save_fake_data_usage()
    sleep(1)

    # seleciona autofill do endereço
    bind.tap(Key.down)

    bind.tap(Key.enter)
    sleep(1)

    # seleciona campo de phone
    for _ in range(3):
        bind.tap(Key.tab)
        _ += 1
        sleep(.5)

    bind.type(fake_data_income.fake_phone)
    sleep(1)

    for x in range(4):
        bind.tap(Key.tab)
        sleep(.1)
        x += 1
    sleep(1)

    bind.tap(Key.enter)
    sleep(6)

    for x in range(4):
        bind.tap(Key.tab)
        sleep(.1)
        x += 1
    sleep(1)

    # password field
    bind.type(DEFAULT_PASSWORD)
    sleep(.5)

    for _ in range(5):
        bind.tap(Key.tab)
        sleep(.1)
        _ += 1
    bind.tap(Key.enter)
    sleep(8)

    pyautogui.click(1080, 400, duration=.2)

    for _ in range(7):
        bind.tap(Key.tab)
        sleep(.5)
        _ += 1
    bind.tap(Key.enter)
    sleep(8)

    # for x in range(5):
    #     bind.tap(Key.tab)
    #     sleep(.1)
    #     x += 1
    # sleep(1)

    # # final enter (account created)
    # bind.tap(Key.enter)

    # sleep(30000)


def gmail_process():

    # opens new nav
    pyautogui.click(1048, 1055, duration=.2, button='right')
    sleep(1)

    pyautogui.click(971, 897, duration=.2)
    sleep(3)

    # selects the navigator
    pyautogui.click(933, 201, duration=.2)

    # set_vpn(first_iteration=True)

    # Select search field
    bind.press(Key.alt_l)
    bind.type('d')
    bind.release(Key.alt_l)
    sleep(1)

    bind.type('gmail.com')
    bind.tap(Key.enter)
    sleep(7)

    # # Gmail login button
    # pyautogui.click(1391, 115, duration=.2)
    # sleep(8)

    # type login fields
    bind.type(conta.email)
    bind.tap(Key.enter)
    sleep(6)

    bind.type(conta.email_password)
    bind.tap(Key.enter)
    sleep(6)

    # google not now button 1
    pyautogui.click(1268, 733, duration=.1, clicks=2, interval=.5)
    sleep(6)

    # google not now button 2
    pyautogui.click(812, 839, duration=.1, clicks=2, interval=.5)
    sleep(8)

    # email search field
    pyautogui.click(411, 114, duration=.2)
    sleep(3)

    bind.type('Bem-vindo à Betano!')
    bind.tap(Key.enter)
    sleep(4)

    # selects account's first email
    pyautogui.click(997, 278, duration=.2)
    sleep(4)

    # deny situational translation
    # for _ in range(2):
    #     pyautogui.click(661, 340, duration=.2)
    #     sleep(3)
    #     _ += 1
    # sleep(1)

    # selects verification code
    pyautogui.click(1158, 681, duration=.2, clicks=2)
    sleep(1)
    bind.press(Key.ctrl_l)
    bind.type('c')
    bind.release(Key.ctrl_l)
    sleep(1)

    # closes gmail window
    pyautogui.click(1894, 14, duration=.2)
    sleep(3)

    # betano verification code input field
    pyautogui.click(1118, 501, duration=.2)
    bind.press(Key.ctrl_l)
    bind.type('v')
    bind.release(Key.ctrl_l)
    sleep(3)

    for _ in range(4):
        bind.tap(Key.tab)
        sleep(.2)
        _ += 1

    bind.tap(Key.enter)
    sleep(5)

    # Here, the account has been succesfully registered

    # Move to desktop (necessary)
    bind.press(Key.cmd)
    bind.type('d')
    bind.release(Key.cmd)

    driver.close()
    sleep(2)


########################################


# DB Accounts loop:
for process in iterator.rows:
    access_betano()
    register_betano_account()  # Verifies CAPTCHA
    gmail_process()  # (Closes driver after process)
    save_info_to_db()
    # connect_to_phone()
    reset_vpn()
    first_account_iteration = False


iterator.cursor.close()
iterator.connection.close()
