from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Profile

User = get_user_model()


class ProfileTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_profile(self):
        """Test creating a user profile"""
        profile_data = {
            'gpa': 3.5,
            'degree_level': "Bachelor's",
            'major': 'Computer Science',
            'country': 'USA',
            'target_country': 'Canada',
        }
        response = self.client.post('/api/profiles/profiles/', profile_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Profile.objects.count(), 1)

    def test_get_profile(self):
        """Test getting user profile"""
        Profile.objects.create(
            user=self.user,
            gpa=3.5,
            degree_level="Bachelor's",
            major='Computer Science'
        )
        response = self.client.get('/api/profiles/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['gpa'], '3.50')
