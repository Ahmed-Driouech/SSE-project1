#!/usr/bin/env python3
import argparse
import os
import time
import pyautogui

class Experiment:
    """
    Handles browser automation for opening a URL, scrolling through the page,
    searching for a word, and closing the browser.
    """
    def __init__(self, url, browser, search_word):
        self.url = url
        self.browser = browser
        self.search_word = search_word

    def open_file(self):
        """
        Opens the specified URL in the given browser.
        """
        os.system(f"open -a '{self.browser}' '{self.url}'")

    def close_file(self):
        """
        Closes the browser application.
        """
        os.system(f"""osascript -e 'tell application "{self.browser}" to quit'"""")

    def scroll(self):
        """
        Scrolls through the webpage after a short delay to activate the window.
        """
        time.sleep(2)
        pyautogui.click(x=pyautogui.size().width // 2, y=pyautogui.size().height // 2)
        time.sleep(1)
        for _ in range(65):
            pyautogui.scroll(-5)
            time.sleep(0.75)

    def search_for_word(self):
        """
        Activates the search functionality in the browser and searches for a word.
        """
        time.sleep(2)
        pyautogui.click(x=pyautogui.size().width // 2, y=pyautogui.size().height // 2)
        time.sleep(1)
        pyautogui.hotkey('command', 'f')
        time.sleep(0.5)
        pyautogui.write(self.search_word)
        time.sleep(1)
        for _ in range(10):
            pyautogui.press('enter')
            time.sleep(0.5)
        time.sleep(1)

    def run_experiment(self):
        """
        Executes the complete experiment workflow: open file, scroll, search, and close.
        """
        self.open_file()
        self.scroll()
        self.search_for_word()
        self.close_file()

def main():
    """
    Parses command-line arguments and runs the experiment.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("browser", default="Google Chrome", choices=["Google Chrome", "safari"])
    parser.add_argument("search_word")
    args = parser.parse_args()
    experiment = Experiment(url=args.url, browser=args.browser, search_word=args.search_word)
    experiment.run_experiment()

if __name__ == '__main__':
    main()
