#!/bin/bash

# Set API key as environment variable
export OPENAI_API_KEY="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"

# Activate virtual environment
cd /Users/jana/rag_chatbot_app
source venv/bin/activate

# Kill any existing Streamlit processes
pkill -f streamlit 2>/dev/null

echo "🚀 Starting Admin page (port 8501)..."
streamlit run rag_chatbot.py --server.port 8501 --server.address 0.0.0.0 &
ADMIN_PID=$!

sleep 3

echo "🚀 Starting User page (port 8502)..."
streamlit run user_chatbot.py --server.port 8502 --server.address 0.0.0.0 &
USER_PID=$!

sleep 3

echo ""
echo "✅ Both pages are starting!"
echo ""
echo "📍 Admin page: http://localhost:8501"
echo "📍 User page: http://localhost:8502"
echo ""
echo "📱 Network access:"
echo "   Admin: http://$(ipconfig getifaddr en0 2>/dev/null || hostname -I | awk '{print $1}'):8501"
echo "   User: http://$(ipconfig getifaddr en0 2>/dev/null || hostname -I | awk '{print $1}'):8502"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for Ctrl+C
trap "kill $ADMIN_PID $USER_PID 2>/dev/null; exit" INT TERM
wait

