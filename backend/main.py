import os
import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.config import APP_NAME, LOG_FILE
from backend.llm_client import ask_local_llm


# Ensure the log directory exists before configuring logging,
# otherwise logging.basicConfig raises FileNotFoundError on startup.
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI(
    title=APP_NAME,
    description="A self-hosted LLM backend for university student support.",
    version="1.0.0"
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "University Student Support Assistant API is running."
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": APP_NAME,
        "timestamp": datetime.now().isoformat()
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):
    question = request.question.strip()

    if not question:
        logging.warning("Empty question received.")
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty. Please enter a question."
        )

    try:
        logging.info(f"Received question: {question}")

        answer = ask_local_llm(question)

        logging.info(f"Generated answer: {answer}")

        return {
            "question": question,
            "answer": answer
        }

    except ConnectionError as e:
        logging.error(f"Model connection error: {str(e)}")
        raise HTTPException(status_code=503, detail=str(e))

    except TimeoutError as e:
        logging.error(f"Model timeout error: {str(e)}")
        raise HTTPException(status_code=504, detail=str(e))

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected server error occurred."
        )