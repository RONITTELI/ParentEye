# 🔗 HOW TO GET MONGODB ATLAS CONNECTION STRING - Visual Guide

## Step-by-Step Screenshots Guide

### Step 1: Go to MongoDB Atlas Website

**Open:** https://www.mongodb.com/cloud/atlas

You'll see login page:
```
┌─────────────────────────────────────┐
│  MongoDB Atlas                      │
│                                     │
│  [Sign In Button]  [Sign Up]       │
│                                     │
│  Login with your email              │
└─────────────────────────────────────┘
```

**Login with:**
- Email: (your MongoDB Atlas email)
- Password: (your MongoDB password)

---

### Step 2: See Your Dashboard

After login, you'll see:

```
┌──────────────────────────────────────────────────┐
│  Ronit's Org                                     │
│                                                  │
│  ┌─ CLUSTERS ─────────────────────────────────┐ │
│  │                                             │ │
│  │  📊 Cyber-Lab  (M0 - Free)                 │ │
│  │  Status: Active                            │ │
│  │                                             │ │
│  │  [Connect Button] ← CLICK THIS!           │ │
│  │                                             │ │
│  └─────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────┘
```

**Click the "Connect" button** (green button next to Cyber-Lab)

---

### Step 3: Connection Options

You'll see a popup with options:

```
┌────────────────────────────────────┐
│  Choose a connection method:        │
│                                    │
│  ✓ Connect your application        │ ← CLICK THIS
│                                    │
│  • Connect with MongoDB Shell      │
│  • Connect with VS Code            │
│  • IP Whitelist                    │
│                                    │
└────────────────────────────────────┘
```

**Click "Connect your application"**

---

### Step 4: Select Language/Driver

You'll see another screen:

```
┌────────────────────────────────────┐
│  Add your connection string to      │
│  your application                  │
│                                    │
│  Language/Driver: [Dropdown ▼]    │
│                   Python 3.12      │ ← SELECT THIS
│                   (or similar)     │
│                                    │
│  Your connection string:            │
│  ┌──────────────────────────────┐  │
│  │ mongodb+srv://ronit:        │  │
│  │ ParentEyeadmintest@cyber-  │  │
│  │ lab.xxxxx.mongodb.net/?... │  │
│  │                              │  │
│  │ [COPY Button] ← CLICK THIS! │  │
│  │                              │  │
│  └──────────────────────────────┘  │
│                                    │
│  ⚠️ Replace <password>             │
│  ⚠️ Replace <username>             │
│                                    │
└────────────────────────────────────┘
```

**Click the "COPY" button** (or select all and copy)

---

## What You Get

The connection string will be:

```
mongodb+srv://ronit:ParentEyeadmintest@cyber-lab.xxxxx.mongodb.net/parenteye?retryWrites=true&w=majority
```

This is what you need!

---

## Where's the Missing Part? (xxxxx)

In your screenshot, you had:
- Organization: **Ronit's Org**
- Project: **Project 0**
- Cluster: **Cyber-Lab**
- Database: **ParentEye**

The `xxxxx` part (cluster ID) should be automatically filled in the connection string MongoDB shows you!

**It will look like:**
```
cyber-lab.abc123xyz.mongodb.net
           ^^^^^^^^^ This is the cluster ID (not xxxxx)
```

---

## Updated Connection String

Your connection string from MongoDB Atlas should already have the cluster ID!

It should look like:
```
mongodb+srv://ronit:ParentEyeadmintest@cyber-lab.123abc456xyz.mongodb.net/parenteye?retryWrites=true&w=majority
```

**Not:**
```
mongodb+srv://ronit:ParentEyeadmintest@cyber-lab.xxxxx.mongodb.net/parenteye?retryWrites=true&w=majority
```

---

## 🎯 QUICK SUMMARY

1. Go to: https://www.mongodb.com/cloud/atlas
2. Login with your credentials
3. Click your **Cyber-Lab** cluster
4. Click **"Connect"** button (green)
5. Click **"Connect your application"**
6. Select **Python** from dropdown
7. **COPY** the connection string shown
8. The string will have the cluster ID already (not xxxxx)

---

## ⚙️ Then Update Your .env File

**Open:** `c:\Users\ronit\Desktop\techshurujan_2026\.env`

**Replace this:**
```env
MONGODB_URI=mongodb+srv://ronit:ParentEyeadmintest@cyber-lab.xxxxx.mongodb.net/parenteye?retryWrites=true&w=majority
```

**With this (from MongoDB):**
```env
MONGODB_URI=mongodb+srv://ronit:ParentEyeadmintest@cyber-lab.123abc456xyz.mongodb.net/parenteye?retryWrites=true&w=majority
```

**Save the file!**

---

## ✅ Verification

Your `.env` should look like:

```env
# 🔐 MongoDB Atlas Connection
MONGODB_URI=mongodb+srv://ronit:ParentEyeadmintest@cyber-lab.123abc456xyz.mongodb.net/parenteye?retryWrites=true&w=majority

# 🔑 Admin Password
ADMIN_PASSWORD=YourSecurePassword123

# 🌐 Flask Settings
FLASK_ENV=production
SECRET_KEY=your-secret-key-here

# 📍 Backend URL
BACKEND_URL=http://192.168.0.104:5000
```

✅ **Then you're ready to run!**

---

## 🚀 Test It

```bash
# Install dependencies
pip install -r requirements.txt

# Run Flask
python backend.py

# Should see:
# * Running on http://127.0.0.1:5000
# * Debugger is active!

# Then open browser:
http://127.0.0.1:5000/login
```

---

## 🆘 Still Stuck?

**Tell me:**
1. You went to https://www.mongodb.com/cloud/atlas
2. You see the screen with "Cyber-Lab" cluster ✓
3. You clicked "Connect" button
4. What do you see next?

Send me a screenshot and I'll help! 📸
