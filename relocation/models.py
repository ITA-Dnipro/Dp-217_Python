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
    type = models.IntegerField(choices=TYPE_CHOICES, verbose_name='тип', default=0, )
    city = models.ForeignKey(City, models.CASCADE, related_name='hostels',
                             verbose_name='місто', )
    university = models.ForeignKey(University, models.SET_NULL, blank=True,
                                   related_name='hostels',
                                   null=True, verbose_name='ВУЗ', )
    address = models.CharField(max_length=50, verbose_name='адреса', default='', )
    phone = models.CharField(max_length=13, verbose_name='телефон', default='', )

    @property
    def belongs_to_uni(self):
        return bool(self.university)

    def __str__(self):
        return f'{self.name} {self.city.name}{(" " + self.university.name) if self.belongs_to_uni else ""}'

    class Meta:
        verbose_name = 'житло'
        verbose_name_plural = 'житла'
