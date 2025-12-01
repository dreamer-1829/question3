from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import WeightEntry
from datetime import date

class WeightAppTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
    
    def test_signup(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!'
        })
        self.assertEqual(response.status_code, 302)  # should redirect
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_logout(self):
        login = self.client.login(username='testuser', password='testpass')
        self.assertTrue(login)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # redirect after logout

    def test_add_weight(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('add_weight'), {'weight': 70})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(WeightEntry.objects.filter(user=self.user, weight=70).exists())

    def test_list_weights(self):
        WeightEntry.objects.create(user=self.user, weight=70, date=date.today())
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('list_weights'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "70")
