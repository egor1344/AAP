from main.models import Apartment
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Analitic price aprtment'

    # def add_arguments(self, parser):
    #     parser.add_argument('pages', default=1, type=int)

    def handle(self, *args, **options):
        apartment = Apartment.objects.filter(city='Уфа')
        self.stdout.write(self.style.SUCCESS('Apartment count "%s"' % apartment))

