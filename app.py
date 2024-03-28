from tkinter import X
import pyautogui
from months import months
from utils.data_usage_test import AccountIterator, Conta
from pynput.keyboard import Controller, Key
from utils.commands import buttons_addresses
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By


iterator = AccountIterator()
iterator.connect_to_db()
driver = webdriver.Firefox()
bind = Controller()


def setSite():
    driver.maximize_window()
    driver.get('https://br.betano.com/')
    sleep(3)


def register_betano_account():
    # Chamando primeira conta do iterator
    conta = iterator.next_account()
    conta = iterator.next_account()

    driver.find_element(
        By.XPATH,
        '/html/body/main/div/div/section[2]/div[6]/div/div/div[2]/div[1]/p[1]/a'
    ).click()
    sleep(4)

    # clica em registrar
    pyautogui.click(1230, 652, duration=.1)
    sleep(3.5)

    bind.type(conta.email)
    bind.tap(Key.tab)

    # campo da data (dia)
    day = str(conta.date_of_birth[0] + conta.date_of_birth[1])

    if day == '22':
        # that's because Betano has the bug of 22 on day field.
        bind.type('222')
        sleep(.1)

    else:
        bind.type(day)
        sleep(.1)

    bind.tap(Key.tab)
    sleep(.1)

    # campo da data (mês)
    month = str(conta.date_of_birth[3] + conta.date_of_birth[4])

    if month in months:
        bind.type(months[f'{month}'])
        sleep(.1)

    bind.tap(Key.tab)
    sleep(.1)

    # campo da data (ano)
    year = str(conta.date_of_birth[6] +
               conta.date_of_birth[7] +
               conta.date_of_birth[8] +
               conta.date_of_birth[9])

    bind.type(year)
    sleep(.1)

    bind.tap(Key.tab)
    sleep(.1)

    bind.type(
        conta.cpf
    )

    sleep(3)
    for x in range(5):
        bind.tap(Key.tab)
        sleep(.1)
        x += 1

    bind.tap(Key.enter)

    sleep(30000)

# driver.close()


########################################


setSite()
register_betano_account()

iterator.cursor.close()
iterator.connection.close()
