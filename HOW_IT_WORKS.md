# HOW THE WEBSITE CONTROLS FILES/SYSTEM

## Simple Overview

Instead of sending Telegram messages like `/start`, `/screenshot`, etc., the website sends HTTP requests to a Flask server that then stores commands in MongoDB. The client script constantly checks MongoDB for new commands and executes them.

---

## Command Flow - Step by Step

### Example 1: Taking a Screenshot

```
┌─────────────────────────────────────────────────────────────────┐
│ YOU (Parent on Website)                                          │
│ ┌──────────────────────────────────────────────────────────────┐│
│ │ Dashboard showing device "CHILD-PC"                           ││
│ │ [PC Info] [📸 Screenshot] [📷 Webcam] [🎥 Record] ...        ││
│ │                   ↓                                           ││
│ │            👆 Click Screenshot Button                        ││
│ └──────────────────────────────────────────────────────────────┘│
└────────────────────┬────────────────────────────────────────────┘
                     │
                     │ Browser sends HTTP POST to /api/command/screenshot
                     │ with { device_id: "CHILD-PC" }
                     ↓
┌────────────────────────────────────────────────────────────────┐
│ FLASK SERVER (backend.py)                                       │
│ ┌──────────────────────────────────────────────────────────────┐│
│ │ @app.route('/api/command/screenshot', methods=['POST'])      ││
│ │ def cmd_screenshot():                                        ││
│ │     # Execute screenshot on THIS SERVER                      ││
│ │     screenshot = pyautogui.screenshot()                      ││
│ │     # Convert to base64 and store in MongoDB                 ││
│ │     screenshots_col.insert_one({...})                        ││
│ │     return image as base64                                   ││
│ └──────────────────────────────────────────────────────────────┘│
└────────────────────┬────────────────────────────────────────────┘
                     │
          (In this example, server and client are on same PC)
          
          If they were on different PCs, it would work like:
          
          │ Browser sends request → Flask → MongoDB stores command
          │
          │ Client periodically checks MongoDB for pending commands
          │ Client finds "screenshot" command and executes it
          │ Client stores result back in MongoDB
          │ Website fetches result and shows to parent
```

---

## File Control Example: Lock PC

```
SCENARIO: Parent wants to lock child's PC immediately

1️⃣  PARENT CLICKS "LOCK PC" BUTTON
    ↓
    JavaScript: fetch('/api/command/lock', { device_id: 'CHILD-PC' })

2️⃣  REQUEST SENT TO FLASK BACKEND
    ↓
    POST /api/command/lock
    Body: { "device_id": "CHILD-PC" }

3️⃣  FLASK EXECUTES COMMAND
    ↓
    In backend.py:
    @app.route('/api/command/lock', methods=['POST'])
    def cmd_lock():
        os.system("rundll32.exe user32.dll,LockWorkStation")
        return {"status": "success"}

4️⃣  MONGODB STORES RESULT
    ↓
    commands collection: {
        device_id: "CHILD-PC",
        command: "lock",
        status: "completed",
        created_at: 2026-02-01T10:35:00Z
    }

5️⃣  WEBSITE SHOWS SUCCESS
    ↓
    Output: "✅ PC locked"

⏱️  TOTAL TIME: ~1 second
```

---

## Important: Client vs Server Location

### Option 1: SAME COMPUTER (Testing)
```
┌──────────────────────────────┐
│ YOUR COMPUTER                │
│                              │
│ ┌────────────────┐           │
│ │ Flask Server   │           │
│ │ (Port 5000)    │           │
│ └────────────────┘           │
│           ↑                  │
│           │ (local)          │
│ ┌────────────────┐           │
│ │ Client Script  │           │
│ │ (client.py)    │           │
│ └────────────────┘           │
│           ↑                  │
│           │                  │
│ ┌────────────────┐           │
│ │ MongoDB        │           │
│ │ (local)        │           │
│ └────────────────┘           │
│           ↑                  │
│ ┌────────────────┐           │
│ │ Web Browser    │           │
│ │ localhost:5000 │           │
│ └────────────────┘           │
└──────────────────────────────┘

All components on same PC = Easy for testing
```

