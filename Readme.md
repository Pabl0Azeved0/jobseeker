# JobSeeker

JobSeeker is a modern, full-stack **Job Portal** designed to demonstrate proficiency in full-stack development, built with Python (Django REST) on the backend and React (TypeScript) on the frontend. It incorporates Elasticsearch for powerful search capabilities, Redis for caching and session management, and Docker for seamless containerization.

## 🚀 Tech Stack

### Backend
- **Python** with Django REST Framework
- **PostgreSQL** Database
- **Elasticsearch** for advanced job search
- **Redis** for caching and task queuing (Celery)
- **JWT** for secure authentication
- **Celery** for background task processing
- **Docker & Docker Compose** for container orchestration

### Frontend
- **React** with TypeScript
- **Chakra UI** for modern responsive UI
- **Redux Toolkit** for state management
- **React Query** for data fetching
- **Vite** as the build tool

## 📌 Key Features

- **User Authentication** (JWT)
- **Role-based Access:** Job Seekers, Recruiters, Admins
- **Advanced Job Search & Filtering** powered by Elasticsearch
- **CV Upload and Management**
- **Application Tracking System (ATS)**
- **Email Notifications** with SMTP Gmail
- **Dockerized** for consistent dev and production environments

## 🐳 Docker Setup (Local Development)

To get started with local development, follow these steps:

### Step 1: Clone the Repository

```bash
git clone <repo-url>
cd jobseeker
```

### Step 2: Docker Compose

Build and run the entire project using Docker Compose:

```bash
docker compose up --build
```

- Backend runs at: `http://localhost:8000`
- Frontend runs at: `http://localhost:5173`

### Step 3: Access the applications

- **Backend (Django REST):** `http://localhost:8000`
- **Frontend (React):** `http://localhost:5173`

## 📁 Project Structure

```
jobseeker/
├── backend/
│   ├── Dockerfile
│   ├── jobseeker/ (Django Project)
│   ├── requirements.txt
│   └── manage.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   └── ui/
│   ├── App.tsx
│   ├── Dockerfile
│   ├── package.json
│   └── tsconfig.json
├── docker-compose.yml
└── README.md
```

## ✅ Commit Guidelines

We use clear commit messages following [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: Add feature X
fix: Correct bug Y
refactor: Refactor Z for improved readability
docs: Update documentation
```

## 📌 Next Steps & Roadmap

- Implement backend API endpoints (Jobs, Users, Applications).
- Elasticsearch integration for advanced job search.
- Frontend authentication and initial UI scaffolding.
