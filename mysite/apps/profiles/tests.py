from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import UserProfile
from django.urls import reverse

User = get_user_model()

class UserProfileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_user_profile_creation(self):
        profile = UserProfile.objects.create(user=self.user, bio='Test bio')
        self.assertEqual(profile.user.username, 'testuser')
        self.assertEqual(profile.bio, 'Test bio')

class ProfileViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.profile = UserProfile.objects.create(user=self.user)

    def test_profile_view_accessible(self):
        response = self.client.get(reverse('profiles:profile_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')

    def test_profile_edit_view_post_success(self):
        response = self.client.post(reverse('profiles:profile_edit'), {'bio': 'Updated bio'})
        self.assertEqual(response.status_code, 200)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.bio, 'Updated bio')
