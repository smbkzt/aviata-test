from django.core.management.base import BaseCommand

from directions.tasks import update_flight_prices


class Command(BaseCommand):
    help = 'Initializes data'

    def handle(self, *args, **options):
        update_flight_prices()
