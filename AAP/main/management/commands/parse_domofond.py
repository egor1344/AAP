from lxml import html
import json
from urllib.request import urlopen
from django.core.management.base import BaseCommand, CommandError
from main.models import Apartment

URL = 'http://www.domofond.ru/prodazha-kvartiry-bashkortostan-r41?SortOrder=Newest'
HOST = 'http://www.domofond.ru'


class Command(BaseCommand):
    help = 'Parse apartments Domofond'

    def add_arguments(self, parser):
        parser.add_argument('pages', default=1, type=int)

    def handle(self, *args, **options):
        r = urlopen(URL)
        ht = r.read().decode('UTF-8')
        page = html.fromstring(ht)
        item_list = page.xpath('//*[@class="df_listingTileExpanded"]')
        price_list = page.xpath(
            '//*[@itemprop="price"]//text()')
        links = [l[0] for l in Apartment.objects.filter(
            site='Domofond').values_list('link')]
        for key, item in enumerate(item_list):
            link = HOST + item.xpath(
                '//a[@itemprop="sameAs"]/@href'
            )[key]
            if link not in links:
                title = item.xpath('//a[@itemprop="sameAs"]/@title')[key]
                agent = ''
                try:
                    rooms = int(title[0])
                except ValueError:
                    rooms = 0
                    agent = title.split(',')
                    agent = agent[-1].strip()
                # self.stdout.write(self.style.SUCCESS(title))
                address = item.xpath('//*[@itemprop="address"]//text()')[key]
                city = address.split(',')[-2].strip()
                # self.stdout.write(self.style.SUCCESS(city))
                # self.stdout.write(self.style.SUCCESS(address))
                price = item.xpath('//*[@itemprop="price"]//text()')[key]
                price = price[:-5].replace('\xa0','')
                try:
                    price = int(price)
                except ValueError:
                    price = 0
                # self.stdout.write(self.style.SUCCESS(price))
                # self.stdout.write(self.style.SUCCESS('----'*3))

                try:
                    a = Apartment.objects.create(
                            title=title.strip(),
                            link=link,
                            price=price,
                            price_m2=0,
                            city=city,
                            agent=agent,
                            site='Domofond',
                            address=address,
                            living_space=0,
                            rooms=rooms,)
                    self.stdout.write(self.style.SUCCESS('Successfully'))
                except Apartment.DoesNotExist:
                    print('Apartmen dont create ', title)
