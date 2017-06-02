from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.landing, name='landing'),
    url(r'^list/$', views.apartment_list, name='apartment_list'),
    url(r'^list_apart/$', views.ApartmentList.as_view(), name='list_apart'),
    url(r'^list/(?P<id>[0-9]+)/$', views.apartmetn_detail, name='apartmetn_detail'),
    url(r'^analiz/$', views.analize, name='analize'),
]
