# 🔗 How Two Computers Connect - Complete Guide

## Overview: Computer A & Computer B

```
COMPUTER A (Parent's PC/Laptop/Phone)          COMPUTER B (Child's Laptop)
════════════════════════════════════            ════════════════════════════
   • Browser: Chrome/Firefox/Safari              • Python Client Running
   • Accesses: http://192.168.0.104:5000        • Monitors System
   • Parent clicks buttons                       • Executes Commands
                                                  
                  ↓↓↓ via MongoDB ↓↓↓
          
                   MONGODB DATABASE
                   (Cloud or Local)
                   ═════════════════
                   • Commands
                   • Screenshots  
                   • Keystrokes
                   • Device Info
```

---

## Step 1: THE CONNECTION FLOW

### When Parent Clicks "Take Screenshot" Button

```
┌─────────────────────────────────────────────────────────┐
│ PARENT (Computer A)                                     │
│ Clicks "Screenshot" button on dashboard                │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ Frontend (index.html) JavaScript:                       │
│ fetch('/api/command/screenshot', {method: 'POST'})      │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ Backend (backend.py) Flask Server:                      │
│ @app.route('/api/command/screenshot', methods=['POST']) │
│ Stores command in MongoDB 'commands' collection         │
│ Command = {device_id: 'CHILD-PC', action: 'screenshot'}│
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ MONGODB DATABASE (Cloud/Local):                         │
│ commands collection: [{device_id: 'CHILD-PC',           │
│                        action: 'screenshot',             │
│                        timestamp: 2024-01-15 10:30}]    │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ CHILD (Computer B)                                      │
│ client.py polling MongoDB every 5 seconds:              │
│ "Any new commands for CHILD-PC?"                        │
│ Finds the screenshot command!                           │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ CHILD's client.py executes:                             │
│ 1. Takes screenshot with pyautogui.screenshot()         │
│ 2. Converts to Base64 encoding                          │
│ 3. Uploads to MongoDB 'results' collection              │
│ 4. Deletes command from 'commands' collection           │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ MONGODB DATABASE                                        │
│ results collection: [{device_id: 'CHILD-PC',            │
│                       screenshot: 'iVBORw0KGgo...'}]    │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ PARENT (Computer A)                                     │
│ Parent refreshes dashboard or auto-updates              │
│ fetch('/api/results/screenshot')                        │
│ Backend retrieves from MongoDB                          │
│ Screenshot displays in browser on parent's screen! ✅   │
└─────────────────────────────────────────────────────────┘
```

---

## Step 2: KEY COMPONENTS

### Device Identification (The ID System)

```python
# On child's computer (client.py):
DEVICE_ID = socket.gethostname()  # Example: "RONIT-LAPTOP"

# This ID is stored in MongoDB with all commands
# Parent's commands target this specific device
# Multiple children? Each has different device_id!
```

### MongoDB Collections (The Message Board)

```python
# Think of these as bulletin boards:

1. commands:
   {device_id: "CHILD-PC", action: "screenshot", timestamp: "2024-01-15"}
   └─ Parent writes here, Child reads from here

2. results:
   {device_id: "CHILD-PC", screenshot: "base64_image_data", timestamp: "2024-01-15"}
   └─ Child writes here, Parent reads from here

3. keystrokes:
   {device_id: "CHILD-PC", key: "a", timestamp: "2024-01-15"}
   └─ Child writes here, Parent reads from here

4. devices:
   {device_id: "CHILD-PC", status: "online", last_seen: "2024-01-15"}
   └─ Child updates every 5 seconds
```

### Polling (How Child Checks for Commands)

```python
# In client.py - runs every 5 seconds:

while True:
    # Check MongoDB: Are there commands for me?
    commands = db['commands'].find({'device_id': DEVICE_ID})
    
    for command in commands:
        # Execute the command
        if command['action'] == 'screenshot':
            take_screenshot()
        elif command['action'] == 'lock':
            lock_screen()
        # ... etc
        
    # Sleep 5 seconds before checking again
    time.sleep(5)
```

---

## Step 3: NETWORK SETUP

### Scenario 1: Same WiFi Network (Home)

```
├─ Router (192.168.0.1)
│  ├─ Computer A (Parent): 192.168.0.104
│  ├─ Computer B (Child): 192.168.0.105
│  └─ MongoDB Server: 192.168.0.106 (or same as Backend)
│
└─ Connection: Direct local network - FAST ✅
```

**Setup:**
- Parent and Child on same WiFi
- Backend runs on Computer A (or separate machine)
- MongoDB runs locally or on Computer A
- Child's `BACKEND_URL = "http://192.168.0.104:5000"`
- Child's `MONGO_URI = "mongodb://192.168.0.104:27017/"`

### Scenario 2: Different Networks (Remote)

```
├─ Parent's Network (Another City/Country)
│  └─ Computer A: 203.45.67.89 (Public IP)
│
└─ Child's Network (Home)
   └─ Computer B: 192.168.1.50 (Local IP)
   
   Connection: Via MongoDB Atlas (Cloud) ✅
```

**Setup:**
- Use MongoDB Atlas (free cloud database)
- Both connect to cloud MongoDB
- Backend deployed to cloud (Heroku, PythonAnywhere, etc.)
- Child's `MONGO_URI = "mongodb+srv://username:password@cluster.mongodb.net/"`

---

## Step 4: LOGIN SYSTEM (Security)

### Why You Need a Login System

```
WITHOUT LOGIN:                  WITH LOGIN:
Any person on network    →      Only parent who knows
can access dashboard      →      password can access
├─ See child's photos    →      ├─ Secure access
├─ Lock computer         →      ├─ Can't be hacked easily
└─ Steal keystrokes      →      └─ Protected! ✅
```

