from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.apartment_list, name='apartment_list'),
]