import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from accounts.models import User, CareerPreferences

class Command(BaseCommand):
    help = 'Import users from backend/data/users.csv (headers: full_name,age,interests,careers)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            help='Relative path to CSV file from project base (default: data/users.csv)',
            default='data/users.csv'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Validate rows and show summary without writing to DB'
        )

    def handle(self, *args, **options):
        rel_path = options['path']
        dry_run = options['dry_run']

        base_dir = getattr(settings, 'BASE_DIR', os.getcwd())
        csv_path = os.path.join(base_dir, rel_path)

        if not os.path.exists(csv_path):
            self.stderr.write(self.style.ERROR(f'CSV file not found: {csv_path}'))
            return

        created = 0
        skipped = 0
        line_no = 1
        problems = []

        with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            header = reader.fieldnames or []
            header_norm = [h.strip().lower() for h in header]
            if 'full_name' not in header_norm and 'fullname' not in header_norm:
                self.stderr.write(self.style.ERROR(f'CSV header must include "full_name". Found: {header}'))
                return

            for row in reader:
                line_no += 1
                row_normalized = { (k.strip().lower() if k else k): (v.strip() if v else '') for k,v in row.items() }

                full_name = row_normalized.get('full_name') or row_normalized.get('fullname') or ''
                age_raw = row_normalized.get('age') or ''
                interests_raw = row_normalized.get('interests') or ''
                careers_raw = row_normalized.get('careers') or ''

                if not full_name:
                    skipped += 1
                    problems.append(f'Line {line_no}: missing full_name - skipping')
                    continue

                # derive username and email (dev safe defaults)
                username = full_name.strip().lower().replace(' ', '_')
                email = f"{username}@local.test"
                password = 'ChangeMe123!'

                # parse age
                age = None
                if age_raw:
                    try:
                        age = int(age_raw)
                    except ValueError:
                        problems.append(f'Line {line_no}: invalid age "{age_raw}" - saved as blank')

                # parse semicolon separated lists into python lists, ignoring empty strings
                interests = [s.strip() for s in interests_raw.split(';') if s.strip()] if interests_raw else []
                careers = [s.strip() for s in careers_raw.split(';') if s.strip()] if careers_raw else []

                # skip if user already exists by email
                if User.objects.filter(email=email).exists():
                    skipped += 1
                    problems.append(f'Line {line_no}: user with email {email} already exists - skipped')
                    continue

                if dry_run:
                    created += 1
                    continue

                # create user and career preferences
                try:
                    user = User(username=username, email=email, full_name=full_name)
                    if age is not None:
                        user.age = age
                    user.set_password(password)
                    user.save()

                    # create or update career preferences
                    cp, _ = CareerPreferences.objects.get_or_create(user=user)
                    cp.career_interests = interests
                    cp.preferred_destinations = careers
                    cp.save()

                    created += 1
                except Exception as e:
                    skipped += 1
                    problems.append(f'Line {line_no}: exception creating user {email or username} — {e}')

        self.stdout.write(self.style.SUCCESS(f'Processed CSV: {csv_path}'))
        if dry_run:
            self.stdout.write(self.style.SUCCESS(f'Rows that WOULD be created: {created} (dry-run)'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Users created: {created}'))
        self.stdout.write(self.style.WARNING(f'Rows skipped: {skipped}'))
        if problems:
            self.stdout.write(self.style.NOTICE('Problems found:'))
            for p in problems:
                self.stdout.write(self.style.NOTICE(f' - {p}'))
