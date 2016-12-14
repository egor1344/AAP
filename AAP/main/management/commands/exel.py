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

        apartments = Apartment.objects.all().filter(city__icontains='Уфа',
         price__gt=1000000, price__lt=10000000)
        ws.append(['Название', 'Цена', 'Цена за кв. м.', 'Город', 'Сайт',
         'Адресс', 'Этаж', 'Жилая площадь', 'Количество квартир', "Район",
          "Тип здания", "Код района", "Этажность"])
        for i in apartments:
            cod = ''
            adr = str(i.address)
            adr = adr.lower()
            dist = str(i.district)
            dist = dist.lower()
            floor = str(i.floor)
            floor = floor.split('/')
            print(floor)
            if (len(floor) == 2):
                if (int(floor[0]) == int(floor[1])):
                    floor = 1
                else:
                    floor = 0
            else:
                floor = 0
            if (adr.find('ленинский') >= 0 ) or (dist.find('ленинский')>= 0 ):
                cod = '00000'
            elif (adr.find('кировский') >= 0 ) or (dist.find('кировский')>= 0 ):
                cod = '00001'
            elif (adr.find('орджоникидзевский') >= 0 ) or (dist.find('орджоникидзевский')>= 0 ):
                cod = '00010'
            elif (adr.find('калининский') >= 0 ) or (dist.find('калининский')>= 0 ):
                cod = '00100'
            elif (adr.find('советский') >= 0 ) or (dist.find('советский')>= 0 ):
                cod = '01000'
            elif (adr.find('октябрьский') >= 0 ) or (dist.find('октябрьский')>= 0 ):
                cod = '10000'

            ws.append([i.title, i.price, i.price_m2, 
             i.city, i.site, i.address, i.floor,
             i.living_space, i.rooms, i.district, i.type_house, cod, floor])


        wb.save('test.xlsx')