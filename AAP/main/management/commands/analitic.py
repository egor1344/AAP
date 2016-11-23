from main.models import Apartment
from django.db.models import Max, Avg, Min, StdDev, Sum, Variance
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Analitic price aprtment'

    # def add_arguments(self, parser):
    #     parser.add_argument('pages', default=1, type=int)

    def handle(self, *args, **options):
        ufa = Apartment.objects.filter(city='Уфа', price__gt=1000000, price__lt=10000000)
        self.stdout.write(self.style.SUCCESS('Ufa count "%s"' % ufa.count()))
        lenin = ufa.filter(district__icontains='Ленинский').count()
        cir = ufa.filter(district__icontains='Кировский').count()
        ordj = ufa.filter(district__icontains='Орджоникидзевский').count()
        calin = ufa.filter(district__icontains='Калининский').count()
        sovet = ufa.filter(district__icontains='Советский').count()
        oktabr = ufa.filter(district__icontains='Октябрьский').count()
        self.stdout.write(self.style.SUCCESS('Ленинский count "%s"' % lenin))
        self.stdout.write(self.style.SUCCESS('Кировский count "%s"' % cir))
        self.stdout.write(self.style.SUCCESS('Орджоникидзевский count "%s"' % ordj))
        self.stdout.write(self.style.SUCCESS('Калининский count "%s"' % calin))
        self.stdout.write(self.style.SUCCESS('Советский count "%s"' % sovet))
        self.stdout.write(self.style.SUCCESS('Октябрьский count "%s"' % oktabr))

