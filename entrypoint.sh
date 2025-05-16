#!/bin/bash
# Start Ollama in the background
ollama serve &

# Optional: wait a bit for Ollama to initialize
sleep 10

# Start your Python app
cd /app/UI
exec python app.py
