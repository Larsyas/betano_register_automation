from code import interact
import pyautogui
from months import months
from utils.data_usage_test import AccountIterator, Conta
from pynput.keyboard import Controller, Key
from utils.commands import profile_path, DEFAULT_PASSWORD
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from utils.register_address import FakeAddress
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
import datetime
from utils.test import FakeData
from pathlib import Path


ROOT_DIR = Path(__file__).parent  # (Sou_um_ser_humano_confia)
CAPTCHA_IMG1 = f'{ROOT_DIR}\\images\\betano_vpn_captcha_indicator.png'
CAPTCHA_IMG2 = f'{ROOT_DIR}\\images\\betano_vpn_captcha_indicator2.png'
EMAIL_CODE_VERIFICATION = f'{ROOT_DIR}\\images\\verification_code_error.png'
ACCOUNT_VERIFICATION_IMG = f'{ROOT_DIR}\\images\\account_successfully_created_verification.png'
GMAIL_PASSWORD_SCREEN_VERIFICATION = f'{ROOT_DIR}\\images\\gmail_password_screen.png'

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


def verifies_email_code_error():
    i = 0
    try:
        verification_code_error = pyautogui.locateOnScreen(
            EMAIL_CODE_VERIFICATION,
            4
        )

    except pyautogui.ImageNotFoundException:
        solved_bug = True
        # (account created)

    while solved_bug != True:
        if verification_code_error:
            # refreshes page
            bind.tap(Key.f5)
            sleep(5)
            i += 1
            if i == 3:
                print(
                    f'{i} Failed attemps to put the verification code, closing app.')
                break


def procura_captcha1(firefoxDriver: webdriver.Firefox, firefoxOptions: webdriver.FirefoxOptions):

    def _procedimento_captcha1(firefoxDriver: webdriver.Firefox, firefoxOptions: webdriver.FirefoxOptions):
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

        reset_vpn(restart=True)

        return firefoxOptions

# after here, the script goes to the begging of the trying loop

    try:
        global captcha1
        captcha1 = pyautogui.locateOnScreen(CAPTCHA_IMG1, 5)

        if captcha1:
            print('Got into a captcha, now starting captcha correction process.')
            sleep(1)
            _procedimento_captcha1(firefoxDriver=driver,
                                   firefoxOptions=options)
            captcha1 = True

    except pyautogui.ImageNotFoundException:
        print('Did not got into the first registration captcha, continuing now.')
        captcha1 = None


def procura_captcha2(firefoxDriver: webdriver.Firefox, firefoxOptions: webdriver.FirefoxOptions):
    def _procedimento_captcha2(firefoxDriver: webdriver.Firefox, firefoxOptions: webdriver.FirefoxOptions):
        # This function closes the driver, resets ip and change tab functioning,
        # (LEAVING ME AT THE DESKTOP)
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

        reset_vpn(restart=True)

        return firefoxOptions

    try:
        global captcha2
        captcha2 = pyautogui.locateOnScreen(CAPTCHA_IMG2, 7)

        if captcha2:
            print('Did not got to the second captcha, continuing, gg.')
            sleep(1)
            captcha2 = None

    except pyautogui.ImageNotFoundException:
        print('Did got into the second registration captcha, starting captcha correction process 2 now.')
        _procedimento_captcha2(firefoxDriver=driver, firefoxOptions=options)
        captcha2 = True


def _confirms_account_registration():
    pyautogui.moveTo(300, 1080)
    try:
        global confirmed_account
        confirmed_account = pyautogui.locateOnScreen(
            ACCOUNT_VERIFICATION_IMG, 18)

        if confirmed_account:
            print()
            print('Account successfully registrated, continuing to next one.')
            confirmed_account = True

    except pyautogui.ImageNotFoundException:
        print('Confirming the code was not possible, trying again now.')
        driver.quit()
        confirmed_account = None


