# ⚙️ ENVIRONMENT CONFIGURATION SETUP

## What Was Created

```
✅ .env              - Your secret configuration (DON'T SHARE!)
✅ .env.example      - Template for others to follow
✅ .gitignore        - Prevents .env from being uploaded to GitHub
✅ requirements.txt  - Updated with python-dotenv
✅ backend.py        - Updated to load from .env
```

---

## 📝 Step 1: Get Your MongoDB Connection String

Go to **MongoDB Atlas**:

1. Click your **Cyber-Lab** cluster
2. Click **"Connect"** button
3. Click **"Connect your application"**
4. Copy the connection string (looks like):
```
mongodb+srv://ronit:ParentEyeadmintest@cyber-lab.xxxxx.mongodb.net/parenteye?retryWrites=true&w=majority
```

---

## ✏️ Step 2: Edit `.env` File

Open `.env` in your text editor and replace:

### Current:
```env
MONGODB_URI=mongodb+srv://ronit:ParentEyeadmintest@cyber-lab.xxxxx.mongodb.net/parenteye?retryWrites=true&w=majority
ADMIN_PASSWORD=YourSecurePassword123
```

### With Your Data:
```env
MONGODB_URI=mongodb+srv://ronit:ParentEyeadmintest@cyber-lab.XXXXX.mongodb.net/parenteye?retryWrites=true&w=majority
ADMIN_PASSWORD=MySecurePassword123
```

**Just replace:**
- `XXXXX` with your actual cluster ID (from connection string)
- `YourSecurePassword123` with your admin password

---

## 🔧 Step 3: Install python-dotenv

```bash
pip install python-dotenv
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

---

## ▶️ Step 4: Run Your Application

```bash
# Terminal 1: Start MongoDB (local only, skip if using Atlas)
mongod

# Terminal 2: Start Flask
python backend.py

# Output should show:
# * Running on http://127.0.0.1:5000
```

Flask will automatically load from `.env` file!

---

## 🔐 Step 5: Update Client (Optional)

If you want `client.py` to also use `.env`:

**In `client.py`, around line 10:**

```python
# Current:
BACKEND_URL = "http://192.168.0.104:5000"
MONGO_URI = "mongodb://localhost:27017/"

# Change to:
import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv('BACKEND_URL', 'http://192.168.0.104:5000')
MONGO_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
```

---

## 📋 What Each Environment Variable Does

```env
# MongoDB Atlas connection string
MONGODB_URI=mongodb+srv://ronit:ParentEyeadmintest@cyber-lab.xxxxx.mongodb.net/parenteye?retryWrites=true&w=majority
└─ Your database connection (from MongoDB Atlas)
└─ Format: mongodb+srv://username:password@cluster/database

# Admin password for parent login
ADMIN_PASSWORD=YourSecurePassword123
└─ Parent uses this to login
└─ Change to something secure!

# Flask environment
FLASK_ENV=production
└─ Set to 'production' for live use
└─ Set to 'development' for testing

# Flask secret key (auto-generated)
SECRET_KEY=your-secret-key-here
└─ Used for session management
└─ Auto-generated if not provided

# Backend URL for remote access
BACKEND_URL=http://192.168.0.104:5000
└─ Used by child's client.py
└─ Change to your server URL if using cloud
```

---

## ✅ Verification

To verify your `.env` is loaded correctly:

**Create a test file `test_env.py`:**

```python
import os
from dotenv import load_dotenv

load_dotenv()

print("✅ Environment Variables:")
print(f"ADMIN_PASSWORD: {os.getenv('ADMIN_PASSWORD')}")
print(f"MONGODB_URI: {os.getenv('MONGODB_URI')}")
print(f"FLASK_ENV: {os.getenv('FLASK_ENV')}")
print(f"BACKEND_URL: {os.getenv('BACKEND_URL')}")
```

**Run it:**
```bash
python test_env.py
```

**Should output:**
```
✅ Environment Variables:
ADMIN_PASSWORD: YourSecurePassword123
MONGODB_URI: mongodb+srv://ronit:ParentEyeadmintest@cyber-lab.xxxxx.mongodb.net/parenteye?retryWrites=true&w=majority
FLASK_ENV: production
BACKEND_URL: http://192.168.0.104:5000
```

---

## 🔒 Security Best Practices

```
✅ DO:
├─ Keep .env file private
├─ Add .env to .gitignore (already done!)
├─ Use strong passwords in .env
├─ Change ADMIN_PASSWORD to something secure
├─ Don't commit .env to GitHub
└─ Use .env.example as template for others

❌ DON'T:
├─ Share .env file with anyone
├─ Put .env in GitHub
├─ Use weak passwords
├─ Upload .env to cloud storage
└─ Commit .env to version control
```

---

## 🚀 Quick Start

```bash
# 1. Edit .env with your MongoDB connection string
nano .env
# Or open in text editor and update MONGODB_URI

# 2. Install python-dotenv
pip install python-dotenv

# 3. Run Flask (it will load from .env)
python backend.py

# 4. Open browser
http://127.0.0.1:5000/login

# 5. Login with password from .env
# Default: YourSecurePassword123
```

---

## 🐛 Troubleshooting

### "Connection refused" error
```
Check:
□ MONGODB_URI is correct in .env
□ Copy-paste entire connection string
□ No typos in password
□ MongoDB Atlas whitelist includes your IP
```

### "Cannot find .env file"
```
Solution:
□ Make sure .env is in same folder as backend.py
□ Check file exists: ls -la .env (or dir .env on Windows)
□ Don't use .env.example, use .env
```

### "Environment variable not loaded"
```
Solution:
□ Install python-dotenv: pip install python-dotenv
□ Add this at top of backend.py:
   from dotenv import load_dotenv
   load_dotenv()
□ Restart Flask
```

---

## Summary

✅ **Created `.env` file** - Stores your secret data
✅ **Created `.env.example`** - Template for others
✅ **Created `.gitignore`** - Protects .env from GitHub
✅ **Updated `backend.py`** - Loads from .env
✅ **Updated `requirements.txt`** - Added python-dotenv

**Your secrets are now safely stored and protected!** 🔐

Now just add your MongoDB connection string to `.env` and you're done!
