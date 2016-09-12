from django.conf.urls import url, include
from .views import apartment_list
 
urlpatterns = [
    url(r'^list/$', apartment_list, name='apartment_list'),
]