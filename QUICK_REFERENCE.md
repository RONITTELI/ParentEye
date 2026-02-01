# ⚡ QUICK REFERENCE CARD

## 🚀 START THE SYSTEM

### Terminal 1: MongoDB
```bash
mongod
# Output: [initandlisten] waiting for connections on port 27017
```

### Terminal 2: Flask Backend
```bash
cd c:\Users\ronit\Desktop\techshurujan_2026
python backend.py
# Output: * Running on http://127.0.0.1:5000
```

### Terminal 3: Child Client (On child's computer)
```bash
# First edit client.py:
# BACKEND_URL = "http://192.168.0.104:5000"  # Parent's IP
# MONGO_URI = "mongodb://192.168.0.104:27017/"

python client.py
# Output: Device registered: CHILD-PC
#         Polling for commands...
```

### Browser: Access Dashboard
```
http://192.168.0.104:5000/login
Password: YourSecurePassword123
```

---

## 🔐 LOGIN CREDENTIALS

```
Default Password: YourSecurePassword123

⚠️ CHANGE THIS IMMEDIATELY!

How to change:
1. Open backend.py
2. Line ~30: ADMIN_PASSWORD = "YourSecurePassword123"
3. Change to: ADMIN_PASSWORD = "YourNewPassword"
4. Restart Flask (Ctrl+C then python backend.py)
5. Use new password to login
```

---

## 📋 DASHBOARD FEATURES

### Available Commands:
```
□ Take Screenshot      → Captures screen, displays in dashboard
□ Lock Computer        → Locks child's PC immediately
□ Restart Computer     → Restarts system (10 second delay)
□ Start Keylogger      → Records all keystrokes
□ Stop Keylogger       → Stops recording keystrokes
□ View Screenshots     → Shows history of screenshots
□ View Keystrokes      → Shows recorded typed text
□ Device Status        → Online/Offline status
```

---

## 🖥️ TWO-COMPUTER CONNECTION

```
PARENT (A)
   ↓
Website Dashboard
   ↓
Flask Backend (backend.py)
   ↓
MongoDB (Database)
   ↓
Client.py (child's computer)
   ↓
CHILD (B)
```

**Simple Rule:**
1. Parent writes command to MongoDB
2. Child reads MongoDB every 5 seconds
3. Child executes command
4. Child writes result to MongoDB
5. Parent reads result

---

## 🔒 SECURITY CHECKLIST

```
BEFORE DEPLOYMENT:
□ Changed default password?
□ Using strong password? (8+ chars, mix of symbols)
□ Firewall allows ports 5000 & 27017?
□ Both computers on same network?
□ MongoDB secured?
□ Session cookie enabled?
```

---

## 🐛 TROUBLESHOOTING

### Problem: "Login page not loading"
```
Solution:
1. Check: python backend.py running?
2. Check: Port 5000 open?
3. Check: Correct IP address?
4. Restart: Ctrl+C and run again
```

### Problem: "Can't login"
```
Solution:
1. Check: Password typo?
2. Check: CAPS LOCK on?
3. Check: Spaces before/after password?
4. Try: Default password
5. Edit: backend.py to change password
```

### Problem: "Child device not appearing"
```
Solution:
1. Check: client.py running on child PC?
2. Check: Shows "Device registered"?
3. Check: Shows "Polling for commands"?
4. Check: Same WiFi network?
5. Check: IP addresses correct?
6. Restart: Both backend and client
```

### Problem: "Commands not executing"
```
Solution:
1. Check: Child console shows no errors?
2. Check: MongoDB running?
3. Check: Ports 27017 open?
4. Restart: client.py
5. Try: Simple command (screenshot first)
```

---

## 📂 FILES OVERVIEW

```
backend.py (222 lines)
├─ Flask server
├─ API endpoints
├─ MongoDB connection
├─ Login system ✅ NEW
└─ Command execution

client.py (205 lines)
├─ Device registration
├─ MongoDB polling
├─ Command execution
├─ Screenshot capture
└─ Keystroke logging

index.html (480+ lines)
├─ Web dashboard
├─ Device display
├─ Command buttons
├─ Results display
└─ Real-time updates

requirements.txt
└─ 12 Python packages

NEW GUIDES:
├─ LOGIN_SYSTEM_GUIDE.md
├─ TWO_COMPUTER_CONNECTION_GUIDE.md
├─ PARENT_CHILD_CONNECTION_VISUAL.md
└─ SYSTEM_SUMMARY.md
```

---

## 🎯 COMMANDS REFERENCE

### API Endpoints (Backend):

