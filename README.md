# SilentWatcher

## Overview

**SilentWatcher** is a comprehensive keylogger designed to monitor and record user activities discreetly. The tool captures keystrokes, screenshots, camera images, and audio recordings. It also tracks browser activity and network interfaces. The collected data is sent via email for analysis.

This project demonstrates advanced logging and monitoring techniques while ensuring stealth and security. It is compatible with Windows, Linux, and macOS systems.

## Features

- **Keystroke Logging:** Captures all keyboard inputs.
- **Screenshot Capture:** Takes periodic screenshots of the user's desktop.
- **Camera Image Capture:** Records images from the system's webcam.
- **Audio Recording:** Records audio from the system's microphone.
- **Browser Activity Tracking:** Logs URLs and visit counts from popular browsers.
- **System Information Gathering:** Collects details about the system's hardware and software.
- **Geolocation Tracking:** Retrieves the user's geolocation based on their IP address.
- **Network Interface Information:** Lists connected network interfaces.
- **Email Reporting:** Sends collected data via email with attachments.

## Installation

### Prerequisites

- Python 3.x
- pip (Python package installer)

### Packages

Ensure you have the required Python packages installed. You can install them using pip:

```bash
pip install pynput pyautogui opencv-python sounddevice wave requests psutil python-dotenv
```

## Configuration
Create a .env file in the project directory to store your email credentials:

```plaintext
EMAIL=your_email@example.com
PASSWORD=your_email_password
```
Make sure to replace your_email@example.com and your_email_password with your actual email credentials.

## Usage
Save the provided code as keylogger.py in your project directory.

Open a terminal or command prompt.

Run the script using Python:

```bash
python keylogger.py
```
The keylogger will start running, capturing data according to the specified intervals.

## Code Details
- **Initialization:** The keylogger starts by initializing the logging interval and setting up stealth mode to hide the console window on Windows.
- **Data Capture:** It captures keystrokes, screenshots, camera images, and audio recordings.
- **Browser Activity:** Logs browsing history from various browsers and saves it to a temporary file.
- **Email Reporting:** Periodically sends an email with collected data, including screenshots, camera images, audio recordings, and browser activity logs.
- **System and Network Information:** Gathers system information and network interfaces to include in the email report.

## Security and Ethical Considerations
- **Usage:** Ensure you use this tool responsibly and with permission. Unauthorized use may violate laws and regulations.
- **Security:** Do not expose your email credentials or other sensitive information.
