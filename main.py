import argparse
import os
import subprocess
import time
import pandas as pd
import pyautogui

energiBridge_path = '/Users/ahmeddriouech/Desktop/SDSAIT/EnergiBridge'
experiment_path = '/Users/ahmeddriouech/Desktop/SSE-project1/experiment.py'
BASE_DIR = '/Users/ahmeddriouech/Desktop/SSE-project1/results/'

def fibonacci(n):
    """
    Computes the Fibonacci sequence recursively.
    """
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

def warm_up():
    """
    Performs a warm-up routine before running the experiment.
    """
    print("Warm-up before experiment...")
    start_time = time.time()
    fib = 0
    i = 0
    while time.time() - start_time < 60:
        fib = fibonacci(30)
        i += 1
    print(f"{i}th Fibonacci number is {fib}")
    print("Warm-up completed!")
    time.sleep(2)

def run_experiment(command):
    """
    Executes the given shell command to run the experiment.
    """
    try:
        os.chdir(energiBridge_path)
        print("Executing command...")
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True
        )
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            print("Experiment completed successfully")
            if stdout:
                print("Output:", stdout)
            return True
        else:
            print(f"Experiment failed with return code {process.returncode}")
            if stderr:
                print("Error:", stderr)
            return False
    except Exception as e:
        print(f"Error running experiment: {str(e)}")
        return False
    finally:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

def concatenate_csvs(file_list, output_file):
    """
    Merges multiple CSV files into one and removes temporary files.
    """
    full_paths = [os.path.join(BASE_DIR, f) for f in file_list]
    dfs = [pd.read_csv(f) for f in full_paths]
    combined_df = pd.concat(dfs, ignore_index=True)
    full_output_path = os.path.join(BASE_DIR, output_file)
    combined_df.to_csv(full_output_path, index=False)
    for f in full_paths:
        os.remove(f)

def main():
    """
    Parses command-line arguments and orchestrates the experiment execution.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("results_prefix")
    parser.add_argument("url")
    parser.add_argument("search_word")
    args = parser.parse_args()
    chrome_output = os.path.join(BASE_DIR, f"{args.results_prefix}_chrome.csv")
    safari_output = os.path.join(BASE_DIR, f"{args.results_prefix}_safari.csv")
    chrome_temp_files = []
    safari_temp_files = []
    browser_runs = ["Google Chrome", "safari"]
    warm_up()
    for i in range(30):
        for browser in browser_runs:
            temp_output = f"{args.results_prefix}_{browser.lower().replace(' ', '_')}_temp_{i + 1}.csv"
            full_temp_path = f"{BASE_DIR}{temp_output}"
            command = f'./target/release/energibridge -o {full_temp_path} --summary {experiment_path} {args.url} "{browser}" {args.search_word}'
            print(f"Running experiment {i + 1}/30 for {browser}...")
            run_experiment(command)
            time.sleep(5)
            if browser == "Google Chrome":
                chrome_temp_files.append(temp_output)
            else:
                safari_temp_files.append(temp_output)
            time.sleep(60)
    print("Combining Chrome results...")
    concatenate_csvs(chrome_temp_files, chrome_output)
    print("Combining Safari results...")
    concatenate_csvs(safari_temp_files, safari_output)

if __name__ == "__main__":
    main()
