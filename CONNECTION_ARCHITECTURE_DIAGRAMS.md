# 🔌 CONNECTION ARCHITECTURE - ASCII DIAGRAMS

## Level 1: Big Picture

```
┏━━━━━━━━━━━━━━━━━━━━┓                          ┏━━━━━━━━━━━━━━━━━━━━┓
┃   PARENT (YOU)     ┃                          ┃   CHILD            ┃
┃   Computer A       ┃                          ┃   Computer B       ┃
┃   📱 Browser       ┃◄────── WiFi ────────────►┃   💻 Python Agent  ┃
┗━━━━━━━━━┬━━━━━━━━━┛                          ┗━━━━━━━━━┬━━━━━━━━━┛
          │                                                │
          │         ┏━━━━━━━━━━━━━━━━━━━━━┓              │
          └────────►┃   MONGODB DATABASE  ┃◄─────────────┘
                    ┃   Shared Message    ┃
                    ┃   Storage           ┃
                    ┗━━━━━━━━━━━━━━━━━━━━━┛

Communication Flow:
Parent → MongoDB ← Child (they don't talk directly!)
```

---

## Level 2: Detailed Architecture

```
╔════════════════════════════════════════════════════════════════╗
║                    PARENT'S COMPUTER                          ║
║ ┌──────────────────────────────────────────────────────────┐  ║
║ │                                                          │  ║
║ │  Web Browser (Chrome/Firefox/Safari)                    │  ║
║ │  ┌────────────────────────────────────────────────────┐ │  ║
║ │  │ http://192.168.0.104:5000/login                   │ │  ║
║ │  │                                                    │ │  ║
║ │  │ 👶 Child Monitor - Login                         │ │  ║
║ │  │ 🔒 Enter password:                               │ │  ║
║ │  │ [______________________]                         │ │  ║
║ │  │ [    Login Button    ]                           │ │  ║
║ │  │                                                    │ │  ║
║ │  │ After login → Dashboard with controls            │ │  ║
║ │  └────────────┬─────────────────────────────────────┘ │  ║
║ │               │                                         │  ║
║ │  ┌────────────▼─────────────────────────────────────┐ │  ║
║ │  │  JavaScript (Browser)                           │ │  ║
║ │  │  fetch('/api/command/screenshot')               │ │  ║
║ │  │  fetch('/api/command/lock')                     │ │  ║
║ │  │  fetch('/api/devices')                          │ │  ║
║ │  │  POST requests to Flask server                  │ │  ║
║ │  └────────────┬─────────────────────────────────────┘ │  ║
║ │               │                                         │  ║
║ │               ▼ Port 5000 (HTTP)                        │  ║
║ │  ┌────────────────────────────────────────────────────┐ │  ║
║ │  │  Flask Backend (backend.py)                      │ │  ║
║ │  │  ┌────────────────────────────────────────────┐  │ │  ║
║ │  │  │ @app.route('/login', methods=['GET','POST'])  │ │  ║
║ │  │  │ @app.route('/api/devices', methods=['GET'])   │ │  ║
║ │  │  │ @app.route('/api/command/screenshot', ...)    │ │  ║
║ │  │  │ ... 20+ API endpoints                          │ │  ║
║ │  │  │ Checks: Is user logged in? (session check)    │ │  ║
║ │  │  │ Actions: Store commands in MongoDB            │ │  ║
║ │  │  └────────────┬─────────────────────────────────┘  │ │  ║
║ │  └─────────────┼──────────────────────────────────────┘ │  ║
║ │                │                                         │  ║
║ │                ▼ Port 27017 (MongoDB)                    │  ║
║ │  ┌────────────────────────────────────────────────────┐ │  ║
║ │  │  MongoDB Server (localhost:27017)                 │ │  ║
║ │  │  db = "child_monitoring"                          │ │  ║
║ │  │  collections:                                     │ │  ║
║ │  │    - devices:     [{device_id, status, ...}]     │ │  ║
║ │  │    - commands:    [{device_id, action, ...}]     │ │  ║
║ │  │    - results:     [{device_id, screenshot, ...}] │ │  ║
║ │  │    - keystrokes:  [{device_id, key, ...}]        │ │  ║
║ │  │    - screenshots: [{device_id, image, ...}]      │ │  ║
║ │  └────────────────────────────────────────────────────┘ │  ║
║ │                                                          │  ║
║ └──────────────────────────────────────────────────────────┘  ║
╚════════════════════════════════════════════════════════════════╝
                           △
                           │
                    (Network Connection)
                           │
                           ▼
╔════════════════════════════════════════════════════════════════╗
║                    CHILD'S COMPUTER                           ║
║ ┌──────────────────────────────────────────────────────────┐  ║
║ │                                                          │  ║
║ │  Python Script (client.py)                              │  ║
║ │  ┌────────────────────────────────────────────────────┐ │  ║
║ │  │ import pymongo, pyautogui, pynput                 │ │  ║
║ │  │ DEVICE_ID = socket.gethostname()  # "CHILD-PC"   │ │  ║
║ │  │                                                    │ │  ║
║ │  │ while True:  # Polling loop                       │ │  ║
║ │  │     commands = db['commands'].find({              │ │  ║
║ │  │         'device_id': DEVICE_ID                    │ │  ║
║ │  │     })                                             │ │  ║
║ │  │                                                    │ │  ║
║ │  │     for cmd in commands:                           │ │  ║
║ │  │         if cmd['action'] == 'screenshot':         │ │  ║
║ │  │             img = pyautogui.screenshot()          │ │  ║
║ │  │             upload_to_mongodb(img)                │ │  ║
║ │  │                                                    │ │  ║
║ │  │     time.sleep(5)  # Check every 5 seconds        │ │  ║
║ │  │                                                    │ │  ║
║ │  │ Keystroke Listener:                               │ │  ║
║ │  │ listener = Listener(on_press=on_key_press)        │ │  ║
║ │  │ listener.start()  # Continuously running          │ │  ║
║ │  └────────────┬─────────────────────────────────────┘ │  ║
║ │               │                                         │  ║
║ │               ▼ Port 27017 (MongoDB)                    │  ║
║ │  ┌────────────────────────────────────────────────────┐ │  ║
║ │  │  MongoDB Connection                               │ │  ║
║ │  │  (Connects to parent's MongoDB)                    │ │  ║
║ │  │                                                    │ │  ║
║ │  │  Reads from: 'commands' collection               │ │  ║
║ │  │  Writes to:  'results' collection                │ │  ║
║ │  │              'keystrokes' collection             │ │  ║
║ │  │              'screenshots' collection            │ │  ║
║ │  │                                                    │ │  ║
║ │  │  Updates device status: 'devices' collection     │ │  ║
║ │  └────────────────────────────────────────────────────┘ │  ║
║ │                                                          │  ║
║ └──────────────────────────────────────────────────────────┘  ║
╚════════════════════════════════════════════════════════════════╝
```

