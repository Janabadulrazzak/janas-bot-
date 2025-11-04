# 🔑 How to Update Your API Key

## Step 1: Get New API Key from OpenAI

1. Go to: **https://platform.openai.com/api-keys**
2. Sign in to your OpenAI account
3. Click **"Create new secret key"**
4. Give it a name (e.g., "Jana's Bot")
5. **Copy the key immediately** (you won't see it again!)

## Step 2: Update Local Development

After you provide the new key, I'll update:
- `START_ALL.sh` - for running locally
- Local environment variable

## Step 3: Update Streamlit Cloud

1. Go to: **https://share.streamlit.io/**
2. For **each app** (user page and admin page):
   - Click **"Manage app"**
   - Go to **"Secrets"** tab
   - Find `OPENAI_API_KEY`
   - Replace the old key with your new key:
     ```toml
     OPENAI_API_KEY = "your-new-key-here"
     ```
   - Click **"Save"**
3. The app will automatically redeploy with the new key

## Step 4: Restart Local Apps

If you're running locally:
```bash
cd /Users/jana/rag_chatbot_app
./START_ALL.sh
```

Or manually:
```bash
export OPENAI_API_KEY="your-new-key-here"
source venv/bin/activate
streamlit run rag_chatbot.py --server.port 8501 --server.address 0.0.0.0
```

## Why API Keys Get Disabled

- **Quota exceeded** - You used all your credits
- **Billing issue** - Payment method needs updating
- **Security** - Key was exposed or compromised
- **Rate limits** - Too many requests in short time

## Tips to Avoid This

1. **Monitor usage:** https://platform.openai.com/usage
2. **Set usage limits:** https://platform.openai.com/account/billing/limits
3. **Keep keys secure** - Never commit to GitHub
4. **Use separate keys** - One for dev, one for production

## Need Help?

- Check billing: https://platform.openai.com/account/billing
- Add credits: https://platform.openai.com/account/billing
- Support: https://help.openai.com/

