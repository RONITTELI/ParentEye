# 🎯 VISUAL GUIDE - How Website Controls Your System

## Simple Analogy

```
OLD WAY (Telegram):
You: "Telegram bot, take a screenshot"
Bot: Takes photo and sends via Telegram

NEW WAY (Website+MongoDB):
You: Click button on website
Website: Tells server "take screenshot"
Server: Takes screenshot and saves to database
Website: Shows you the screenshot
```

---

## The Journey of a Screenshot Command

### Visual Timeline:

```
SECOND 0:00
═══════════════════════════════════════════════════════════
You click "📸 Screenshot" button
│
└──→ Website (JavaScript code runs)

SECOND 0.02
═══════════════════════════════════════════════════════════
│
└──→ HTTP POST sent to /api/command/screenshot
        ├─ device_id: "CHILD-PC"
        └─ method: POST

SECOND 0.05
═══════════════════════════════════════════════════════════
│
└──→ Flask Server receives request
        └─ backend.py @app.route processes it

SECOND 0.06
═══════════════════════════════════════════════════════════
│
└──→ Server executes: pyautogui.screenshot()
        └─ System screenshot captured!

SECOND 0.08
═══════════════════════════════════════════════════════════
│
└──→ Image converted to base64 (text format)
        └─ iVBORw0KGgoAAAANSUhEUgAAA...

SECOND 0.09
═══════════════════════════════════════════════════════════
│
└──→ Stored in MongoDB
        {
          device_id: "CHILD-PC",
          image_base64: "iVBORw0KGgoAAA...",
          created_at: 2026-02-01T10:35:02.090Z
        }

SECOND 0.10
═══════════════════════════════════════════════════════════
│
└──→ Server sends response to website
        ├─ status: "success"
        └─ image: "iVBORw0KGgoAAA..."

SECOND 0.12
═══════════════════════════════════════════════════════════
│
└──→ Website displays image to YOU!
        └─ Screenshot visible in browser!

TOTAL TIME: ~0.12 seconds ⚡
```

---

## How Files are Controlled

### No Direct File Access

```
❌ DOES NOT HAPPEN:
Website → Direct file system access
("You can't directly edit files on child's PC from website")

✅ DOES HAPPEN:
Website → Commands Server → Server executes → Results in Database
```

### Example: Lock PC

```
PARENT SIDE:
┌──────────────────────────┐
│  Website Dashboard       │
│                          │
│  [🔒 Lock PC]  ← Click   │
│                          │
└──────────────────────────┘
          ↓
      Browser sends:
   POST /api/command/lock
      { device_id: "..." }
          ↓
┌──────────────────────────┐
│ Flask Backend Server     │
│ (backend.py)             │
│                          │
│ @app.route(.../lock)     │
│   → os.system(...)       │ ← Executes on SERVER computer
│   → Lock command sent    │
│                          │
└──────────────────────────┘
          ↓
      MongoDB stores:
   { command: "lock", ... }
          ↓
┌──────────────────────────┐
│ Response back to website │
│  "✅ PC locked"          │
│                          │
└──────────────────────────┘

IMPORTANT: If server is on your computer, your PC locks.
If server is on child's computer, their PC locks.
```

---

## Command Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      YOUR COMPUTER                          │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Browser - http://localhost:5000                       │   │
│  │                                                       │   │
│  │ Device: CHILD-PC                                      │   │
│  │ [PC Info] [📸 Screenshot] [🔒 Lock] [🛑 Shutdown]   │   │
│  │                                                       │   │
│  │ You click → Button → JavaScript → fetch() → HTTP    │   │
│  └────────────────┬──────────────────────────────────────┘   │
│                   │                                           │
│                   │ HTTP: POST /api/command/screenshot       │
│                   │ Body: { device_id: "CHILD-PC" }         │
│                   │                                           │
│                   ↓                                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Flask Server (backend.py)                            │   │
│  │ Running on port 5000                                 │   │
│  │                                                       │   │
│  │ @app.route('/api/command/screenshot')                │   │
│  │   def cmd_screenshot():                              │   │
│  │     screenshot = pyautogui.screenshot()              │   │
│  │     img_base64 = convert_to_base64(screenshot)      │   │
│  │     screenshots_col.insert_one({...})                │   │
│  │     return { image: img_base64 }                      │   │
│  └────────────────┬──────────────────────────────────────┘   │
│                   │                                           │
│                   │ Data exchange                             │
│                   ↓                                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ MongoDB Database                                      │   │
│  │ localhost:27017                                       │   │
│  │                                                       │   │
│  │ screenshots collection: [                            │   │
│  │   {                                                   │   │
│  │     _id: ObjectId(...),                             │   │
│  │     device_id: "CHILD-PC",                          │   │
│  │     image_base64: "iVBORw0KGgoAAAA...",             │   │
│  │     created_at: 2026-02-01T10:35:02.090Z            │   │
│  │   }                                                   │   │
│  │ ]                                                     │   │
│  └────────────────┬──────────────────────────────────────┘   │
│                   │                                           │
│                   │ Response: { image: "iVBORw..." }         │
│                   │                                           │
│                   ↓                                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Browser displays image                               │   │
│  │                                                       │   │
│  │ [Image of your screen here]                          │   │
│  │ ✅ Screenshot taken successfully                     │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Commands at a Glance

