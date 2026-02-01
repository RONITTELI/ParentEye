# 🎬 MONGODB ATLAS - EXACT STEPS TO GET CONNECTION STRING

## YOUR MONGODB ATLAS SETUP

From your screenshot, I can see:
```
Organization: Ronit's Org - 2026-01-...
Project: Project 0
Cluster: Cyber-Lab
Database: ParentEye
```

---

## 🎯 EXACT STEPS (Copy-Paste Friendly)

### STEP 1️⃣: Open MongoDB Atlas

```
Open browser and go to:
https://www.mongodb.com/cloud/atlas

You should see your organization already or login screen.
```

---

### STEP 2️⃣: Find Your Cluster

Look for this in the left sidebar or main screen:

```
┌─ Clusters (1)
│
└─ 📊 Cyber-Lab
   Status: Active ✓
   
   [Connect Button]  ← HERE!
   [Other buttons...]
```

**Or in main area, you'll see the card:**

```
╔═══════════════════════════════╗
║  Cyber-Lab                    ║
║  M0 - Shared Tier (Free)      ║
║  Status: Active               ║
║                               ║
║  [Connect]  [...]  [...]      ║ ← Click Connect
║                               ║
╚═══════════════════════════════╝
```

---

### STEP 3️⃣: Click Connect Button

You'll see popup with 4 options:

```
┌────────────────────────────────────┐
│  Choose how to connect to your     │
│  Cyber-Lab cluster                 │
│                                    │
│  1. Connect with MongoDB Shell ☐  │
│  2. Connect with VS Code       ☐  │
│  3. Connect your application   ☑  │ ← CLICK THIS ONE!
│  4. IP Whitelist               ☐  │
└────────────────────────────────────┘
```

**Click on: "Connect your application"**

---

### STEP 4️⃣: Select Python Driver

Next screen shows:

```
┌────────────────────────────────────┐
│  Add your connection string to     │
│  your application                  │
│                                    │
│  Drivers:                          │
│  [Dropdown showing:]               │
│                                    │
│  • Node.js                         │
│  • Python 3.12                 ✓  │ ← SELECT THIS
│  • Java                           │
│  • Go                             │
│  • C#/.NET                        │
│  • C++ Drivers                    │
│  • Ruby                           │
│  • Scala                          │
│                                    │
│  ⬇️ (scroll to see more)           │
└────────────────────────────────────┘
```

**Make sure "Python" is selected** (or any version)

---

### STEP 5️⃣: Copy Connection String

After selecting Python, you'll see:

```
┌────────────────────────────────────┐
│  Connection string for Python:    │
│                                    │
│  mongodb+srv://ronit:             │
│  ParentEyeadmintest@cyber-lab.    │
│  XXXXX.mongodb.net/?              │
│  retryWrites=true&w=majority       │
│                                    │
│  [COPY BUTTON]  ← CLICK THIS!     │
│                                    │
│  ⚠️  Replace <username>            │
│  ⚠️  Replace <password>            │
│                                    │
└────────────────────────────────────┘
```

**Click the COPY button** (or manually select all text and Ctrl+C)

---

### STEP 6️⃣: What You Copied

The string you copied should look like:

```
mongodb+srv://ronit:ParentEyeadmintest@cyber-lab.abc123def456ghi789.mongodb.net/parenteye?retryWrites=true&w=majority
```

**Notice:**
- ✅ Username: `ronit`
- ✅ Password: `ParentEyeadmintest`
- ✅ Cluster: `cyber-lab.abc123def456ghi789` ← This part has the ID now!
- ✅ Database: `parenteye`

---

## 📝 UPDATE YOUR .env FILE

Now you have the connection string!

**Open file:**
```
c:\Users\ronit\Desktop\techshurujan_2026\.env
```

**Find this line:**
```env
MONGODB_URI=mongodb+srv://ronit:ParentEyeadmintest@cyber-lab.xxxxx.mongodb.net/parenteye?retryWrites=true&w=majority
```

**Replace with what you copied:**
```env
MONGODB_URI=mongodb+srv://ronit:ParentEyeadmintest@cyber-lab.abc123def456ghi789.mongodb.net/parenteye?retryWrites=true&w=majority
```

**The only change is replacing `xxxxx` with the real cluster ID!**

---

## ✅ COMPLETE .env FILE

Your `.env` should now look like:

```env
# 🔐 MongoDB Atlas Connection
MONGODB_URI=mongodb+srv://ronit:ParentEyeadmintest@cyber-lab.abc123def456ghi789.mongodb.net/parenteye?retryWrites=true&w=majority

# 🔑 Admin Password (CHANGE THIS!)
ADMIN_PASSWORD=YourSecurePassword123

# 🌐 Flask Settings
FLASK_ENV=production
SECRET_KEY=your-secret-key-here

# 📍 Backend URL for remote access
BACKEND_URL=http://192.168.0.104:5000
```

**Save it!** (Ctrl+S)

---

## 🚀 NOW YOU CAN RUN IT

```bash
# Terminal 1: Install packages
pip install -r requirements.txt

# Terminal 2: Start Flask
python backend.py

# Should see:
# * Running on http://127.0.0.1:5000
```

---

## 🎬 VISUAL SUMMARY

```
MongoDB Atlas
    ↓
Login
    ↓
Find "Cyber-Lab" cluster
    ↓
Click "Connect" button
    ↓
Click "Connect your application"
    ↓
Select "Python"
    ↓
Click "COPY" button
    ↓
Paste in .env file
    ↓
Replace xxxxx with cluster ID
    ↓
Save .env
    ↓
Run: python backend.py
    ↓
✅ DONE! Works with MongoDB Atlas!
```

---

## ❓ COMMON ISSUES

### "I can't find the Connect button"

**Look for:**
1. Top menu: Click "Deployments"
2. In list, find "Cyber-Lab"
3. Right side should have buttons including "Connect"

**OR:**

1. Left sidebar: Click "Clusters"
2. You'll see Cyber-Lab card
3. Click "Connect" on that card

---

### "Where's the cluster ID?"

**It's in the connection string MongoDB gives you!**

```
mongodb+srv://ronit:ParentEyeadmintest@cyber-lab.XXXXX.mongodb.net/
                                                ^^^^^ This is it!
```

MongoDB fills it in automatically. Don't worry about it!

---

### "I see 'xxxxx' instead of the cluster ID"

**Don't worry!** The actual string from MongoDB will have the real ID.

Just copy-paste the whole string MongoDB gives you into `.env`

---

### "Connection failed when I run Flask"

Check:
1. ✓ .env has correct MongoDB URI
2. ✓ .env has your correct password
3. ✓ MongoDB Atlas whitelist includes 0.0.0.0/0
4. ✓ python-dotenv installed: `pip install python-dotenv`

---

## 📞 STUCK?

1. Tell me which step you're stuck on
2. Send me a screenshot
3. I'll help you immediately!

**Don't worry, it's easy once you do it!** 🚀
