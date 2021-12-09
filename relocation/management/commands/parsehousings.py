from django.core.management.base import BaseCommand, CommandError
from relocation.services import parse_housings

class Command(BaseCommand):
    help = '''Reaches out to a remote parsing server to get all housing
              data from external resources and save it to the db.'''

    def handle(self, *args, **options):
        parse_housings()
        self.stdout.write(self.style.SUCCESS('Successfully parsed housings from a remote server!'))