### Option 2: DIFFERENT COMPUTERS (Production)
```
YOUR COMPUTER (Parent)          CHILD'S COMPUTER
┌─────────────────────┐        ┌──────────────────┐
│ Web Browser         │        │                  │
│ localhost:5000  ◄───┼────HTTP request──────────┤
│                 │   │                           │
│                 │   │  Commands: {"lock", ...} │
│                 ▼   │                           │
│ Flask Server        │ ◄──────Fetch pending────┤  Client Script
│ (backend.py)        │                          │ (client.py)
│ Port 5000           │ ─Stores results──────────►
└─────────────────────┘                          │
        │                                         │
        └──────────MongoDB Database──────────────┘
              (Shared by both)
```

---

## What Happens Behind The Scenes

### When You Click "Screenshot":

**Frontend (index.html):**
```javascript
// JavaScript code runs in your browser
button.onclick = function() {
    fetch('/api/command/screenshot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ device_id: selectedDevice })
    })
    .then(res => res.json())
    .then(data => {
        // Display image in browser
        document.querySelector('img').src = 'data:image/png;base64,' + data.image;
    })
}
```

**Backend (backend.py):**
```python
@app.route('/api/command/screenshot', methods=['POST'])
def cmd_screenshot():
    data = request.json
    device_id = data.get('device_id')
    
    # Take screenshot
    screenshot = pyautogui.screenshot()
    
    # Convert to base64
    img_byte_arr = BytesIO()
    screenshot.save(img_byte_arr, format='PNG')
    img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
    
    # Store in MongoDB
    screenshot_doc = {
        "device_id": device_id,
        "image_base64": img_base64,
        "created_at": datetime.now()
    }
    screenshots_col.insert_one(screenshot_doc)
    
    # Return to website
    return jsonify({"status": "success", "image": img_base64})
```

**Client (client.py):**
```python
# In this example, client doesn't need to do anything
# The server itself takes the screenshot
# But if client was on different PC, it would:
# - Poll MongoDB for command
# - See "screenshot" command
# - Execute screenshot
# - Store result back
```

---

## MongoDB Storage Structure

### How Commands Flow Through Database:

```
1️⃣  PENDING COMMAND
┌───────────────────────────────────────┐
│ commands collection                   │
├───────────────────────────────────────┤
│ {                                     │
│   _id: ObjectId(...),                │
│   device_id: "CHILD-PC",             │
│   command: "screenshot",              │
│   status: "pending",                  │
│   executed: false,                    │
│   created_at: 2026-02-01T10:35:00Z   │
│ }                                     │
└───────────────────────────────────────┘

2️⃣  CLIENT FINDS & EXECUTES
    ↓
3️⃣  RESULT STORED
┌───────────────────────────────────────┐
│ results collection                    │
├───────────────────────────────────────┤
│ {                                     │
│   _id: ObjectId(...),                │
│   device_id: "CHILD-PC",             │
│   command_id: ObjectId(...),         │
│   result: "Screenshot captured",      │
│   success: true,                      │
│   created_at: 2026-02-01T10:35:05Z   │
│ }                                     │
└───────────────────────────────────────┘

    AND/OR

┌───────────────────────────────────────┐
│ screenshots collection                │
├───────────────────────────────────────┤
│ {                                     │
│   _id: ObjectId(...),                │
│   device_id: "CHILD-PC",             │
│   command_id: ObjectId(...),         │
│   image_base64: "iVBORw0KGgo...",   │
│   created_at: 2026-02-01T10:35:05Z   │
│ }                                     │
└───────────────────────────────────────┘

4️⃣  WEBSITE FETCHES & DISPLAYS
    ↓
5️⃣  PARENT SEES IMAGE
```

---

## Comparison: Telegram vs Website+MongoDB

### OLD SYSTEM (Telegram):
```
Parent types /screenshot
        ↓
Telegram Bot receives message
        ↓
Bot executes: pyautogui.screenshot()
        ↓
Bot sends image via Telegram API
        ↓
Image sent over Telegram servers
        ↓
Parent receives in Telegram chat

❌ Depends on Telegram API
❌ Telegram logs everything
❌ Limited features
❌ Only works on same device (bot and control)
```

