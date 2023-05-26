from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from django.utils.timezone import now
from datetime import timedelta

from users.forms import UserRegistrationForm
from users.models import User, EmailVerification
# python manage.py test .


class UserRegistrationViewTestCase(TestCase):

    def setUp(self):
        self.path = reverse('users:signup')
        self.data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'john',
            'email': 'john@mail.ru',
            'password1': 'Asdfg1234',
            'password2': 'Asdfg1234',
        }

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Sign up')
        self.assertTemplateUsed(response, 'users/register.html')

    def test_user_registration_post_success(self):
        # check user creation
        user = User.objects.filter(username=self.data['username'])
        self.assertFalse(user.exists())

        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(user.exists())

        # check sending email
        email_v = EmailVerification.objects.filter(user__username=user.first().username)
        self.assertTrue(email_v.exists())
        self.assertTrue(
            email_v.first().expiration.date(),
            (now() + timedelta(hours=48)).date()
        )

    def test_user_registration_post_error(self):
        # check user creation
        User.objects.create(username=self.data['username'])
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'A user with that username already exists.', html=True)



