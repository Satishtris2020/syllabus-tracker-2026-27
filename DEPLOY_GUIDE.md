# 🚀 Deploy to GitHub + Railway — Step by Step Guide

## What You'll Get
A live URL like: `https://your-school-syllabus.up.railway.app`
Share this with all teachers and the principal.

---

## PART 1 — Upload to GitHub (10 minutes)

### Step 1 — Create a GitHub Account
1. Go to **https://github.com**
2. Click "Sign up" → use your school email
3. Verify your email

### Step 2 — Create a New Repository
1. Click the **green "New"** button (or go to https://github.com/new)
2. Repository name: `syllabus-tracker-2026`
3. Set to **Public**
4. Click **"Create repository"**

### Step 3 — Upload Your Files
On the new empty repository page:
1. Click **"uploading an existing file"** link
2. Drag and drop ALL these files from your folder:
   ```
   app.py
   requirements.txt
   Procfile
   .gitignore
   static/
     index.html
     syllabus_data.json
   ```
   ⚠️ Also create a folder called `static` first:
   - Click "Create new file"
   - Type `static/.gitkeep` → commit
   - Then upload `index.html` and `syllabus_data.json` into the static folder

   **Easier method — GitHub Desktop:**
   1. Download GitHub Desktop: https://desktop.github.com
   2. File → Clone Repository → paste your repo URL
   3. Copy all app files into the cloned folder
   4. Click "Commit to main" → "Push origin"

3. Click **"Commit changes"**

---

## PART 2 — Deploy on Railway (5 minutes, FREE)

### Step 1 — Sign up at Railway
1. Go to **https://railway.app**
2. Click "Start a New Project"
3. Click **"Login with GitHub"** → authorize Railway

### Step 2 — Deploy from GitHub
1. Click **"Deploy from GitHub repo"**
2. Select your `syllabus-tracker-2026` repository
3. Railway auto-detects Python → click **"Deploy Now"**

### Step 3 — Set Environment Variables
In Railway dashboard → your project → **Variables** tab, add:
```
SECRET_KEY      = any-random-string-like-abc123xyz
TEACHER_PASSWORD = teacher123
ADMIN_PASSWORD   = principal123
```
(Change these passwords to anything you like!)

### Step 4 — Get Your Live URL
1. Click the **"Settings"** tab in Railway
2. Under "Domains" click **"Generate Domain"**
3. You'll get a URL like: `syllabus-tracker-2026.up.railway.app`

**That's your app — it's live! 🎉**

---

## PART 3 — Share with Teachers & Principal

### For Teachers
Send this message:
```
Syllabus Tracker App Link: https://YOUR-APP.up.railway.app
Password: teacher123

How to use:
1. Open the link
2. Select "Teacher" tab, enter your name and password
3. Click your class grade
4. Tick topics as you complete them
5. Mark topics for PT1/PT2/etc exams by clicking the exam buttons
6. Click "Save Progress" — it saves automatically to the server
```

### For Principal
```
Principal Dashboard: https://YOUR-APP.up.railway.app
Password: principal123

Select "Principal" tab → view full school progress,
subject-wise completion, and exam topics across all grades.
```

---

## PART 4 — Updating Passwords

To change passwords, go to Railway → Variables and update:
- `TEACHER_PASSWORD` — teachers use this
- `ADMIN_PASSWORD` — principal uses this

---

## Troubleshooting

**App shows error after deploy:**
- Check Railway "Deploy Logs" for errors
- Make sure `requirements.txt` and `Procfile` are uploaded

**Database resets on Railway free tier:**
- Railway free tier has temporary storage
- For permanent storage, upgrade to Railway Hobby ($5/month)
  OR use Railway + a free PostgreSQL add-on

**Want a custom domain (school.yourschool.com)?**
- In Railway → Settings → Custom Domain
- Add a CNAME record in your domain registrar pointing to Railway

---

## Alternative: Deploy on Render.com (also free)

1. Go to https://render.com → "New Web Service"
2. Connect GitHub → select repo
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn app:app`
5. Add same environment variables
6. Deploy!

Render gives you: `https://syllabus-tracker.onrender.com`
⚠️ Render free tier sleeps after 15 min of inactivity (slow first load)
Railway is faster for active school use.

---
Questions? The app works immediately — just upload and deploy!
