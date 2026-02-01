# 🌍 REMOTE ACCESS WITH MONGODB ATLAS

## Complete Setup Guide (Home → College)

---

## STEP 1: Update backend.py

Open `backend.py` and change line ~37:

### Find:
```python
MONGO_URI = "mongodb://localhost:27017/"  # Change if using MongoDB Atlas
```

### Replace with your MongoDB Atlas connection:
```python
MONGO_URI = "mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/child_monitoring?retryWrites=true&w=majority"
```

**Where to get this:**
1. Go to: https://www.mongodb.com/cloud/atlas
2. Login to your account
3. Click your cluster
4. Click "Connect"
5. Choose "Connect your application"
6. Copy the connection string
7. Replace `<username>` and `<password>` with your credentials
8. Make sure `/child_monitoring` is in the URL

---

## STEP 2: Update client.py

On your **home laptop**, edit `client.py`:

### Find (around line 10):
```python
MONGO_URI = "mongodb://localhost:27017/"
```

### Replace with:
```python
MONGO_URI = "mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/child_monitoring?retryWrites=true&w=majority"
```

**Use the SAME connection string as backend.py**

---

## STEP 3: Test Locally First

Before accessing remotely, test on home WiFi:

```bash
# Terminal 1: Start Flask (no MongoDB needed, it uses Atlas)
python backend.py

# Terminal 2: Start client (on your laptop)
python client.py

# Browser: Test locally
http://127.0.0.1:5000/login
# Or:
http://192.168.0.104:5000/login

# Should work? Great! ✅
```

**If it doesn't work:**
- Check connection string spelling
- Check username/password correct
- Check MongoDB Atlas whitelist your IP (Settings → Network Access)

---

## STEP 4: Deploy Flask to Internet

Now deploy Flask so you can access from **college**:

### Option A: Ngrok (Easiest - Quick Test)

```bash
# Download from: https://ngrok.com/download
# Unzip to your project folder

# Run in terminal:
ngrok http 5000

# You'll see:
# Forwarding: https://abc123def.ngrok.io -> http://localhost:5000

# From college, open:
https://abc123def.ngrok.io/login
```

**Pros:**
- ✅ Instant setup
- ✅ Works immediately
- ✅ Free tier available

**Cons:**
- ❌ URL changes every restart
- ❌ Limited uptime (free tier)

---

### Option B: PythonAnywhere (Permanent - Recommended)

#### Free Account:
1. Go to: https://www.pythonanywhere.com
2. Sign up (free account)
3. Login to dashboard

#### Upload Your Files:
1. Click "Files"
2. Click "Upload a file"
3. Upload these files:
   - `backend.py` (UPDATED with Atlas URI)
   - `requirements.txt`
   - Upload `templates/index.html` to `templates/` folder

#### Create Web App:
1. Click "Web" (top menu)
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Choose "Python 3.x"
5. Setup Flask:
   - Virtualenv: `/home/yourname/.virtualenvs/mysite`
   - WSGI file: `/home/yourname/mysite/flask_app.py`

#### Create WSGI File:
1. Go to "Files"
2. Create new file: `flask_app.py`
3. Paste this:

```python
import sys
import os

path = '/home/yourname'  # Change to your username
if path not in sys.path:
    sys.path.append(path)

os.chdir(path)

from backend import app as application
```

#### Configure Environment:
1. Go to "Web" tab
2. Scroll to "Virtualenv"
3. Click it and setup:
   ```bash
   pip install flask pymongo requests psutil
   ```

#### Reload:
1. Click "Reload" button
2. Get your URL: `https://yourname.pythonanywhere.com`

#### Access from College:
```
https://yourname.pythonanywhere.com/login
Password: YourSecurePassword123
```

---

### Option C: Heroku (Also Good)

1. Go to: https://www.heroku.com
2. Sign up (free tier available)
3. Create new app
4. Connect GitHub or upload code
5. Deploy
6. Get URL: `https://yourapp-12345.herokuapp.com`

---

## STEP 5: Update client.py Backend URL (Optional)

If using PythonAnywhere, update `client.py`:

### Find (around line 15):
```python
BACKEND_URL = "http://192.168.0.104:5000"
```

### Change to:
```python
BACKEND_URL = "https://yourname.pythonanywhere.com"
```

**Now client.py will send results to cloud backend!**

---

## STEP 6: Run Everything

### On Home Laptop:

```bash
# Terminal 1: Start Flask (uses MongoDB Atlas)
python backend.py
# Output: Running on http://127.0.0.1:5000

# Terminal 2: Start client (uses MongoDB Atlas)
python client.py
# Output: Device registered: YOUR-LAPTOP
#         Polling for commands...
```

