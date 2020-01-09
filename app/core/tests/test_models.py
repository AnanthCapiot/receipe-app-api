from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating new user is successful!"""
        email = 'test@capiot.com'
        password = 'welcome@123'
        print('Running create user with email UTC')

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalised(self):
        """Test new user email normalised"""
        email = "test@LONDONAPPDEV.com"
        user = get_user_model().objects.create_user(email, 'test123')
        self.assertEquals(user.email, email.lower())

    def test_new_user_email_invalid(self):
        """Test new email when it is invalid """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_superuser(self):
        """Test creation of super user!"""
        user = get_user_model().objects.create_superuser(
            'admin@capiot.com', 'test123')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