### NEW SYSTEM (Website+MongoDB):
```
Parent clicks button on website
        ↓
Flask backend receives HTTP request
        ↓
Backend executes: pyautogui.screenshot()
        ↓
Image stored in MongoDB
        ↓
Website fetches from MongoDB
        ↓
Parent sees in browser

✅ No external API needed
✅ Full data control
✅ Unlimited features
✅ Works on any device (client and control can be different)
✅ Better UI/UX
✅ Real-time updates
✅ Complete history stored
```

---

## Adding Custom Commands

To add a new command like "Get Window Titles":

### Step 1: Add to backend.py
```python
import pygetwindow as gw

@app.route('/api/command/getwindows', methods=['POST'])
def cmd_getwindows():
    data = request.json
    device_id = data.get('device_id')
    
    windows = []
    for window in gw.getAllWindows():
        windows.append({
            'title': window.title,
            'isActive': window.isActive
        })
    
    result_doc = {
        "device_id": device_id,
        "result": windows,
        "created_at": datetime.now()
    }
    results_col.insert_one(result_doc)
    
    return jsonify({"status": "success", "windows": windows})
```

### Step 2: Add button to index.html
```html
<button class="btn-primary" onclick="executeCommand('getwindows')">
    🪟 Get Windows
</button>
```

### Step 3: Add to client.py (if needed)
```python
elif command_type == "getwindows":
    # Client side execution (if different from server)
    import pygetwindow as gw
    windows = [w.title for w in gw.getAllWindows()]
```

---

## Real-World Timeline Example

```
10:35:00 - Parent opens website and sees device "CHILD-PC"
10:35:02 - Parent clicks "Take Screenshot"
10:35:02.500 - Flask receives request
10:35:02.600 - Screenshot executed
10:35:02.800 - Image stored in MongoDB
10:35:02.900 - Response sent to website
10:35:03 - Parent sees screenshot in browser
         - Complete within 1 second!

Meanwhile:
10:35:04 - Client checks MongoDB for pending commands
10:35:04.500 - No pending commands (backend did it)
           or
           - Found command from backend
           - Executes command
           - Stores result in MongoDB

10:35:10 - Client checks MongoDB again
10:35:30 - Client checks MongoDB again
... (repeats every 5 seconds)
```

---

## Security & Performance

### MongoDB Security:
```python
# In production, use authentication:
MONGO_URI = "mongodb+srv://user:password@cluster.mongodb.net/?retryWrites=true"

# Add indexes for better performance:
commands_col.create_index("device_id")
results_col.create_index("device_id")
screenshots_col.create_index("created_at", expireAfterSeconds=604800)  # Delete after 7 days
```

### Encryption (Optional):
```python
from cryptography.fernet import Fernet

# Encrypt sensitive data before storing
cipher = Fernet(encryption_key)
encrypted_data = cipher.encrypt(data.encode())

# Store encrypted_data in MongoDB
```

---

## Troubleshooting Control Issues

### Command not executing:
1. **Check if backend is running:**
   ```bash
   python backend.py
   ```

2. **Check MongoDB is running:**
   ```bash
   mongod
   ```

3. **Check network connectivity:**
   ```bash
   ping your-server-ip
   ```

4. **Check logs:**
   Look at Flask console and client console for errors

### Command executes but result not showing:
1. Check if MongoDB connection string is correct
2. Check database permissions
3. Try refreshing website

### Slow response:
1. MongoDB performance - add indexes
2. Network latency - move server closer
3. Check browser console for errors (F12)

---

## Summary

The website doesn't control files directly. Instead:

1. **Website** → Sends HTTP request to Flask
2. **Flask** → Executes Python code on the server
3. **MongoDB** → Stores all data and commands
4. **Client** → (Optional) Fetches commands and executes
5. **Website** → Shows results to parent

It's like:
- **Telegram**: Send message → API processes → Result back
- **Website**: Click button → Server processes → Result in database → Display

Much more powerful and flexible! 🚀

---

*For more details, see README.md*