```
POST /api/command/screenshot    → Capture screen
POST /api/command/lock          → Lock computer
POST /api/command/shutdown      → Shutdown PC
POST /api/command/restart       → Restart PC
POST /api/command/keylogger     → Start keylogger
POST /api/command/stop          → Stop operation
GET  /api/devices               → List devices
GET  /api/device/<id>           → Device info
GET  /api/results/<type>        → Get results
GET  /                          → Dashboard (protected)
GET  /login                     → Login page
POST /login                     → Authenticate
GET  /logout                    → Logout
```

---

## 💻 DEVICE IDs

```
Each child = unique Device ID

Examples:
• RONIT-LAPTOP
• SARAH-DESKTOP  
• ALI-COMPUTER

Multiple children:
├─ Create separate client.py on each
├─ Each has own device_id
├─ Control independently
└─ All in same MongoDB
```

---

## 📊 MONGODB COLLECTIONS

```
devices        → Device list & status
commands       → Commands to execute
results        → Execution results
screenshots    → Screenshot storage
keystrokes     → Logged keystrokes
```

---

## 🌐 NETWORK SETUP

### Home Network (Same WiFi):
```
Parent IP: 192.168.0.104
Child IP:  192.168.0.105
Backend URL: http://192.168.0.104:5000
MongoDB URL: mongodb://192.168.0.104:27017/
```

### Remote Network (Different locations):
```
Use MongoDB Atlas (cloud)
Use backend deployment (Heroku/PythonAnywhere)
mongodb+srv://user:pass@cluster.mongodb.net/
```

---

## ⏱️ TIMING

```
Parent clicks button: 1 second
Command stored in MongoDB: Instant
Child polls MongoDB: Every 5 seconds
Child finds command: 1 second
Child executes: Varies (1-5 seconds)
Result uploaded: 1-2 seconds
Parent sees result: 1 second
──────────────────────────
Total: 10-15 seconds
```

---

## 📱 MOBILE ACCESS

```
✅ Parent can use:
├─ Laptop browser
├─ Desktop browser
├─ Mobile phone browser
├─ Tablet browser
└─ Any device with browser

Just visit: http://192.168.0.104:5000/login
```

---

## 🔑 PASSWORD SECURITY

```
❌ Weak:    password123
✅ Strong:  BlueSky#Monitor2024
✅ Strong:  MyChild@2024!Protect
✅ Strong:  Kx8$mP2nQw9@Lq1

Pattern: Adjective + Symbol + Word + Number
```

---

## 🛠️ COMMON TASKS

### Change Password:
```
1. Edit backend.py (line ~30)
2. Change ADMIN_PASSWORD = "new_password"
3. Save
4. Restart Flask (Ctrl+C, python backend.py)
```

### Monitor Multiple Children:
```
1. Run client.py on each child's PC
2. Each gets unique device_id
3. Select device in dashboard
4. Send commands to specific child
```

### View History:
```
Dashboard tabs:
├─ Screenshots  → Past screenshots
├─ Keystrokes   → Typed text
├─ History      → Command history
└─ Status       → Device status
```

### Export Data:
```
MongoDB collections store everything
Use MongoDB Compass to export
Or: db.collection.find().forEach(...)
```

---

## 🚨 EMERGENCY

### Restart Everything:
```
1. Ctrl+C in Flask terminal
2. Ctrl+C in client terminal
3. Stop mongod (Ctrl+C)
4. Wait 5 seconds
5. Start mongod
6. Start Flask (backend.py)
7. Start client.py
```

### Clear All Data:
```
Python console:
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['child_monitoring']
db.drop_collection('commands')
db.drop_collection('results')
db.drop_collection('screenshots')
db.drop_collection('keystrokes')
```

### Force Logout All:
```
Python console:
from flask import session
session.clear()
```

---

## 📞 SUPPORT

```
Issue: Can't start Flask
Action: Check port 5000 not in use
        or:
        lsof -i :5000  (macOS/Linux)
        netstat -ano | findstr :5000  (Windows)

Issue: MongoDB not connecting
Action: Check mongod running
        mongod --version (verify installed)

Issue: Client not responding
Action: Check IP addresses match
        Check firewall allows 27017
        Restart client.py

Issue: Password forgotten
Action: Edit backend.py directly
        Change ADMIN_PASSWORD
        Restart Flask
```

---

## ✅ FINAL CHECKLIST

```
Before using:
□ MongoDB running
□ Flask running
□ client.py running (on child PC)
□ Can login to dashboard
□ Child device appears
□ Can execute commands
□ Results appear in dashboard
□ Logout works
□ Login works again

Then:
□ Change default password
□ Test all features
□ Set up on second child (if needed)
□ Configure for remote access (if needed)
```

---

**🎉 You're ready to monitor! Good luck!**
