from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.contrib.postgres.fields import ArrayField
from universearch.models import City


class CustomUser(AbstractUser):
    GENDER_CHOICES = (
        (_('чол'), _('чоловіча')),
        (_('жін'), _('жіноча')),
        (_('н.в.'), _('не визначено'))
    )

    phone_validator = RegexValidator(
        regex=r'^(\s*)?(\+)?([- _():=+]?\d[- _():=+]?){12}(\s*)?$',
        message=_("Введіть номер телефону в міжнародному форматі.")
    )

    gender = models.CharField(choices=GENDER_CHOICES, default='н.в.', max_length=9)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name='users', blank=True)
    phone = models.CharField(blank=True, max_length=37, validators=[phone_validator])
    email = models.EmailField(unique=True)
    deletion_request_date = models.DateTimeField(null=True)
    favourites = ArrayField(models.CharField(max_length=10, blank=True), default=list)
