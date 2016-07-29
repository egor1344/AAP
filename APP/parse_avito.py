#!/usr/bin/env python3

import sys
import argparse
import json
from datetime import date, timedelta, time, datetime
from configparser import ConfigParser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from grab import Grab
from bild_db import Advertisement, Base

# def test_speed(func):
#     import time

#     def f(*args, **kwargs):
#         # print('Получен аргумент ', *args)
#         print('Name func = ', func.__name__)
#         start = time.time()
#         m = func(*args, **kwargs)
#         print('Time = ', time.time() - start)
#         return m
#     return f


def cmd_parser():
    pr = argparse.ArgumentParser()
    pr.add_argument('-n', '--number', type=int)

    return pr


class Parse():
    """
    Class for parsing valuable real estate on Avito.ru

    """

    def __init__(self, page_number):
        self.ad = []
        config = ConfigParser()
        config.read('./config_avito')
        self.url = 'https://www.avito.ru/bashkortostan/kvartiry/prodam'
        self.host = 'https://www.avito.ru'
        self.today = date.today()
        self.yesterday = date.today() - timedelta(days=1)
        self.page_number = page_number

    def parse(self):
        """
        Main func.
        """
        if not self.page_number:
            self.page_number = self.get_pages_number(self.url)
        print('All pages = ', self.page_number)
        self.get_content_pages(self.page_number)
        self._ad_add_db(self.ad)
        # self._show_ad()

    def get_pages_number(self, url):
        """
        Get pages number.

        Argumetns:
        url -- Any page. 

        """
        g = Grab()
        g.go(url)
        pagination_page = g.xpath(
            '//*[contains(text(),"Последняя")]/@href'
        )
        num = str(pagination_page)[-3:]
        return (int(num))

    def get_content_pages(self, number_pages):
        """
        Func parsing.
        """
        g = Grab()
        for i in range(1, number_pages + 1):

            print('Done = ', (i / number_pages) * 100, ' page = ', i)

            g.go(self._creare_next_url(i))
            item_list = g.xpath_list('//*[@class="description"]')
            price_list = g.xpath_list(
                '//*[@class="popup-prices popup-prices__wrapper clearfix"]/@data-prices')
            for key, item in enumerate(item_list):
                title = item.xpath(
                    '//h3[@class="title item-description-title"]/a//text()'
                )[key]

                link = self.host + item.xpath(
                    '//h3[@class="title item-description-title"]/a/@href'
                )[key]

                about = item.xpath(
                    '//div[@class="about"]'
                )[key]
                about = about.text
                data = item.xpath('//div[@class="data"]')[key]
                date_time = item.xpath('//div[@class="date c-2"]//text()')[key]
                date_time = self._get_time(date_time)
                # print(date_time)
                price = 0  # Default value
                if (not about.isspace()) and ((about.strip()[0]).isdigit()):
                    price, opis = self._get_price(price_list.pop(0))

                self.ad.append({
                    'title': title.strip(),
                    'link': link,
                    'price': price,
                    'agent': str(data[0].text).strip(),
                    'city': data[1].text,
                    'time': date_time
                })

    def _get_price(self, price):
        """
        Parse json data in price.

        Return price and status.

        """
        price = json.loads(price)
        if (price[0]['title']) == 'Цена':
            return (price[0]['currencies']['RUB']), 'Продается'
        else:
            return (price[0]['currencies']['RUB']), 'Сдается'

    def _get_time(self, date_time):
        date_time = date_time.strip()
        hour_minut = time(int(date_time[-5:-3]), int(date_time[-2:]))
        if date_time[0] == 'С':
            return (datetime.combine(self.today, hour_minut)).isoformat()
        else:
            return (datetime.combine(self.yesterday, hour_minut)).isoformat()

    def _creare_next_url(self, number_page):
        return(str(self.url + '?p={}'.format(number_page)))

    def _ad_add_db(self, item_list):
        """
        Add to DataBase.
        """
        self._initial_db()
        links = [link[0]
                 for link in self.session.query(Advertisement.link).all()]
        for item in item_list:
            if item['link'] not in links:
                new_ad = Advertisement(title=item['title'],
                                       link=item['link'],
                                       price=item['price'],
                                       agent=item['agent'],
                                       city=item['city'],
                                       time=item['time'])
                self.session.add(new_ad)
                self.session.commit()
                print('Add ', item['title'])

    def _initial_db(self):
        """
        Create connect to DB.
        """
        engine = create_engine(
            'postgresql+psycopg2://marko:cthutq68@localhost:5432/parcer_t')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def _show_ad(self):
        for i in self.ad:
            print(i['title'], ' = ', i['price'])


if __name__ == '__main__':
    number_page = cmd_parser().parse_args(sys.argv[1:])
    a = Parse(number_page.number)
    a.parse()