---

## Level 3: Command Execution Flow

```
┌─────────────────────────────────────────────────────────────┐
│ PARENT CLICKS: [📷 Take Screenshot]                        │
└─────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ JavaScript in Browser                                       │
│ fetch('http://192.168.0.104:5000/api/command/screenshot',  │
│        {method: 'POST', device_id: 'CHILD-PC'})            │
└─────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ Flask Backend (@app.route('/api/command/screenshot'))       │
│                                                             │
│ 1. Check: session['user_id'] exists? ✅                    │
│ 2. Validate: device_id = "CHILD-PC" ✓                      │
│ 3. Create command document:                                 │
│    {                                                        │
│        _id: ObjectId("..."),                               │
│        device_id: "CHILD-PC",                              │
│        action: "screenshot",                               │
│        status: "pending",                                  │
│        created_at: DateTime.now()                          │
│    }                                                        │
│ 4. Insert into db['commands'] ✓                            │
│ 5. Return: {"status": "success"}                           │
└─────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ MongoDB 'commands' Collection                              │
│                                                             │
│ [                                                           │
│   {                                                         │
│     _id: ObjectId("507f1f77bcf86cd799439011"),             │
│     device_id: "CHILD-PC",                                 │
│     action: "screenshot",  ⬅─ WAITING HERE                │
│     status: "pending",                                     │
│     created_at: "2024-01-15 10:30:00"                      │
│   }                                                         │
│ ]                                                           │
└─────────────────────────────────────────────────────────────┘
        ▲                                        △
        │                                        │
        │                                        │ 5 second wait
        │                                        │
        └────────────────────────────────────────┘
                    (Polling check)
                            
┌─────────────────────────────────────────────────────────────┐
│ Child's client.py (Every 5 Seconds)                        │
│                                                             │
│ Query MongoDB:                                              │
│ db['commands'].find({'device_id': 'CHILD-PC'})             │
│                                                             │
│ Result: ✅ FOUND! (Not empty)                              │
│ {                                                           │
│   device_id: "CHILD-PC",                                   │
│   action: "screenshot",                                    │
│   status: "pending"                                        │
│ }                                                           │
└─────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ Execute Command                                             │
│                                                             │
│ 1. screenshot = pyautogui.screenshot()                     │
│ 2. Convert to PNG bytes                                    │
│ 3. Encode to Base64 (text format for JSON)                │
│ 4. Create result document:                                 │
│    {                                                        │
│        device_id: "CHILD-PC",                              │
│        command_id: ObjectId("507f1f77bcf86cd799439011"),  │
│        screenshot: "iVBORw0KGgoAAAANSUhEUgAAAAUA...",    │
│        success: true,                                      │
│        created_at: DateTime.now()                          │
│    }                                                        │
│ 5. Insert into db['results']                               │
│ 6. Delete from db['commands']                              │
└─────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ MongoDB 'results' Collection                               │
│                                                             │
│ [                                                           │
│   {                                                         │
│     _id: ObjectId("507f1f77bcf86cd799439012"),             │
│     device_id: "CHILD-PC",                                 │
│     command_id: ObjectId("507f1f77bcf86cd799439011"),     │
│     screenshot: "iVBORw0KGgo..."  ⬅─ IMAGE DATA           │
│     success: true,                                         │
│     created_at: "2024-01-15 10:30:15"                      │
│   }                                                         │
│ ]                                                           │
│                                                             │
│ 'commands' Collection:  [EMPTY - Deleted]                 │
└─────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ Parent Refreshes Dashboard                                  │
│                                                             │
│ GET /api/results/screenshot                                │
│ Flask queries MongoDB: db['results'].find_one({...})       │
│ Gets Base64 image data                                      │
│ Returns to browser                                          │
│ Browser converts Base64 → Image                             │
│ 🖼️ SCREENSHOT DISPLAYS IN DASHBOARD! ✅                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Level 4: Message Flow

```
TIME: 10:30:00 AM

