# Deploy to Run 24/7 (Even When Computer is Off)

## Why ngrok Won't Work
❌ ngrok requires your computer to be ON and running
❌ If your computer sleeps or turns off, the URL stops working

## Solution: Deploy to Streamlit Cloud (FREE, PERMANENT)

### Step 1: Push Your Code to GitHub
Your code is already committed locally. Now push it:

```bash
cd /Users/jana/rag_chatbot_app
git push -u origin main
```

(You'll need to authenticate with a Personal Access Token - see PUSH_TO_GITHUB.txt)

### Step 2: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud:**
   https://share.streamlit.io

2. **Sign in with GitHub:**
   - Click "Sign in"
   - Authorize with your GitHub account

3. **Deploy Your App:**
   - Click "New app"
   - Repository: `Janabadulrazzak/janas-bot-`
   - Branch: `main`
   - Main file path: `user_chatbot.py`
   - Click "Deploy"

4. **Get Your Permanent URL:**
   - After 2-3 minutes, you'll get a URL like:
   - `https://janabadulrazzak-user-chatbot.streamlit.app`
   - **This works 24/7, even when your computer is off!**

### Step 3: Set API Key as Secret

1. In Streamlit Cloud, go to your app settings
2. Click "Secrets"
3. Add:
   ```
   OPENAI_API_KEY = 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
   ```

### Step 4: Update Code to Use Secrets

We need to modify `user_chatbot.py` to read from Streamlit secrets instead of hardcoded API key.

---

## Alternative: Railway/Render (Also Free)

Both Railway and Render offer free tiers for hosting:
- **Railway:** https://railway.app
- **Render:** https://render.com

Both can run your Streamlit app 24/7 for free.

---

## Important Notes

⚠️ **Your API key is in the code** - Consider using environment variables or Streamlit Secrets
⚠️ **Resume database** - You'll need to upload `faiss_db/` to GitHub or set it up on the cloud
⚠️ **Free tier limits** - Streamlit Cloud free tier may have some limits, but it's usually sufficient

---

## Quick Deploy Checklist

- [ ] Push code to GitHub
- [ ] Deploy to Streamlit Cloud
- [ ] Set API key in Secrets
- [ ] Upload resume database (if needed)
- [ ] Get permanent 24/7 URL

