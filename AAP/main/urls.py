from django.conf.urls import url, include
from .views import ApartmetnsListView
 
urlpatterns = [
    url(r'^$', ApartmetnsListView.as_view(), name='apartment_list'),
]