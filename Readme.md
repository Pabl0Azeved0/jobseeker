# JobSeeker

JobSeeker is a modern, full-stack **Job Portal** designed to demonstrate proficiency in full-stack development, built with Python (Django REST) on the backend and React (TypeScript) on the frontend. It incorporates Elasticsearch for powerful search capabilities, Redis for caching and session management, and Docker for seamless containerization.

## 🚀 Tech Stack

### Backend
- **Python with Django REST Framework:** The backend is built using Python and Django REST framework to provide scalable, robust, and RESTful API services.
- **PostgreSQL Database:** Relational database management system used for storing job-related data.
- **Elasticsearch:** Provides powerful, real-time job search functionality.
- **Redis:** Used for caching and background task management with Celery.
- **JWT (JSON Web Token):** Provides secure, token-based authentication for API requests.
- **Celery:** Manages background tasks such as sending emails, job notifications, etc.
- **Docker & Docker Compose:** Ensures consistent environments for development, testing, and production.

### Frontend
- **React with TypeScript**: The frontend is built using React for a dynamic, modern UI and TypeScript for type safety.
- **Tailwind CSS** for styling & responsiveness
- **Redux Toolkit** for state management
- **React Query** for data fetching
- **Vite** as the build tool

## 📌 Key Features

- **User Authentication** (JWT)
- **Role-based Access:** Job Seekers, Recruiters, Admins
- **Advanced Job Search & Filtering:** Powered by Elasticsearch for searching jobs based on various criteria.
- **CV Upload and Management:** Allows users to upload and manage resumes.
- **Application Tracking System (ATS):** Job seekers can track their job applications.
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
