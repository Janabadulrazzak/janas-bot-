#!/bin/bash
# Quick start script for RAG Chatbot

echo "Starting RAG Chatbot Application..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run the application
echo ""
echo "Launching Streamlit app..."
streamlit run rag_chatbot.py

