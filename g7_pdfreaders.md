---
author: Ahmed Driouech, Taoufik el Kadi, Ahmed Ibrahim, Moegiez Bhatti
title: "Energy Consumption in PDF Readers: A Comparative Analysis"
image: "../img/p1_measuring_software/gX_template/cover.png"
date: 28/02/2025
summary: |-
  PDF readers are a widely used software tool, especially for students who spend considerable time reading e-books and study materials. This project explores the energy consumption of different PDF readers in various scenarios to provide insights into energy-efficient software choices. Our findings aim to help students and other users extend battery life, minimize environmental impact, and enhance user experience through informed software selection.
---

## Introduction

### Importance of Energy-Efficient Software

PDF readers are crucial for many users, particularly students who rely on them to read e-books and other study materials. Considering that students typically spend hours using these applications on their laptops, energy efficiency becomes a key factor. Prolonged use of power-hungry software can lead to frequent charging, reduced battery life, and overall environmental impact.

This report compares the energy consumption of multiple PDF readers in various scenarios, focusing on settings most relevant to student use cases. By understanding the energy consumption patterns, we aim to suggest the most efficient choices for students who want to maximize their battery life and reduce their carbon footprint.

## Research Objective

This project aims to investigate and compare the energy consumption of different PDF readers across the following dimensions:
**Different PDF Reader Applications** - Comparing different PDF reader apps for the same use case.

The ultimate goal is to provide insights into energy-efficient software choices for common use cases.

## Methodology

We conducted the experiment on two different PDF readers in browsers: the built-in Safari PDF reader and the Google Chrome PDF reader. With the experiment we simulated a typical reading session by opening a XX-page PDF file and interacting with it using common features. We includes actions that typical users might perform frequently, such as scrolling through the document and searching for specific keywords. The workflow for the experiment was as follows:

1. Open the browser.
2. Load the PDF file
3. Scroll through the entire document at a controlled speed
4. Use the dearch function to find a specific term multiple times (the first hit might not be what the person is looking for)
5. Close the document and quit the browser

Each iteration of the experiment lasted approximately 3 minutes. This includes a 60 second wait time between runs to prevent tail effect. With 60 iterations in total we have a total experiment runtime of about 3 hours.
We ran an automated script that opened the PDF in both browsers and performed the workflow actions. Each test was repeated 30 times per browser with the order of execution being interleaved (meaning, 1 experiment using Chrome, then 1 using Safari, 1 using Chrome etc).
### Experiment Setup

To ensure unbiased and accurate energy consumption data, we have adhered to the following best practices:

1. **Zen Mode Configuration**: During the experiments, all non-essential applications and services were turned off. Notifications were disabled, and unnecessary hardware (e.g., external drives, displays) was disconnected. This ensured that the only variable affecting energy consumption was the PDF reader.
   
2. **Fixed System Settings**: To maintain consistency across tests, system settings such as screen brightness and resolution were fixed throughout the experiment. Any potential energy-saving features, like automatic brightness adjustment, were disabled to avoid interference.

3. **Measurement Tools**: We used the EnergiBridge tool to meausre the energy consumption, cpu memory use, frequency and voltage over a period of time.

### PDF Readers Tested

### PDF Readers Tested

We selected two built-in PDF readers integrated into widely used web browsers for this study:

- **Built-in Google Chrome PDF Reader**: Google Chrome’s PDF reader is integrated directly into the browser, offering a fast and convenient way to open and view PDF files without requiring any additional software. It supports basic functions such as zooming, searching text, and navigating through pages. However, it lacks advanced features such as annotations, text editing, or form filling, focusing primarily on rendering and reading PDFs efficiently. Its cross-platform nature makes it a common choice for users across different operating systems, including Windows, macOS, and Linux.

- **Built-in Safari PDF Reader**: Safari’s PDF reader, integrated into Apple’s default web browser on macOS and iOS devices, provides a streamlined PDF viewing experience. Like Chrome’s PDF reader, it offers basic features like zooming, text search, and page navigation. However, Safari benefits from deeper integration with macOS, including support for macOS system-wide features like annotation via Preview and Continuity across Apple devices. Safari’s PDF reader is optimized for energy efficiency on macOS devices, benefiting from Apple's hardware-software synergy.


### Test Scenarios

We performed our tests in the following configurations:
   
**App Comparison**: We compared the energy consumption of different PDF readers while performing the same task, such as reading a 50-page PDF file.

## Results

### Comparison of Different PDF Reader Applications

**Key Findings**:

## Discussion

### Practical Implications for Students



### Recommendations for Energy-Efficient Usage



## Conclusion



---

## Replication Package

For those interested in replicating our experiments, we have provided the full setup and scripts in our [GitHub repository](link). This includes:
- A detailed guide on setting up the test environment.
- Scripts for measuring energy consumption.
- Instructions on how to compare different versions and settings.

---

## References

- [Insert relevant articles and studies here]