Parent                MongoDB              Child
  │                    │                    │
  │ POST /api/cmd/ss   │                    │
  ├───────────────────►│                    │
  │                    │ Store command      │
  │ "Command sent" ◄───┤ {action:ss,       │
  │                    │  status:pending}   │
  │                    │                    │
  │                    │◄─── Poll every 5s──┤
  │                    │ "Any commands?"   │
  │                    │                    │
  │                    ├─ Find command ────►│
  │                    │ {action:ss}        │
  │                    │                    │
  │                    │                    ├─ Execute
  │                    │                    │ pyautogui.screenshot()
  │                    │                    │
  │                    │◄─ Upload result ───┤
  │                    │ {screenshot:b64}   │
  │                    ├─ Delete command ───┤
  │                    │                    │
  │ GET /api/results   │                    │
  ├───────────────────►│                    │
  │                    │ Query results      │
  │◄─ {screenshot:b64}─┤                    │
  │                    │                    │
  ├─ Decode Base64    │                    │
  │ Display image      │                    │
  │                    │                    │
  ✅ SUCCESS! (10-15s total)                 │
```

---

## Level 5: Device Registration

```
First Time Child Computer Connects:

1. Start client.py on child's computer

2. client.py connects to MongoDB
   from pymongo import MongoClient
   client = MongoClient('mongodb://192.168.0.104:27017/')
   
3. Get device info
   DEVICE_ID = socket.gethostname()  # "CHILD-PC"
   device_name = "Child's Laptop"
   pc_info = {OS, CPU, RAM, etc}
   
4. Register in MongoDB
   db['devices'].insert_one({
       device_id: "CHILD-PC",
       device_name: "Child's Laptop",
       status: "online",
       registered_at: DateTime.now(),
       last_seen: DateTime.now(),
       pc_info: {...}
   })
   
5. Polling starts
   while True:
       # Check for commands every 5 seconds
       time.sleep(5)
       
6. Update last_seen every 5 seconds
   db['devices'].update_one({
       "device_id": "CHILD-PC"
   }, {
       "$set": {"last_seen": DateTime.now()}
   })
   
7. If client.py stops running
   → last_seen doesn't update
   → Parent sees: "CHILD-PC: Offline" ⚠️
```

---

## Level 6: Sessions & Authentication

```
Login Process:

1. User opens http://192.168.0.104:5000/login
   ↓
2. Server sends LOGIN_HTML
   ┌─────────────────────┐
   │ 👶 Child Monitor   │
   │ Password: [_____]  │
   │ [Login Button]     │
   └─────────────────────┘
   
3. User enters password: "BlueSky#2024"
   Clicks Submit
   ↓
4. Browser sends: POST /login
   Form data: {password: "BlueSky#2024"}
   ↓
5. Flask checks:
   if password == ADMIN_PASSWORD:
       ✅ Match!
       session['user_id'] = 'admin'
       session['login_time'] = DateTime.now()
       
       Browser gets cookie:
       Set-Cookie: FLASK_SESSION_ID=abc123xyz
       
       Redirect to: /
   else:
       ❌ No match!
       Re-render login page with error:
       "❌ Wrong password! Try again."
   
6. Browser gets cookie in future requests
   Every request includes:
   Cookie: FLASK_SESSION_ID=abc123xyz
   
7. Flask verifies:
   if session.get('user_id') == 'admin':
       ✅ Allow request
   else:
       ❌ Redirect to /login
   
