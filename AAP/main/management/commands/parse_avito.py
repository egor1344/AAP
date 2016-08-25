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

                try:
                    rooms = int(rooms[0])
                except ValueError:
                    rooms = 0  # Если вместо квартиры студия

                try:
                    address = urlopen(link)
                except URLError:
                    print("Address don't open = ", address)
                except HTTPError:
                    print("Address don't open = ", address)                    
                else:
                    address = address.read().decode('UTF-8')
                    address = html.fromstring(address)
                    address = address.xpath(
                        '//*[@itemprop="streetAddress"]//text()')
                try:
                    address = address[0]
                except IndexError:
                    address = ''

                about = item.xpath('//div[@class="about"]')[key]
                about = about.text
                data = item.xpath('//div[@class="data"]')[key]
                price = 0  # Default value
                price_all = 0
                price_m2 = 0
                if (not about.isspace()) and ((about.strip()[0]).isdigit()):
                    price = json.loads(price_list.pop(0))
                    price_all = price[0]['currencies']['RUB']
                    price_m2 = price[1]['currencies']['RUB']
                
                try:
                    a = Apartment.objects.create(
                        title=title.strip(),
                        link=link,
                        price=price_all,
                        price_m2=price_m2,
                        city=data[1].text,
                        agent=str(data[0].text).strip(),
                        site='Avito',
                        address=address[0],
                        rooms=rooms,
                        living_space=living_space[:-3],
                        floor=floor[:-4],)
                    add_apartments = add_apartments +1
                except Apartment.DoesNotExist:
                    print('Apartmen dont create ', title)
        logger.info('Added apartments from site Avito %s', add_apartments)

