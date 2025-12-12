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

## Testing

1. In case you'd like to test Memory Sentry on a simulated memory leak, I have you covered!
2. Simply run this command in a separate terminal instance:
   ```bash
   mvictim
3. Then, as usual, run:
   ```bash
   msentry
4. Wait until the strikes, and eventually the popup, show up, and voila, the leak is detected!
5. Make sure to stop both programs once you're done or else they will run forever. Do so with:
   ```bash
   Ctrl + C
