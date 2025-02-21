#!/usr/bin/env python3
import argparse
import os
import time
import pyautogui

class Experiment:
    def __init__(self, url, browser, search_word):
        self.url = url
        self.browser = browser
        self.search_word = search_word

    def open_file(self):
        os.system(f"open -a '{self.browser}' '{self.url}'")


    def scroll(self):
        #activate window
        time.sleep(2)
        pyautogui.click(x=pyautogui.size().width // 2, y=pyautogui.size().height // 2)
        time.sleep(1)

        #scroll through page
        for i in range(65):
            pyautogui.scroll(-5)
            time.sleep(0.75)

    def search_for_word(self):
        #activate window
        time.sleep(2)
        pyautogui.click(x=pyautogui.size().width // 2, y=pyautogui.size().height // 2)
        time.sleep(1)

        pyautogui.hotkey('command', 'f')
        time.sleep(0.5)

        pyautogui.write(self.search_word)
        time.sleep(1)

        for i in range(10):
            pyautogui.press('enter')
            time.sleep(0.5)

        time.sleep(1)

    def run_experiment(self):
        self.open_file()
        self.scroll()
        self.search_for_word()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("--browser", default="default",
                        choices=["Google Chrome", "safari"])
    parser.add_argument("search_word")

    args = parser.parse_args()

    experiment = Experiment(
        url= args.url,
        browser=args.browser,
        search_word=args.search_word
    )

    experiment.run_experiment()

if __name__ == '__main__':
    main()