### How Login Works

```
1. Parent goes to: http://192.168.0.104:5000/login
   ↓
2. Sees login page (NEW LOGIN_HTML template)
   ↓
3. Enters password: "YourSecurePassword123"
   ↓
4. Flask checks: password == ADMIN_PASSWORD ✓
   ↓
5. Session created: session['user_id'] = 'admin'
   ↓
6. Redirected to dashboard (/)
   ↓
7. Access granted to all /api/ endpoints ✓
```

### Routes with Login Protection

```python
# PROTECTED (redirects to /login if not authenticated):
GET  /                          → Dashboard
POST /api/command/screenshot    → Take screenshot
POST /api/command/lock          → Lock screen
POST /api/command/restart       → Restart computer
GET  /api/devices               → List devices

# UNPROTECTED (public access):
GET  /login                     → Login page
POST /login                     → Process login
GET  /logout                    → Clear session
```

---

## Step 5: COMPLETE SETUP INSTRUCTIONS

### For Parent (Computer A):

```bash
# 1. Clone/Download the project
cd techshurujan_2026

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start MongoDB (local or use Atlas)
# Local: mongod (starts MongoDB server)
# Cloud: Already running (Atlas)

# 4. Start Flask backend
python backend.py
# Output: * Running on http://127.0.0.1:5000

# 5. Open browser
# URL: http://192.168.0.104:5000/login
# Password: YourSecurePassword123 (CHANGE THIS!)
# Click Login
# ✅ Dashboard appears!
```

### For Child (Computer B):

```bash
# 1. Copy client.py to child's computer
# (Same project folder)

# 2. IMPORTANT: Update configuration in client.py
BACKEND_URL = "http://192.168.0.104:5000"  # Parent's IP
MONGO_URI = "mongodb://192.168.0.104:27017/"  # MongoDB location

# 3. Run client
python client.py
# Output: Device registered: CHILD-PC
#         Polling for commands...

# ✅ Child's computer is now monitored!
```

---

## Step 6: CHANGE THE PASSWORD!

### CRITICAL: Update Admin Password

**In `backend.py` (line ~30):**

```python
# ❌ DEFAULT (INSECURE):
ADMIN_PASSWORD = "YourSecurePassword123"

# ✅ CHANGE TO (SECURE):
ADMIN_PASSWORD = "MySecurePassword@2024#ChildMonitor"
```

**Generate a strong password:**
```
Option 1: Use random generator
- "Kx8$mP2nQw9@Lq1"

Option 2: Use passphrase
- "BlueSky#Sunrise2024!Monitor"

Option 3: Make it memorable
- "MyChild#2024!Protect"
```

---

## Step 7: AUTHENTICATION DECORATOR

### How Routes Are Protected

```python
# When parent clicks button:
fetch('/api/command/screenshot', {method: 'POST'})
                                    ↓
                    @app.before_request
                    check_logged_in()
                    ↓
            Is user logged in?
            (Check session['user_id'])
            ├─ YES: Continue to route ✅
            └─ NO: Return 401 error ❌
                   Redirect to /login ❌
```

---

## Step 8: TROUBLESHOOTING CONNECTION

### Issue: "Child's computer not showing in dashboard"

```
Checklist:
□ Is MongoDB running?
  → Local: mongod running?
  → Cloud: MongoDB Atlas connection string correct?

□ Is child's client.py running?
  → Console should show: "Device registered: CHILD-PC"
  → Should show: "Polling for commands..."

□ Are IPs correct?
  → Parent: http://192.168.0.104:5000
  → Child: BACKEND_URL = "http://192.168.0.104:5000"

□ Same WiFi network?
  → Both on 192.168.0.* ?

□ Firewall blocking?
  → Allow port 5000 (Flask)
  → Allow port 27017 (MongoDB)
```

### Issue: "Screenshot takes too long"

```
Solutions:
1. Try lower resolution:
   Edit client.py → screenshot quality
   
2. Close background apps on child's PC

3. Faster internet connection

4. Use local MongoDB (not cloud)
   → Faster than cloud MongoDB
```

### Issue: "Keylogger not recording"

```
Troubleshooting:
1. Is pynput installed?
   → pip install pynput

2. Run from command prompt (not IDE)
   → Some IDEs block pynput

3. On Windows: Run as Administrator
   → Right-click → "Run as Administrator"

4. Check pynput permissions
   → Settings → Privacy → Camera/Mic
```

---

## QUICK REFERENCE DIAGRAM

```
                    ┌─────────────────────┐
                    │   PARENT (A)        │
                    │  Web Dashboard      │
                    │  :5000/login        │
                    │  [Screenshot]       │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  FLASK BACKEND      │
                    │  Routes & Endpoints │
                    │  backend.py         │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │   MONGODB           │
                    │  (commands/results) │
                    │  localhost:27017    │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  CHILD (B)          │
                    │  Monitoring Agent   │
                    │  client.py          │
                    │  (Polling every 5s) │
                    └─────────────────────┘
```

---

## SUMMARY

✅ **How A & B Connect:**
- Parent clicks button on dashboard (A)
- Command stored in MongoDB
- Child polls MongoDB every 5 seconds (B)
- Child executes command
- Result uploaded to MongoDB
- Parent sees result in dashboard

✅ **Why Login System:**
- Prevents unauthorized access
- Only parent can see child's data
- Protects privacy

✅ **Password Protection:**
- Change default password!
- Use strong password (letters + numbers + symbols)
- Session-based authentication

✅ **Network Flexibility:**
- Same WiFi: Use local IPs
- Different locations: Use MongoDB Atlas + deployed backend

🎉 **You're ready to deploy!**
