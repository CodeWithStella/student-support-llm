import os

# Settings can be overridden with environment variables so the same code runs
# locally and inside Docker (where the model is reached via host.docker.internal).
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3.2:1b")
APP_NAME = os.getenv("APP_NAME", "University Student Support Assistant")
LOG_FILE = os.getenv("LOG_FILE", "backend/logs/app.log")