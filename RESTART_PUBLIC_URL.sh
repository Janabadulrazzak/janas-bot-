#!/bin/bash
# Restart public URL (user page + ngrok)

cd /Users/jana/rag_chatbot_app

echo "Restarting public URL..."
echo ""

# Kill existing instances
pkill -9 -f "streamlit run.*user_chatbot" 2>/dev/null
pkill -9 -f "ngrok.*8502" 2>/dev/null
sleep 2

# Start user page
echo "Starting user page..."
source venv/bin/activate
streamlit run user_chatbot.py --server.address 0.0.0.0 --server.port 8502 --server.headless=true > /tmp/user_bot.log 2>&1 &
sleep 5

if lsof -ti:8502 >/dev/null 2>&1; then
    echo "✅ User page started"
else
    echo "❌ User page failed to start"
    exit 1
fi

# Start ngrok
echo "Starting ngrok tunnel..."
~/Downloads/ngrok http 8502 --domain=hyaloid-nonhypnotically-carmen.ngrok-free.dev > /tmp/ngrok.log 2>&1 &
sleep 3

echo ""
echo "✅ Public URL should be working now!"
echo "🌍 https://hyaloid-nonhypnotically-carmen.ngrok-free.dev"
echo ""
echo "Check the URL in your browser"

