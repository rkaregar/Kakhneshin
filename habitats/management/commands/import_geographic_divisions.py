from django.core.management.base import BaseCommand, CommandError
import json

from habitats.models import GeographicDivision


def load_divisons(data, region=None):
    if type(data) is list:
        for city in data:
            GeographicDivision.objects.get_or_create(name=city, region=region, is_city=True)
        return
    for division in data.keys():
        load_divisons(data[division],
                      GeographicDivision.objects.get_or_create(name=division, region=region, is_city=False)[0])


class Command(BaseCommand):
    help = 'Add Geographic Divisions to database'

    def add_arguments(self, parser):
        parser.add_argument('data_address')

    def handle(self, *args, **options):
        try:
            with open(options['data_address'], encoding='utf-8') as input_file:
                data = json.load(input_file)
                load_divisons(data)
        except IOError:
            raise CommandError('File doesn\'t exists')
