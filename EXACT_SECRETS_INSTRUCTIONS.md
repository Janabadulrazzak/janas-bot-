# 🔴 EXACT Instructions: Fix API Key in Secrets

## Current Problem
The app at https://janasbot.streamlit.app/ is STILL using the OLD API key (ending in `3-UA`).

## Step-by-Step Fix (DO THIS NOW)

### Step 1: Open Secrets Tab
1. Go to: **https://share.streamlit.io/**
2. Click on your app: **janasbot**
3. Click **"Manage app"** (three dots ⋮ or gear icon ⚙️)
4. Click **"Secrets"** tab at the top

### Step 2: Check What's There
Look at the `OPENAI_API_KEY` line. What does it show?

**If you see:**
```
OPENAI_API_KEY = "sk-proj-7iL_H0A_...something ending in 3-UA"
```
→ This is WRONG! Delete it and use the new key below.

**If you see:**
```
OPENAI_API_KEY = "sk-proj-WLecXAAn5_...something ending in 9zGoA"
```
→ This SHOULD be correct, but if it's still not working, see troubleshooting below.

### Step 3: Delete Everything and Add New Key
1. **DELETE** the entire `OPENAI_API_KEY` line (or clear its value)
2. **Type this EXACTLY** (copy the entire line):

```toml
OPENAI_API_KEY = "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"
```

3. **Make sure:**
   - It starts with: `sk-proj-WLecXAAn5`
   - It ends with: `...9zGoA` (NOT `...3-UA`)
   - It's in quotes: `"key"`
   - Format is: `OPENAI_API_KEY = "..."`

### Step 4: Save
1. Scroll to the bottom of the Secrets page
2. Click **"Save"** button
3. You should see a message like "Secrets saved"

### Step 5: Force Reboot
1. Go to **"Logs"** tab
2. Look for **"Reboot app"** or **"Restart"** button
3. Click it
4. Wait 2-3 minutes

### Step 6: Test
1. Go to: **https://janasbot.streamlit.app/**
2. Try asking a question
3. Check the sidebar - you should see: "🔑 API Key loaded: sk-proj-WLecXAAn5...9zGoA"

## If It STILL Doesn't Work

### Option A: Check if Multiple Apps
1. Do you see MULTIPLE apps in Streamlit Cloud?
2. Make sure you're updating the CORRECT app (the one that matches https://janasbot.streamlit.app/)

### Option B: Delete and Recreate
1. **Delete** the app from Streamlit Cloud
2. **Create NEW app:**
   - Repository: `Janabadulrazzak/janas-bot-`
   - Branch: `main`
   - Main file: `user_chatbot.py`
   - App URL: `janasbot`
3. **BEFORE clicking Deploy:**
   - Go to "Secrets" tab
   - Add the NEW API key (the one ending in `9zGoA`)
   - Save
4. **THEN click Deploy**

### Option C: Verify Key Format
The key should look EXACTLY like this (all one line):
```
OPENAI_API_KEY = "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"
```

## What to Tell Me

After checking Secrets, tell me:
1. **What does the key END with?** (`3-UA` or `9zGoA`?)
2. **What does the key START with?** (should be `sk-proj-WLecXAAn5`)
3. **Did you click Save?**
4. **Did you reboot the app?**
5. **How many apps do you see in Streamlit Cloud?**

## Visual Guide

```
Streamlit Cloud Dashboard
    ↓
Click "janasbot" app
    ↓
Click "Manage app" (⋮)
    ↓
Click "Secrets" tab
    ↓
Find: OPENAI_API_KEY = "..."
    ↓
Check last 5 characters:
    ❌ "...3-UA" = OLD KEY (DELETE IT!)
    ✅ "...9zGoA" = NEW KEY (CORRECT)
    ↓
If OLD: Delete and paste NEW key
    ↓
Click "Save"
    ↓
Go to "Logs" → Click "Reboot"
    ↓
Wait 2 minutes
    ↓
Test: https://janasbot.streamlit.app/
```