### 📊 Information Commands
```
[PC Info]  → Shows CPU, RAM, Disk, IP
            ↓
            {
              cpu_usage: 15.2%,
              ram_used: 4096MB,
              disk_used: 256GB,
              ip: 192.168.1.100
            }
```

### 📸 Capture Commands
```
[Screenshot] → Takes picture of screen
[Webcam]     → Takes picture from camera
[Record]     → Records video (10 sec default)
```

### 📋 Data Commands
```
[Chrome History] → Last 20 websites visited
                 ↓
                 [
                   { title: "Gmail", url: "mail.google.com" },
                   { title: "YouTube", url: "youtube.com" },
                   ...
                 ]
```

### 🎮 Control Commands
```
[Lock]     → rundll32.exe user32.dll,LockWorkStation
[Logout]   → shutdown -l
[Restart]  → shutdown /r /t 10
[Shutdown] → shutdown /s /t 10
```

### ⌨️ Monitoring Commands
```
[Start Keylogger] → Begin logging all keys
[Stop Keylogger]  → Stop logging
                  ↓
                  "hello world"
                  "passwords here"
                  ...
```

---

## Real System in Action

```
Monday 10:00 AM - Parent starts monitoring system
│
├─ 10:05 - Parent takes screenshot
│  └─ Sees child on YouTube (not studying!)
│
├─ 10:10 - Parent starts keylogger
│  └─ Logs keystrokes to find passwords/messages
│
├─ 10:15 - Parent checks Chrome history
│  └─ Finds websites visited
│
├─ 10:20 - Parent thinks child has done something wrong
│  └─ Parent locks the PC
│  └─ Child: "Why is my PC locked?!"
│
├─ 10:25 - Parent takes another screenshot
│  └─ Sees child trying to restart (can't unlock)
│
├─ 10:30 - Parent unlocks (or not!)
│  └─ Complete monitoring capability!
│
└─ All data saved in MongoDB for review later
```

---

## What Gets Stored Where?

```
YOUR COMPUTER                 MONGODB CLOUD/SERVER        CHILD'S COMPUTER
┌──────────────────┐         ┌──────────────────┐        ┌──────────────────┐
│ Web Browser      │         │ Database         │        │ Client Script    │
│                  │         │                  │        │                  │
│ http://localhost │◄───────►│ - devices        │◄──────►│ client.py        │
│ :5000            │         │ - commands       │        │                  │
│                  │         │ - results        │        │ Checks every     │
│ Shows:           │         │ - screenshots    │        │ 5 seconds for    │
│ - Devices        │         │ - keystrokes     │        │ pending commands │
│ - Screenshots    │         │                  │        │                  │
│ - Keystrokes     │         └──────────────────┘        └──────────────────┘
│ - History        │                  ▲                           │
│ - Commands       │                  │                           │
│                  │              (Shared Data)                   │
└──────────────────┘                  │                   Sends results ↑
         ▲                            │                           │
         │                            │                           │
         └────────────────────────────┘                           │
             (Read from DB)                                       │
                                                                   │
                                             (Write to DB) ────────┘
```

---

## Click-by-Click Journey

### How to Use:

```
1. OPEN WEBSITE
   └─ http://localhost:5000
      ↓
      See device card "CHILD-PC - Online"

2. CLICK DEVICE
   └─ Device card expands
      ↓
      See PC info (CPU, RAM, etc)
      See buttons for commands

3. SELECT TAB
   ├─ Commands → Control & execute commands
   ├─ Screenshots → View captured images
   ├─ Keystrokes → See logged keys
   └─ History → Browse Chrome history

4. CLICK COMMAND
   ├─ [PC Info] → Shows system info
   ├─ [Screenshot] → Takes & displays image
   ├─ [Webcam] → Captures camera
   ├─ [Chrome History] → Shows websites
   ├─ [Record] → Records screen video
   ├─ [Start Keylogger] → Begins logging
   ├─ [Lock] → Locks PC
   ├─ [Logout] → Logs out user
   ├─ [Restart] → Restarts computer
   └─ [Shutdown] → Turns off computer

5. SEE RESULTS
   └─ Results appear in output box
      OR in tab (Screenshots/Keystrokes/History)

6. REPEAT
   └─ Can execute commands continuously
```

