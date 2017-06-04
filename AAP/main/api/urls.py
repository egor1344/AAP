from django.conf.urls import url, include
from .views import ApartmentsViewSet, ApartmentDetail

urlpatterns = [
    url(r'^apartments/$', ApartmentsViewSet.as_view(), name='api_apartment_list'),
    url(r'^apartments/(?P<id>[0-9]+)/$', ApartmentDetail.as_view(), name='api_apartment_detail'),
]
