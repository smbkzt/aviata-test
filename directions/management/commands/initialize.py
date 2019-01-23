import sys

from django.core.management.base import BaseCommand

from directions.tasks import update_flight_prices


class Command(BaseCommand):
    help = 'Initializes data'

    def handle(self, *args, **options):
        try:
            update_flight_prices()
        except KeyboardInterrupt:
            sys.exit(1)
