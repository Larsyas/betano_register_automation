from code import interact
import email
from pickletools import pytuple
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
EMAIL_ALREADY_EXISTS = f'{ROOT_DIR}\\images\\email_ja_existe.png'
ACCOUNT_VERIFICATION_IMG = f'{ROOT_DIR}\\images\\account_successfully_created_verification.png'
EXISTING_CPF = f'{ROOT_DIR}\\images\\cpf_existente.png'
EMPTY_USER_NAME_VERIFICATION = f'{ROOT_DIR}\\images\\usuario_em_branco.png'
SECOND_REGISTRATION_STEP = f'{ROOT_DIR}\\images\\second_registration_step.png'

GMAIL_USERNAME_SCREEN_VERIFICATION = f'{ROOT_DIR}\\images\\gmail_initial_screen.png'
GMAIL_PASSWORD_SCREEN_VERIFICATION = f'{ROOT_DIR}\\images\\gmail_password_screen.png'
GMAIL_NOT_NOW_SCREEN_VERIFICATION1 = f'{ROOT_DIR}\\images\\gmail_not_now_screen1.png'
GMAIL_NOT_NOW_SCREEN_VERIFICATION2 = f'{ROOT_DIR}\\images\\gmail_not_now_screen2.png'
GMAIL_LOGGED_ON_SCREEN_VERIFICATION = f'{ROOT_DIR}\\images\\gmail_logged_on_screen.png'


iterator = AccountIterator()
iterator.connect_to_db()

service = FirefoxService(executable_path=GeckoDriverManager().install())

options = webdriver.FirefoxOptions()
# options.add_argument('--private')
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


def reinicia_tentativa_de_conta(firefoxDriver: webdriver.Firefox, firefoxOptions: webdriver.FirefoxOptions):
    firefoxDriver.quit()
    reset_vpn(restart=True)
    access_betano_and_verifies_first_captcha(login=False)
    account_registration_process(solving_problem_mode=True)


def verifies_email_code_error():
    tentativas_codigo_gmail = 0
    try:
        verification_code_error = pyautogui.locateOnScreen(
            EMAIL_CODE_VERIFICATION,
            4, confidence=0.9
        )

        while verification_code_error:
            try:
                sleep(1)
                # refreshes page
                bind.tap(Key.f5)
                sleep(5)

                pyautogui.locateAllOnScreen(
                    EMAIL_CODE_VERIFICATION,
                    4, confidence=0.9
                )

                print()
                print(
                    'Got into the verification bug, trying to fix it by refreshing page.')

                tentativas_codigo_gmail += 1

                if tentativas_codigo_gmail == 3:
                    print(
                        f'{tentativas_codigo_gmail} Failed attemps to put the verification code, closing app.')
                    break

            except pyautogui.ImageNotFoundException:
                # Se o bug nao foi encontrado, significa que a conta foi confirmada.
                verification_code_error = False

    except pyautogui.ImageNotFoundException:
        verification_code_error = False
        # (account created)


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

        return firefoxDriver, firefoxOptions

# after here, the script goes to the beginning of the trying loop

    try:
        captcha1 = pyautogui.locateOnScreen(CAPTCHA_IMG1, 4, confidence=0.9)

        if captcha1:
            print('Got into a captcha, now starting captcha correction process.')
            sleep(1)
            _procedimento_captcha1(firefoxDriver=driver,
                                   firefoxOptions=options)

            captcha1 = True
            return True

    except pyautogui.ImageNotFoundException:
        print('Did not got into the first registration captcha, continuing now.')
        captcha1 = False
        return False


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

        return firefoxDriver, firefoxOptions

    try:
        captcha2 = pyautogui.locateOnScreen(CAPTCHA_IMG2, 7, confidence=0.9)

        if captcha2:
            print('Did not got to the second captcha, continuing, gg.')
            sleep(1)
            captcha2 = False
            return False

    except pyautogui.ImageNotFoundException:
        print('Did got into the second registration captcha, starting captcha correction process 2 now.')
        _procedimento_captcha2(firefoxDriver=driver, firefoxOptions=options)
        captcha2 = True
        return True


def _confirms_account_registration():
    pyautogui.moveTo(300, 1080)
    try:
        global confirmed_account
        confirmed_account = pyautogui.locateOnScreen(
            ACCOUNT_VERIFICATION_IMG, 18, confidence=0.9)

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
        sleep(4)

        # turns vpn off and on again
        print('resetando o vpn')
        pyautogui.click(1347, 629, duration=.2)
        sleep(18)
        pyautogui.click(1347, 629, duration=.2)
        sleep(4)

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
    # sleep(2)

    ###########################################################################
    # HERE IS WHERE THE REGISTRATION CAPTCHA POPS UP (NEED TO VERIFY) #########
    return procura_captcha1(firefoxDriver=driver, firefoxOptions=options)


