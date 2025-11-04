# 🚀 Deploy to Run 24/7 - Quick Guide

## The Problem
- ngrok requires your computer to be ON
- If your computer turns off, the URL stops working

## The Solution: Streamlit Cloud (FREE, PERMANENT)

### ✅ What's Already Done
- Code updated to use Streamlit secrets
- Ready for cloud deployment

### 📋 Steps to Deploy

**1. Push to GitHub (if not done yet):**
```bash
cd /Users/jana/rag_chatbot_app
git add user_chatbot.py rag_chatbot.py
git commit -m "Update for Streamlit Cloud deployment"
git push -u origin main
```

**2. Deploy to Streamlit Cloud:**
- Go to: https://share.streamlit.io
- Sign in with GitHub
- Click "New app"
- Repository: `Janabadulrazzak/janas-bot-`
- Branch: `main`
- Main file: `user_chatbot.py`
- Click "Deploy"

**3. Add API Key Secret:**
- In Streamlit Cloud, go to your app
- Click "⚙️ Settings" (top right)
- Click "Secrets"
- Paste this:
```
OPENAI_API_KEY = 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
```
- Click "Save"

**4. Get Your 24/7 URL:**
- After deployment, you'll get: `https://janabadulrazzak-user-chatbot.streamlit.app`
- **This works 24/7, even when your computer is off!**

---

## ⚠️ Important: Resume Database

The `faiss_db/` folder needs to be uploaded to GitHub so the chatbot has your resume:

```bash
cd /Users/jana/rag_chatbot_app
git add faiss_db/
git commit -m "Add resume database"
git push
```

---

## 🎉 Result

Once deployed, you'll have:
- ✅ Permanent URL (works 24/7)
- ✅ No need for your computer to be on
- ✅ Free hosting
- ✅ Works anywhere in the world

---

**Need help?** See `DEPLOY_24_7.md` for detailed instructions.

