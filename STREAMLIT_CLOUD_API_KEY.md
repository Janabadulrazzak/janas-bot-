# 🔑 Update API Key in Streamlit Cloud

## Your New API Key
```
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
```

## Steps to Update

### For User Page (Public Chat)
1. Go to: **https://share.streamlit.io/**
2. Find your app (the one with `user_chatbot.py`)
3. Click **"Manage app"**
4. Go to **"Secrets"** tab
5. Replace the `OPENAI_API_KEY` value with:
   ```toml
   OPENAI_API_KEY = "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"
   ```
6. Click **"Save"**
7. The app will automatically redeploy

### For Admin Page
1. Go to: **https://share.streamlit.io/**
2. Find your admin app (the one with `rag_chatbot.py`)
3. Click **"Manage app"**
4. Go to **"Secrets"** tab
5. Replace the `OPENAI_API_KEY` value with the same key above
6. Click **"Save"**
7. The app will automatically redeploy

## ✅ Updated Locally

The following files have been updated:
- ✅ `START_ALL.sh` - Local startup script
- ✅ `START_LOCAL.sh` - Local development script
- ✅ `ADMIN_LINKS.txt` - Admin links documentation

## Test Locally

Restart your local apps:
```bash
cd /Users/jana/rag_chatbot_app
./START_ALL.sh
```

Or manually:
```bash
export OPENAI_API_KEY="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"
source venv/bin/activate
streamlit run rag_chatbot.py --server.port 8501 --server.address 0.0.0.0
```

## Links

- **Local Admin:** http://localhost:8501
- **Local User:** http://localhost:8502
- **Network Admin:** http://192.168.0.115:8501
- **Network User:** http://192.168.0.115:8502