def account_registration_process(solving_problem_mode: bool = None):

    if solving_problem_mode == True:
        pass

    else:
        # Chamando próxima conta do iterator
        global conta
        conta = iterator.next_account()

        # Instanciando e gerando fake data class
        global fake_data_income
        fake_data_income = FakeAddress()
        fake_data_income.gerar_endereco_e_phone_unicos()

    # navega ate registrar com email via click + tab
        # clica em registrar com email
        pyautogui.click(1216, 866, duration=.1)
        sleep(2)
        pyautogui.click(1216, 866, duration=.1)
        sleep(1)
        bind.tap(Key.tab)
        sleep(.5)
        bind.tap(Key.enter)
        sleep(5)

    bind.type(conta.email)
    sleep(1)

    # Try do email ja existente (passa pra proxima conta)
    verifica_se_email_existe(conta)

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
    sleep(2)

    # campo da data (mês)
    month = str(conta.date_of_birth[3] + conta.date_of_birth[4])

    if month in months:
        bind.type(months[f'{month}'])
        sleep(.5)

    bind.tap(Key.tab)
    sleep(2)

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

    sleep(1)

    # Try do cpf invalido
    try:
        cpf_already_in_use = pyautogui.locateOnScreen(
            EXISTING_CPF,
            5, confidence=0.9
        )

        while cpf_already_in_use:
            print('This CPF is already in use. Passing to next account.')
            try:
                driver.quit()
                sleep(3)

                access_betano_and_verifies_first_captcha(login=False)

                # clica em registrar com email
                pyautogui.click(1216, 866, duration=.1)
                sleep(2)
                pyautogui.click(1216, 866, duration=.1)
                sleep(1)
                bind.tap(Key.tab)
                sleep(.5)
                bind.tap(Key.enter)
                sleep(5)

                # (repeats same process but now with new data)
                conta = iterator.next_account()
                # selects email field again
                pyautogui.click(1193, 380, duration=.2)
                sleep(.5)

                bind.type(
                    conta.email
                )

                verifica_se_email_existe(conta)

                if email_already_exists == False:

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
                    month = str(
                        conta.date_of_birth[3] + conta.date_of_birth[4])

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

                    sleep(2)

                    # Tenta localizar a imagem EMAIL_ALREADY_EXISTS na tela
                    pyautogui.locateOnScreen(EXISTING_CPF, 4, confidence=0.9)

            except pyautogui.ImageNotFoundException:
                cpf_already_in_use = False

    except pyautogui.ImageNotFoundException:
        # print('Essa conta tem o cpf valido.')
        pass

    for x in range(5):
        bind.tap(Key.tab)
        sleep(.2)
        x += 1

    bind.tap(Key.enter)
    sleep(1)

    try:
        second_registration_step_confirmation = pyautogui.locateOnScreen(
            SECOND_REGISTRATION_STEP,
            4, confidence=0.9
        )

        if second_registration_step_confirmation:
            pass

    except pyautogui.ImageNotFoundException:
        print('Não consegui chegar no segundo passo da Betano.')
        reinicia_tentativa_de_conta(driver, options)
        return

    sleep(2.5)
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
    print('Senha do email: ', conta.email_password)
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
        sleep(.3)
        _ += 1

    bind.type(fake_data_income.fake_phone)
    sleep(1)

    for x in range(4):
        bind.tap(Key.tab)
        sleep(.3)
        x += 1
    sleep(1)

    bind.tap(Key.enter)
    sleep(3)

    # Try no nickname necessario
    try:
        nome_de_usuario_necessario = pyautogui.locateOnScreen(
            EMPTY_USER_NAME_VERIFICATION,
            4, confidence=0.9
        )

        if nome_de_usuario_necessario:
            # selects nickname field
            pyautogui.click(1211, 359, duration=.2)
            sleep(.5)

            # creates a nickname based on first 4 letters of email + cpf start + random '7'
            for indices_de_letras_do_email in range(4):
                bind.type(
                    conta.email[indices_de_letras_do_email])

            bind.type(
                conta.cpf[0] +
                conta.cpf[0] +
                conta.cpf[1] +
                conta.cpf[1] +
                conta.cpf[2] +
                conta.cpf[2] +
                '7'
            )

    except pyautogui.ImageNotFoundException:
        pass

    # betano passoword field
    pyautogui.click(1202, 444, duration=.2)
    sleep(1)

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

    return procura_captcha2(firefoxDriver=driver, firefoxOptions=options)

    # while captcha2 is True:
    #     try:
    #         print('To na linha 596')
    #         access_betano_and_verifies_first_captcha(login=False)
    #         account_registration_process(solving_problem_mode=True)
    #     except:
    #         pass


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

        # Verifies gmail's username screen
        try:
            gmail_username_step = pyautogui.locateOnScreen(
                GMAIL_USERNAME_SCREEN_VERIFICATION,
                9, confidence=0.9
            )

            if gmail_username_step:
                sleep(1.5)
                # type login fields
                bind.type(conta.email)
                sleep(.5)
                bind.tap(Key.enter)

        except pyautogui.ImageNotFoundException:
            print('Could not open gmail. Trying again now.')
            bind.press(Key.alt_l)
            bind.tap(Key.f4)
            bind.release(Key.alt_l)
            sleep(2)

            open_gmail()

        # Verifies gmail password screen
        try:
            global gmail_password_step
            gmail_password_step = pyautogui.locateOnScreen(
                GMAIL_PASSWORD_SCREEN_VERIFICATION,
                7, confidence=0.9
            )

            if gmail_password_step:
                sleep(1.5)
                pass

        # if this except comes, we need to pass to the next account
        except pyautogui.ImageNotFoundException:
            print('This email apparently does not exit, passing to the  account now.')
            gmail_password_step = False
            print()
            print(f'The account with the email "{conta.email}" does NOT work.')

            bind.press(Key.alt_l)
            bind.tap(Key.f4)
            bind.release(Key.alt_l)
            sleep(2)

    # open_gmail leaves us on the gmail password screen
    open_gmail()

    bind.type(conta.email_password)
    bind.tap(Key.enter)

    # Google not now 1 verification sreen (situational)
    try:
        not_now1_situational = pyautogui.locateOnScreen(
            GMAIL_NOT_NOW_SCREEN_VERIFICATION1,
            8, confidence=0.9
        )

        if not_now1_situational:
            # google not now button 1
            pyautogui.click(1268, 733, duration=.1)

    except pyautogui.ImageNotFoundException:
        pass

    # Google not now 2 verification sreen
    try:
        not_now2 = pyautogui.locateOnScreen(
            GMAIL_NOT_NOW_SCREEN_VERIFICATION2,
            8, confidence=0.9
        )

        if not_now2:
            # google not now button 2
            sleep(1)
            pyautogui.click(812, 839, duration=.1)

    except pyautogui.ImageNotFoundException:
        pass

    # Google logged on screen verification
    try:
        gmail_logged_on_screen = pyautogui.locateOnScreen(
            GMAIL_LOGGED_ON_SCREEN_VERIFICATION,
            25, confidence=0.9
        )

        if gmail_logged_on_screen:
            # email search field
            pyautogui.click(411, 114, duration=.2)
            sleep(2)

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
            sleep(.5)
            bind.tap(Key.enter)
            sleep(2)

    except pyautogui.ImageNotFoundException:
        print('Rapaz, deu pra logar no gmail n, aqui cabo.')
        exit()

    # betano verification code input field
    pyautogui.click(1118, 501, duration=.2)
    bind.press(Key.ctrl_l)
    bind.type('v')
    bind.release(Key.ctrl_l)
    sleep(2)

    pyautogui.click(
        1329, 873, duration=.2
    )
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