### From College:

**Open browser:**
```
https://yourname.pythonanywhere.com/login
```

**Enter password:**
```
YourSecurePassword123
```

**See dashboard:**
```
✅ Your laptop appears as "YOUR-LAPTOP: Online"
✅ Can click [Screenshot]
✅ Can click [Lock]
✅ Can see keystrokes
✅ Monitoring works! 🎉
```

---

## How It Works (Remote)

```
COLLEGE                    INTERNET                    HOME
════════════════════════════════════════════════════════════════

Your laptop                                       Your home laptop
with browser                                      running client.py
    │                                                    │
    │ https://yourname.pythonanywhere.com/login        │
    ├───────────────────────────┐                      │
    │                           ▼                      │
    │                    PYTHONANYWHERE                │
    │                    (Flask Backend)               │
    │                           ├──────────────────────┤
    │                           │                      │
    │                    MONGODB ATLAS (Cloud)         │
    │                    (Shared Database)             │
    │                           │                      │
    │                           ▼                      │
    └───────────────────────────┘                      │
           (Commands written here)              │
                                                │
                                                ▼ (Every 5 seconds)
                                    client.py polls for commands
                                                │
                                    Executes: Screenshot/Lock
                                                │
                                    Uploads result to Atlas
                                                │
    ◄───────────────────────────────────────────┘
    
    You see screenshot in browser! ✅
```

---

## CHECKLIST

```
MongoDB Atlas:
□ Created account
□ Created cluster
□ Got connection string
□ Connection string has username:password
□ Whitelist your home IP in Network Access
□ Whitelist 0.0.0.0/0 (for college/anywhere)

backend.py:
□ Updated MONGO_URI on line ~37
□ Connection string is correct
□ No typos in connection string

client.py:
□ Updated MONGO_URI (same as backend.py)
□ BACKEND_URL updated (if using cloud backend)

Testing:
□ Flask starts without errors
□ client.py shows "Device registered"
□ Can login locally (192.168.0.104:5000)
□ Dashboard shows your device

Deployment:
□ Chose deployment method (Ngrok/PythonAnywhere/Heroku)
□ Deployed Flask backend
□ Got public URL
□ Can access from college

Remote Testing:
□ Open https://yourname.pythonanywhere.com/login
□ Login with password
□ See your device
□ Click [Screenshot]
□ Screenshot appears from home laptop! ✅
```

---

## Troubleshooting Remote Access

### "Can't connect to database"
```
Solution:
1. Check connection string in backend.py
2. Check MongoDB Atlas whitelist includes:
   - Your home IP: Settings → Network Access
   - College IP: 0.0.0.0/0 (allows anywhere)
3. Test: mongosh command (from MongoDB Atlas)
```

### "Page not loading from college"
```
Solution:
1. Check Flask backend deployed correctly
2. Check URL is correct
3. Try: https://yourname.pythonanywhere.com
4. Check firewall allows HTTPS (port 443)
5. Try different browser
```

### "Device shows offline"
```
Solution:
1. Check client.py is running on home laptop
2. Check connection string in client.py
3. Check client.py can reach MongoDB Atlas
4. Restart client.py
5. Check home laptop still has internet
```

### "Commands not executing"
```
Solution:
1. Check device is "Online" (green indicator)
2. Click [Screenshot] button
3. Check console output on home laptop
4. Wait 10 seconds for polling
5. Refresh dashboard
6. Check MongoDB Atlas for errors (Metrics)
```

---

## SECURITY NOTE

```
⚠️ Connection String has password:
mongodb+srv://username:PASSWORD@...

KEEP IT SAFE!
- Don't share it
- Don't put in GitHub (public)
- Don't give to friends
- Only you should have it
```

---

## Summary

✅ **MongoDB Atlas:** Database in cloud (accessible everywhere)
✅ **backend.py:** Updated with Atlas URI
✅ **client.py:** Updated with Atlas URI
✅ **PythonAnywhere:** Flask deployed to internet
✅ **From College:** Access via cloud backend

**Now you can monitor from anywhere! 🌍**

---

## Next Steps

1. ✅ Update backend.py (add Atlas URI)
2. ✅ Update client.py (add Atlas URI)
3. ✅ Test locally (should work)
4. ✅ Choose deployment (PythonAnywhere recommended)
5. ✅ Deploy Flask backend
6. ✅ Access from college
7. ✅ Start monitoring! 🎉

**Need help with any step? Let me know!**
