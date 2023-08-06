from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class TestRegisterView(TestCase):
    def setUp(self) -> None:
        self.register_url = reverse('register')
        self.login_url = reverse('login')

        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }

    def test_register_view(self):
        self.assertEqual(User.objects.count(), 0)

        response = self.client.post(self.register_url, data=self.user_data)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(User.objects.count(), 1)

        user = User.objects.first()

        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@example.com')

        self.assertRedirects(response, self.login_url, status_code=302, target_status_code=200)
