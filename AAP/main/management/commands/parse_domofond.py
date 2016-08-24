from lxml import html
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
        price_list = page.xpath('//*[@itemprop="price"]//text()')
        links = [l[0] for l in Apartment.objects.filter(
            site='Domofond').values_list('link')]
        for key, item in enumerate(item_list):
            self.stdout.write(self.style.SUCCESS('-'*10))

            link = HOST + item.xpath('//a[@itemprop="sameAs"]/@href')[key]
            if link not in links:
                title = item.xpath('//a[@itemprop="sameAs"]/@title')[key]
                self.stdout.write(self.style.SUCCESS(title))
                price_m2 = item.xpath('a/div[1]/div[1]/span//text()')
                try:
                    price_m2 = price_m2.pop(0)
                except IndexError:
                    price_m2 = 0
                else:
                    price_m2 = price_m2.split(' ')
                    price_m2 = price_m2[0].replace('\xa0', '')
                self.stdout.write(self.style.SUCCESS(price_m2))
                living_space = item.xpath('a/div[1]/div[3]/ul/li[1]/span//text()')
                self.stdout.write(self.style.SUCCESS(living_space))
                try:
                    living_space = living_space.pop(0)
                except IndexError:
                    living_space = 0
                else:
                    if living_space.find('м²') != -1:
                        living_space = living_space[:-2].replace(',', '.')
                        living_space = float(living_space)
                    else:
                        living_space = 0
                        floor = living_space 
                self.stdout.write(self.style.SUCCESS(living_space))

                floor = item.xpath('a/div[1]/div[3]/ul/li[2]/span//text()')
                try:
                    floor = floor.pop(0)
                except IndexError:
                    floor = 0
                agent = ''
                try:
                    rooms = int(title[0])
                except ValueError:
                    rooms = 0
                    agent = title.split(',')
                    agent = agent[-1].strip()
                address = item.xpath('//*[@itemprop="address"]//text()')[key]
                city = address.split(',')[-2].strip()
                price = item.xpath('//*[@itemprop="price"]//text()')[key]
                price = price[:-5].replace('\xa0','')
                try:
                    price = int(price)
                except ValueError:
                    price = 0
                try:
                    a = Apartment.objects.create(
                            title=title.strip(),
                            link=link,
                            price=price,
                            price_m2=price_m2,
                            city=city,
                            agent=agent,
                            site='Domofond',
                            address=address,
                            living_space=living_space,
                            rooms=rooms,
                            floor=floor, )
                    self.stdout.write(self.style.SUCCESS('Successfully'))
                except Apartment.DoesNotExist:
                    print('Apartmen dont create ', title)
