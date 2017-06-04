from lxml import html
import json
import logging
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import configparser

from django.core.management.base import BaseCommand, CommandError

from main.models import Apartment

logger = logging.getLogger('parse_avito')

class Command(BaseCommand):
    help = 'Parse apartments Avito'

    def add_arguments(self, parser):
        parser.add_argument('pages', default=1, type=int)

    def _confing(self):
        confing = configparser.ConfigParser()
        confing.read('parser.ini')
        avito = confing['Avito']
        return avito['Url'], avito['Host']

    def handle(self, *args, **options):
        add_apartments = 0
        url, host = self._confing()
        print(url, host)
        r = urlopen(url)
        ht = r.read().decode('UTF-8')
        page = html.fromstring(ht)
        print(page)
        item_list = page.xpath('//div[contains(@class, "item")]')
        print(len(item_list))
        price_list = page.xpath(
            '//*[@class="popup-prices popup-prices__wrapper clearfix"]/@data-prices')
        links = [l[0] for l in Apartment.objects.filter(
            site='Avito').values_list('link')]
        for key, item in enumerate(item_list):
            link = host + item.xpath(
                '//h3[@class="title item-description-title"]/a/@href'
            )[key]

            if link not in links:
                title = item.xpath(
                    '//h3[@class="title item-description-title"]/a//text()'
                )[key]

                # Обработка квадратуры
                rooms, living_space, floor = title.strip().split(',')
                living_space = living_space[:-3]
                living_space = living_space.strip()
                living_space = float(living_space)

                try:
                    rooms = int(rooms[0])
                except ValueError:
                    rooms = 0  # Если вместо квартиры студия

                try:
                    page_in = urlopen(link)
                except URLError:
                    pass
                except HTTPError:
                    pass
                else:
                    page_in = page_in.read().decode('UTF-8')
                    page_in = html.fromstring(page_in)
                    price = 0
                    price = page_in.xpath('//span[@class="price-value-string"][1]//text()')
                    address = page_in.xpath(
                            '//div[@class="seller-info-prop"][last()]//text()')
                    address = address[3]
                    try:
                        price = price[0]
                    except IndexError:
                        price = 0
                    else:
                        price = price.strip()

                if( price != 0):
                    price = price.replace('\u2009','')
                    price = price.replace(' ','')
                    price = price.strip()
                address = address.strip()
                city = address.split(',')[1]
                try:
                    city, district = city.split('р-н')
                except ValueError:
                    district = ' '
                type_house = page_in.xpath('//li[@class="item-params-list-item" and span = "Тип дома: "]//text()')
                type_house = type_house[-1].strip()
                price_m2 = 0
                try:
                    price = int(price)
                except ValueError:
                    price = 0
                else:
                    price_m2 = int(price) / living_space
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
                    pass
        logger.info('Added apartments from site Avito %s', add_apartments)
