from lxml import html
import json
import logging
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
import requests

logger = logging.getLogger('proxy_logers')


class Proxy(object):
    """ Класс для парсинга прокси """

    proxy_url = 'https://hidemy.name/ru/proxy-list/?maxtime=1000&type=h'
    proxy_list = []

    def __init__(self):
        """ Соберем все адреса прокси """

        r = self.open_url(self.proxy_url)
        self.proxy_list = list(self.get_ip_proxy(r))

    def get_ip_proxy(self, url):
        """ Получение списка прокси """

        ip_list = url.xpath('//*[@class="proxy__t"]/tbody/tr')
        for ip_l in ip_list:
            ip = ip_l.xpath('td[1]//text()')
            port = ip_l.xpath('td[2]//text()')
            ip = str(ip[0] + ':' + port[0])
            yield ip

    def open_url(self, url):
        """ Открытие адреса и его преобразование """

        url = Request(url=url)
        url.add_header(
            'User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0')
        # print(url)
        try:
            page = urlopen(url)
        except Exception as e:
            logger.exception('Not open url {}, execpt {}'.format(url, e))
        else:
            page = page.read().decode('windows-1251')
            page = html.fromstring(page)
            return page
        return False

    def get_proxy_list(self):
        """ Отдает лист с проки IP """

        return self.proxy_list
