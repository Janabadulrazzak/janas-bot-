# 🔧 Setting Up Admin Page on Streamlit Cloud

## Current Issue
You're getting "you do not have access" when trying to access `https://janasbot.streamlit.app/`

## Solutions

### Option 1: Deploy Admin Page as Separate App (Recommended)

1. **Go to Streamlit Cloud Dashboard:**
   - Visit: https://share.streamlit.io/
   - Sign in with GitHub

2. **Deploy New App:**
   - Click "New app"
   - Select repository: `Janabadulrazzak/janas-bot-`
   - **Main file:** `rag_chatbot.py` (NOT `user_chatbot.py`)
   - **App URL:** Choose a name like `janasbot-admin` or `janasbot-admin-only`
   - Click "Deploy"

3. **Set API Key:**
   - After deployment starts, click "Manage app"
   - Go to "Secrets" tab
   - Add:
     ```toml
     OPENAI_API_KEY = "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"
     ```
   - Save

4. **Make App Private (Optional):**
   - In "Settings" → "Sharing"
   - Set to "Private" (only you can access)
   - Or keep it public but don't share the link

### Option 2: Fix Access to Existing App

If `janasbot.streamlit.app` is already deployed:

1. **Check Repository Access:**
   - Go to: https://share.streamlit.io/
   - Click "Settings" → "GitHub Integration"
   - Make sure Streamlit Cloud has access to your private repos
   - If not, authorize it

2. **Check App Status:**
   - Go to: https://share.streamlit.io/
   - Find your app: `janasbot`
   - Check if it's running or has errors
   - Look at the logs for `ValidationError` issues

3. **Verify Secrets:**
   - Click "Manage app" → "Secrets"
   - Make sure `OPENAI_API_KEY` is set correctly

## Current Admin Links

**Local (Your Computer):**
- http://localhost:8501
- http://192.168.0.115:8501 (same WiFi)

**Streamlit Cloud (After Deployment):**
- https://janasbot-admin.streamlit.app (or whatever name you choose)

## Notes

- The user page (`user_chatbot.py`) should be deployed separately
- The admin page (`rag_chatbot.py`) should be deployed separately
- Both need the same API key in Streamlit Secrets
- Both need access to the `faiss_db/` folder (make sure it's in GitHub)

