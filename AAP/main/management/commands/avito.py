from lxml import html
import json
import logging
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
import configparser
import time
from multiprocessing import Process
import os

from django.core.management.base import BaseCommand, CommandError

from main.models import Apartment, HistoryApartmentPrice, Sites

from .proxy import Proxy

HOST = 'https://www.avito.ru'

# logger = logging.getLogger('parse_avito')


class Command(BaseCommand):
    help = 'Parse apartments Avito'

    proxy_ip = ''
    proxy_number = 0
    proxy_list = []
    len_proxy_list = 0

    # def add_arguments(self, parser):
    #     parser.add_argument('pages', default=1, type=int)

    def handle(self, *args, **options):

        self.proxy_list = Proxy().get_proxy_list()
        self.len_proxy_list = len(self.proxy_list)
        print(self.proxy_list, self.len_proxy_list)

        urls = Sites.objects.filter(url__contains='avito')
        print(urls)

        # self.add_apartment('https://www.avito.ru/ufa/kvartiry/1-k_kvartira_37.8_m_818_et._1055574321')

        links = [l[0] for l in Apartment.objects.filter(
            site='Avito').values_list('link')]

        for url in urls:
            print(url.url)
            req_url = Request(url=url.url)
            req_url.add_header(
                'User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0')

            url_list = self.get_ad_apartment(req_url)
            self.handle_ad_url(links, url_list)
            print(url_list)

    def get_ad_apartment(self, url):
        """ Получение списка обьявлений на квартиры """

        while(self.len_proxy_list >= self.proxy_number):

            self.proxy_ip = self.proxy_list[self.proxy_number]
            print(self.proxy_ip)

            url.set_proxy(self.proxy_ip, 'http')
            cond, page = self.open_url(url)

            if cond:
                url_list = page.xpath(
                    '//div[contains(@class, "js-catalog-item-enum")]')
                return url_list
            else:
                self.proxy_number += 1
                continue

    def open_url(self, url):
        """ Открытие адреса и его преобразование """

        try:
            page = urlopen(url)
            print(page.getcode())
        except Exception as e:
            # logger.exception('Not open url {}, execpt {}'.format(url, e))
            return False, None
        else:
            page = page.read().decode('UTF-8')
            page = html.fromstring(page)
            return True, page

    def handle_ad_url(self, links,  ads):
        """ Обработка обьявлений """

        for num, item in enumerate(ads):
            try:
                link_apartment = HOST + item.xpath(
                    '//h3[@class="title item-description-title"]/a/@href'
                )[num]
            except IndexError:
                return False
            if link_apartment not in links:
                p = Process(target=self.add_apartment, args=(link_apartment,))
                p.start()
                p.join() 
            else:
                self.update_apart(link_apartment)

    def update_apart(self, url):
        """ Обновление цены  """

        print('Update price ',url)
        req_url = Request(url=url)
        req_url.add_header(
                'User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0')


        while (self.len_proxy_list >= self.proxy_number):

            self.proxy_ip = self.proxy_list[self.proxy_number]
            print(self.proxy_ip)

            req_url.set_proxy(self.proxy_ip, 'http')
            cond, page = self.open_url(req_url)
            if cond:
                apart = Apartment.objects.get(link=url)
                params = self.parsing_page_ad(page)
                apart_price_history = HistoryApartmentPrice.objects.create(apartment=apart, price=apart.price)
                apart.price = params['price']
                apart.save()
                return True
            else:
                self.proxy_number += 1
                continue


    def add_apartment(self, url):
        """ Добавление обьявления о квартире в базу """

        print(url)
        req_url = Request(url=url)
        req_url.add_header(
                'User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0')


        while (self.len_proxy_list >= self.proxy_number):

            self.proxy_ip = self.proxy_list[self.proxy_number]
            print(self.proxy_ip)

            req_url.set_proxy(self.proxy_ip, 'http')
            cond, page = self.open_url(req_url)
            if cond:
                params = self.parsing_page_ad(page)
                self.save_apartment(params, url)
                return True
            else:
                self.proxy_number += 1
                continue

    def parsing_page_ad(self, page):
        """ Парсинг обьявления о квартире """

        print('parent process:', os.getppid())
        print('process id:', os.getpid())
        params = {}
        params['title'] = self.get_title(page)
        params['living_space'] = self.get_living_space(page)
        params['price'], params['price_m2'] = self.get_price(page)
        params['agent'] = 'None'
        params['address'], params['city'] = self.get_address(page)
        params['rooms'] = self.get_rooms(page)
        params['floor'] = self.get_floor(page)
        params['type_house'] = self.get_type_house(page)
        params['district'] = self.get_district(params['address'])
        print(params)
        return params

    def get_title(self, page):
        """" Получение заголовка """
        
        r = page.xpath('//span[@class="title-info-title-text"]//text()')
        return r

    def get_address(self, page):
        """ Получние адреса """

        city = page.xpath('//div[@class="item-map-location"]/span[@itemprop="name"]//text()')
        address = city[0] + ' ' + ' '.join(page.xpath('//div[@class="item-map-location"]/span[@itemprop="address"]//text()'))
        address = address.replace('\n', '')
        address = address.replace('\u2009', '')
        address = address.replace('\xa0', '')
        address = address.replace('  ', ' ')
        return address, city[0]


    def get_district(self, address):
        """ Получние района города """

        i = address.find('р-н') + 1
        if i:
            dis = address.split(',')
            dis = dis[0]
            dis = dis[(i+3):]
            return dis
        else:
            return  ' '


    def get_type_house(self, page):
        """ Получение типа дома"""

        s = page.xpath('//li[span="Тип дома: "]//text()')
        s = s[-1]
        s = s.strip()
        return s

    def get_floor(self, page):
        """ Получение этажа """

        r = page.xpath('//span[@class="title-info-title-text"]//text()')
        r = r[0]
        r = r.strip()
        r = r.split(',')
        r = r[-1]
        r = r.replace('\u2009', '')
        r = r.replace('\xa0', '')
        r = r[:-3]
        return r


    def get_rooms(self, page):
        """ Получение количества комнат """

        s = page.xpath('//li[span="Количество комнат: "]//text()')
        s = s[-1]
        s = s[0]
        try:
            s = int(s)
        except ValueError:
            s = 0
        return s


    def get_living_space(self, page):
        """ Получене квадратуры квартиры """

        s = page.xpath('//li[span="Общая площадь: "]//text()')
        print(s)
        try:
            s = s[-1]
        except IndexError:
            return 0
        else:
            s = s[:-5]
            s = float(s)
            return s


    def get_price(self, page):
        """ Полученеи цены и цены за квадрат """

        price = page.xpath('//ul[@class="price-value-prices-list js-price-value-prices-list"]/li[1]//text()')
        try:
            price = price[0]
        except IndexError:
            return 0, 0
        else:
            price = price.strip()
            price = price.replace('\u2009', '')
            price = price.replace('\xa0', '')
            price = float(price)
            price_m2 = page.xpath('//ul[@class="price-value-prices-list js-price-value-prices-list"]/li[4]//text()')
            price_m2 = price_m2[0]
            price_m2 = price_m2.strip()
            price_m2 = price_m2.replace('\u2009', '')
            price_m2 = price_m2.replace('\xa0', '')
            price_m2 = price_m2[6:]
            price_m2 = float(price_m2)
        return price, price_m2


    def save_apartment(self, param, url):
        """ Сохранение обьявления """

        a = Apartment.objects.create(
                        title=param['title'],
                        link=url,
                        price=param['price'],
                        price_m2=param['price_m2'],
                        city= param['city'],
                        agent=param['agent'],
                        site='Avito',
                        address=param['address'],
                        rooms=param['rooms'],
                        living_space=param['living_space'],
                        floor=param['floor'],
                        type_house=param['type_house'],
                        district=param['district'],
                        active=True)
        print(a)
