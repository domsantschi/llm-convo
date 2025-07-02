# PowerShell script to set up two Ollama instances with different models
Write-Host "Setting up Ollama instances with specific models..." -ForegroundColor Green

# Check if Docker is running
if (!(Get-Process "Docker Desktop" -ErrorAction SilentlyContinue)) {
    Write-Host "Please start Docker Desktop first!" -ForegroundColor Red
    exit 1
}

# Start the containers
Write-Host "Starting containers..." -ForegroundColor Yellow
docker compose up -d

# Wait a bit for Ollama instances to start
Write-Host "Waiting for Ollama instances to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

# Pull Llama 3.2 3B model to first instance
Write-Host "Setting up Ollama1 with Llama 3.2 3B model..." -ForegroundColor Yellow
docker exec ollama1 ollama pull llama3.2:3b

# Pull Phi-3 Mini model to second instance
Write-Host "Setting up Ollama2 with Phi-3 Mini model..." -ForegroundColor Yellow
docker exec ollama2 ollama pull phi3:mini

# List available models for each instance
Write-Host "Ollama1 models:" -ForegroundColor Green
docker exec ollama1 ollama list

Write-Host "Ollama2 models:" -ForegroundColor Green
docker exec ollama2 ollama list

Write-Host ""
Write-Host "Setup complete! Your endpoints:" -ForegroundColor Green
Write-Host "- LLM Convo App: http://localhost:5234" -ForegroundColor Cyan
Write-Host "- Ollama1 (Llama 3.2 3B): http://localhost:11434/v1" -ForegroundColor Cyan
Write-Host "- Ollama2 (Phi-3 Mini): http://localhost:11435/v1" -ForegroundColor Cyan
Write-Host ""
Write-Host "In your app, use these endpoint URLs:" -ForegroundColor Yellow
Write-Host "Endpoint 1: http://localhost:11434/v1" -ForegroundColor White
Write-Host "Endpoint 2: http://localhost:11435/v1" -ForegroundColor White
