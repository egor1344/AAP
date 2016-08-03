from lxml import html
import json
from datetime import date, timedelta, time, datetime
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
                self.stdout.write(self.style.SUCCESS(title))
                address = item.xpath('//*[@itemprop="address"]//text()')[key]
                price = item.xpath('//*[@itemprop="price"]//text()')[key]
                self.stdout.write(self.style.SUCCESS(price))
                datetime
        #         try:
        #             a = Apartment.objects.create(
        #                 title=title.strip(),
        #                 link=link,
        #                 price=price,
        #                 date_time=date_t,
        #                 city=data[1].text,
        #                 agent=str(data[0].text).strip(),
        #                 site='Avito',
        #                 address=address[0],)
        #             self.stdout.write(self.style.SUCCESS('Successfully'))
        #         except Apartment.DoesNotExist:
        #             raise CommandError("Don't create")
