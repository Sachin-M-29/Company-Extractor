#!/bin/bash

# Setup script for Company Information Extractor

echo "🚀 Setting up Company Information Extractor..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed."
    exit 1
fi

echo "✓ Python and Node.js found"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install flask flask-cors requests beautifulsoup4 playwright ollama

# Install Playwright browsers
python -m playwright install

# Setup Next.js UI
echo "📦 Setting up Next.js UI..."
cd nextjs-ui
npm install
cd ..

echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Make sure Ollama is running: ollama serve"
echo "2. Start Flask API: python api.py"
echo "3. Start Next.js dev: cd nextjs-ui && npm run dev"
echo "4. Open http://localhost:3000 in your browser"