8. User clicks Logout:
   session.clear()
   Cookie deleted
   Redirect to /login
   ↓
9. Next request without cookie:
   ❌ Not authenticated
   🔒 Redirected to login page
```

---

## Level 7: Data Flow Summary

```
INCOMING DATA (Child to Parent):
─────────────────────────────────

Client.py                   MongoDB          Flask            Browser
(Child PC)                  (Database)       (Backend)        (Parent)
   │                           │               │                │
   ├─ Screenshot captured      │               │                │
   ├─ Encode to Base64         │               │                │
   ├─ Upload to MongoDB ───────►               │                │
   │  'results' collection      │               │                │
   │                           │── Query ────► │                │
   │                           │               ├─ Decode ──────►│
   │                           │               │ Display Image  │
   │                                          │                │


OUTGOING DATA (Parent to Child):
────────────────────────────────

Browser                      Flask            MongoDB          Client.py
(Parent)                     (Backend)        (Database)       (Child PC)
   │                           │               │                │
   ├─ Clicks button            │               │                │
   ├─ POST request ───────────► │               │                │
   │                           │── Store ────► │                │
   │                           │ 'commands'    │                │
   │                           │               ├─ Query every 5s─┤
   │                           │               │                │
   │                           │               │◄─ "Poll"        │
   │                           │               │                │
   │                           │               ├─ Send command──►│
   │                           │               │                │
   │                           │               │                ├─ Execute
```

---

## Level 8: Multiple Children Support

```
One Parent Monitoring Multiple Children:

MongoDB Collections:
    devices:
    [
        {device_id: "RONIT-LAPTOP", status: "online"},
        {device_id: "SARAH-DESKTOP", status: "online"},
        {device_id: "ALI-COMPUTER", status: "offline"}
    ]
    
    commands:
    [
        {device_id: "RONIT-LAPTOP", action: "screenshot", ...},
        {device_id: "SARAH-DESKTOP", action: "lock", ...}
    ]

Parent's Dashboard Shows:
    ┌─ Devices
    │  ├─ RONIT-LAPTOP (🟢 Online)
    │  │  ├─ [📷 Screenshot] [🔒 Lock] [🔄 Restart]
    │  │
    │  ├─ SARAH-DESKTOP (🟢 Online)
    │  │  ├─ [📷 Screenshot] [🔒 Lock] [🔄 Restart]
    │  │
    │  └─ ALI-COMPUTER (🔴 Offline)
    │     └─ (No commands available - offline)

When Parent sends command:
    1. Selects: "RONIT-LAPTOP"
    2. Clicks: [📷 Screenshot]
    3. Command stored: {device_id: "RONIT-LAPTOP", action: "screenshot"}
    4. SARAH-DESKTOP's client.py checks:
       "Any commands for SARAH-DESKTOP?" → No
       Ignores it ✓
    5. RONIT-LAPTOP's client.py checks:
       "Any commands for RONIT-LAPTOP?" → Yes!
       Executes ✓

Result:
    Only RONIT-LAPTOP executes the command
    SARAH-DESKTOP unaffected
    Each child monitored independently!
```

---

## Level 9: Network Security

```
INSIDE THE HOME (Secure):
─────────────────────────

    WiFi Network: 192.168.0.0/24
    ┌─────────────────────────────┐
    │ Parent    192.168.0.104:5000│
    │ Child     192.168.0.105     │
    │ MongoDB   192.168.0.104:27017
    └─────────────────────────────┘
    
    ✅ Firewall: Private network
    ✅ Encryption: Can add (optional)
    ✅ Access: Only home network devices


CONNECTING FROM OUTSIDE (Less Secure):
───────────────────────────────────────

    Parent at work: 203.45.67.89
    Child at home:  192.168.0.105
    
    How to connect:
    Option 1: VPN
        Parent → VPN Connection → Home Network → Child
        ✅ Secure tunnel
        
    Option 2: Cloud (MongoDB Atlas)
        Both → Internet → MongoDB Atlas Cloud → Both
        ⚠️ Need authentication
        ⚠️ Need HTTPS on backend
        
    Option 3: Deployed Backend
        Parent → Internet → Heroku/PythonAnywhere → Child
        ⚠️ Most complex setup
        ⚠️ Most flexible access


FUTURE: Add Encryption Layer
────────────────────────────

Option 1: SSL/TLS (HTTPS)
    from flask_sslify import SSLify
    ssl_context = SSL_CONTEXT
    app.run(ssl_context=ssl_context)
    
Option 2: VPN Tunnel
    OpenVPN, WireGuard, etc.
    
Option 3: Encrypted Messaging
    Encrypt data before MongoDB storage
    Decrypt after retrieval
```

---

**✅ Complete connection architecture explained!**

Each level shows deeper detail. Start with Level 1 for big picture, go deeper as needed.
