from django.db import models
from django.contrib.auth.models import AbstractUser
from universearch.models import City


class CustomUser(AbstractUser):
    GENDER_CHOICES = (
        ('чол', 'чоловіча'),
        ('жін', 'жіноча'),
        ('н.в.', 'не визначено')
    )

    gender = models.CharField(choices=GENDER_CHOICES, default='н.в.', max_length=9)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name='users', blank=True)
    phone = models.CharField(blank=True, default='', max_length=12)
    email = models.EmailField(unique=True)
    deletion_request_date = models.DateTimeField(null=True)