def reset_vpn(
    on: bool | None = None,
    off: bool | None = None,
    restart: bool | None = None
):
    # This function leaves me at desktop

    if restart is True:
        # search for norton on windows search
        bind.tap(Key.cmd)
        sleep(2)
        pyautogui.typewrite("Norton 360", interval=0.1)
        sleep(2)

        # opens it
        bind.tap(Key.enter)
        sleep(5)

        # turns vpn off and on again
        print('resetando o vpn')
        pyautogui.click(1347, 629, duration=.2)
        sleep(30)
        pyautogui.click(1347, 629, duration=.2)
        sleep(6)

        bind.press(Key.alt_l)
        bind.tap(Key.f4)
        bind.release(Key.alt_l)

    elif on is True:
        # search for norton on windows search
        bind.tap(Key.cmd)
        sleep(2)
        pyautogui.typewrite("Norton 360", interval=0.1)
        sleep(2)

        # opens it
        bind.tap(Key.enter)
        sleep(5)

        # turns vpn on
        print('Ligando o vpn...')
        pyautogui.click(1347, 629, duration=.2)
        sleep(8)

        bind.press(Key.alt_l)
        bind.tap(Key.f4)
        bind.release(Key.alt_l)

    elif off is True:
        # search for norton on windows search
        bind.tap(Key.cmd)
        sleep(2)
        pyautogui.typewrite("Norton 360", interval=0.1)
        sleep(2)

        # opens it
        bind.tap(Key.enter)
        sleep(5)

        # turns vpn on
        print('Desligando o vpn...')
        pyautogui.click(1347, 629, duration=.2)
        sleep(8)

        bind.press(Key.alt_l)
        bind.tap(Key.f4)
        bind.release(Key.alt_l)

    else:
        ...


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


def access_betano_and_verifies_first_captcha(login: bool | None):
    if login is True:
        global driver
        driver = webdriver.Firefox(service=service, options=options)
        driver.maximize_window()

        driver.get('https://br.betano.com/')
        sleep(2)
        bind.tap(Key.esc)
        sleep(2)

        # Selects navigator
        pyautogui.click(1505, 808, duration=.2)
        bind.tap(Key.esc)

        # clica em logar
        pyautogui.click(1848, 112, duration=.5)
        sleep(8)

        # LOGIN CHECKBOX CAPTCHA3
        pyautogui.click(700, 397, duration=.2)
        sleep(5)

        # User login process
        pyautogui.click(1233, 257, duration=.2)
        bind.type(conta.email)
        sleep(1)
        bind.tap(Key.tab)
        sleep(1)
        bind.type(conta.betano_password)
        sleep(1)
        bind.tap(Key.enter)

        # HERE WE GET TO THE EMAIL INPUT CODE SCREEN, ALREADY LOGGED ON

    driver = webdriver.Firefox(service=service, options=options)
    driver.maximize_window()

    driver.get('https://br.betano.com/')
    sleep(2)
    bind.tap(Key.esc)
    sleep(2)

    # Selects navigator
    pyautogui.click(1505, 808, duration=.2)
    bind.tap(Key.esc)

    # clica em registar
    pyautogui.click(1778, 118, duration=.5)
    sleep(6)

    ###########################################################################
    # HERE IS WHERE THE REGISTRATION CAPTCHA POPS UP (NEED TO VERIFY) #########
    procura_captcha1(firefoxDriver=driver, firefoxOptions=options)

    while captcha1 is True:
        try:
            access_betano_and_verifies_first_captcha(login=False)
            account_registration_process(solving_problem_mode=True)
        except:
            pass


