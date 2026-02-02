# Ngrok Setup Guide - Local Backend Deployment

## What is Ngrok?

Ngrok creates a secure tunnel from a public URL to your local machine. This lets you:

- ✅ Run your backend locally (on your powerful PC)
- ✅ Access it from anywhere via a public URL
- ✅ No deployment needed
- ✅ **FREE** for basic use

## 🚀 Setup Steps

### Step 1: Install Ngrok

**Option A: Using Chocolatey (Recommended)**

```powershell
choco install ngrok
```

**Option B: Manual Download**

1. Go to https://ngrok.com/download
2. Download Windows version
3. Extract to `C:\ngrok\`
4. Add to PATH or run from that directory

### Step 2: Sign Up for Ngrok (Free Account)

1. Go to https://dashboard.ngrok.com/signup
2. Sign up (free - no credit card needed)
3. Copy your **Authtoken** from the dashboard

### Step 3: Configure Ngrok

Run this command (replace with your actual token):

```powershell
ngrok config add-authtoken YOUR_AUTHTOKEN_HERE
```

### Step 4: Start Your Backend Server

Make sure your backend is running:

```powershell
cd C:\projects\fish_disease_backend
$env:HF_TOKEN="your_huggingface_token_here"
uvicorn main:app --host 0.0.0.0 --port 8000
```

Keep this terminal open!

### Step 5: Start Ngrok Tunnel

Open a **NEW** terminal window and run:

```powershell
ngrok http 8000
```

You'll see output like:

```
Forwarding   https://abc123.ngrok-free.app -> http://localhost:8000
```

**Copy the `https://` URL** - this is your public backend URL!

## 🌐 Update Your Frontend

### Update Frontend Environment Variable

1. Go to your frontend folder:

   ```powershell
   cd C:\projects\aqua-health-pro
   ```

2. Edit `.env.development`:

   ```bash
   VITE_API_URL=https://abc123.ngrok-free.app
   ```

   (Replace with YOUR ngrok URL)

3. Restart your frontend:
   ```powershell
   npm run dev
   ```

## ✅ Verification

1. **Test Backend:** Visit `https://your-ngrok-url.ngrok-free.app/docs`
2. **Test Health:** Visit `https://your-ngrok-url.ngrok-free.app/health`
3. **Upload Image:** Try the `/predict` endpoint with a fish image

## 📱 For Mobile App (APK)

Update your app's API URL:

1. Edit `.env.production`:

   ```bash
   VITE_API_URL=https://your-ngrok-url.ngrok-free.app
   ```

2. Rebuild:

   ```powershell
   npm run build
   npx cap sync android
   ```

3. Generate new APK with updated URL

## ⚠️ Important Notes

### Free Tier Limitations:

- ✅ 1 online ngrok process
- ✅ 40 connections/minute
- ⚠️ **URL changes each time** you restart ngrok
- ⚠️ Session timeout after 2 hours (need to restart)

### Keeping URL Stable:

**Option A: Keep Ngrok Running**

- Don't close the ngrok terminal
- Your PC must stay on

**Option B: Use Static Domain (Paid - $8/month)**

- Get a permanent URL that doesn't change
- Upgrade at https://dashboard.ngrok.com/billing

## 🔄 Daily Workflow

**Every time you start working:**

1. Start backend:

   ```powershell
   cd C:\projects\fish_disease_backend
   $env:HF_TOKEN="your_huggingface_token_here"
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

2. Start ngrok (new terminal):

   ```powershell
   ngrok http 8000
   ```

3. Copy new ngrok URL

4. Update frontend `.env.development` with new URL

5. Restart frontend:
   ```powershell
   npm run dev
   ```

## 💡 Pro Tips

### Auto-start Scripts

Create `start_backend.ps1`:

```powershell
cd C:\projects\fish_disease_backend
$env:HF_TOKEN="your_huggingface_token_here"
uvicorn main:app --host 0.0.0.0 --port 8000
```

Create `start_ngrok.ps1`:

```powershell
ngrok http 8000
```

Then just double-click these files to start!

### CORS Configuration

Your backend already has CORS configured to accept all origins (`"*"`), so ngrok URLs will work automatically.

## 🎯 For Production

If you need a permanent solution later:

- Consider Hugging Face Spaces (free, 16GB RAM)
- Or upgrade ngrok to get a static domain ($8/month)
- Or use Oracle Cloud's always-free tier (24GB RAM)

## 🔧 Troubleshooting

**ngrok command not found:**

- Install using chocolatey: `choco install ngrok`
- Or add ngrok.exe location to PATH

**Connection refused:**

- Make sure your backend is running first
- Check it's on port 8000: http://localhost:8000

**CORS errors:**

- Your backend already allows all origins
- But if issues occur, add your ngrok URL to CORS in `main.py`

## 🎉 Done!

Your Fish Disease Detector backend is now accessible from anywhere via ngrok!
