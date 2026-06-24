# University Student Support Assistant

## Technical Report — Full-Stack Pipeline for Deploying a Self-Hosted LLM Application

**Course:** IS 365 — Practical Assignment
**Project:** University Student Support Assistant
**Repository structure:** backend / frontend / tests / docs

---

## 1. Introduction

This report documents the design, implementation, testing, and deployment preparation
of a self-hosted Large Language Model (LLM) application called the **University Student
Support Assistant**.

The aim of the project is not to build the most intelligent chatbot, but to demonstrate
a clear understanding of the **complete pipeline** required to deploy an LLM-based system,
similar to what is found in a real industry environment. The system connects a user-facing
frontend, an API backend, and a locally hosted language model into one working flow, and
adds the supporting components that a production system relies on: configuration, logging,
error handling, testing, and documentation.

The assistant runs entirely on local infrastructure. No data leaves the machine, and no
external paid API is required, which makes the system suitable for a privacy-sensitive
context such as a university.

---

## 2. System Use Case

The system is a **University Student Support Assistant** that helps students get quick
answers to common questions about university services, including:

- Course registration
- Examination rules
- Library services
- ICT support
- Hostel application
- Fee payment
- Academic calendar
- Student conduct

A student types a question into a simple web interface. The question is sent to the backend,
which forwards it to the local model with a guiding prompt, and the generated answer is
returned and displayed. The prompt restricts the model to university support topics so that
off-topic questions are politely declined.

---

## 3. Tools and Technologies Used

| Component            | Tool Used                            |
| -------------------- | ------------------------------------ |
| Operating System     | Windows (cross-platform compatible)  |
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

The direct dependencies are pinned in `requirements.txt`: `fastapi`, `uvicorn`,
`pydantic`, `requests`, and `streamlit`.

---

## 4. System Architecture

The system follows a layered request/response flow:

```text
User
 |
 v
Streamlit Frontend (frontend/app.py)
 |  HTTP POST /ask
 v
FastAPI Backend (backend/main.py)
 |  HTTP POST /api/generate
 v
Ollama Local LLM API (llama3.2:1b)
 |
 v
Generated Response
 |
 v
Frontend Output to User
```

Supporting components:

- **Configuration file** (`backend/config.py`) — central place for the model name,
  Ollama URL, application name, and log file path.
- **Logging** (`backend/logs/app.log`) — records questions, answers, errors, and timestamps.
- **Error handling** — both backend and frontend handle failure cases gracefully.
- **Testing script** (`tests/test_api.py`) — verifies the `/health` and `/ask` endpoints.
- **Documentation** — this report, the `README.md`, and screenshots in `docs/screenshots/`.

### Component responsibilities

- **Frontend (Streamlit):** collects the question, shows a loading spinner during processing,
  displays the answer, and lets the user rate the response (bonus feature).
- **Backend (FastAPI):** exposes `/`, `/health`, and `/ask` endpoints, validates input,
  calls the model client, logs every interaction, and translates failures into clear HTTP
  status codes.
- **LLM client (`backend/llm_client.py`):** builds the guiding prompt, calls the Ollama
  generate endpoint, and converts network failures into typed Python exceptions
  (`ConnectionError`, `TimeoutError`, `RuntimeError`).
- **Local LLM (Ollama + llama3.2:1b):** performs the actual text generation.

---

## 5. Implementation Steps

1. **Environment setup.** Created a Python virtual environment (`python -m venv venv`),
   activated it, and installed dependencies from `requirements.txt`.
2. **Local LLM setup.** Installed Ollama, pulled `llama3.2:1b` (`ollama pull llama3.2:1b`),
   and confirmed it serves on `http://localhost:11434`.
3. **Configuration.** Centralised settings in `backend/config.py` (Ollama URL, model name,
   application name, log file path).
4. **LLM client.** Implemented `ask_local_llm()` to build a scoped prompt and POST to the
   Ollama generate API with `stream=False` and a 60-second timeout.
5. **Backend API.** Built the FastAPI app with three endpoints (`/`, `/health`, `/ask`),
   a Pydantic request model, structured logging, and exception handling.
