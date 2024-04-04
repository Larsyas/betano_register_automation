import pyautogui
from selenium import webdriver
from time import sleep
from pynput.keyboard import Controller, Key
bind = Controller()


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
    pyautogui.click(1347, 629, duration=.2, clicks=2, interval=6)
    sleep(3)

    bind.press(Key.alt_l)
    bind.tap(Key.f4)
    bind.release(Key.alt_l)


reset_vpn()
