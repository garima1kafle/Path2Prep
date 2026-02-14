from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Scholarship, Application, Bookmark
from datetime import date, timedelta

User = get_user_model()


class ScholarshipTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.scholarship = Scholarship.objects.create(
            title='Test Scholarship',
            organization='Test Org',
            description='Test description',
            eligibility='GPA 3.0+',
            deadline=date.today() + timedelta(days=30),
            country='USA',
            funding_amount='$10,000',
            link='https://example.com',
            is_approved=True,
            is_active=True
        )

    def test_list_scholarships(self):
        """Test listing scholarships"""
        response = self.client.get('/api/scholarships/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_create_application(self):
        """Test creating a scholarship application"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/applications/', {
            'scholarship_id': self.scholarship.id,
            'status': 'not_started'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Application.objects.count(), 1)

    def test_create_bookmark(self):
        """Test creating a bookmark"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/bookmarks/', {
            'scholarship_id': self.scholarship.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Bookmark.objects.count(), 1)
