from django.contrib import admin
from .models import Apartment

class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'city')

admin.site.register(Apartment, ApartmentAdmin)