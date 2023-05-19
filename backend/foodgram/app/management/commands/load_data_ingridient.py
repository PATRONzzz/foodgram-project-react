import csv
from pathlib import Path

from django.core.management import BaseCommand

from ...models import Ingredient

DIR = Path(__file__).resolve().parents[5]


class Command(BaseCommand):
    help = "Load data ingridient from csv files"

    def handle(self, *args, **kwargs):
        with open(
            f"{DIR}/data/ingredients.csv",
            "r",
            encoding="utf-8",
        ) as csv_file:
            reader = csv.DictReader(csv_file, delimiter=",")
            Ingredient.objects.bulk_create(Ingredient(**data) for data in reader)
        
        self.stdout.write(self.style.SUCCESS("Successfully load data"))
