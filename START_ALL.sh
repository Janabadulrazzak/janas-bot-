#!/bin/bash

cd /Users/jana/rag_chatbot_app

# Set API key
export OPENAI_API_KEY="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"

# Activate venv
source venv/bin/activate

# Kill old processes
pkill -f streamlit 2>/dev/null
pkill -f ngrok 2>/dev/null

echo "🚀 Starting Admin page..."
nohup streamlit run rag_chatbot.py --server.port 8501 --server.address 0.0.0.0 > /dev/null 2>&1 &

sleep 3

echo "🚀 Starting User page..."
nohup streamlit run user_chatbot.py --server.port 8502 --server.address 0.0.0.0 > /dev/null 2>&1 &

sleep 3

echo "🚀 Starting ngrok tunnel..."
nohup ngrok http 8502 --domain=hyaloid-nonhypnotically-carmen.ngrok-free.dev > /dev/null 2>&1 &

sleep 5

echo ""
echo "✅ All services started!"
echo ""
echo "📍 Admin: http://localhost:8501"
echo "📍 User:  http://localhost:8502"
echo "📍 Public: https://hyaloid-nonhypnotically-carmen.ngrok-free.dev"
echo ""

