import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import os


def detect_runs(df):
    """
    Identifies distinct runs in the dataset based on time gaps between consecutive entries.
    """
    time_col = df.columns[1]  # Assuming the second column is the timestamp (milliseconds)
    df[time_col] = pd.to_numeric(df[time_col], errors="coerce")
    df["time_diff"] = df[time_col].diff()
    df["run_number"] = (df["time_diff"] > 60000).cumsum()
    df.drop(columns=["time_diff"], inplace=True)
    return df

def load_data(file_path):
    """
    Loads CSV data and processes it to identify runs.
    """
    df = pd.read_csv(file_path)
    df = detect_runs(df)
    return df

def compute_energy_per_run(df):
    """
    Computes total energy consumption per run using power and time.
    """
    time_col = df.columns[0]
    power_col = "SYSTEM_POWER (Watts)"
    df["energy"] = (df[time_col] / 1000) * df[power_col]
    return df.groupby("run_number")["energy"].sum()

def detect_outliers(energy_data, threshold=3.0):
    """
    Detects outliers in energy consumption using the Z-score method.
    """
    mean_energy = np.mean(energy_data)
    std_energy = np.std(energy_data)
    z_scores = (energy_data - mean_energy) / std_energy
    return energy_data[np.abs(z_scores) > threshold].index.tolist()

def check_normality(energy_series):
    """
    Tests whether the energy consumption data follows a normal distribution.
    """
    stat, p_value = stats.normaltest(energy_series)
    return p_value > 0.05

def significance_test(energy_1, energy_2, normal_1, normal_2):
    """
    Compares two energy datasets using an appropriate statistical test based on normality.
    """
    if normal_1 and normal_2:
        test_stat, p_value = stats.ttest_ind(energy_1, energy_2, equal_var=False)
        test_used = "Welch’s t-test"
    else:
        test_stat, p_value = stats.mannwhitneyu(energy_1, energy_2)
        test_used = "Mann-Whitney U test"
    return test_used, test_stat, p_value

def plot_violin(chrome_energy, safari_energy, filename):
    """
    Creates a violin plot comparing Chrome and Safari energy consumption.
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    parts = ax.violinplot([chrome_energy, safari_energy], showmeans=False, showmedians=True)
    colors = ["#1f77b4", "#ff7f0e"]
    for i, pc in enumerate(parts["bodies"]):
        pc.set_facecolor(colors[i])
        pc.set_edgecolor("black")
        pc.set_linewidth(1)
        pc.set_alpha(0.7)
    medianprops = dict(color="black", linewidth=2)
    ax.boxplot([chrome_energy, safari_energy], medianprops=medianprops)
    ax.set_xticks([1, 2])
    ax.set_xticklabels(["Chrome", "Safari"], fontsize=12)
    ax.set_ylabel("Energy Consumption (Joules)", fontsize=12)
    ax.set_title("Energy Consumption per Run", fontsize=14, fontweight="bold")
    ax.grid(axis="y", linestyle="--", alpha=0.6)
    plt.tight_layout()
    fig.savefig(f"results/{filename}", dpi=300)

def plot_time_series(df_chrome, df_safari):
    """
    Generates a time series plot for power consumption in Chrome and Safari.
    """
    fig, ax = plt.subplots(2, 1)
    for _, data_set in df_chrome.groupby("run_number"):
        ax[0].plot(np.cumsum(data_set.iloc[:, 0]), data_set["SYSTEM_POWER (Watts)"])
    ax[0].set_title("Chrome")
    ax[0].set_ylabel("Power (W)")
    ax[0].set_xlabel("Time (ns)")
    for _, data_set in df_safari.groupby("run_number"):
        ax[1].plot(np.cumsum(data_set.iloc[:, 0]), data_set["SYSTEM_POWER (Watts)"])
    ax[1].set_title("Safari")
    ax[1].set_ylabel("Power (W)")
    ax[1].set_xlabel("Time (ns)")
    plt.subplots_adjust(hspace=0.5)
    fig.savefig("results/time_series.png")

chrome_path = "results/test_chrome.csv"
safari_path = "results/test_safari.csv"

df_chrome = load_data(chrome_path)
df_safari = load_data(safari_path)

chrome_energy = compute_energy_per_run(df_chrome)
safari_energy = compute_energy_per_run(df_safari)

chrome_outliers = detect_outliers(chrome_energy)
safari_outliers = detect_outliers(safari_energy)

chrome_energy_no_outliers = chrome_energy.drop(chrome_outliers)
safari_energy_no_outliers = safari_energy.drop(safari_outliers)

chrome_normal = check_normality(chrome_energy_no_outliers)
safari_normal = check_normality(safari_energy_no_outliers)

test_used, test_stat, p_value = significance_test(chrome_energy_no_outliers, safari_energy_no_outliers, chrome_normal, safari_normal)

print(f"Detected runs in Chrome: {df_chrome['run_number'].nunique()}")
print(f"Detected runs in Safari: {df_safari['run_number'].nunique()}")

print(f"Chrome Outliers Detected: {len(chrome_outliers)} / {len(chrome_energy)} runs")
print(f"Safari Outliers Detected: {len(safari_outliers)} / {len(safari_energy)} runs")

print("\nSummary Statistics (Including Outliers):")
print(f"Chrome - Min: {chrome_energy.min()} J, Max: {chrome_energy.max()} J, Variance: {np.var(chrome_energy)}, Mean: {chrome_energy.mean()} J")
print(f"Safari - Min: {safari_energy.min()} J, Max: {safari_energy.max()} J, Variance: {np.var(safari_energy)}, Mean: {safari_energy.mean()} J")

print("\nSummary Statistics (Without Outliers):")
print(f"Chrome - Min: {chrome_energy_no_outliers.min()} J, Max: {chrome_energy_no_outliers.max()} J, Variance: {np.var(chrome_energy_no_outliers)}, Mean: {chrome_energy_no_outliers.mean()} J")
print(f"Safari - Min: {safari_energy_no_outliers.min()} J, Max: {safari_energy_no_outliers.max()} J, Variance: {np.var(safari_energy_no_outliers)}, Mean: {safari_energy_no_outliers.mean()} J")


print(f"\nNormality Check: Chrome ({'Normal' if chrome_normal else 'Non-Normal'}), Safari ({'Normal' if safari_normal else 'Non-Normal'})")
print(f"Statistical Test Used: {test_used}")
print(f"Test Statistic: {test_stat}, p-value: {p_value}")
if p_value < 0.05:
    print("Significant difference found between Chrome and Safari energy consumption.")
else:
    print("No significant difference found.")

plot_violin(chrome_energy, safari_energy, "violin_plot_with_outliers.png")

plot_violin(chrome_energy_no_outliers, safari_energy_no_outliers, "violin_plot_without_outliers.png")

plot_time_series(df_chrome, df_safari)

print("Analysis complete. Plots saved in results directory.")
