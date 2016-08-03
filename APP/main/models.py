from django.db import models

class Apartment(models.Model):
    title = models.CharField(max_length=250)
    link = models.URLField(max_length=300, db_index=True)
    price = models.IntegerField(blank=True)
    price_m2 = models.IntegerField(blank=True)
    date_time = models.DateField(auto_now_add=True)
    city = models.CharField(max_length=50)
    agent = models.CharField(max_length=300, blank=True)
    site = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    floor = models.CharField(max_length=7, blank=True)
    living_space = models.FloatField(blank=True)
    rooms = models.IntegerField(blank=True)