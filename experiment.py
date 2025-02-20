import os
import time
import pyautogui
import AppKit

def open_file(url, browser):
    os.system(f"open -a '{browser}' '{url}'")


def scroll():
    #activate window
    time.sleep(2)
    pyautogui.click(x=pyautogui.size().width // 2, y=pyautogui.size().height // 2)
    time.sleep(1)

    #scroll through page
    for i in range(65):
        pyautogui.scroll(-5)
        time.sleep(0.75)

def search_word(word):
    #activate window
    time.sleep(2)
    pyautogui.click(x=pyautogui.size().width // 2, y=pyautogui.size().height // 2)
    time.sleep(1)

    pyautogui.hotkey('command', 'f')
    time.sleep(0.5)

    pyautogui.write(word)
    time.sleep(1)

    for i in range(10):
        pyautogui.press('enter')
        time.sleep(0.5)

    time.sleep(1)

open_file('/Users/ahmeddriouech/Desktop/ML4SE/2306.08568v1.pdf', 'Google Chrome')
#scroll()

search_word("LLM")