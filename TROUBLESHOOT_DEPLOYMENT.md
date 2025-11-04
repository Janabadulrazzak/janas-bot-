# 🔧 Troubleshoot Streamlit Cloud Deployment

## Step 1: Check Deployment Status

1. **Go to Streamlit Cloud Dashboard:**
   - Visit: https://share.streamlit.io/
   - Sign in with GitHub
   - Look for your app(s)

2. **Check App Status:**
   - Is the app showing as "Deploying..."?
   - Is it showing an error?
   - Is it showing "Failed to deploy"?

## Step 2: Check Deployment Logs

1. **Click on your app** in the dashboard
2. **Click "Manage app"**
3. **Go to "Logs" tab**
4. **Look for error messages** - Common errors:
   - `ModuleNotFoundError` - Missing dependency
   - `ImportError` - Import issue
   - `ValidationError` - API key/configuration issue
   - `FileNotFoundError` - Missing file
   - Build errors

## Step 3: Common Issues & Fixes

### Issue: "Repository not found" or "Access denied"
**Fix:**
- Make sure repository is public OR
- Authorize Streamlit Cloud to access private repos
- Go to: https://share.streamlit.io/ → Settings → GitHub Integration

### Issue: "Main file not found"
**Fix:**
- Make sure you selected the correct main file:
  - User page: `user_chatbot.py`
  - Admin page: `rag_chatbot.py`
- Verify the file exists in your GitHub repo

### Issue: "Error installing requirements"
**Fix:**
- Check `requirements.txt` exists
- Make sure all dependencies are compatible
- Check logs for specific package errors

### Issue: "ValidationError" or API key errors
**Fix:**
- Make sure API key is set in Secrets
- Go to: Manage app → Secrets → Add:
  ```toml
  OPENAI_API_KEY = "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"
  ```

### Issue: "Module not found" or Import errors
**Fix:**
- Check `requirements.txt` has all needed packages
- Make sure package versions are compatible
- Check logs for specific missing module

## Step 4: Verify Repository Setup

1. **Check GitHub Repository:**
   - Go to: https://github.com/Janabadulrazzak/janas-bot-
   - Make sure all files are there:
     - `user_chatbot.py`
     - `rag_chatbot.py`
     - `requirements.txt`
     - `faiss_db/` (if needed)

2. **Check Branch:**
   - Make sure you're deploying from `main` branch (or `master`)
   - Verify your code is pushed to GitHub

## Step 5: Redeploy

1. **Delete and recreate the app:**
   - Go to: https://share.streamlit.io/
   - Click "Manage app" → "Settings" → "Delete app"
   - Click "New app" and deploy again

2. **Or update existing app:**
   - Push new changes to GitHub
   - Streamlit Cloud will auto-redeploy
   - Or click "Manage app" → "Reboot app"

## Step 6: Check Specific Errors

### If you see logs/errors, share them and I can help fix:
- Copy the error message from the logs
- Share the full traceback if available
- Note which step failed (installing, building, running)

## Quick Checklist

- [ ] Repository is accessible (public or authorized)
- [ ] Main file is correct (`user_chatbot.py` or `rag_chatbot.py`)
- [ ] Branch is correct (`main` or `master`)
- [ ] `requirements.txt` exists and is valid
- [ ] API key is set in Secrets (for deployed apps)
- [ ] All files are pushed to GitHub
- [ ] Checked deployment logs for specific errors

## Need More Help?

**Share with me:**
1. What error message you see (copy from logs)
2. What step it fails at (deploying, installing, running)
3. Screenshot of the error (if possible)

