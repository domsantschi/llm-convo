#!/bin/bash

echo "Setting up two Ollama instances with specific models..."

# Start the containers
echo "Starting containers..."
docker compose up -d

# Wait a bit for Ollama instances to start
echo "Waiting for Ollama instances to start..."
sleep 15

# Pull Llama 3.2 3B model to first instance
echo "Setting up Ollama1 with Llama 3.2 3B model..."
docker exec ollama1 ollama pull llama3.2:3b

# Pull Phi-3 Mini model to second instance
echo "Setting up Ollama2 with Phi-3 Mini model..."
docker exec ollama2 ollama pull phi3:mini

# List available models for each instance
echo "Ollama1 models:"
docker exec ollama1 ollama list

echo "Ollama2 models:"
docker exec ollama2 ollama list

echo ""
echo "Setup complete! Your endpoints:"
echo "- LLM Convo App: http://localhost:5234"
echo "- Ollama1 (Llama 3.2 3B): http://localhost:11434/v1"
echo "- Ollama2 (Phi-3 Mini): http://localhost:11435/v1"
echo ""
echo "In your app, use these endpoint URLs:"
echo "Endpoint 1: http://localhost:11434/v1"
echo "Endpoint 2: http://localhost:11435/v1"
