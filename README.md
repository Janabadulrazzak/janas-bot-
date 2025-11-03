# Jana's Bot - RAG Chatbot Application

A RAG (Retrieval-Augmented Generation) chatbot application that answers questions about Jana based on her resume.

## Features

- **Admin Page**: Upload and manage resume documents
- **User Page**: Public-facing chat interface (chat only, no uploads)
- **Light Pink Theme**: Beautiful, professional design
- **FAISS Vector Store**: Fast and efficient document retrieval
- **OpenAI Integration**: Powered by GPT-3.5-turbo

## Setup

### Prerequisites

- Python 3.9+
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd rag_chatbot_app
```

2. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set your OpenAI API key:
   - Edit `rag_chatbot.py` and `user_chatbot.py`
   - Update the `API_KEY` variable with your OpenAI API key

## Running the Application

### Start Admin Page (Port 8501)
```bash
streamlit run rag_chatbot.py --server.port 8501
```

### Start User Page (Port 8502)
```bash
streamlit run user_chatbot.py --server.port 8502
```

### Network Access

To make accessible on your local network:
```bash
streamlit run rag_chatbot.py --server.address 0.0.0.0 --server.port 8501
streamlit run user_chatbot.py --server.address 0.0.0.0 --server.port 8502
```

### Public Access (Any WiFi)

Use ngrok or deploy to Streamlit Cloud:

**ngrok:**
```bash
ngrok http 8502 --domain=your-domain.ngrok-free.dev
```

**Streamlit Cloud:**
1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Deploy `user_chatbot.py`

## File Structure

```
rag_chatbot_app/
├── rag_chatbot.py          # Admin page (upload documents)
├── user_chatbot.py         # User page (public chat)
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── config.toml         # Streamlit configuration
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Usage

1. **Admin Page** (`http://localhost:8501`):
   - Upload resume PDF
   - Manage documents
   - Test chatbot

2. **User Page** (`http://localhost:8502`):
   - Chat with the bot
   - Ask questions about Jana
   - No upload capability

## Configuration

### API Key
Update the `API_KEY` variable in both `rag_chatbot.py` and `user_chatbot.py`:
```python
API_KEY = "your-openai-api-key-here"
```

### Ports
Default ports:
- Admin: 8501
- User: 8502

## Dependencies

See `requirements.txt` for full list. Key dependencies:
- streamlit
- langchain
- langchain-openai
- langchain-community
- faiss-cpu
- openai

## Notes

- Resume must be uploaded on admin page first
- Vector database is stored in `faiss_db/` directory
- Chatbot generates responses in its own words, not verbatim copying

## License

Private use only.

