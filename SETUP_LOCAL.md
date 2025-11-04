# 🔐 Local Development Setup

## API Key Setup

Since the API key is no longer hardcoded, you need to set it as an environment variable for local development.

### Option 1: Set Environment Variable (Recommended)

**macOS/Linux:**
```bash
export OPENAI_API_KEY="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"
```

**Windows:**
```cmd
set OPENAI_API_KEY=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
```

### Option 2: Create `.env` File (Alternative)

Create a `.env` file in the project root:
```
OPENAI_API_KEY=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
```

**Note:** `.env` files are already in `.gitignore`, so they won't be committed.

---

## Running Locally

1. Set the environment variable (see above)
2. Activate virtual environment:
   ```bash
   cd /Users/jana/rag_chatbot_app
   source venv/bin/activate
   ```
3. Run the app:
   ```bash
   streamlit run user_chatbot.py  # User page
   # or
   streamlit run rag_chatbot.py   # Admin page
   ```

---

## For Streamlit Cloud

✅ **No changes needed!** Just add the API key in Streamlit Secrets:
- Go to your app settings → Secrets
- Add: `OPENAI_API_KEY = sk-proj-...`

The code will automatically use the secret instead of environment variables.

