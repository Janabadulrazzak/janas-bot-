# 🔴 URGENT: Fix API Key - The Old Key is Still There!

## The Problem
The error shows `...3-UA` which means the **OLD disabled key** is still in Secrets.

## MUST DO THIS NOW:

### Step 1: Open Secrets
1. Go to: **https://share.streamlit.io/**
2. Find your app: **janasbot**
3. Click **"Manage app"** (three dots ⋮ or gear ⚙️)
4. Click **"Secrets"** tab

### Step 2: Find and DELETE the Old Key
1. Look for this line:
   ```
   OPENAI_API_KEY = "sk-proj-...something...3-UA"
   ```
2. **SELECT THE ENTIRE LINE** (including `OPENAI_API_KEY =`)
3. **DELETE IT COMPLETELY**
4. The Secrets box should be empty or have other keys only

### Step 3: Add the NEW Key
1. In the Secrets text box, type or paste this **EXACTLY**:

```toml
OPENAI_API_KEY = "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"
```

2. **VERIFY:**
   - ✅ Starts with: `sk-proj-WLecXAAn5`
   - ✅ Ends with: `...9zGoA` (NOT `...3-UA`)
   - ✅ Has quotes: `"key"`
   - ✅ Format: `OPENAI_API_KEY = "..."`

### Step 4: SAVE
1. Scroll to the **BOTTOM** of the page
2. Click **"Save"** button
3. Wait for confirmation message

### Step 5: REBOOT
1. Go to **"Logs"** tab
2. Look for **"Reboot app"** or **"Restart"** button
3. Click it
4. Wait 2-3 minutes

### Step 6: TEST
1. Go to: **https://janasbot.streamlit.app/**
2. Try asking a question
3. The error should be gone!

## If You Still Don't See It Working

### Check These:
1. **Did you delete the OLD key completely?**
   - There should be NO key ending in `3-UA`
   
2. **Did you add the NEW key?**
   - Must end in `9zGoA`
   
3. **Did you click SAVE?**
   - Must see "Secrets saved" message
   
4. **Did you reboot?**
   - App must restart to use new key
   
5. **Are you looking at the RIGHT app?**
   - Make sure it's the one for https://janasbot.streamlit.app/

## Still Not Working? Try This:

### Delete and Recreate the App
1. In Streamlit Cloud, **DELETE** the app
2. **Create NEW app:**
   - Repository: `Janabadulrazzak/janas-bot-`
   - Branch: `main`
   - Main file: `user_chatbot.py`
   - App URL: `janasbot`
3. **BEFORE clicking "Deploy":**
   - Click **"Secrets"** tab
   - Add the NEW key (ending in `9zGoA`)
   - Click **"Save"**
4. **THEN click "Deploy"**

This way the new key is set BEFORE deployment starts.

## Visual Checklist

```
□ Deleted old key (ending in 3-UA)
□ Added new key (ending in 9zGoA)
□ Clicked Save
□ Rebooted app
□ Waited 2-3 minutes
□ Tested the app
```

## What the Key Should Look Like

**WRONG (OLD - DELETE THIS):**
```
OPENAI_API_KEY = "sk-proj-...3-UA"
```

**CORRECT (NEW - USE THIS):**
```
OPENAI_API_KEY = "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"
```

