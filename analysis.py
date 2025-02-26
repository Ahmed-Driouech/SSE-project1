import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import os


# Function to detect runs based on time gaps
def detect_runs(df):
    time_col = df.columns[1]  # Assuming the second column is the timestamp (milliseconds)
    df[time_col] = pd.to_numeric(df[time_col], errors="coerce")  # Ensure numeric timestamps

    df["time_diff"] = df[time_col].diff()  # Compute time difference between consecutive rows

    # Identify new runs when the time gap is greater than 60 seconds (60,000 ms)
    df["run_number"] = (df["time_diff"] > 60000).cumsum()

    df.drop(columns=["time_diff"], inplace=True)  # Drop temporary column

    return df


# Load and process the data
def load_data(file_path):
    df = pd.read_csv(file_path)
    df = detect_runs(df)  # Detect runs automatically
    return df


# Compute Energy Consumption per Run (Energy = Power * Time)
def compute_energy_per_run(df):
    time_col = df.columns[0]  # Delta time in milliseconds
    power_col = "SYSTEM_POWER (Watts)"  # Power consumption column

    # Convert milliseconds to seconds for energy calculation
    df["energy"] = (df[time_col] / 1000) * df[power_col]

    # Sum total energy for each run
    total_energy_per_run = df.groupby("run_number")["energy"].sum()
    return total_energy_per_run


# Detect Outliers using Z-score method
def detect_outliers(energy_data, threshold=3.0):
    mean_energy = np.mean(energy_data)
    std_energy = np.std(energy_data)

    z_scores = (energy_data - mean_energy) / std_energy
    outliers = energy_data[np.abs(z_scores) > threshold]

    return outliers.index.tolist()

# Normality Test (D'Agostino K² Test)
def check_normality(energy_series):
    stat, p_value = stats.normaltest(energy_series)
    return p_value > 0.05  # If p > 0.05, assume normal distribution

# Statistical Significance Test (Welch’s t-test for normal, Mann-Whitney U for non-normal)
def significance_test(energy_1, energy_2, normal_1, normal_2):
    if normal_1 and normal_2:
        test_stat, p_value = stats.ttest_ind(energy_1, energy_2, equal_var=False)
        test_used = "Welch’s t-test"
    else:
        test_stat, p_value = stats.mannwhitneyu(energy_1, energy_2)
        test_used = "Mann-Whitney U test"
    return test_used, test_stat, p_value

# Generate Enhanced Violin Plot
def make_violin_plot(chrome_energy, safari_energy, filename):
    fig, ax = plt.subplots(figsize=(8, 6))

    # Create the violin plot with distinct colors
    parts = ax.violinplot([chrome_energy, safari_energy], showmeans=False, showmedians=True)

    # Set colors
    colors = ["#1f77b4", "#ff7f0e"]  # Blue for Chrome, Orange for Safari
    for i, pc in enumerate(parts["bodies"]):
        pc.set_facecolor(colors[i])
        pc.set_edgecolor("black")
        pc.set_linewidth(1)
        pc.set_alpha(0.7)

    # Boxplot overlay for quartiles
    medianprops = dict(color="black", linewidth=2)
    ax.boxplot([chrome_energy, safari_energy], medianprops=medianprops)

    # Improve readability
    ax.set_xticks([1, 2])
    ax.set_xticklabels(["Chrome", "Safari"], fontsize=12)
    ax.set_ylabel("Energy Consumption (Joules)", fontsize=12)
    ax.set_title("Energy Consumption per Run", fontsize=14, fontweight="bold")
    ax.grid(axis="y", linestyle="--", alpha=0.6)

    # Save figure
    plt.tight_layout()
    fig.savefig(f"results/{filename}", dpi=300)

# Generate Time Series Plot
def make_time_series_plot(df_chrome, df_safari):
    fig, ax = plt.subplots(2, 1)

    for run_id, data_set in df_chrome.groupby("run_number"):
        ax[0].plot(np.cumsum(data_set.iloc[:, 0]), data_set["SYSTEM_POWER (Watts)"])
    ax[0].set_title("Chrome")
    ax[0].set_ylabel("Power (W)")
    ax[0].set_xlabel("Time (ns)")

    for run_id, data_set in df_safari.groupby("run_number"):
        ax[1].plot(np.cumsum(data_set.iloc[:, 0]), data_set["SYSTEM_POWER (Watts)"])
    ax[1].set_title("Safari")
    ax[1].set_ylabel("Power (W)")
    ax[1].set_xlabel("Time (ns)")

    plt.subplots_adjust(hspace=0.5)
    fig.savefig("results/time_series.png")


# Main execution
chrome_path = "results/test_chrome.csv"
safari_path = "results/test_safari.csv"

df_chrome = load_data(chrome_path)
df_safari = load_data(safari_path)

chrome_energy = compute_energy_per_run(df_chrome)
safari_energy = compute_energy_per_run(df_safari)

# Detect outliers
chrome_outliers = detect_outliers(chrome_energy)
safari_outliers = detect_outliers(safari_energy)

# Filter data without outliers
chrome_energy_no_outliers = chrome_energy.drop(chrome_outliers)
safari_energy_no_outliers = safari_energy.drop(safari_outliers)

# Normality Testing
chrome_normal = check_normality(chrome_energy_no_outliers)
safari_normal = check_normality(safari_energy_no_outliers)

# Statistical Test
test_used, test_stat, p_value = significance_test(chrome_energy_no_outliers, safari_energy_no_outliers, chrome_normal, safari_normal)

# Print Summary Stats & Outlier Counts
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

# Generate Plots With Outliers
make_violin_plot(chrome_energy, safari_energy, "violin_plot_with_outliers.png")

# Generate Plots Without Outliers
make_violin_plot(chrome_energy_no_outliers, safari_energy_no_outliers, "violin_plot_without_outliers.png")

make_time_series_plot(df_chrome, df_safari)

print("Analysis complete. Plots saved in results directory.")
