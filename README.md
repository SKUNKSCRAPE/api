<<<<<<< HEAD
# SkunkScrape API

FastAPI backend scaffold for:

- `POST /auth/login`
- `POST /jobs`
- `GET /jobs/{id}`
- `GET /results/{id}`

This repo is designed to sit behind:

- `https://skunkscrape.com` for the static frontend
- `https://api.skunkscrape.com` for the API

## What this includes

- FastAPI app with JWT authentication
- SQLite persistence via SQLAlchemy
- Bootstrap admin user from environment variables
- Job creation and status tracking
- Result retrieval endpoint
- Background job runner placeholder you can replace with the real SkunkScrape engine
- Dockerfile and `.env.example`
- Pytest smoke tests

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Open:

- `http://127.0.0.1:8000/docs`

## Default flow

1. `POST /auth/login` with form fields `username` and `password`
2. Use the returned bearer token
3. `POST /jobs` with a JSON payload
4. `GET /jobs/{id}` for state
5. `GET /results/{id}` for output

## Production notes

The included background runner is intentionally simple so the repo works immediately.
For real production workloads, replace `app/services/job_runner.py` with one of:

- Cloud Run Jobs
- Celery + Redis
- Cloud Tasks / Pub/Sub
- RQ / Dramatiq

The API contract stays the same.

## Suggested repo layout

```text
app/
  core/
  db/
  routers/
  schemas/
  services/
tests/
```
=======
# api
API endpoint
>>>>>>> 9283559212cb3f31a2478b2ef5e1871fdecedc79
