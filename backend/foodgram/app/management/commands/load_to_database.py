import csv
from pathlib import Path

from django.core.management import BaseCommand

from ...models import Ingredient

DIR = Path(__file__).resolve().parents[5]


class Command(BaseCommand):
    help = "Load data from csv files"

    def handle(self, *args, **kwargs):
        with open(
            f"{DIR}/data/ingredients.csv",
            "r",
            encoding="utf-8",
        ) as csv_file:
            reader = csv.reader(csv_file, delimiter=",")
            for name, unit in dict(reader).items():
                Ingredient.objects.create(name=name, measurement_unit=unit)

        self.stdout.write(self.style.SUCCESS("Successfully load data"))
