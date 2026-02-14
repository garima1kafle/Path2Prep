# Path2Prep Setup Instructions

## Complete Setup Checklist

### 1. Initial Setup
- [x] Backend foundation with PostgreSQL configuration
- [x] All Django apps created (profiles, careers, scholarships, recommendations, notifications, scraper)
- [x] Database models defined
- [x] JWT authentication implemented
- [x] ML career recommendation engine
- [x] NLP scholarship matching
- [x] Scholarship scraper with Celery
- [x] Frontend migrated to TypeScript
- [x] Redux Toolkit setup
- [x] Docker configuration
- [x] Documentation

### 2. First Time Setup

1. **Install Dependencies**
   ```bash
   # Backend
   cd backend
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   
   # Frontend
   cd ../path2prep
   npm install
   ```

2. **Set Up Databases**
   - PostgreSQL: Create database `path2prep`
   - MongoDB: No setup needed (auto-created)
   - Redis: No setup needed

3. **Run Migrations**
   ```bash
   cd backend
   python manage.py migrate
   ```

4. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

5. **Seed Data (Optional)**
   ```bash
   python manage.py seed_scholarships --count 500 --approve
   ```

6. **Train ML Models (Optional)**
   ```bash
   python recommendations/train.py
   ```

### 3. Running with Docker

```bash
# Build and start all services
docker-compose up --build

# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Seed scholarships
docker-compose exec backend python manage.py seed_scholarships --count 500 --approve
```

### 4. Access Points

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Admin Panel: http://localhost:8000/admin
- PostgreSQL: localhost:5432
- MongoDB: localhost:27017
- Redis: localhost:6379

### 5. Testing

```bash
# Backend tests
cd backend
python manage.py test

# Frontend tests
cd path2prep
npm test
```

### 6. Common Issues

**Issue: Models not loading**
- Solution: Run `python recommendations/train.py` to generate models

**Issue: spaCy model not found**
- Solution: Run `python -m spacy download en_core_web_sm`

**Issue: MongoDB connection error**
- Solution: Ensure MongoDB is running or use Docker Compose

**Issue: Celery tasks not running**
- Solution: Start Celery worker: `celery -A path2prep_backend worker --loglevel=info`

### 7. Production Checklist

- [ ] Update SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up SSL certificates
- [ ] Configure production database
- [ ] Set up email service
- [ ] Configure CORS properly
- [ ] Set up monitoring
- [ ] Configure backups
- [ ] Review security settings

## Next Steps

1. Complete user profile setup
2. Train ML models with real data
3. Configure actual scholarship scraping sources
4. Set up email notifications
5. Deploy to production

