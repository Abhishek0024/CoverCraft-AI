# CoverCraft AI

CoverCraft AI is a powerful full-stack application designed to help users generate professional, tailored cover letters using Artificial Intelligence. By analyzing your resume and the specific job description, CoverCraft AI creates personalized cover letters to increase your chances of landing your dream job.

## 🚀 Features

*   **AI-Powered Generation**: Generates custom cover letters based on your profile and job description.
*   **User Authentication**: Secure Login and Registration system to manage your profile.
*   **Profile Management**: Store your professional details for quick access.
*   **Interactive UI**: A modern, responsive interface built with React and Framer Motion.
*   **Job Matching**: Match score analysis between your resume and the job description.

## 🛠️ Technology Stack

### Frontend
*   **React** (v19)
*   **Vite** (for fast build and development)
*   **TailwindCSS** (for styling)
*   **Framer Motion** (for smooth animations)
*   **React Router** (for navigation)
*   **Axios** (for API integration)

### Backend
*   **FastAPI** (High-performance Python web framework)
*   **Uvicorn** (ASGI server)
*   **SQLAlchemy** (ORM for database interactions)
*   **JWT** (JSON Web Tokens for secure authentication)

## 📦 Installation & Setup

Prerequisites:
*   Node.js & npm
*   Python (3.8+)

### 1. Backend Setup
Navigate to the backend directory and set up the Python environment.

```bash
cd backend
python -m venv .venv
# Activate Virtual Environment
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# Install Dependencies
pip install -r requirements.txt

# Run the Server
uvicorn app.main:app --reload
```
The backend server will run at `http://127.0.0.1:8000`.

### 2. Frontend Setup
Open a new terminal, navigate to the frontend directory, and start the development server.

```bash
cd frontend
npm install
npm run dev
```
The frontend application will run at `http://localhost:5173`.

## 🤝 Contributing
Contributions are welcome! Please fork the repository and create a pull request.

## 📄 License
This project is open-source and available under the MIT License.
