from lxml import html
import json
import logging
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from django.core.management.base import BaseCommand, CommandError
from main.models import Apartment

URL = 'https://www.avito.ru/bashkortostan/kvartiry/prodam'
HOST = 'https://www.avito.ru'

logger = logging.getLogger('parse_avito')

class Command(BaseCommand):
    help = 'Parse apartments Avito'

    def add_arguments(self, parser):
        parser.add_argument('pages', default=1, type=int)

    def handle(self, *args, **options):
        add_apartments = 0
        r = urlopen(URL)
        ht = r.read().decode('UTF-8')
        page = html.fromstring(ht)
        item_list = page.xpath('//*[@class="description"]')
        print(len(item_list))
        price_list = page.xpath(
            '//*[@class="popup-prices popup-prices__wrapper clearfix"]/@data-prices')
        links = [l[0] for l in Apartment.objects.filter(
            site='Avito').values_list('link')]
        for key, item in enumerate(item_list):
            link = HOST + item.xpath(
                '//h3[@class="title item-description-title"]/a/@href'
            )[key]
            if link not in links:
                # print('+'*20)
                title = item.xpath(
                    '//h3[@class="title item-description-title"]/a//text()'
                )[key]
                # print('Title = ', title)
                rooms, living_space, floor = title.strip().split(',')
                # print('rooms = ', rooms, ' living_space = ', living_space, ' floor = ', floor)
                living_space = living_space[:-3]
                living_space = living_space.strip()
                living_space = float(living_space)

                try:
                    rooms = int(rooms[0])
                except ValueError:
                    rooms = 0  # Если вместо квартиры студия

                print(link)
                try:
                    page_in = urlopen(link)
                except URLError:
                    print("Address don't open = ", link)
                except HTTPError:
                    print("Address don't open = ", link)                    
                else:
                    page_in = page_in.read().decode('UTF-8')
                    page_in = html.fromstring(page_in)
                    price = 0
                    price = page_in.xpath('//span[@class="price-value-string"][1]//text()')
                    # print(price)
                    address = page_in.xpath(
                            '//div[@class="seller-info-prop"][last()]//text()')
                    # print(address)
                    address = address[3]
                    try:
                        price = price[0]
                    except IndexError:
                        price = 0
                    else:                    
                        price = price.strip()
                
                if( price != 0):
                    print('Price = ',price)
                    price = price.replace('\u2009','')
                    print('Price = ',price)
                    price = price.replace(' ','')
                    price = price.strip()
                    print('Price = ',price)
                address = address.strip()
                # print(address)
                city = address.split(',')[1]
                # print(city)
                try:
                    city, district = city.split('р-н')
                except ValueError:
                    district = ' '
                # print('City = ', city, ' district = ', district)
                # print(address)
                type_house = page_in.xpath('//li[@class="item-params-list-item" and span = "Тип дома: "]//text()')
                # print(type_house)
                type_house = type_house[-1].strip()
                # print(type_house)
                # print(type_house)
                # self.stdout.write(self.style.SUCCESS('Type house = {}'.format(type_house)))
                price_m2 = 0
                try:
                    price = int(price)
                except ValueError:
                    price = 0
                else:
                    price_m2 = int(price) / living_space
                print(  '\ntitle=',title.strip(),
                        '\nlink=',link,
                        '\nprice=',price,
                        '\nprice_m2=',price_m2,
                        '\ncity=',city,
                        '\nagent=','str(data[0].text).strip()',
                        '\naddress=',address,
                        '\nrooms=',rooms,
                        '\nliving_space=',living_space,
                        '\nfloor=',floor.strip()[:-4],
                        '\ntype_house=',type_house,
                        '\ndistrict=',district
                      )
                
                try:
                    a = Apartment.objects.create(
                        title=title.strip(),
                        link=link,
                        price=price,
                        price_m2=price_m2,
                        city=city,
                        agent=' ',
                        site='Avito',
                        address=address,
                        rooms=rooms,
                        living_space=living_space,
                        floor=floor.strip()[:-4],
                        type_house=type_house,
                        district=district,
                        active=True,
                        )
                    add_apartments = add_apartments +1
                except Apartment.DoesNotExist:
                    print('Apartmen dont create ', title)
        logger.info('Added apartments from site Avito %s', add_apartments)

