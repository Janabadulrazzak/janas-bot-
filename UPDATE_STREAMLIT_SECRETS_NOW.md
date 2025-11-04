# 🔑 UPDATE STREAMLIT CLOUD SECRETS - URGENT

## Your New API Key
```
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
```

## ⚠️ The Error Shows You're Using the OLD API Key

The error message shows the old key ending in `...3-UA`. You need to update Streamlit Cloud Secrets.

## Step-by-Step: Update Secrets in Streamlit Cloud

### For User Page (Public Chat)

1. **Go to:** https://share.streamlit.io/
2. **Find your app** (the one with `user_chatbot.py`)
3. **Click "Manage app"** (three dots or gear icon)
4. **Click "Secrets" tab**
5. **Find the `OPENAI_API_KEY` line**
6. **Replace the entire value** with your new key:
   ```toml
   OPENAI_API_KEY = "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"
   ```
7. **Click "Save"** (bottom of the page)
8. **Wait for the app to redeploy** (30 seconds - 2 minutes)

### For Admin Page (If You Have One)

1. **Repeat the same steps** for your admin app (`rag_chatbot.py`)
2. **Update the same API key** in its Secrets

## How to Verify It's Updated

1. After saving, check the app logs
2. The error should disappear
3. Try asking a question in the chat
4. If it works, the API key is correct!

## Important Notes

- **Make sure to use the NEW key** (starts with `sk-proj-WLecXAAn5`)
- **The old key** (ending in `3-UA`) is disabled - that's why you're getting the error
- **After updating**, the app will automatically redeploy
- **It may take 1-2 minutes** for changes to take effect

## If You Still Get Errors

1. **Double-check** you copied the entire key correctly
2. **Make sure** there are no extra spaces or quotes
3. **Check** both apps (user and admin) have the updated key
4. **Wait** a few minutes for the redeploy to complete

