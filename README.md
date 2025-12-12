# Memory Sentry

A heuristic-based memory leak detector for macOS. 
It sits in the background, filtering out noise (like Chrome tabs) and alerting you only when a process shows a definitive "Rising Floor" leak pattern.

## Features
* **Smart Filtering:** Distinguishes between "Heavy Usage" (YouTube) and "Memory Leaks" (Slope Detection).
* **Browser Aware:** Applies stricter probation logic to Chrome/Electron helpers to avoid false positives.
* **Critical Alerts:** Uses native macOS modal popups so you never miss a memory leak.

## Installation

1. Open Terminal in this folder.
2. Run the installation command:
   ```bash
   pip3 install .
3. Then, from anywhere you can run the command:
   ```bash
   msentry
4. You have successfully started Memory Sentry! Now wait until it detects a memory leak.
5. You can use Ctrl + C to quit Memory Sentry within the CLI.
