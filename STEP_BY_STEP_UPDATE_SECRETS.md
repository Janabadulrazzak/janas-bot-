# 🔴 STEP-BY-STEP: Update API Key in Streamlit Cloud

## ⚠️ You're Still Using the OLD Key!

The error shows the old key ending in `...3-UA`. You MUST update it in Streamlit Cloud.

## Detailed Steps

### Step 1: Open Streamlit Cloud
1. Open your web browser
2. Go to: **https://share.streamlit.io/**
3. Sign in with GitHub if needed

### Step 2: Find Your App
1. You should see a list of your apps
2. Find the app that's showing the error (probably `janasbot` or similar)
3. **Click on the app name** or click the **three dots (⋮)** next to it

### Step 3: Open Secrets
1. Click **"Manage app"** or **"Settings"**
2. Look for tabs at the top: **"Secrets"**, **"Settings"**, **"Logs"**, etc.
3. Click the **"Secrets"** tab

### Step 4: Update the API Key
1. You should see a text box with something like:
   ```toml
   OPENAI_API_KEY = "sk-proj-7iL_H0A_...3-UA"
   ```
   (This is the OLD key - you need to replace it)

2. **Select ALL the text** in the `OPENAI_API_KEY` line
3. **Delete it completely**
4. **Paste this NEW key:**
   ```toml
   OPENAI_API_KEY = "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"
   ```

5. **Double-check:**
   - The key starts with `sk-proj-WLecXAAn5`
   - The key ends with `...9zGoA` (NOT `...3-UA`)
   - There are quotes around the key: `"..."`

### Step 5: Save
1. Scroll to the bottom of the Secrets page
2. Click the **"Save"** button
3. You should see a message like "Secrets saved" or "App will redeploy"

### Step 6: Wait for Redeploy
1. Go to the **"Logs"** tab
2. Wait 1-2 minutes
3. You should see the app redeploying
4. The error should disappear

## If You Can't Find the Secrets Tab

1. Make sure you clicked **"Manage app"** (not just the app name)
2. Look for a menu with: Settings, Secrets, Logs, etc.
3. If you still don't see it, try:
   - Clicking the gear icon (⚙️)
   - Looking for "Configuration"
   - Checking if the app is still deploying (wait for it to finish)

## If You Have Multiple Apps

**Update BOTH:**
- User page app (with `user_chatbot.py`)
- Admin page app (with `rag_chatbot.py`)

Both need the same new API key!

## Verify It Worked

1. After saving, wait 2 minutes
2. Go back to your app URL
3. Try asking a question
4. If it works, the key is updated! ✅
5. If you still get the error, double-check the key was saved correctly

## Still Having Issues?

**Share with me:**
1. Can you see the "Secrets" tab?
2. What does the current `OPENAI_API_KEY` value show?
3. Did you click "Save"?
4. What does the Logs tab show after saving?

