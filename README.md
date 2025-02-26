# Energy Consumption in PDF Readers: A Comparative Analysis

## Overview

This repository contains a Python project developed for the **Sustainable Software Engineering** course at **Delft University of Technology**. The project investigates the energy consumption of two built-in PDF readers, **Google Chrome** and **Safari**, on macOS. It aims to determine whether significant differences exist in their power usage when rendering and interacting with PDFs.

## Features

- **Automated PDF interaction**: Uses Python scripts to scroll through and search within PDFs.
- **Energy measurement**: Utilizes **EnergiBridge** to log power consumption.
- **Data analysis**: Detects outliers, calculates summary statistics, and performs statistical tests.
- **Visualization**: Generates **violin plots** and **time-series graphs** to illustrate energy usage patterns.

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/ahsmi47/SSE-project1.git
cd SSE-project1
```

### 2. Install Dependencies
Ensure Python is installed, then install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### 1. Run the Experiment
This script launches **Chrome** and **Safari**, automates PDF interactions, and records power consumption.
```bash
python main.py
```

### 2. Analyze Results
Processes logs, detects outliers, computes summary statistics, and generates plots.
```bash
python analysis.py
```

## Output

- **Energy consumption statistics** are printed in the terminal.
- **Violin and time-series plots** are saved in the `results/` directory.

## Replication Package

All code and data required to replicate the experiment are available in this repository:  
[GitHub Repository](https://github.com/ahsmi47/SSE-project1)

- The experiment can be rerun by executing `main.py`, which will perform the measurements.
- After data collection, `analysis.py` can be run to process the results.
- All results, including computed statistics and plots, will be stored in the `results/` directory.

The code is **license-free** and can be modified or extended as needed.

## License

This project is **open-source** and provided under an MIT license. Feel free to use, modify, and improve the code as needed.

## Authors

Ahmed Driouech, Ahmed Ibrahim, Taoufik el Kadi, Moegiez Bhatti  
**February 28, 2025**
```