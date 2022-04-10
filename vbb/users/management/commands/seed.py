from django.core.management.base import BaseCommand, CommandError
from vbb.utils.seeds.seed import seed


class Command(BaseCommand):
    help = "Creates Seed Data"

    def handle(self, *args, **options):
        seed()
        print("Completed Adding Seed Data.")
