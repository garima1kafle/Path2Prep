# Deployment Guide

## Production Deployment

### Prerequisites
- Docker and Docker Compose installed
- Domain name (optional)
- SSL certificate (for HTTPS)

### Steps

1. **Clone and Configure**
```bash
git clone <repository-url>
cd Path2Prep
cp .env.example .env
```

2. **Update Environment Variables**
Edit `.env` with production values:
```env
DJANGO_ENV=production
SECRET_KEY=<strong-secret-key>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

DB_NAME=path2prep_prod
DB_USER=postgres
DB_PASSWORD=<strong-password>
DB_HOST=db

MONGODB_HOST=mongodb
MONGODB_PASSWORD=<strong-password>

CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

3. **Build and Deploy**
```bash
docker-compose up --build -d
```

4. **Run Migrations**
```bash
docker-compose exec backend python manage.py migrate
```

5. **Create Superuser**
```bash
docker-compose exec backend python manage.py createsuperuser
```

6. **Collect Static Files**
```bash
docker-compose exec backend python manage.py collectstatic --noinput
```

7. **Seed Initial Data (Optional)**
```bash
docker-compose exec backend python manage.py seed_scholarships --count 500 --approve
```

8. **Train ML Models (Optional)**
```bash
docker-compose exec backend python recommendations/train.py
```

### AWS Deployment

#### Using EC2 + RDS

1. **Launch EC2 Instance**
   - Ubuntu 22.04 LTS
   - t3.medium or larger
   - Security group: Allow ports 80, 443, 8000

2. **Set up RDS PostgreSQL**
   - Engine: PostgreSQL 15
   - Instance class: db.t3.micro (minimum)
   - Update `DB_HOST` in `.env` to RDS endpoint

3. **Set up ElastiCache Redis**
   - Update `CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND`

4. **Deploy Application**
   - SSH into EC2
   - Install Docker
   - Clone repository
   - Update `.env` with RDS and ElastiCache endpoints
   - Run `docker-compose up -d`

### Monitoring

- Set up CloudWatch for logs
- Monitor database connections
- Set up alerts for errors
- Monitor Celery task queue

### Backup

- Regular PostgreSQL backups
- MongoDB backups for raw data
- Environment variable backups

### Scaling

- Use load balancer for multiple backend instances
- Scale Celery workers based on queue size
- Use managed database services (RDS, DocumentDB)

