#!/bin/bash
set -e

echo "Starting Ollama server in background..."
ollama serve &

# Save the background PID
OLLAMA_PID=$!

echo "Waiting for Ollama server to be active..."
until ollama list 2>/dev/null | grep -q 'NAME'; do
  sleep 1
done

echo "Ollama server active. Pulling model: $MODEL_NAME"
ollama pull "$MODEL_NAME"

echo "Killing temporary Ollama server..."
kill $OLLAMA_PID
wait $OLLAMA_PID || true

echo "Starting Ollama server in foreground..."
exec ollama serve

