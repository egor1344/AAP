from main.models import Apartment
from django.db.models import Max, Avg, Min, StdDev, Sum, Variance
from django.core.management.base import BaseCommand, CommandError
from openpyxl import Workbook


class Command(BaseCommand):
    help = 'Analitic price aprtment'

    # def add_arguments(self, parser):
    #     parser.add_argument('pages', default=1, type=int)

    def handle(self, *args, **options):
        wb = Workbook()

        ws = wb.active

        ws.title = "Все обьявления по Уфе"

        apartments = Apartment.objects.filter(city__icontains='Уфа',
         price__gt=1000000, price__lt=10000000, living_space__gt=10).distinct('address')
        print('ufa all = ', apartments.count())
        ws.append(['name', 'price', 'price_for_metr', 'city', 'site',
         'adress', 'floor', 'living_space', 'count_room', "district",
          "type_house", "coef_floor", "f1",'f2','f3', 'f4', 'f5', 'f6',
          't1','t2','t3','t4'])
        j = 0
        for i in apartments:
            cod = []
            t_cod = []
            adr = str(i.address)
            adr = adr.lower()
            dist = str(i.district)
            dist = dist.lower()
            floor = str(i.floor)
            floor = floor.split('/')
            type_house = str(i.type_house)
            type_house = type_house.lower()
            # print(floor)
            if (len(floor) == 2):
                if (int(floor[0]) == int(floor[1])):
                    floor = 1
                else:
                    floor = 0
            else:
                floor = 0

            if (adr.find('калининский') >= 0 ) or (dist.find('калининский')>= 0 ):
                cod = [0,0,0,0,0,0]
            elif (adr.find('кировский') >= 0 ) or (dist.find('кировский')>= 0 ):
                cod = [0,0,0,0,0,1]
            elif (adr.find('орджоникидзевский') >= 0 ) or (dist.find('орджоникидзевский')>= 0 ):
                cod = [0,0,0,0,1,0]
            elif (adr.find('ленинский') >= 0 ) or (dist.find('ленинский')>= 0 ):
                cod = [0,0,0,1,0,0]
            elif (adr.find('советский') >= 0 ) or (dist.find('советский')>= 0 ):
                cod = [0,0,1,0,0,0]
            elif (adr.find('октябрьский') >= 0 ) or (dist.find('октябрьский')>= 0 ):
                cod = [0,1,0,0,0,0]
            elif (adr.find('дёмский') >= 0 ) or (dist.find('дёмский')>= 0 ):
                cod = [1,0,0,0,0,0]

            if (type_house.find('дер') >= 0):
                t_cod = [0,0,0,0]
            elif(type_house.find('бло') >= 0):
                t_cod = [0,0,0,1]
            elif(type_house.find('кир') >= 0):
                t_cod = [0,0,1,0]
            elif(type_house.find('мон') >= 0):
                t_cod = [0,1,0,0]                
            elif(type_house.find('пан') >= 0):
                t_cod = [1,0,0,0]

            if cod and t_cod:
                j+=1
                ws.append([i.title, i.price, i.price_m2, 
                 i.city, i.site, i.address, i.floor,
                 i.living_space, i.rooms, i.district, i.type_house, floor,
                 cod[0], cod[1], cod[2], cod[3], cod[4], cod[5],
                 t_cod[0],t_cod[1],t_cod[2],t_cod[3]])
        print('end count = ', j)
            

        wb.save('test.xlsx')