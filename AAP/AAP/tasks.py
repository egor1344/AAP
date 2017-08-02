from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from main.parsers import Parser_avito

@task(name="parse_avito")
def parse():
    print('parse')
    p = Parser_avito()
    p.run()
