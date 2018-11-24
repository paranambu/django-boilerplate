from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.management import call_command

from ...csv_importer import CSVImporter


class Command(BaseCommand):
    def handle(self, *args, **options):
        for fixture in settings.FIXTURES:
            if fixture.endswith('.json'):
                call_command('loaddata', fixture)
            elif fixture.endswith('.csv'):
                csv_importer = CSVImporter(fixture)
                csv_importer.import_csv()
            else:
                raise CommandError('Invalid extension for {}'.format(fixture))
