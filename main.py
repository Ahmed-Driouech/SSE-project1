import argparse
import os
import subprocess
import time
import pandas as pd
import pyautogui

from experiment import Experiment

energiBridge_path = '/Users/taouf/Documents/TUD/Courses/Year1/Q3/SSE/EnergiBridge'
experiment_path = '/Users/taouf/Documents/TUD/Courses/Year1/Q3/SSE/experiment.py'
BASE_DIR = '/Users/taouf/Documents/TUD/Courses/Year1/Q3/SSE/'


def open_terminal():
    command = f'open -a Terminal "{energiBridge_path}"'
    subprocess.run(command, shell=True)


def close_terminal():
    max_attempts = 3
    for attempt in range(max_attempts):
        os.system("osascript -e 'tell application \"Terminal\" to close front window'")
        time.sleep(1)
        # Check if Terminal is still running with front window
        result = subprocess.run(
            ["osascript", "-e", 'tell application "Terminal" to count windows'],
            capture_output=True,
            text=True
        )
        if result.stdout.strip() == "0":
            break
        time.sleep(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("results_prefix")
    parser.add_argument("url")
    parser.add_argument("search_word")
    args = parser.parse_args()

    # Define output files
    combined_output = os.path.join(BASE_DIR, f"{args.results_prefix}_combined.csv")
    chrome_output = os.path.join(BASE_DIR, f"{args.results_prefix}_chrome.csv")
    safari_output = os.path.join(BASE_DIR, f"{args.results_prefix}_safari.csv")

    # Create alternating browser sequence
    browser_sequence = []
    for i in range(1):
        browser_sequence.extend(['--browser "Google Chrome"', '--browser "safari"'])

    # Build the full command with all 60 browser tests
    browser_args = ' '.join(browser_sequence)
    command = f'./target/release/energibridge -o {combined_output} --summary {experiment_path} {args.url} {browser_args} {args.search_word}'

    # Run single energibridge session for all tests
    print("Starting energibridge session for all tests...")
    open_terminal()
    time.sleep(3)
    pyautogui.write(command, interval=0.05)
    pyautogui.press('enter')

    # Wait for all tests to complete
    total_wait_time = 60 * 60  # Adjust based on actual test duration
    time.sleep(4)

    # Close energibridge session
    close_terminal()

    # Split results into separate files by browser
    print("Splitting results by browser...")
    df = pd.read_csv(combined_output)
    chrome_df = df[df['browser'] == 'Google Chrome']
    safari_df = df[df['browser'] == 'safari']

    chrome_df.to_csv(chrome_output, index=False)
    safari_df.to_csv(safari_output, index=False)
    os.remove(combined_output)


if __name__ == "__main__":
    main()