# ✅ SIMPLE CHECKLIST - Get Connection String

## 3 EASY STEPS

### Step 1: Open MongoDB Atlas
```
Go to: https://www.mongodb.com/cloud/atlas
Login
```

### Step 2: Get Connection String
```
1. See "Cyber-Lab" cluster
2. Click [Connect] button
3. Click "Connect your application"
4. Select "Python"
5. Click [COPY]
```

### Step 3: Update .env File
```
1. Open: c:\Users\ronit\Desktop\techshurujan_2026\.env
2. Find: MONGODB_URI=mongodb+srv://ronit:ParentEyeadmintest@cyber-lab.xxxxx.mongodb.net/parenteye?retryWrites=true&w=majority
3. Replace xxxxx with cluster ID from MongoDB
4. Save (Ctrl+S)
```

---

## Done! 🎉

Your .env should look like:
```env
MONGODB_URI=mongodb+srv://ronit:ParentEyeadmintest@cyber-lab.abc123def456.mongodb.net/parenteye?retryWrites=true&w=majority
ADMIN_PASSWORD=YourSecurePassword123
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
BACKEND_URL=http://192.168.0.104:5000
```

---

## Run It

```bash
pip install python-dotenv
python backend.py
```

✅ **That's it!**
