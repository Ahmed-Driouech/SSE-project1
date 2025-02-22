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
    os.system("osascript -e 'tell application \"Terminal\" to close front window'")


def run_experiment(command):
    open_terminal()
    time.sleep(3)
    pyautogui.write(command, interval=0.05)
    pyautogui.press('enter')
    time.sleep(10)
    close_terminal()

def concatenate_csvs(file_list, output_file):
    #Combine multiple CSV files into one
  
    full_paths = [os.path.join(BASE_DIR, f) for f in file_list]
    dfs = [pd.read_csv(f) for f in full_paths]
    combined_df = pd.concat(dfs, ignore_index=True)
   
    full_output_path = os.path.join(BASE_DIR, output_file)
    combined_df.to_csv(full_output_path, index=False)
    
    for f in full_paths:
        os.remove(f)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("results_prefix")
    parser.add_argument("url")
    parser.add_argument("search_word")
    args = parser.parse_args()

    # Final output files
    chrome_output = os.path.join(BASE_DIR, f"{args.results_prefix}_chrome.csv")
    safari_output = os.path.join(BASE_DIR, f"{args.results_prefix}_safari.csv")

    # Temporary file lists
    chrome_temp_files = []
    safari_temp_files = []

    # Define browsers
    browser_runs = ["Google Chrome", "safari"]

    for i in range(1):  
        for browser in browser_runs:
            
            temp_output = f"{args.results_prefix}_{browser.lower().replace(' ', '_')}_temp_{i + 1}.csv"
            full_temp_path = f"{BASE_DIR}{temp_output}"
            command = f'./target/release/energibridge -o {full_temp_path} --summary {experiment_path} {args.url} --browser "{browser}" {args.search_word}'

            print(f"Running experiment {i + 1}/30 for {browser}...")
            run_experiment(command)
            time.sleep(10)  # Delay between runs to avoid overlap

          
            if browser == "Google Chrome":
                chrome_temp_files.append(temp_output)
            else:  # Safari
                safari_temp_files.append(temp_output)

    # Combine results into final CSV files
    print("Combining Chrome results...")
    concatenate_csvs(chrome_temp_files, chrome_output)
    print("Combining Safari results...")
    concatenate_csvs(safari_temp_files, safari_output)
    #command = f'./target/release/energibridge -o {args.results}.csv --summary {experiment_path} {args.url} --browser "{args.browser}" {args.search_word}'
    #close_terminal()


if __name__ == "__main__":
    main()
