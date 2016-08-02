from django.db import models

class Apartment(models.Model):
    title = models.CharField(max_length=250)
    link = models.URLField(max_length=300, db_index=True)
    price = models.IntegerField()
    date_time = models.DateTimeField()
    city = models.CharField(max_length=50)
    agent = models.CharField(max_length=300, blank=True)
    site = models.CharField(max_length=30)
    address = models.CharField(max_length=50)

