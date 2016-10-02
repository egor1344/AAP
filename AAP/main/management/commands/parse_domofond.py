from lxml import html
import logging
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from django.core.management.base import BaseCommand, CommandError
from main.models import Apartment

URL = 'http://www.domofond.ru/prodazha-kvartiry-bashkortostan-r41?SortOrder=Newest'
HOST = 'http://www.domofond.ru'

logger = logging.getLogger('parse_domofond')

class Command(BaseCommand):
    help = 'Parse apartments Domofond'

    def add_arguments(self, parser):
        parser.add_argument('pages', default=1, type=int)

    def handle(self, *args, **options):
        add_apartments = 0
        try:
            r = urlopen(URL)
        except URLError:
            self.stdout.write(self.style.SUCCESS('UrlError'))
        except HTTPError:
            self.stdout.write(self.style.SUCCESS('HttpError'))
        ht = r.read().decode('UTF-8')
        page = html.fromstring(ht)
        item_list = page.xpath('//div[@id="listingResults"][1]/*')
        item_list = item_list[:-4] # 24 обьявления на странице
        price_list = page.xpath('//*[@itemprop="price"]//text()')
        links = [l[0] for l in Apartment.objects.filter(
            site='Domofond').values_list('link')]
        for key, item in enumerate(item_list):
            link = HOST + item.xpath('//a[@itemprop="sameAs"]/@href')[key]
            if (link not in links):
                try:
                    page_in = urlopen(link)
                except URLError:
                    print("Address don't open = ", link)
                except HTTPError:
                    print("Address don't open = ", link)
                else:
                    page_in = page_in.read().decode('UTF-8')
                    page_in = html.fromstring(page_in)
                    # Парсинг названия обьявления
                    title = page_in.xpath('//div[@class="b-listing-details"]/h5[1]//text()')
                    try:
                        title = title[0]
                    except IndexError:
                        title = ''
                    self.stdout.write(self.style.SUCCESS('Title = {}'.format(title)))
                    # Парсинг цены
                    price = page_in.xpath('//li[strong="Цена:"]//text()')
                    try:
                        price = price[2]
                    except IndexError:
                        continue
                    else:
                        price = price.strip()[:-5]
                        price = price.replace('\xa0', '')
                        try:
                            price = int(price)
                        except ValueError:
                            price = 0

                    # Парсинг цены за квадрат
                    price_m2 = page_in.xpath('//li[strong="Цена за м²:"]//text()')
                    try:
                        price_m2 = price_m2[2]
                    except IndexError:
                        price_m2 = 0
                    else:
                        price_m2 = price_m2.strip()[:-5]
                        price_m2 = price_m2.replace('\xa0', '')
                        try:
                            price_m2 = float(price_m2)
                        except ValueError:
                            price_m2 = 0

                    # Парсинг адреса, района и города
                    address = page_in.xpath('//div[h5="Расположение "]/p//text()')
                    if (len(address) == 2):
                        district = address[1]
                        address = address[0]
                        city = address.split(',')
                        city = city[-2]
                    elif(len(address) == 1):
                        address = address[0]
                        city = address.split(',')
                        city = city[-2]
                        district = ''                    
                    # self.stdout.write(self.style.SUCCESS(
                    #     'City = {} , address = {} , district = {} '.
                    #     format(city,address,district)))

                    # Парсер типов домов
                    type_house = page_in.xpath('//li[strong="Материал здания:"]//text()')
                    try:
                        type_house = type_house[2]
                    except IndexError:
                        type_house = "Не указанно"
                    else:
                        type_house = type_house.strip()
                        type_house = type_house.replace('\xa0', '')

                    # Парсер этажей
                    floor = page_in.xpath('//li[strong="Этаж:"]//text()')
                    try:
                        floor = floor[2]
                    except IndexError:
                        floor = "Не указанно"
                    else:
                        floor = floor.strip()
                        floor = floor.replace('\xa0', '')
                    # self.stdout.write(self.style.SUCCESS('Floor = {}'.format(floor)))
                    
                    # Парсер площади квартиры
                    living_space = page_in.xpath('//li[strong="Площадь:"]//text()')
                    try:
                        living_space = living_space[2]
                    except IndexError:
                        living_space = "Не указанно"
                    else:
                        living_space = living_space.strip()
                        living_space = living_space.replace('\xa0', '')
                        try:
                            living_space = float(living_space[:-2])
                        except ValueError:
                            living_space = 0

                    # Парсер количества комнат
                    rooms = page_in.xpath('//li[strong="Комнаты:"]//text()')
                    try:
                        rooms = rooms[2]
                    except IndexError:
                        rooms = "Не указанно"
                    else:
                        rooms = rooms.strip()
                        rooms = rooms.replace('\xa0', '')
                        try:
                            rooms = int(rooms)
                        except ValueError:
                            rooms = 0
                    self.stdout.write(self.style.SUCCESS('Rooms = {}'.format(rooms)))
                    try:
                        a = Apartment.objects.create(
                                title=title,
                                link=link,
                                price=price,
                                price_m2=price_m2,
                                city=city,
                                agent='',
                                site='Domofond',
                                address=address,
                                living_space=living_space,
                                rooms=rooms,
                                floor=floor,
                                type_house=type_house,
                                district=district,
                                active=True,)
                        add_apartments = add_apartments + 1
                    except Apartment.DoesNotExist:
                        print('Apartmen dont create ', title)
            logger.info('Added apartments from site Domofond %s', add_apartments)
