from django.shortcuts import render
from django.views.generic import ListView
from .models import Apartment
from .serilializers import ApartmentSerializer
from rest_framework import viewsets

class ApartmentsViewSet(viewsets.ModelViewSet):
    """
    API for apartment
    """
    queryset = Apartment.objects.all().order_by('-date_time')
    serializer_class = ApartmentSerializer

# def apartment_list(request):
#     apartments = Apartment.objects.all()
#     return render(request,
#                   'main/pages/list.html',
#                   {'apartments': apartments})

class ApartmetnsListView(ListView):
    model = Apartment
    context_object_name = 'apartments'
    template_name = 'main/pages/list.html'