def account_registration_process(solving_problem_mode: bool = None):

    if solving_problem_mode == True:
        pass

    else:
        # Chamando próxima conta do iterator
        global conta
        conta = iterator.next_account()

        # Instanciando e gerando fake data class
        fake_data_income = FakeAddress()
        fake_data_income.gerar_endereco_e_phone_unicos()

    # clica em registrar com email
    pyautogui.click(1230, 652, duration=.1)
    pyautogui.click(1230, 652, duration=.1)
    pyautogui.click(1230, 652, duration=.1)
    sleep(2)

    bind.type(conta.email)
    bind.tap(Key.tab)

    # campo da data (dia)
    day = str(conta.date_of_birth[0] + conta.date_of_birth[1])

    if day == '22':
        # that's because Betano has the bug of 22 on day field.
        bind.type('222')
        sleep(.5)

    else:
        bind.type(day)
        sleep(.5)

    bind.tap(Key.tab)
    sleep(1)

    # campo da data (mês)
    month = str(conta.date_of_birth[3] + conta.date_of_birth[4])

    if month in months:
        bind.type(months[f'{month}'])
        sleep(.5)

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
        sleep(.2)
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
    pyautogui.typewrite(betano_address, 0.1)
    print(betano_address)
    print('Email usado: ', conta.email)
    fake_data_income.save_fake_data_usage()
    sleep(1)

    # seleciona autofill do endereço
    bind.tap(Key.down)
    sleep(1)
    bind.tap(Key.enter)
    sleep(1)

    # seleciona campo de phone
    for _ in range(3):
        bind.tap(Key.tab)
        sleep(.5)
        _ += 1

    bind.type(fake_data_income.fake_phone)
    sleep(1)

    for x in range(4):
        bind.tap(Key.tab)
        sleep(.5)
        x += 1
    sleep(1)

    bind.tap(Key.enter)
    sleep(6)

    for x in range(4):
        bind.tap(Key.tab)
        sleep(.5)
        x += 1
    sleep(3)

    # password field
    pyautogui.typewrite(DEFAULT_PASSWORD, interval=0.1)
    sleep(1.5)

    for _ in range(5):
        bind.tap(Key.tab)
        sleep(.1)
        _ += 1
    bind.tap(Key.enter)
    sleep(4)

    # Betano's terms of use checkbox (Next step is calling gmail_process.)
    pyautogui.click(1080, 400, duration=.2)
    sleep(1)

    for _ in range(7):
        bind.tap(Key.tab)
        sleep(.3)
        _ += 1
    bind.tap(Key.enter)

    procura_captcha2(firefoxDriver=driver, firefoxOptions=options)

    while captcha2 is True:
        try:
            access_betano_and_verifies_first_captcha(login=False)
            account_registration_process(solving_problem_mode=True)
        except:
            pass

    # if captcha2:
    #     # Keep trying registrating the account, now with VPN restarted, until it gets it.
    #     while captcha2 == True:

    #         access_betano_and_verifies_first_captcha(login=False)
    #         account_registration_process()
    #         gmail_process()
    #         captcha2 = None


