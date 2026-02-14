# Path2Prep - Scholarship Assistance System

A production-ready, AI-powered scholarship assistance system that provides career recommendations, NLP-based scholarship matching, and real-time scholarship data scraping.

## Features

- **AI Career Recommendations**: ML models (Random Forest, KNN, Neural Network) for personalized career suggestions
- **NLP Scholarship Matching**: TF-IDF + BERT embeddings for intelligent scholarship matching
- **Real-time Scraping**: Automated scholarship data collection with Celery
- **Secure Authentication**: JWT-based authentication with role-based access control
- **Student Dashboard**: Comprehensive dashboard with recommendations, matches, and application tracking
- **Notifications**: Real-time notifications for deadlines and new matches
- **Cloud-ready**: Dockerized deployment with PostgreSQL, MongoDB, and Redis

## Tech Stack

### Backend
- Django 5.2 + Django REST Framework
- PostgreSQL (structured data)
- MongoDB (raw scraped data)
- Celery + Redis (background tasks)
- JWT Authentication
- scikit-learn, TensorFlow, BERT for ML/NLP

### Frontend
- React 19 + TypeScript
- TailwindCSS
- Redux Toolkit
- Axios

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for local frontend development)

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd Path2Prep
```

2. Copy environment file:
```bash
cp .env.example .env
```

3. Build and start all services:
```bash
docker-compose up --build
```

4. Run database migrations:
```bash
docker-compose exec backend python manage.py migrate
```

5. Create superuser:
```bash
docker-compose exec backend python manage.py createsuperuser
```

6. Seed scholarships (optional):
```bash
docker-compose exec backend python manage.py seed_scholarships --count 500 --approve
```

7. Train ML models (optional):
```bash
docker-compose exec backend python manage.py shell
>>> from recommendations.train import main
>>> main()
```

### Access the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Admin Panel: http://localhost:8000/admin
- API Documentation: http://localhost:8000/api/

## Local Development

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install spaCy model:
```bash
python -m spacy download en_core_web_sm
```

5. Set up environment variables:
```bash
export DJANGO_ENV=development
export DB_NAME=path2prep
export DB_USER=postgres
export DB_PASSWORD=postgres
```

6. Run migrations:
```bash
python manage.py migrate
```

7. Create superuser:
```bash
python manage.py createsuperuser
```

8. Run development server:
```bash
python manage.py runserver
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd path2prep
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm start
```

## Project Structure

```
Path2Prep/
├── backend/
│   ├── accounts/          # Authentication & User management
│   ├── profiles/          # User profiles
│   ├── careers/           # Career models
│   ├── scholarships/      # Scholarship models & NLP matching
│   ├── recommendations/   # ML career recommendation engine
│   ├── notifications/     # Notification system
│   ├── scraper/           # Scholarship scraping
│   ├── data/              # ML datasets, seed data
│   └── path2prep_backend/ # Django project settings
├── path2prep/             # React frontend
│   ├── src/
│   │   ├── pages/         # Page components
│   │   ├── store/         # Redux store
│   │   ├── services/      # API services
│   │   └── types/         # TypeScript types
│   └── public/
├── docker-compose.yml     # Docker orchestration
└── README.md
```

## API Endpoints

### Authentication
- `POST /api/auth/login/` - Login
- `POST /api/auth/users/register/` - Register
- `POST /api/auth/users/logout/` - Logout
- `GET /api/auth/users/me/` - Get current user

### Profile
- `GET /api/profiles/me/` - Get profile
- `POST /api/profiles/profiles/` - Create profile
- `PATCH /api/profiles/profiles/` - Update profile

### Career Recommendations
- `POST /api/recommend-career/recommend/` - Get career recommendations
- `GET /api/recommend-career/my_recommendations/` - Get stored recommendations

### Scholarships
- `GET /api/scholarships/` - List scholarships
- `POST /api/scholarships/match/` - Match scholarships
- `GET /api/applications/` - List applications
- `POST /api/bookmarks/` - Create bookmark

### Notifications
- `GET /api/notifications/` - List notifications
- `POST /api/notifications/{id}/mark_read/` - Mark as read

## ML Model Training

To train the career recommendation models:

```bash
cd backend
python recommendations/train.py
```

This will:
1. Generate a mock dataset (1000 records)
2. Train Random Forest, KNN, and Neural Network models
3. Evaluate models with cross-validation
4. Save models to `ml_models/` directory

## Testing

Run backend tests:
```bash
cd backend
python manage.py test
```

Run frontend tests:
```bash
cd path2prep
npm test
```

## Production Deployment

1. Update `.env` with production values
2. Set `DJANGO_ENV=production`
3. Update `SECRET_KEY`, database credentials, and CORS settings
4. Build and deploy:
```bash
docker-compose -f docker-compose.yml up --build -d
```

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

