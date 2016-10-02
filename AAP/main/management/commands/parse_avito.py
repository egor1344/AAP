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
        price_list = page.xpath(
            '//*[@class="popup-prices popup-prices__wrapper clearfix"]/@data-prices')
        links = [l[0] for l in Apartment.objects.filter(
            site='Avito').values_list('link')]
        for key, item in enumerate(item_list):
            link = HOST + item.xpath(
                '//h3[@class="title item-description-title"]/a/@href'
            )[key]
            if link not in links:
                title = item.xpath(
                    '//h3[@class="title item-description-title"]/a//text()'
                )[key]
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
                    print("Address don't open = ", page_in)
                except HTTPError:
                    print("Address don't open = ", page_in)                    
                else:
                    page_in = page_in.read().decode('UTF-8')
                    page_in = html.fromstring(page_in)
                    price = 0
                    price = page_in.xpath('//span[@itemprop="price"]//text()')
                    try:
                        price = price[0]
                    except IndexError:
                        price = 0
                    else:                    
                        price = price.strip()
                        price = price[:-5].replace(' ','')
                        address = page_in.xpath(
                            '//span[@id="toggle_map"]//text()')
                district = ' '
                if (len(address) == 2):
                    district = address[0]
                    district = district.split(' ')
                    district = district[1][:-1]
                    address = address[1]
                else:
                    address = address[0]
                type_house = page_in.xpath('//div[@class="item-params c-1"][2]/a[2]/@title')
                type_house = type_house[0].split('—')
                type_house  = type_house[1]
                self.stdout.write(self.style.SUCCESS('Type house = {}'.format(type_house)))
                price_m2 = 0
                try:
                    price = int(price)
                except ValueError:
                    price = 0
                else:
                    price_m2 = int(price) / living_space
                about = item.xpath('//div[@class="about"]')[key]
                about = about.text
                data = item.xpath('//div[@class="data"]')[key]
                
        #         try:
        #             a = Apartment.objects.create(
        #                 title=title.strip(),
        #                 link=link,
        #                 price=price,
        #                 price_m2=price_m2,
        #                 city=data[1].text,
        #                 agent=str(data[0].text).strip(),
        #                 site='Avito',
        #                 address=address,
        #                 rooms=rooms,
        #                 living_space=living_space,
        #                 floor=floor.strip()[:-4],
        #                 )
        #             add_apartments = add_apartments +1
        #         except Apartment.DoesNotExist:
        #             print('Apartmen dont create ', title)
        # logger.info('Added apartments from site Avito %s', add_apartments)

