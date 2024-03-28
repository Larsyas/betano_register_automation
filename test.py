from pickletools import pytuple
from re import M
import pyautogui
from utils.data_usage_test import AccountIterator, Conta
from pynput.keyboard import Controller, Key
from utils.commands import buttons_addresses
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from months import months


iterator = AccountIterator()
iterator.connect_to_db()
# driver = webdriver.Firefox()
bind = Controller()


def setSite():
    conta = iterator.next_account()
    conta = iterator.next_account()
    conta = iterator.next_account()
    # campo da data (mês)
    month = str(conta.date_of_birth[3] + conta.date_of_birth[4])
    if month in months:
        print(month)
        print(months[f'{month}'])


setSite()

iterator.cursor.close()
iterator.connection.close()
# driver.close()
