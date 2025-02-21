import argparse
import os
import subprocess
import time

import pyautogui

from experiment import Experiment

energiBridge_path = '/Users/ahmeddriouech/Desktop/SDSAIT/EnergiBridge'
experiment_path = '/Users/ahmeddriouech/Desktop/SSE-project1/experiment.py'

def open_terminal():
    command = f'open -a Terminal "{energiBridge_path}"'
    subprocess.run(command, shell=True)

def close_terminal():
    os.system("osascript -e 'tell application \"Terminal\" to close front window'")


def run_experiment(command):
    open_terminal()
    time.sleep(1)
    pyautogui.write(command, interval=0.1)
    pyautogui.press('enter')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("results")
    parser.add_argument("url")
    parser.add_argument("browser", default="default",
                        choices=["Google Chrome", "safari"])
    parser.add_argument("search_word")
    args = parser.parse_args()

    command = f'./target/release/energibridge -o {args.results}.csv --summary {experiment_path} {args.url} --browser "{args.browser}" {args.search_word}'
    run_experiment(command)
    #close_terminal()


if __name__ == "__main__":
    main()