def gmail_process():

    def open_gmail():
        # opens new nav
        bind.tap(Key.cmd)
        sleep(1)

        pyautogui.typewrite('privativa do firefox', .1)
        bind.tap(Key.enter)
        sleep(4)

        # selects the navigator
        pyautogui.click(933, 201, duration=.2)

        # Select search field
        bind.press(Key.alt_l)
        bind.type('d')
        bind.release(Key.alt_l)
        sleep(1)

        bind.type('gmail.com')
        bind.tap(Key.enter)
        sleep(7)

        # type login fields
        bind.type(conta.email)
        bind.tap(Key.enter)
        sleep(1)

    # Verifies gmail password screen
        try:
            gmail_password_step = pyautogui.locateOnScreen(
                GMAIL_PASSWORD_SCREEN_VERIFICATION,
                8
            )

            if gmail_password_step:
                sleep(1)
                gmail_password_step = None
                pass

        except pyautogui.ImageNotFoundException:
            print('Could not login to gmail. Stopping execution.')
            print('STILL NEED TO CONFIRM THE CODE ON BETANO.')
            print()

            bind.press(Key.alt_l)
            bind.tap(Key.f4)
            bind.release(Key.alt_l)
            sleep(2)

            open_gmail()

    open_gmail()

    bind.type(conta.email_password)
    bind.tap(Key.enter)
    sleep(8)

    # google not now button 1
    pyautogui.click(1268, 733, duration=.1, clicks=2, interval=.5)
    sleep(5)

    # google not now button 2
    pyautogui.click(812, 839, duration=.1, clicks=2, interval=.5)
    sleep(10)

    # email search field
    pyautogui.click(411, 114, duration=.2)
    sleep(3)

    bind.type('Bem-vindo à Betano!')
    bind.tap(Key.enter)
    sleep(4)

    # selects account's first email
    pyautogui.click(997, 278, duration=.2)
    sleep(4)

    # selects verification code
    pyautogui.click(1158, 681, duration=.2, clicks=2)
    sleep(1)
    bind.press(Key.ctrl_l)
    bind.type('c')
    bind.release(Key.ctrl_l)
    sleep(1)

    # closes gmail window
    pyautogui.click(1894, 14, duration=.2)
    sleep(1)
    bind.tap(Key.enter)
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
    sleep(1)

    # Sometimes, pasting the email code on Betano fails.
    # This function tries to send the code to the site three times, and if
    # it can't proceed, it closes.
    verifies_email_code_error()

    # Closes driver if the email was't received by Betano.
    _confirms_account_registration()

    # (_confirms_account_registration defines confirmed_account's value.)
    if confirmed_account == None:
        reset_vpn(off=True)

    # Keep trying registrating the account, now with VPN turned off, until it gets it.
    while confirmed_account == None:
        # Just logs in and get to the code input screen.
        access_betano_and_verifies_first_captcha(login=True)
        gmail_process()

        if confirmed_account is True:
            reset_vpn(on=True)

    # Here, the account is supposed to be succesfully registrated

    # Move to desktop (necessary)
    bind.press(Key.cmd)
    bind.type('d')
    bind.release(Key.cmd)

    driver.quit()
    sleep(2)


########################################


account_num = 0
print()
print(f'{len(iterator.rows)} contas da DB a serem registradas.')
first_iteration = True
# DB Accounts loop:
for process in iterator.rows:
    print()
    account_num += 1
    print(f'Account number {account_num}.')

    # Tries to access and use betano successfully
    try:
        access_betano_and_verifies_first_captcha(login=False)
        account_registration_process()  # Verifies if email was sent to gmail.
        gmail_process()  # (Closes driver after process)

    # In the case de IP from VPN comes offline, the script tries again with other IP
    except WebDriverException:
        reset_vpn(restart=True)
        access_betano_and_verifies_first_captcha(login=False)
        account_registration_process()  # Verifies if email was sent to gmail.
        gmail_process()  # (Closes driver after process)

    # In the case of the first captcha pops up
    while captcha1 == True:
        # while captcha1 is True, access_betano_and_verifies_first_captcha will try to fix it,
        # so I don't need to call reset_vpn.
        access_betano_and_verifies_first_captcha(login=False)
        # Verifies if email was sent to gmail. (captcha2)
        if first_iteration == True:
            account_registration_process()
        else:
            account_registration_process(solving_problem_mode=True)
        gmail_process()  # (Closes driver after process)

    # In the case of the second captcha pops up
    while captcha2 == True:
        access_betano_and_verifies_first_captcha(login=False)
        # Verifies if email was sent to gmail. (captcha2)
        # if first_iteration == True, we call next account in case of captcha
        if first_iteration == True:
            account_registration_process()
        else:
            account_registration_process(solving_problem_mode=True)
        gmail_process()  # (Closes driver after process)

    save_info_to_db()
    reset_vpn(restart=True)
    first_iteration = False


iterator.cursor.close()
iterator.connection.close()
