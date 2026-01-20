# CoverCraft AI Backend

A FastAPI-based backend for generating AI-powered cover letters.

## Features
- **Authentication**: JWT-based Register & Login.
- **Resume Parsing**: Extracts skills and experience (Stubbed).
- **Job Matching**: Matches resume against Job Description (Stubbed).
- **Generation**: Creates a tailored cover letter (Stubbed).

## Setup

1. **Create Virtual Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Server**:
   ```bash
   uvicorn app.main:app --reload
   ```
   Server runs at: `http://127.0.0.1:8000`

## API Documentation (Swagger UI)

Navigate to `http://127.0.0.1:8000/docs`.

### Authentication Flow
1. **Register**: `POST /auth/register`
2. **Login**: `POST /auth/login` (Returns `access_token`)
3. **Authorize**:
   - Click the **Authorize** button.
   - Paste the `access_token` into the **Value** field.
   - Click **Authorize**.

## Project Structure
- `app/api`: API Routes
- `app/auth`: Authentication logic
- `app/services`: Core logic (Parser, Matcher, Generator)
- `app/core`: Configuration & DB
- `app/models`: Database & Pydantic models
