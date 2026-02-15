"""
Management command to seed the database with sample data for Path2Prep.
Creates careers, scholarships, and welcome notifications.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal


class Command(BaseCommand):
    help = 'Seeds the database with sample careers, scholarships, and notifications'

    def handle(self, *args, **options):
        self.seed_careers()
        self.seed_scholarships()
        self.seed_notifications()
        self.stdout.write(self.style.SUCCESS('\n[OK] Database seeded successfully!'))

    def seed_careers(self):
        from careers.models import Career

        careers_data = [
            {
                'name': 'Software Engineer',
                'description': 'Design, develop, and maintain software applications and systems. Work with programming languages, frameworks, and tools to solve complex problems.',
                'category': 'STEM',
                'required_skills': ['Python', 'JavaScript', 'Data Structures', 'Algorithms', 'Git', 'SQL'],
                'average_salary': Decimal('105000.00'),
                'growth_rate': 'High',
            },
            {
                'name': 'Data Scientist',
                'description': 'Analyze and interpret complex datasets using statistical methods and machine learning. Build predictive models and extract actionable insights.',
                'category': 'STEM',
                'required_skills': ['Python', 'R', 'Machine Learning', 'Statistics', 'SQL', 'Data Visualization'],
                'average_salary': Decimal('120000.00'),
                'growth_rate': 'High',
            },
            {
                'name': 'Business Analyst',
                'description': 'Bridge the gap between IT and business using data analytics to assess processes, determine requirements, and deliver data-driven recommendations.',
                'category': 'Business',
                'required_skills': ['Excel', 'SQL', 'Communication', 'Problem Solving', 'Data Analysis', 'Project Management'],
                'average_salary': Decimal('85000.00'),
                'growth_rate': 'Medium',
            },
            {
                'name': 'UX/UI Designer',
                'description': 'Create intuitive and visually appealing user interfaces. Conduct user research, create wireframes, prototypes, and design systems.',
                'category': 'Arts',
                'required_skills': ['Figma', 'User Research', 'Wireframing', 'Prototyping', 'Typography', 'Color Theory'],
                'average_salary': Decimal('90000.00'),
                'growth_rate': 'High',
            },
            {
                'name': 'Cybersecurity Analyst',
                'description': 'Protect organizations from cyber threats by monitoring networks, investigating breaches, and implementing security measures.',
                'category': 'STEM',
                'required_skills': ['Network Security', 'Penetration Testing', 'Linux', 'Firewalls', 'SIEM', 'Incident Response'],
                'average_salary': Decimal('100000.00'),
                'growth_rate': 'High',
            },
            {
                'name': 'Product Manager',
                'description': 'Lead cross-functional teams to define, build, and launch products. Prioritize features based on user needs and business goals.',
                'category': 'Business',
                'required_skills': ['Strategy', 'Communication', 'Agile', 'Data Analysis', 'Leadership', 'User Research'],
                'average_salary': Decimal('115000.00'),
                'growth_rate': 'High',
            },
            {
                'name': 'Financial Analyst',
                'description': 'Evaluate financial data and trends to guide investment decisions, budgeting, and forecasting for organizations.',
                'category': 'Business',
                'required_skills': ['Financial Modeling', 'Excel', 'Accounting', 'Statistics', 'Valuation', 'Communication'],
                'average_salary': Decimal('80000.00'),
                'growth_rate': 'Medium',
            },
            {
                'name': 'Machine Learning Engineer',
                'description': 'Design and deploy machine learning models at scale. Work on training pipelines, model optimization, and production inference systems.',
                'category': 'STEM',
                'required_skills': ['Python', 'TensorFlow', 'PyTorch', 'MLOps', 'Docker', 'Mathematics'],
                'average_salary': Decimal('130000.00'),
                'growth_rate': 'High',
            },
            {
                'name': 'Environmental Scientist',
                'description': 'Study environmental problems and develop solutions. Conduct field research, analyze data, and advise on environmental policy.',
                'category': 'Science',
                'required_skills': ['Research', 'GIS', 'Data Analysis', 'Environmental Law', 'Chemistry', 'Report Writing'],
                'average_salary': Decimal('72000.00'),
                'growth_rate': 'Medium',
            },
            {
                'name': 'Healthcare Administrator',
                'description': 'Plan, direct, and coordinate medical and health services in hospitals, clinics, or managed care organizations.',
                'category': 'Healthcare',
                'required_skills': ['Healthcare Policy', 'Management', 'Budgeting', 'Compliance', 'Communication', 'Leadership'],
                'average_salary': Decimal('95000.00'),
                'growth_rate': 'High',
            },
            {
                'name': 'Civil Engineer',
                'description': 'Design, build, and maintain infrastructure projects such as roads, bridges, water systems, and buildings.',
                'category': 'STEM',
                'required_skills': ['AutoCAD', 'Structural Analysis', 'Mathematics', 'Project Management', 'Environmental Engineering', 'Surveying'],
                'average_salary': Decimal('88000.00'),
                'growth_rate': 'Medium',
            },
            {
                'name': 'Marketing Manager',
                'description': 'Develop and execute marketing strategies to promote products and services. Manage campaigns, analyze market trends, and drive brand growth.',
                'category': 'Business',
                'required_skills': ['Digital Marketing', 'SEO', 'Content Strategy', 'Analytics', 'Social Media', 'Brand Management'],
                'average_salary': Decimal('92000.00'),
                'growth_rate': 'Medium',
            },
        ]

        created = 0
        for data in careers_data:
            _, was_created = Career.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            if was_created:
                created += 1

        self.stdout.write(f'  [OK] Careers: {created} created, {len(careers_data) - created} already existed')

    def seed_scholarships(self):
        from scholarships.models import Scholarship

        now = timezone.now()
        scholarships_data = [
            {
                'title': 'Fulbright Foreign Student Program',
                'organization': 'U.S. Department of State',
                'description': 'Full scholarship for graduate studies in the United States. Covers tuition, living expenses, airfare, and health insurance.',
                'eligibility': 'Open to graduate students from 155+ countries. Must have a bachelor\'s degree, strong academic record, and English proficiency.',
                'deadline': (now + timedelta(days=120)).date(),
                'country': 'USA',
                'funding_amount': 'Full Tuition + Living Expenses',
                'link': 'https://foreign.fulbrightonline.org/',
                'is_approved': True,
                'is_active': True,
            },
            {
                'title': 'Chevening Scholarships',
                'organization': 'UK Government',
                'description': 'Fully funded master\'s degree at any UK university. Covers tuition, monthly living allowance, travel costs, and arrival allowance.',
                'eligibility': 'Open to citizens of Chevening-eligible countries. Requires 2+ years work experience, bachelor\'s degree, and meeting English language requirements.',
                'deadline': (now + timedelta(days=90)).date(),
                'country': 'UK',
                'funding_amount': 'Full Tuition + £1,133/month',
                'link': 'https://www.chevening.org/',
                'is_approved': True,
                'is_active': True,
            },
            {
                'title': 'DAAD Scholarships',
                'organization': 'German Academic Exchange Service',
                'description': 'Scholarships for master\'s and PhD programs in Germany. Provides monthly stipend, travel allowance, and health insurance.',
                'eligibility': 'Open to international students. Must have excellent academic record and relevant bachelor\'s degree. German or English proficiency required.',
                'deadline': (now + timedelta(days=150)).date(),
                'country': 'Germany',
                'funding_amount': '€934/month + Tuition Waiver',
                'link': 'https://www.daad.de/en/',
                'is_approved': True,
                'is_active': True,
            },
            {
                'title': 'Erasmus Mundus Joint Masters',
                'organization': 'European Commission',
                'description': 'Study-abroad master\'s program across multiple European universities. Covers participation costs, travel, installation, and monthly allowance.',
                'eligibility': 'Open to students worldwide. Must hold a bachelor\'s degree. Program-specific requirements vary.',
                'deadline': (now + timedelta(days=180)).date(),
                'country': 'Europe',
                'funding_amount': '€1,400/month + Travel + Tuition',
                'link': 'https://erasmus-plus.ec.europa.eu/',
                'is_approved': True,
                'is_active': True,
            },
            {
                'title': 'Australia Awards Scholarships',
                'organization': 'Australian Government',
                'description': 'Full scholarships for undergraduate and postgraduate study at participating Australian institutions.',
                'eligibility': 'Citizens of participating countries in Asia, Pacific, Africa, and Middle East. Must meet academic and English requirements.',
                'deadline': (now + timedelta(days=200)).date(),
                'country': 'Australia',
                'funding_amount': 'Full Tuition + Living Allowance + Airfare',
                'link': 'https://www.australiaawards.gov.au/',
                'is_approved': True,
                'is_active': True,
            },
            {
                'title': 'Korean Government Scholarship (KGSP)',
                'organization': 'National Institute for International Education',
                'description': 'Full scholarship for undergraduate and graduate programs in South Korea. Includes Korean language training, tuition, living expenses, and airfare.',
                'eligibility': 'Open to citizens of countries with diplomatic relations with Korea. Must be under 40 for graduate and under 25 for undergraduate.',
                'deadline': (now + timedelta(days=100)).date(),
                'country': 'South Korea',
                'funding_amount': 'Full Tuition + ₩900,000/month',
                'link': 'https://www.studyinkorea.go.kr/',
                'is_approved': True,
                'is_active': True,
            },
            {
                'title': 'Swiss Government Excellence Scholarships',
                'organization': 'Swiss Confederation',
                'description': 'Research scholarships and PhD positions at Swiss universities. Monthly stipend and tuition waiver included.',
                'eligibility': 'Postgraduate researchers and PhD candidates. Must have a master\'s degree for research scholarships.',
                'deadline': (now + timedelta(days=160)).date(),
                'country': 'Switzerland',
                'funding_amount': 'CHF 1,920/month + Tuition',
                'link': 'https://www.sbfi.admin.ch/',
                'is_approved': True,
                'is_active': True,
            },
            {
                'title': 'Japanese Government (MEXT) Scholarship',
                'organization': 'Ministry of Education, Culture, Sports, Science and Technology',
                'description': 'Full scholarship for undergraduate, research, and graduate studies in Japan. Includes tuition, monthly allowance, and airfare.',
                'eligibility': 'Open to citizens of countries with diplomatic relations with Japan. Age and academic requirements vary by program type.',
                'deadline': (now + timedelta(days=130)).date(),
                'country': 'Japan',
                'funding_amount': 'Full Tuition + ¥143,000/month + Airfare',
                'link': 'https://www.mext.go.jp/',
                'is_approved': True,
                'is_active': True,
            },
            {
                'title': 'Gates Cambridge Scholarship',
                'organization': 'Bill and Melinda Gates Foundation',
                'description': 'Full-cost scholarship for postgraduate study at the University of Cambridge. One of the most prestigious scholarships worldwide.',
                'eligibility': 'Outstanding applicants from any country outside the UK. Must apply to and be admitted to Cambridge.',
                'deadline': (now + timedelta(days=110)).date(),
                'country': 'UK',
                'funding_amount': 'Full Tuition + £18,744/year + Airfare',
                'link': 'https://www.gatescambridge.org/',
                'is_approved': True,
                'is_active': True,
            },
            {
                'title': 'New Zealand Scholarships',
                'organization': 'New Zealand Government',
                'description': 'Scholarships for students from selected developing countries to study in New Zealand. Covers tuition, living, and travel.',
                'eligibility': 'Citizens of eligible developing countries. Must meet academic and English proficiency requirements.',
                'deadline': (now + timedelta(days=140)).date(),
                'country': 'New Zealand',
                'funding_amount': 'Full Tuition + NZ$491/week + Airfare',
                'link': 'https://www.nzscholarships.govt.nz/',
                'is_approved': True,
                'is_active': True,
            },
        ]

        created = 0
        for data in scholarships_data:
            _, was_created = Scholarship.objects.get_or_create(
                title=data['title'],
                defaults=data
            )
            if was_created:
                created += 1

        self.stdout.write(f'  [OK] Scholarships: {created} created, {len(scholarships_data) - created} already existed')

    def seed_notifications(self):
        """Create welcome notifications for all existing users"""
        from django.contrib.auth import get_user_model
        from notifications.models import Notification

        User = get_user_model()
        created = 0

        for user in User.objects.all():
            _, was_created = Notification.objects.get_or_create(
                user=user,
                notification_type='profile_incomplete',
                title='Complete Your Profile',
                defaults={
                    'message': 'Fill in your academic information, test scores, and skills to get personalized scholarship matches and career recommendations!',
                }
            )
            if was_created:
                created += 1

            _, was_created = Notification.objects.get_or_create(
                user=user,
                notification_type='new_match',
                title='New Scholarships Available!',
                defaults={
                    'message': 'We\'ve added new scholarships to our database. Check the Scholarships page to find matches for your profile!',
                }
            )
            if was_created:
                created += 1

        self.stdout.write(f'  [OK] Notifications: {created} created for {User.objects.count()} users')
