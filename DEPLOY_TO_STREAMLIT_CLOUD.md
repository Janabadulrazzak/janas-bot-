# 🚀 Deploy to Streamlit Cloud - Step by Step

## Step 1: Go to Streamlit Cloud
1. Visit: **https://share.streamlit.io/**
2. Click **"Sign in"** (top right)
3. Choose **"Continue with GitHub"**
4. Authorize Streamlit to access your GitHub account

## Step 2: Deploy User Page (Public Chat)

1. Click **"New app"** button
2. Fill in the form:
   - **Repository:** Select `Janabadulrazzak/janas-bot-`
   - **Branch:** `main` (or `master`)
   - **Main file:** `user_chatbot.py`
   - **App URL:** `janasbot` (or any name you want)
3. Click **"Deploy"**

## Step 3: Add API Key Secret

1. After deployment starts, click **"Manage app"** (or wait for it to finish)
2. Click **"Secrets"** tab
3. Add this secret:
   ```toml
   OPENAI_API_KEY = "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"
   ```
4. Click **"Save"**

## Step 4: Deploy Admin Page (Separate App)

1. Click **"New app"** again
2. Fill in the form:
   - **Repository:** Select `Janabadulrazzak/janas-bot-`
   - **Branch:** `main` (or `master`)
   - **Main file:** `rag_chatbot.py`
   - **App URL:** `janasbot-admin` (or any name you want)
3. Click **"Deploy"**

## Step 5: Add API Key to Admin Page Too

1. Click **"Manage app"** for the admin app
2. Click **"Secrets"** tab
3. Add the same API key secret:
   ```toml
   OPENAI_API_KEY = "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"
   ```
4. Click **"Save"**

## Step 6: Make Admin Private (Optional)

1. For the admin app, click **"Settings"**
2. Under **"Sharing"**, set to **"Private"**
3. This way only you can access it

## Your URLs After Deployment

- **User Page (Public):** `https://janasbot.streamlit.app/`
- **Admin Page:** `https://janasbot-admin.streamlit.app/` (or whatever name you chose)

## Important Notes

⚠️ **If you get errors:**
- Check the logs in "Manage app" → "Logs"
- Make sure `faiss_db/` folder is in your GitHub repo (it should be)
- The `ValidationError` might still appear - we'll need to fix that if it does

⚠️ **First time using Streamlit Cloud:**
- If your repo is private, Streamlit will ask you to authorize access
- Make sure to grant access to your private repositories

## Need Help?

If deployment fails:
1. Check the deployment logs
2. Make sure all files are pushed to GitHub
3. Verify the API key is correct in Secrets

