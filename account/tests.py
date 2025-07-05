from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status


class AuthenticationTestCase(APITestCase):
    
    def setUp(self):
        self.register_url = reverse('signup-list')
        self.login_url = reverse('login-list')
        self.refresh_url = reverse('refresh-list')
        
        self.valid_user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "TestPass123!",
            "confirm_password": "TestPass123!"
        }
        
        self.valid_login_data = {
            "username": "testuser",
            "password": "TestPass123!"
        }

    def test_user_registration_valid_data(self):
        response = self.client.post(self.register_url, self.valid_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_user_registration_duplicate_username(self):
        User.objects.create_user(username="testuser", password="TestPass123!")
        response = self.client.post(self.register_url, self.valid_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_duplicate_email(self):
        User.objects.create_user(username="existinguser", email="testuser@example.com", password="TestPass123!")
        response = self.client.post(self.register_url, self.valid_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_valid_credentials(self):
        User.objects.create_user(username="testuser", email="testuser@example.com", password="TestPass123!")
        response = self.client.post(self.login_url, self.valid_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("user", response.data)
        self.assertIn("tokens", response.data["user"])

    def test_user_login_invalid_credentials(self):
        response = self.client.post(self.login_url, {"username": "nonexistent", "password": "wrongpass"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_refresh_functionality(self):
        User.objects.create_user(username="testuser", email="testuser@example.com", password="TestPass123!")
        login_response = self.client.post(self.login_url, self.valid_login_data, format='json')
        refresh_token = login_response.data["user"]["tokens"]["refresh"]
        
        response = self.client.post(self.refresh_url, {"refresh": refresh_token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_access_protected_endpoint_with_token(self):
        User.objects.create_user(username="testuser", email="testuser@example.com", password="TestPass123!")
        login_response = self.client.post(self.login_url, self.valid_login_data, format='json')
        access_token = login_response.data["user"]["tokens"]["access"]
        
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.get('/api/expenses/')
        self.assertNotEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_protected_endpoint_without_token(self):
        response = self.client.get('/api/expenses/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)