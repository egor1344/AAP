from django.contrib import admin
from .models import Apartment, HistoryApartmentPrice

class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'city', 'date_time', 'site')

class ApartmentHistoryPriceAdmin(admin.ModelAdmin):
    list_display = ('titles', 'cytis',
                    'dates', 'prices_new','price')

    def titles(self, obj):
        return obj.apartment.title
    def cytis(self, obj):
        return obj.apartment.city
    def dates(self, obj):
        return obj.apartment.date_time
    def prices_new(self, obj):
        return obj.apartment.price

admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(HistoryApartmentPrice, ApartmentHistoryPriceAdmin)