def verifica_se_email_existe(conta):
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
    captcha1 = None
    captcha2 = None

    # Tries to access and use betano successfully
    try:
        captcha1 = access_betano_and_verifies_first_captcha(login=False)
        if captcha1 != True:
            captcha2 = account_registration_process()
            if captcha2 != True:
                gmail_process()  # (Closes driver after process)

        # (Equanto houver algum captcha)
        while captcha1 == True or captcha2 == True:
            print('ovo tentar dnv')
            access_betano_and_verifies_first_captcha(login=False)
            captcha1 = False

            if captcha1 != True:
                print('if captcha1 L918')
                # if we're in first iteration, we need to call next account
                if first_iteration == True:
                    account_registration_process(solving_problem_mode=True)

                    if captcha2 == True:
                        print('if captcha2 L924')
                        gmail_process()  # (Closes driver after process)

        if gmail_password_step == False:
            driver.quit()
            continue

    # In the case de IP from VPN comes offline, the script tries again with other IP
    except WebDriverException:
        reset_vpn(restart=True)
        access_betano_and_verifies_first_captcha(login=False)
        account_registration_process()  # Verifies if email was sent to gmail.
        gmail_process()  # (Closes driver after process)

    save_info_to_db()
    print('reset de vpn da linha 947')
    reset_vpn(restart=True)
    first_iteration = False
    print('Tenorio Vagabundo!!')


iterator.cursor.close()
iterator.connection.close()

print('Acabei, então se você já não tiver bebendo, vai beber enquanto espera o pixKKK')
