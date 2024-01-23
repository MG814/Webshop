from django.test import TestCase
from django.urls import reverse
from django.test import tag
from users.models import User, Profile


@tag("authentication")
class TestRegisterView(TestCase):
    def setUp(self) -> None:
        self.register_url = reverse("register")
        self.login_url = reverse("login")

        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password1": "testpassword123",
            "password2": "testpassword123",
            'role': 'Seller',
        }

        self.user_data_login = {
            "username": "testuser",
            "password": "testpassword123",
        }

    def test_register_view(self):
        self.assertEqual(User.objects.count(), 0)

        response = self.client.post(reverse("register"), data=self.user_data)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(User.objects.count(), 1)

        user = User.objects.first()

        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "testuser@example.com")

        self.assertRedirects(
            response, self.login_url, status_code=302, target_status_code=200
        )

    def test_login_view(self):
        self.client.post(self.register_url, data=self.user_data)
        response = self.client.get(self.login_url)
        self.assertContains(response, "You have been successfully signed up!")

        response = self.client.post(
            self.login_url, {"username": "testuser", "password": "testpassword123"}
        )
        self.assertEqual(response.status_code, 302)

    def test_profile_view(self):
        profile_url = reverse("profile")
        self.client.post(self.register_url, data=self.user_data)
        response = self.client.post(profile_url, data={"username": "testuser"})
        self.assertEqual(response.status_code, 302)

        profile = Profile.objects.first()
        user = User.objects.first()
        self.assertEqual(user, profile.user)
