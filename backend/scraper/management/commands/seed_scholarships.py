"""
Management command to seed 500 scholarships
"""
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
import random
from scholarships.models import Scholarship
from scraper.scrapers import scrape_mock_scholarships


class Command(BaseCommand):
    help = 'Seed database with 500 scholarships'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=500,
            help='Number of scholarships to create',
        )
        parser.add_argument(
            '--no-approve',
            action='store_true',
            default=False,
            help='Do NOT auto-approve scholarships (by default they are approved)',
        )

    def handle(self, *args, **options):
        count = options['count']
        auto_approve = not options['no_approve']
        
        self.stdout.write(f'Creating {count} scholarships...')
        
        # Categories and templates
        categories = {
            'STEM': ['Data Science', 'Engineering', 'Computer Science', 'Mathematics', 'Physics', 'Chemistry'],
            'Business': ['MBA', 'Finance', 'Marketing', 'Management', 'Entrepreneurship'],
            'Arts': ['Fine Arts', 'Music', 'Literature', 'Design', 'Film'],
            'Healthcare': ['Medicine', 'Nursing', 'Public Health', 'Pharmacy'],
            'Education': ['Teaching', 'Educational Leadership', 'Curriculum Development'],
            'Social': ['Social Work', 'Psychology', 'Sociology', 'International Relations'],
        }
        
        countries = [
            'United States', 'Canada', 'Australia', 'United Kingdom', 
            'Germany', 'France', 'Netherlands', 'Sweden', 'Switzerland', 'Japan'
        ]
        
        organizations = [
            'International Education Foundation', 'Global Scholarship Network',
            'Academic Excellence Council', 'Future Leaders Program',
            'World Education Initiative', 'Merit Scholarship Foundation',
            'International Student Support', 'Academic Achievement Society',
            'Global Talent Development', 'Educational Opportunity Fund'
        ]
        
        created = 0
        for i in range(count):
            # Select random category and field
            category = random.choice(list(categories.keys()))
            field = random.choice(categories[category])
            
            # Generate scholarship data
            title = f"{field} Excellence Scholarship {i+1}"
            organization = random.choice(organizations)
            country = random.choice(countries)
            
            # Random deadline (30-730 days from now)
            days_ahead = random.randint(30, 730)
            deadline = (datetime.now() + timedelta(days=days_ahead)).date()
            
            # Random funding amount
            amount = random.choice([
                f"${random.randint(5000, 10000):,}",
                f"${random.randint(10000, 25000):,}",
                f"${random.randint(25000, 50000):,}",
                "Full tuition coverage",
                "Partial funding available"
            ])
            
            # Create scholarship
            scholarship = Scholarship.objects.create(
                title=title,
                organization=organization,
                description=f"Merit-based scholarship for outstanding students pursuing {field} studies. This scholarship aims to support talented individuals in their academic journey.",
                eligibility=f"GPA 3.0+, relevant field of study, international students welcome. Additional requirements may apply.",
                deadline=deadline,
                country=country,
                funding_amount=amount,
                link=f"https://example.com/scholarship/{i+1}",
                source_url="https://example.com/scholarships",
                is_approved=auto_approve,
                is_active=True,
            )
            created += 1
            
            if (i + 1) % 50 == 0:
                self.stdout.write(f'Created {i + 1} scholarships...')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created} scholarships')
        )

