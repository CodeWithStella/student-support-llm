# University Student Support Assistant — Self-Hosted LLM Application

## 1. Project Overview

The University Student Support Assistant is a self-hosted Large Language Model application designed to help university students ask questions about common university services.

The assistant can respond to questions related to:

* Course registration
* Examination rules
* Library services
* ICT support
* Hostel application
* Fee payment
* Academic calendar
* Student conduct

The main purpose of this project is not to build the most intelligent chatbot, but to demonstrate a complete full-stack LLM application pipeline similar to what may be required in a real industry environment.

---

## 2. System Architecture

The system follows this flow:

```text
User
 |
 v
Streamlit Frontend
 |
 v
FastAPI Backend
 |
 v
Ollama Local LLM API
 |
 v
Generated Response
 |
 v
Frontend Output to User
```

The application includes:

* Local development environment
* Python virtual environment
* Locally hosted LLM using Ollama
* FastAPI backend
* Streamlit frontend
* API testing script
* Logging
* Error handling
* Prompt improvement
* Feedback rating bonus feature
* Documentation and screenshots

---

## 3. Tools and Technologies Used

| Component            | Tool Used                            |
| -------------------- | ------------------------------------ |
| Operating System     | Windows / Linux / macOS              |
| Code Editor          | Visual Studio Code                   |
| Programming Language | Python 3.10+                         |
| Virtual Environment  | Python venv                          |
| Backend API          | FastAPI                              |
| Web Server           | Uvicorn                              |
| Local LLM Serving    | Ollama                               |
| Local Model          | llama3.2:1b                          |
| Frontend             | Streamlit                            |
| API Testing          | Swagger UI, Browser, Python requests |
| Version Control      | Git and GitHub                       |
| Logging              | Python logging module                |

---

## 4. Project Structure

```text
student-support-llm/
├── backend/
│   ├── main.py
│   ├── llm_client.py
│   ├── config.py
│   └── logs/
│       └── app.log
├── frontend/
│   └── app.py
├── tests/
│   └── test_api.py
├── docs/
│   ├── screenshots/
│   └── report.md
├── feedback/
│   └── feedback.txt
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 5. Setup Instructions

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/student-support-llm.git
cd student-support-llm
```

---

### Step 2: Create Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment.

For Windows:

```bash
venv\Scripts\activate
```

For Linux/macOS:

```bash
source venv/bin/activate
```

---

### Step 3: Install Required Libraries

```bash
pip install -r requirements.txt
```

---

## 6. Install and Run Ollama

Download and install Ollama from:

```text
https://ollama.com/download
```

After installation, check if Ollama is installed:

```bash
ollama --version
```

Pull the local model:

```bash
ollama pull llama3.2:1b
```

Run the model:

```bash
ollama run llama3.2:1b
```

---

## 7. Run the FastAPI Backend

Open a new terminal in the project folder.

Activate the virtual environment:

```bash
venv\Scripts\activate
```

Run the backend:

```bash
uvicorn backend.main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

Swagger documentation is available at:

```text
http://127.0.0.1:8000/docs
```

Health endpoint:

```text
http://127.0.0.1:8000/health
```

---

## 8. Run the Streamlit Frontend

Open another terminal in the project folder.

Activate the virtual environment:

```bash
venv\Scripts\activate
```

Run the frontend:

```bash
streamlit run frontend/app.py
```

The frontend will open at:

```text
http://localhost:8501
```

---

## 8b. Run the Backend with Docker (Optional Extension: Option C)

The backend can be containerised with the provided `Dockerfile`.

Make sure Ollama is installed and running on the host machine first
(`ollama run llama3.2:1b`).

Build the image:

```bash
docker build -t student-support-backend .
```

Run the container:

```bash
docker run -p 8000:8000 student-support-backend
```

The container reaches the host's Ollama service through
`host.docker.internal` (configured via the `OLLAMA_URL` environment variable in
the `Dockerfile`). The backend is then available at `http://127.0.0.1:8000`,
and the Streamlit frontend can be run on the host as usual.

---

## 9. API Endpoints

### Home Endpoint

```http
GET /
```

Returns a simple message showing that the API is running.

---

### Health Check Endpoint

```http
GET /health
```

Example response:

