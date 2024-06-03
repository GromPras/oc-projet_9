from django.db import IntegrityError
from django.test import TestCase
from .models import User


class UserModelTest(TestCase):
    def test_user_model_exists(self):
        self.assertEqual(User.objects.count(), 0)

    def test_unauthenticated_user_redirected_to_signin_page(self):
        response = self.client.get("/reviews/feed")
        self.assertEqual(response.status_code, 301)
