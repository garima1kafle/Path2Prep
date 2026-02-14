"""
Celery tasks for scholarship scraping
"""
from celery import shared_task
from datetime import datetime, timedelta
from .scrapers import scrape_mock_scholarships, ScholarshipScraper
from .models import ScrapingLog
from scholarships.models import Scholarship
import random


@shared_task
def scrape_scholarships():
    """
    Daily task to scrape scholarships
    """
    log = ScrapingLog.objects.create(
        source_url="https://example.com/scholarships",
        status='success',
        started_at=datetime.now()
    )
    
    try:
        records_new = 0
        records_duplicate = 0
        
        # For now, use mock data generator
        # In production, this would call actual scrapers
        mock_scholarships = scrape_mock_scholarships()
        
        for scholarship_data in mock_scholarships:
            # Check for duplicates
            if Scholarship.objects.filter(
                title=scholarship_data['title']
            ).exists() or Scholarship.objects.filter(
                link=scholarship_data['link']
            ).exists():
                records_duplicate += 1
                continue
            
            # Set random deadline (30-365 days from now)
            days_ahead = random.randint(30, 365)
            scholarship_data['deadline'] = (datetime.now() + timedelta(days=days_ahead)).date()
            
            # Create scholarship (not approved by default)
            Scholarship.objects.create(
                title=scholarship_data['title'],
                organization=scholarship_data['organization'],
                description=scholarship_data['description'],
                eligibility=scholarship_data['eligibility'],
                deadline=scholarship_data['deadline'],
                country=scholarship_data['country'],
                funding_amount=scholarship_data['funding_amount'],
                link=scholarship_data['link'],
                source_url=scholarship_data['source_url'],
                is_approved=False,  # Requires admin approval
                is_active=True,
                mongo_id=scholarship_data.get('mongo_id', '')
            )
            records_new += 1
        
        log.status = 'success'
        log.records_scraped = len(mock_scholarships)
        log.records_new = records_new
        log.records_duplicate = records_duplicate
        log.completed_at = datetime.now()
        log.save()
        
        return f"Scraped {records_new} new scholarships, {records_duplicate} duplicates"
    
    except Exception as e:
        log.status = 'failed'
        log.error_message = str(e)
        log.completed_at = datetime.now()
        log.save()
        raise


@shared_task
def scrape_specific_url(url):
    """Scrape a specific scholarship URL"""
    scraper = ScholarshipScraper()
    result = scraper.scrape_scholarship(url)
    
    if result and not scraper._check_duplicate(result['title'], result.get('link')):
        Scholarship.objects.create(
            title=result['title'],
            description=result['description'],
            link=result.get('link', ''),
            source_url=result['source_url'],
            is_approved=False,
            is_active=True,
            mongo_id=result.get('mongo_id', '')
        )
        return f"Successfully scraped: {result['title']}"
    return "Scholarship already exists or scraping failed"

