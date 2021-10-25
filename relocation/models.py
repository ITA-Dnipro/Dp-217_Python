from django.db import models
from universearch.models import Region, City, University


class Housing(models.Model):
    TYPE_CHOICES = (
        (0, 'гуртожиток'),
        (1, 'готель'),
        (2, 'орендована квартира'),
        (3, 'хостел'),
    )
    name = models.CharField(max_length=50, verbose_name='назва', )
    type = models.IntegerField(choices=TYPE_CHOICES, verbose_name='тип', )
    city = models.ForeignKey(City, models.CASCADE, related_name='hostels',
                             verbose_name='місто', )
    university = models.ForeignKey(University, models.SET_NULL, blank=True,
                                   related_name='hostels',
                                   null=True, verbose_name='ВУЗ', )

    class Meta:
        verbose_name = 'житло'
        verbose_name_plural = 'житла'
