from lxml import html
import json
from datetime import date, timedelta, time, datetime
from urllib.request import urlopen
from django.core.management.base import BaseCommand, CommandError
from main.models import Apartment

URL = 'https://www.avito.ru/bashkortostan/kvartiry/prodam'
HOST = 'https://www.avito.ru'


class Command(BaseCommand):
    help = 'Parse apartments Avito'

    def add_arguments(self, parser):
        parser.add_argument('pages', default=1, type=int)

    def handle(self, *args, **options):
        r = urlopen(URL)
        ht = r.read().decode('UTF-8')
        page = html.fromstring(ht)
        item_list = page.xpath('//*[@class="description"]')
        price_list = page.xpath(
            '//*[@class="popup-prices popup-prices__wrapper clearfix"]/@data-prices')
        links = [l[0] for l in Apartment.objects.filter(site='Avito').values_list('link')]
        for key, item in enumerate(item_list):
            link = HOST + item.xpath(
                '//h3[@class="title item-description-title"]/a/@href'
            )[key]
            if link not in links:
                title = item.xpath(
                    '//h3[@class="title item-description-title"]/a//text()'
                )[key]
                address = urlopen(link)
                address = address.read().decode('UTF-8')
                address = html.fromstring(address)
                address = address.xpath('//*[@itemprop="streetAddress"]//text()')
                about = item.xpath(
                    '//div[@class="about"]'
                )[key]
                about = about.text
                data = item.xpath('//div[@class="data"]')[key]
                date_t = item.xpath('//div[@class="date c-2"]//text()')[key]
                date_t = str(date_t).strip()
                hour_minut = time(int(date_t[-5:-3]), int(date_t[-2:]))
                date_t = datetime.combine(date.today(), hour_minut).isoformat()
                price = 0  # Default value
                if (not about.isspace()) and ((about.strip()[0]).isdigit()):
                    price = json.loads(price_list.pop(0))
                    price = price[0]['currencies']['RUB']

                try:
                    a = Apartment.objects.create(
                        title=title.strip(),
                        link=link,
                        price=price,
                        date_time=date_t,
                        city=data[1].text,
                        agent=str(data[0].text).strip(),
                        site='Avito',
                        address=address[0],)
                    self.stdout.write(self.style.SUCCESS('Successfully'))
                except Apartment.DoesNotExist:
                    raise CommandError("Don't create")

