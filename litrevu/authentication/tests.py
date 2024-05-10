from django.db import IntegrityError
from django.test import TestCase
from .models import User


class UserModelTest(TestCase):
    def test_create_user_without_username(self):
        """users can't be created without a valid username"""
        with self.assertRaises(TypeError):
            User.objects.create_user(password="password")

    def test_create_user_without_password(self):
        """users can't be created without a valid password"""
        with self.assertRaises(IntegrityError):
            new_user = User(username="username")
            new_user.save()
