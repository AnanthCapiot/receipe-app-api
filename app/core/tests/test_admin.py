from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@londonappdev.com',
            password='test123'
        )

        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user1@londonappdev.com',
            password='test123',
            name='Regular user'
        )

    def test_get_listed_users(self):
        """Test users who are listed in list page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works!!"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)
        self.assertEquals(res.status_code, 200)

    def test_user_create_page(self):
        """Test user create page"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)
        self.assertEquals(res.status_code, 200)
