# Push Your Code to GitHub - Step by Step

## Your Repository
https://github.com/Janabadulrazzak/janas-bot-

## Step 1: Get Personal Access Token

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Name: `janas-bot-push`
4. Select scope: ✅ **repo** (check all boxes under repo)
5. Click "Generate token"
6. **COPY THE TOKEN** (you'll only see it once!)

## Step 2: Push Your Code

Run these commands in Terminal:

```bash
cd /Users/jana/rag_chatbot_app
git push -u origin main
```

When prompted:
- **Username:** `Janabadulrazzak`
- **Password:** Paste your token (NOT your GitHub password)

## Alternative: Use GitHub Desktop

If you have GitHub Desktop:
1. Open GitHub Desktop
2. File → Add Local Repository
3. Navigate to: `/Users/jana/rag_chatbot_app`
4. Click "Publish repository"
5. It will authenticate automatically

## After Pushing

Once your code is on GitHub, you can deploy to Streamlit Cloud for 24/7 access!

See `QUICK_DEPLOY_24_7.md` for deployment steps.

