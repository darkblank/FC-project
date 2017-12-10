from django.core.management import BaseCommand

from accounts.models import Preference


class Command(BaseCommand):
    def handle(self, *args, **options):
        Preference.objects.create(
            preferences='kor',
        )
        Preference.objects.create(
            preferences='chn',
        )
        Preference.objects.create(
            preferences='jpn',
        )
        Preference.objects.create(
            preferences='mex',
        )
        Preference.objects.create(
            preferences='amc',
        )
        Preference.objects.create(
            preferences='tha',
        )
        Preference.objects.create(
            preferences='med',
        )
        Preference.objects.create(
            preferences='ita',
        )
        Preference.objects.create(
            preferences='vtn',
        )
        Preference.objects.create(
            preferences='spn',
        )
        Preference.objects.create(
            preferences='ind',
        )
        Preference.objects.create(
            preferences='etc',
        )

    print("Successfully created preferences")
