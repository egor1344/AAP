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

        ws.title = "Все обьявления"

        apartments = Apartment.objects.all()
        ws.append(['Название', 'Цена', 'Цена за кв. м.', 'Город', 'Сайт',
         'Адресс', 'Этаж', 'Жилая площадь', 'Количество квартир', "Район",
          "Тип здания", "Коэф. этажности"])
        k = 0
        for i in apartments:
            floor = str(i.floor)
            floor = floor.split('/')
            # print(floor)
            if (len(floor) == 2):
                if (int(floor[0]) == int(floor[1])):
                    floor = 1
                else:
                    floor = 0
            else:
                floor = 0
            k+=1
            print(k)
            ws.append([i.title, i.price, i.price_m2, 
             i.city, i.site, i.address, i.floor,
             i.living_space, i.rooms, i.district, i.type_house, floor])


        wb.save('all_house.xlsx')