6. **Frontend.** Built a Streamlit interface with a question box, a submit button, a loading
   spinner, answer display, and a feedback rating widget.
7. **Testing.** Wrote a Python `requests`-based script to test `/health` and `/ask`.
8. **Logging and error handling.** Added file logging and mapped each failure type to a
   clear user-facing message and HTTP status code.
9. **Prompt improvement.** Replaced a minimal prompt with a role-scoped prompt that limits
   answers to university support topics.
10. **Documentation.** Wrote the README, captured screenshots, and produced this report.

### Key endpoint behaviour

- `GET /health` returns service status and an ISO timestamp.
- `POST /ask` strips the input; an empty question returns HTTP 400; a model connection
  failure returns 503; a timeout returns 504; any other error returns 500. Every request
  and response is logged.

---

## 6. Testing and Results

Testing was performed in three ways:

1. **Swagger UI** at `http://127.0.0.1:8000/docs` — used to manually issue `/ask` and
   `/health` requests and inspect responses.
2. **Browser / health check** — `GET /health` returns `{"status": "ok", ...}`.
3. **Automated script** — `python tests/test_api.py` checks that `/health` returns 200 with
   `status == "ok"`, and that `/ask` returns 200 with a non-empty `answer` field.

Expected output:

```text
Health status code: 200
Ask status code: 200
All API tests passed successfully.
```

Error-handling situations were verified manually and captured as screenshots
(see `docs/screenshots/`):

| Situation              | Expected Behaviour                           | Result |
| ---------------------- | -------------------------------------------- | ------ |
| Backend is not running | Frontend shows a connection error            | Pass   |
| Model is not running   | Backend returns a clear 503 error            | Pass   |
| Empty question         | Frontend asks the user to enter a question   | Pass   |
| Slow response          | Frontend shows a loading spinner             | Pass   |

---

## 7. Challenges Encountered

- **Log directory startup error.** Python's `logging.basicConfig` fails if the target
  directory does not exist. We resolved this by creating `backend/logs/` automatically at
  startup before configuring logging.
- **Dependency file encoding.** The initial `requirements.txt` was saved in an encoding
  that broke `pip install`. We regenerated it as clean UTF-8 with only the direct
  dependencies.
- **Model speed on a small machine.** The local model can be slow on first load. We added a
  60-second backend timeout and a 70-second frontend timeout, plus a loading spinner, so the
  user is never left with a frozen screen.
- **Keeping answers on topic.** The first prompt produced off-topic answers. A role-scoped
  prompt fixed this (see Section: Prompt Improvement below).

---

## Prompt Improvement

### Original prompt

```text
Answer the student question clearly.

Student question:
{question}
```

### Improved prompt

```text
Answer the student question clearly.

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
If the question is outside university student support, politely say you can only help
with university support topics.

Student question:
{question}
```

The improved prompt gives the model a clear role, restricts its scope to university support
topics, sets a tone (simple and professional), and instructs it to decline off-topic
questions. This produced more focused, relevant, and consistent answers.

---

## Bonus Extensions Implemented

Two optional extensions were added:

- **Option E — Response Evaluation.** After each answer, the user can rate it as Good,
  Average, or Poor. Ratings are appended to `feedback/feedback.txt` together with the
  question and answer.
- **Option C — Docker.** The backend is containerised with a `Dockerfile`. The image
  installs the dependencies, copies the backend source, and runs Uvicorn. The Ollama URL is
  configurable through the `OLLAMA_URL` environment variable so the container reaches the
  host's model server via `host.docker.internal`. Build and run instructions are in the
  README.

---

## 8. Production Readiness Discussion

The current system is a **prototype**: it runs on a single developer machine, with a
reload-enabled development server, no authentication, and plain-text local logging. Moving
to **production** would require:

- Authentication and authorisation (login or API keys).
- HTTPS / TLS termination.
- A production server setup (for example Uvicorn workers behind Gunicorn or a reverse proxy).
- Input validation and rate limiting to prevent abuse.
- Centralised, secured, and rotated logging.
- A database for storing interactions and feedback instead of flat files.
- Containerisation (Docker) for reproducible deployment.
- Monitoring, alerting, and health probes.
- A data-privacy and backup/recovery plan for student information.

