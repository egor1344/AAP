from django.shortcuts import render
from django.views.generic import ListView
from .models import Apartment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .serilializers import ApartmentSerializer
from rest_framework import viewsets

class ApartmentsViewSet(viewsets.ModelViewSet):
    """
    API for apartment
    """
    queryset = Apartment.objects.all().order_by('-date_time')
    serializer_class = ApartmentSerializer


def apartment_list(request):
    apartments = Apartment.objects.all()

    paginator = Paginator(apartments, 30)

    page = request.GET.get('page')
    try:
        apartments = paginator.page(page)
    except PageNotAnInteger:
        apartments = paginator.page(1)
    except EmptyPage:
        apartments = paginator.page(paginator.num_pages)
    return render(request,
                  'main/pages/list.html',
                  {'apartments': apartments})