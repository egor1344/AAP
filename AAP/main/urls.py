from django.conf.urls import url, include
from .views import apartment_list, landing
 
urlpatterns = [
    url(r'^landing/$', landing, name='landing'),
    url(r'^list/$', apartment_list, name='apartment_list'),
    
]