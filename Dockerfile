# Dockerfile for the FastAPI backend (Optional Extension: Option C)
FROM python:3.11-slim

# Avoid writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first to take advantage of Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source
COPY backend/ ./backend/

# The container reaches Ollama running on the host machine.
# On Docker Desktop (Windows/macOS) host.docker.internal resolves to the host.
ENV OLLAMA_URL=http://host.docker.internal:11434/api/generate

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
