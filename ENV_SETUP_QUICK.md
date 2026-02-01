# 🎯 SETUP YOUR .env FILE - Step by Step

## What You Need to Do (3 Steps Only!)

### Step 1: Get MongoDB Connection String

**In MongoDB Atlas:**

```
Atlas Dashboard
    ↓
Click "Cyber-Lab" cluster
    ↓
Click Green "Connect" Button
    ↓
Click "Connect your application"
    ↓
Copy this (it has your password):
mongodb+srv://ronit:ParentEyeadmintest@cyber-lab.XXXXX.mongodb.net/parenteye?retryWrites=true&w=majority
                                                        ↑
                                        Your cluster ID (XXXXX)
```

---

### Step 2: Open `.env` File

**Location:** `c:\Users\ronit\Desktop\techshurujan_2026\.env`

**Current content:**
```env
MONGODB_URI=mongodb+srv://ronit:ParentEyeadmintest@cyber-lab.xxxxx.mongodb.net/parenteye?retryWrites=true&w=majority
ADMIN_PASSWORD=YourSecurePassword123
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
BACKEND_URL=http://192.168.0.104:5000
```

---

### Step 3: Replace the Values

**Find `xxxxx` in MongoDB URI:**

From your connection string, get the cluster ID (usually looks like: `cyber-lab.123abc45.mongodb.net`)

Replace:
```env
# ❌ OLD:
MONGODB_URI=mongodb+srv://ronit:ParentEyeadmintest@cyber-lab.xxxxx.mongodb.net/parenteye?retryWrites=true&w=majority

# ✅ NEW (example):
MONGODB_URI=mongodb+srv://ronit:ParentEyeadmintest@cyber-lab.123abc45.mongodb.net/parenteye?retryWrites=true&w=majority
```

**Also change the password if needed:**
```env
# ✅ Change this to your secure admin password
ADMIN_PASSWORD=MySecurePassword@2024
```

---

## Complete Example

### Your `.env` File Should Look Like:

```env
# MongoDB Atlas - REPLACE xxxxx WITH YOUR CLUSTER ID
MONGODB_URI=mongodb+srv://ronit:ParentEyeadmintest@cyber-lab.123abc45.mongodb.net/parenteye?retryWrites=true&w=majority

# Admin password - CHANGE THIS!
ADMIN_PASSWORD=BlueSky#Monitor2024

# Flask settings
FLASK_ENV=production
SECRET_KEY=auto-generated-by-app

# Backend URL
BACKEND_URL=http://192.168.0.104:5000
```

---

## ✅ Verification Checklist

```
Before running Flask, verify:

□ .env file exists in project folder
□ MONGODB_URI has your cluster ID (not xxxxx)
□ MONGODB_URI has your password (ParentEyeadmintest)
□ ADMIN_PASSWORD is set to something secure
□ No spaces at beginning or end of lines
□ No quotes around values
```

---

## 🚀 After Setup, Run Flask

```bash
# 1. Make sure python-dotenv is installed
pip install python-dotenv

# 2. Start Flask (it auto-loads from .env)
python backend.py

# 3. You should see:
# * Running on http://127.0.0.1:5000

# 4. Open browser:
http://127.0.0.1:5000/login

# 5. Login with your ADMIN_PASSWORD from .env
```

---

## 🔐 Security Notes

```
⚠️ IMPORTANT:

✅ .env file is in .gitignore (won't be uploaded)
✅ Never share .env with anyone
✅ Never put .env password in messages
✅ Change ADMIN_PASSWORD to something strong
✅ Keep MongoDB password safe

Your .env contains:
- MongoDB connection string (with password)
- Admin password for dashboard
- Flask secret key
```

---

## File Structure After Setup

```
techshurujan_2026/
├─ .env                    ← Your secrets (DON'T SHARE!)
├─ .env.example            ← Template for others
├─ .gitignore              ← Protects .env from GitHub
├─ backend.py              ← Updated to load from .env
├─ client.py
├─ requirements.txt        ← Updated with python-dotenv
├─ templates/
│  └─ index.html
└─ [other files...]
```

---

## That's It! ✅

Once you:
1. ✅ Add your MongoDB connection string to `.env`
2. ✅ Change ADMIN_PASSWORD in `.env`
3. ✅ Install python-dotenv (`pip install python-dotenv`)
4. ✅ Run Flask (`python backend.py`)

Your system will be secure and ready to use! 🚀

---

## Questions?

**"Where's the cluster ID?"**
→ In your MongoDB connection string, it's the part between `@` and `.mongodb.net`
→ Example: `cyber-lab.123abc45` ← 123abc45 is the cluster ID

**"What if I forget the password?"**
→ Edit `.env` again and change ADMIN_PASSWORD
→ Restart Flask
→ Use new password to login

**"Is .env file safe?"**
→ Yes! It's in .gitignore so it won't be uploaded to GitHub
→ Keep it private and don't share

**"What to put in ADMIN_PASSWORD?"**
→ Something strong: `BlueSky#Monitor2024!Secure`
→ Mix of letters, numbers, symbols
→ At least 8 characters