---

## 9. Conclusion

This project demonstrates a complete self-hosted LLM application pipeline. It shows how a
user interface, an API backend, a locally hosted model, testing, logging, error handling,
and documentation work together to form a functioning AI application. The focus throughout
was understanding **how requests and responses move through the system** and **what would be
required to take the prototype to production**, rather than maximising the intelligence of the
model itself.

---

## Task 9: Industry Production Reflection

**1. What are the main components of your deployed LLM system?**
A Streamlit frontend, a FastAPI backend with `/`, `/health`, and `/ask` endpoints, a local
LLM client, the Ollama model server running `llama3.2:1b`, plus supporting components: a
configuration file, file-based logging, error handling, a test script, and documentation.

**2. Why is FastAPI useful in this pipeline?**
FastAPI provides a fast, lightweight way to build an HTTP API. It gives automatic request
validation through Pydantic models, automatic interactive documentation via Swagger UI at
`/docs`, clear HTTP status codes and exception handling, and good performance through its
ASGI/async foundation. This lets the frontend and the model communicate through a clean,
well-documented contract.

**3. What role does your chosen LLM model play?**
The model (`llama3.2:1b` served by Ollama) is the reasoning and text-generation engine. It
receives the scoped prompt plus the student's question and produces the natural-language
answer that is returned to the user. It is a small, lightweight model chosen so it can run
locally on a normal machine.

**4. What role does the frontend play?**
The frontend is the interaction layer. It collects the student's question, validates that it
is not empty, shows a loading spinner during processing, sends the request to the backend,
displays the returned answer, handles and explains errors, and collects a response rating
for feedback.

**5. What is the difference between running the model locally and using an external API?**
Running locally means the model executes on our own machine, so data never leaves the
organisation, there are no per-request costs, and there is no dependency on internet
connectivity or a third party. The trade-offs are limited compute, slower responses, and a
smaller/less capable model. An external API offers larger and more capable models with no
local hardware needed, but introduces ongoing costs, network dependency, data-privacy
concerns (data leaves the organisation), and rate limits.

**6. What security risks may exist if this system is deployed in an organisation?**
No authentication on the API; no HTTPS, so traffic could be intercepted; prompt-injection or
abuse of the open question field; denial of service from unlimited requests; sensitive
student questions written to plain-text logs; and exposure of the internal Ollama port if
the network is not segmented.

**7. What improvements would be needed before deploying this system in production?**
Add authentication and authorisation, enable HTTPS, run a production-grade server
configuration (workers behind a reverse proxy) instead of `--reload`, add input validation
and rate limiting, move logging and feedback to a secured database, containerise with Docker,
and add monitoring and health checks.

**8. How would you monitor the system in real-world use?**
Use the `/health` endpoint with an uptime/health-probe tool, collect structured logs and
metrics (request counts, error rates, response latency) in a central system, set up alerts
for high error rates or slow responses, and track model performance and user feedback
ratings over time.

**9. How would you protect sensitive student information?**
Authenticate users, encrypt data in transit (HTTPS) and at rest, minimise and anonymise what
is logged, restrict who can access logs and feedback, apply data-retention and deletion
policies, keep the model fully local so data never leaves the organisation, and follow
relevant data-protection regulations.

**10. What challenges did you face during implementation?**
Fixing a logging startup crash caused by a missing log directory, correcting a corrupted
`requirements.txt` encoding, handling slow model responses with timeouts and a spinner, and
improving the prompt so the model stayed on university-support topics.

---

## 10. Appendix: Screenshots and Code Snippets

Screenshots evidencing each task are stored in `docs/screenshots/`, covering: virtual
environment setup, installed libraries, model pulled and running, a successful model API
response, FastAPI running, Swagger `/docs`, `/health` and `/ask` responses, the frontend and
a question-and-answer interaction, the test script output, the error-handling situations, the
log file, and the bonus feedback feature.

Key code files: `backend/main.py` (API and logging), `backend/llm_client.py` (prompt and
model call), `backend/config.py` (configuration), `frontend/app.py` (frontend and feedback),
and `tests/test_api.py` (test script).