```json
{
  "status": "ok",
  "service": "University Student Support Assistant",
  "timestamp": "2026-06-23T10:00:00"
}
```

---

### Ask Endpoint

```http
POST /ask
```

Example request body:

```json
{
  "question": "How can a student register for courses?"
}
```

Example response:

```json
{
  "question": "How can a student register for courses?",
  "answer": "To register for courses, log in to the university student portal..."
}
```

---

## 10. Testing

Make sure Ollama and FastAPI are running first.

Then run:

```bash
python tests/test_api.py
```

Expected output:

```text
Health status code: 200
Ask status code: 200
All API tests passed successfully.
```

---

## 11. Logging

The backend records:

* Received questions
* Generated answers
* Errors
* Timestamp of each interaction

Logs are saved in:

```text
backend/logs/app.log
```

Example log:

```text
2026-06-23 10:45:12 - INFO - Received question: How do I apply for hostel accommodation?
2026-06-23 10:45:20 - INFO - Generated answer: To apply for hostel accommodation...
2026-06-23 10:50:31 - ERROR - Model connection error: Local LLM is not running.
```

---

## 12. Error Handling

The system handles the following errors:

| Situation              | Expected Behaviour                           |
| ---------------------- | -------------------------------------------- |
| Backend is not running | Frontend shows connection error              |
| Model is not running   | Backend returns clear model connection error |
| Empty question         | Frontend asks user to enter a question       |
| Slow response          | Frontend shows loading spinner               |

---

## 13. Prompt Improvement

### Original Prompt

```text
Answer the student question clearly.

Student question:
{question}
```

### Improved Prompt

```text
You are a University Student Support Assistant.

Answer only questions related to university student services such as:
- course registration
- examination rules
- library services
- ICT support
- hostel application
- fee payment
- academic calendar
- student conduct

Use simple, clear, and professional language.
If the question is outside university student support, politely say you can only help with university support topics.

Student question:
{question}
```

The improved prompt gives the model a clear role, limits the scope, improves answer quality, and prevents irrelevant responses.

---

## 14. Bonus Feature: Response Evaluation

A response rating feature was added.

After receiving an answer, the user can rate the response as:

* Good
* Average
* Poor

The feedback is saved in:

```text
feedback/feedback.txt
```

Example:

```text
Question: How do students pay tuition fees?
Answer: Students can pay tuition fees through the university payment system...
Rating: Good
--------------------------------------------------
```

---

## 15. Screenshots Required

Screenshots should be saved in:

```text
docs/screenshots/
```

Captured screenshots (in `docs/screenshots/`):

```text
task1-virtual environment screenshoot.png
task1-installed librabries screenshot.png
task2-model pulled.png
task2-model running.png
task2-confirmed local model exists.png
task2-API-response.png
task3-fastapi running screenshot.png
task3-swagger docs.png
task3-health response.png
task3-ask response.png
task4-frontend page.png
task4-generating response.png
task4-uestion answer.png
task5-test script output.png
task6-before prompt improvement.png
task6-after prompt improvement.png
task7-backend not running error.png
task7-model not running.png
task7-empty question.png
task7-slow response loading.png
task8-logs captured.png
task9-bonus feedback UI.png
task9-bonus feedback saved.png
task9-bonus feedback log.png
```

---

## 16. Production Reflection

In a real production environment, this system would need improvements such as:

* Authentication and authorization
* HTTPS
* Secure logging
* Input validation
* Rate limiting
* Monitoring
* Database storage
* Better frontend design
* Docker deployment
* Server hosting
* Data privacy protection
* Backup and recovery plan

---

---

## 17. How to Contribute

Group members should follow this process:

```bash
git pull
git checkout -b feature-name
```

After making changes:

```bash
git add .
git commit -m "Describe the change made"
git push origin feature-name
```

Then create a Pull Request on GitHub.

---

## 18. Final Deliverables

The final submission should include:

1. Complete source code folder or GitHub repository link
2. README.md
3. Screenshots
4. Technical report PDF
5. Reflection answers
6. Bonus feature evidence

---

## 19. Conclusion

This project demonstrates a complete self-hosted LLM application pipeline. It shows how a user interface, backend API, local LLM server, testing, logging, error handling, and documentation work together to form an AI application system.
