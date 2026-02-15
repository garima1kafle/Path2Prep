# Path2Prep — Developer Setup Guide

> Complete setup instructions for running the project locally on a new machine.

## Prerequisites

| Tool | Version | Check |
|------|---------|-------|
| **Python** | 3.10 – 3.13 | `python --version` |
| **Node.js** | 18+ | `node --version` |
| **npm** | 9+ | `npm --version` |
| **Git** | Any | `git --version` |

---

## 1. Clone the Repository

```bash
git clone <repo-url>
cd Path2Prep
```

---

## 2. Backend Setup

### 2.1 Create Virtual Environment

```bash
cd backend
python -m venv .venv
```

**Activate it:**

| OS | Command |
|----|---------|
| Windows (PowerShell) | `.venv\Scripts\Activate.ps1` |
| Windows (CMD) | `.venv\Scripts\activate.bat` |
| macOS / Linux | `source .venv/bin/activate` |

### 2.2 Install Dependencies

```bash
pip install -r requirements.txt
```

> **Note:** TensorFlow lines in `requirements.txt` may be commented out.
> If you're on Python 3.13+ or don't need ML features, leave them commented.
> The app has fallback logic that works without TensorFlow.

### 2.3 Run Migrations

```bash
python manage.py migrate
```

### 2.4 Create Superuser

```bash
python manage.py createsuperuser
```

### 2.5 Seed Sample Data

```bash
python manage.py seed_data
```

This creates **12 careers**, **10 international scholarships**, and **welcome notifications** for all users.

### 2.6 Start the Backend Server

```bash
python manage.py runserver
```

Backend runs at **http://localhost:8000**

Verify: open http://localhost:8000 → should return `{"message": "Path2Prep Backend API is running", "version": "1.0.0"}`

---

## 3. Frontend Setup

Open a **new terminal** (keep backend running):

```bash
cd path2prep
```

### 3.1 Install Dependencies

> **IMPORTANT:** You MUST use `--legacy-peer-deps`. The project uses React 19 with `react-scripts` 5, which has a peer dependency conflict with TypeScript 5. This flag is safe and required.

```bash
npm install --legacy-peer-deps
```

### 3.2 Create `.env` File

Create `path2prep/.env` if it doesn't exist:

```
GENERATE_SOURCEMAP=false
```

This prevents source-map resolution errors during build.

### 3.3 Start the Frontend

```bash
npm start
```

Frontend runs at **http://localhost:3000**

---

## 4. Verify Everything Works

1. Open **http://localhost:3000** in your browser
2. Click **Sign Up** → Create an account (use a strong password, 8+ chars, e.g. `TestPass123!`)
3. You'll be auto-logged-in and land on the **Dashboard**
4. Go to **Profile** → Fill in GPA, Degree Level, Major, Target Country
5. Go back to **Dashboard** → Click **"Get Recommendations"**
6. Check **Scholarships** page → Should show 10 scholarships

---

## Troubleshooting

### Frontend: `ENOENT` during `npm install`
Windows path length issue. Run in a shorter directory path (e.g. `C:\dev\Path2Prep`), or enable long paths:
```powershell
# Run as Administrator
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

### Frontend: `ajv` / `ajv-keywords` errors
If you see schema validation errors during build:
```bash
npm install ajv@6 ajv-keywords@3 --legacy-peer-deps
```

### Frontend: Provider error (`could not find react-redux context value`)
Make sure `src/index.js` does NOT exist. The correct entry point is `src/index.tsx` which wraps the app in the Redux `<Provider>`. If `index.js` exists alongside `index.tsx`, delete `index.js`.

### Backend: `ModuleNotFoundError` for tensorflow/keras
Safe to ignore. The ML engine falls back to rule-based recommendations when TensorFlow is not installed.

### Backend: `django-ratelimit-backend` install fails
```bash
pip install django-ratelimit-backend --no-deps
```

### General: CORS errors in browser console
The development settings (`CORS_ALLOW_ALL_ORIGINS = True`) should handle this. Make sure:
- Backend is running on port **8000**
- `DJANGO_ENV` environment variable is not set (defaults to `development`)

---

## Project Structure

```
Path2Prep/
├── backend/                    # Django REST API
│   ├── accounts/               # User auth, registration, JWT
│   ├── profiles/               # Student profiles (GPA, scores)
│   ├── careers/                # Career database
│   ├── scholarships/           # Scholarship data + NLP matching
│   ├── recommendations/        # ML career recommendation engine
│   ├── notifications/          # User notifications
│   └── path2prep_backend/      # Django settings & URLs
├── path2prep/                  # React frontend
│   ├── src/
│   │   ├── pages/              # Route components
│   │   ├── store/              # Redux slices
│   │   ├── services/           # API client (axios)
│   │   └── types/              # TypeScript interfaces
│   └── package.json
└── SETUP_DEV.md                # ← This file
```

---

## Quick Reference

| Action | Command | Directory |
|--------|---------|-----------|
| Start backend | `python manage.py runserver` | `backend/` |
| Start frontend | `npm start` | `path2prep/` |
| Run migrations | `python manage.py migrate` | `backend/` |
| Seed data | `python manage.py seed_data` | `backend/` |
| Create superuser | `python manage.py createsuperuser` | `backend/` |
| Install frontend deps | `npm install --legacy-peer-deps` | `path2prep/` |
| Build frontend | `npm run build` | `path2prep/` |
| Django admin | http://localhost:8000/admin/ | — |
| API root | http://localhost:8000/ | — |
| Frontend | http://localhost:3000/ | — |
