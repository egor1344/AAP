from django.shortcuts import render
from django.views.generic import ListView
from .models import Apartment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .serilializers import ApartmentSerializer
from rest_framework import viewsets, generics
from django.db.models import Max, Avg, Min, StdDev, Sum, Variance
from rest_framework.views import APIView
from rest_framework.response import Response


class ApartmentList(APIView):
    def get(self, request, format=None):
        apartments = Apartment.objects.all().order_by('-date_time')[0]
        apart_serilize = ApartmentSerializer(apartments)
        return Response(apart_serilize.data)

class ApartmentsViewSet(viewsets.ModelViewSet):
    """
    API for apartment
    """
    queryset = Apartment.objects.all().order_by('-date_time')
    serializer_class = ApartmentSerializer


def apartment_list(request):
    apartments = Apartment.objects.all().order_by('-date_time')

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


def apartmetn_detail(request, id):
    apartment = Apartment.objects.get(id=id)
    return render(request,
                  'main/detail/apartment.html',
                  {'apartment': apartment})


def landing(request):
    return render(request,
                  'main/pages/landing.html',
                  )


def data(sql):
    count = sql.count()
    stddev_price = sql.aggregate(StdDev('price'))
    print('stddev_price')
    variab_price = sql.aggregate(Variance('price'))
    avg_price = sql.aggregate(Avg('price'))
    print('avg_price', avg_price)
    stddev_m = sql.aggregate(StdDev('price_m2'))
    svariab_m = sql.aggregate(Variance('price_m2'))
    avg_m = sql.aggregate(Avg('price_m2'))

    return [count, stddev_price['price__stddev'], variab_price['price__variance'],
            avg_price['price__avg'], stddev_m['price_m2__stddev'],
            svariab_m['price_m2__variance'], avg_m['price_m2__avg']]


def analize(request):
    dict_ufa = {}
    ufa = Apartment.objects.filter(
        city='Уфа', price__gt=1000000, price__lt=10000000)
    lenin = ufa.filter(district__icontains='Ленинский')
    dict_ufa['Ленинский'] = data(lenin)
    cir = ufa.filter(district__icontains='Кировский')
    dict_ufa['Кировский'] = data(cir)
    ordj = ufa.filter(district__icontains='Орджоникидзевский')
    dict_ufa['Орджоникидзевский'] = data(ordj)
    calin = ufa.filter(district__icontains='Калининский')
    dict_ufa['Калининский'] = data(calin)
    sovet = ufa.filter(district__icontains='Советский')
    dict_ufa['Советский'] = data(sovet)
    oktabr = ufa.filter(district__icontains='Октябрьский')
    dict_ufa['Октябрьский'] = data(oktabr)
    return render(request,
                  'main/detail/analiz.html',
                  {'dict_ufa': dict_ufa})
