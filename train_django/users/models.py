from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now

# чтоб пофиксить конфликт классов пользователя и приткнуть кастомный,
# надо удалить БД и загрузить из фикстур
# python manage.py loaddata products/fixtures/categories.json


class User(AbstractUser):
    image = models.ImageField(upload_to='products_images', blank=True)
    is_verified = models.BooleanField(default=False)


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f'EmailVerification for {self.user.email}'

    def send_verification_email(self):
        link = reverse('users:verify', kwargs={
            'username': self.user.username,
            'email': self.user.email,
            'code': self.code,
        })
        subject = f"Email Verification for {self.user.username}"
        message = f"To verify your email click the link below:\n{settings.DOMAIN_NAME + link}"

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            # fail_silently=False,
        )

    def is_expired(self):
        return True if now() >= self.expiration else False
