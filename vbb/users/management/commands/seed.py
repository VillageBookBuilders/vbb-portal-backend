from django.core.management.base import BaseCommand

from vbb.utils.seeds.seed import seed


class Command(BaseCommand):
    help = "Creates Seed Data"

    def handle(self, *args, **options):
        seed()
        self.stdout.write("Completed Adding Seed Data.")
