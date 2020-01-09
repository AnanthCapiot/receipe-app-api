from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

app_name = 'user'
CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


# -- helper function
def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserAPITest(TestCase):
    """Test User API public"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Create valid user creation is successful"""
        payload = {
            'email': 'test@londappdev.com',
            'password': '123123123',
            'name': 'testname'
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEquals(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Testing already existing user"""
        payload = {
            'email': 'test@londappdev.com',
            'password': '123123123',
            'name': 'testname'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_length(self):
        """Password must be more than 5 chars"""
        payload = {
            'email': 'test@londappdev.com',
            'password': '123',
            'name': 'testname'
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test a token is created for user"""
        payload = {
            'email': 'test@londappdev.com',
            'password': '123',
            'name': 'testname'
        }

        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_for_user_invalid_credentials(self):
        """Test token not created as invalid credentials are created"""
        create_user(email='test@londonappdev.com', password='123123123')
        payload = {'email':'test@londonappdev.com', 'password': 'wrongpass'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """"Test token not created if user does not exist"""
        payload = {'email': 'test@londonappdev.com', 'password': 'wrongpass'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_using_missing_field(self):
        """Test create token not created due to missing field"""
        payload = {'email':'test@londonappdev.com', 'password':''}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)