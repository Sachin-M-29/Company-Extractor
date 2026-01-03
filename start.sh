#!/bin/bash

set -e

echo "Starting Company Extractor Backend..."

# Start Ollama in background
echo "Starting Ollama service..."
ollama serve &

# Wait for Ollama to be ready
echo "Waiting for Ollama to start..."
sleep 10

# Pull Mistral model if not exists
echo "Checking Mistral model..."
if ! ollama list | grep -q "mistral:7b-instruct-q4_0"; then
    echo "Downloading Mistral 7B model (this will take a few minutes)..."
    ollama pull mistral:7b-instruct-q4_0
else
    echo "Mistral model already available"
fi

# Verify model is loaded
echo "Verifying model..."
ollama list

echo "Starting Flask API..."
# Start Flask app
cd /app
python3 api.py
