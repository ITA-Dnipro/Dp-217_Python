from django.db import models


class StudyField(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class Speciality(models.Model):
    name = models.CharField(max_length=200)
    study_field = models.ForeignKey(StudyField, on_delete=models.CASCADE, related_name='specialities')

    def __str__(self):
        return f"{self.name}"


class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class City(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='cities')

    def __str__(self):
        return f"{self.name}"


class University(models.Model):
    name = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='universities')
    specialities = models.ManyToManyField(Speciality, related_name='universities')

    def __str__(self):
        return f"{self.name}"
