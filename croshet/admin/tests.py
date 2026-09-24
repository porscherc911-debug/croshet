from django.contrib.auth import get_user_model
from django.test import TestCase

from admin.models import Product


class SharedProductDataTests(TestCase):
    def test_products_api_returns_database_products(self):
        Product.objects.create(
            name='Shared Product',
            price=250,
            category='Bags',
            image_url='https://example.com/shared.jpg',
            description='Shared product from database',
        )

        response = self.client.get('/api/products/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['products'][0]['name'], 'Shared Product')

    def test_dashboard_add_action_persists_in_database(self):
        User = get_user_model()
        User.objects.create_superuser('admin', 'admin@example.com', 'secret123')
        self.client.login(username='admin', password='secret123')

        response = self.client.post(
            '/dashboard/',
            {
                'action': 'add',
                'name': 'Admin Added Product',
                'price': 310,
                'category': 'Accessories',
                'image_url': 'https://example.com/new.jpg',
                'description': 'Saved by admin',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Product.objects.filter(name='Admin Added Product').exists())

    def test_dashboard_requires_admin_login(self):
        response = self.client.get('/dashboard/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Admin Sign In')

    def test_admin_signup_creates_staff_user(self):
        response = self.client.post(
            '/dashboard/',
            {
                'auth_action': 'signup',
                'username': 'shopadmin',
                'password1': 'StrongPassword123',
                'password2': 'StrongPassword123',
            },
        )

        self.assertEqual(response.status_code, 302)
        user = get_user_model().objects.get(username='shopadmin')
        self.assertTrue(user.is_staff)

    def test_admin_can_logout_and_login_again(self):
        User = get_user_model()
        User.objects.create_user(
            username='loginadmin',
            password='StrongPassword123',
            is_staff=True,
        )

        login_response = self.client.post(
            '/dashboard/login/',
            {
                'auth_action': 'login',
                'username': 'loginadmin',
                'password': 'StrongPassword123',
            },
        )
        self.assertRedirects(login_response, '/dashboard/')
        self.assertContains(self.client.get('/dashboard/'), 'Admin Dashboard')

        logout_response = self.client.get('/dashboard/logout/')
        self.assertRedirects(logout_response, '/dashboard/login/')
        self.assertContains(self.client.get('/dashboard/'), 'Admin Sign In')
