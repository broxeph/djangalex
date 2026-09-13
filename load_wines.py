import csv
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangalex.settings")

import django
django.setup()

from wineapp.models import Wine


def save_wine_from_row(row):
    wine = Wine()
    wine.id = int(row['id'])
    wine.name = row['name']
    wine.save()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        print("Reading from file " + sys.argv[1])
        with open(sys.argv[1], newline='') as f:
            for row in csv.DictReader(f):
                save_wine_from_row(row)

        print("There are {} wines".format(Wine.objects.count()))
    else:
        print("Please provide Wine file path.")