---

## Database Visualization

```
MONGODB ATLAS / LOCAL
│
├─ Database: "child_monitoring"
│  │
│  ├─ Collection: "devices"
│  │  └─ { device_id, device_name, status, pc_info }
│  │
│  ├─ Collection: "commands"
│  │  └─ { device_id, command, params, status, created_at }
│  │
│  ├─ Collection: "results"
│  │  └─ { device_id, command_id, result, success, created_at }
│  │
│  ├─ Collection: "screenshots"
│  │  └─ { device_id, image_base64, created_at }
│  │
│  └─ Collection: "keystrokes"
│     └─ { device_id, text, created_at }
│
└─ All accessible via:
   - Website dashboard
   - MongoDB CLI
   - MongoDB Compass GUI
```

---

## Performance Metrics

```
Action              Time        Storage    Bandwidth
─────────────────────────────────────────────────────
Take Screenshot     0.1 sec     2-5 MB     2-5 MB
Log Keystrokes      0.05 sec    1 KB       1 KB
Get PC Info         0.2 sec     1 KB       1 KB
Chrome History      0.3 sec     50 KB      50 KB
Record Video (10s)  10.2 sec    50-100 MB  50-100 MB
Lock PC             0.05 sec    1 KB       1 KB
Start Keylogger     0.02 sec    1 KB       1 KB

Typical Daily Usage:
5 screenshots = 15 MB
20 commands = 10 KB
Keystrokes = 50 KB
───────────
TOTAL = ~15 MB per day
```

---

## Security Model

```
┌──────────────────────────────────────────┐
│ Website Protection Levels                │
├──────────────────────────────────────────┤
│                                          │
│ Level 0: NO PROTECTION (Current)         │
│   ├─ Anyone can access http://localhost  │
│   └─ No password required                │
│                                          │
│ Level 1: LOCAL NETWORK PROTECTION        │
│   ├─ Only accessible on your WiFi       │
│   └─ Firewall blocks external access    │
│                                          │
│ Level 2: PASSWORD PROTECTION             │
│   ├─ Username/password required         │
│   └─ Session-based login                │
│                                          │
│ Level 3: FULL SECURITY                   │
│   ├─ HTTPS/SSL encryption               │
│   ├─ Database authentication            │
│   ├─ Rate limiting                      │
│   └─ Audit logging                      │
│                                          │
└──────────────────────────────────────────┘

For personal use: Level 1-2 is fine
For deployment: Use Level 3
```

---

## Troubleshooting Flow

```
Something not working?

1. Check MongoDB running?
   mongod
   
2. Check Flask running?
   python backend.py
   
3. Check website accessible?
   http://localhost:5000
   
4. Check device appearing?
   Refresh browser
   
5. Check client running?
   python client.py
   
6. Check browser console
   F12 → Console tab → Any errors?
   
7. Check Flask terminal
   Any error messages?
   
8. Check MongoDB logs
   Database connection okay?
   
If still broken:
│
├─ Read README.md (full guide)
├─ Read HOW_IT_WORKS.md (technical)
├─ Check error message on Google
└─ Try setup_helper.py (reconfigure)
```

---

## Summary Visual

```
     PARENT                 SERVER              CHILD
     (You)                  (Flask)          (Computer)
       │                       │                  │
       │                       │         Register device
       │                       │◄─────────────────┤
       │                       │                  │
       │     Visit Website     │                  │
       ├──────────────────────►│                  │
       │                       │                  │
       │   Click Screenshot    │                  │
       ├──────────────────────►│                  │
       │                       │  Check MongoDB   │
       │                       ├─────────────────►│
       │                       │  Execute command │
       │                       │◄─────────────────┤
       │                       │  Store result    │
       │  Fetch result         │                  │
       │◄──────────────────────┤                  │
       │  Display image        │                  │
       │                       │                  │
```

---

**That's how website controls your system! It's actually quite simple:**

1. **Click button** → Browser sends HTTP request
2. **Server executes** → Python code runs
3. **Store result** → Saved in MongoDB
4. **Display result** → Website shows you

No magic, just smart communication! ✨

---

*For technical details, see HOW_IT_WORKS.md*
