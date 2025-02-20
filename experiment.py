import os
import time
import pyautogui
import AppKit

def open_file(url, browser):
    os.system(f"open -a '{browser}' '{url}'")


def scroll():
    time.sleep(2)
    pyautogui.click(x=pyautogui.size().width // 2, y=pyautogui.size().height // 2)
    time.sleep(1)
    for i in range(5):
        pyautogui.press('down')


open_file('/Users/ahmeddriouech/Desktop/ML4SE/2306.08568v1.pdf', 'Safari')
scroll()