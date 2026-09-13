import csv
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangalex.settings")

import django
django.setup()

from django.utils import timezone

from wineapp.models import Review, Wine


def save_review_from_row(row):
    review = Review()
    review.id = int(row['id'])
    review.user_name = row['username']
    review.wine = Wine.objects.get(id=int(row['wine_id']))
    review.rating = int(row['rating'])
    review.pub_date = timezone.now()
    review.comment = row['comment']
    review.save()


if __name__ == "__main__":
    # Check number of arguments (including the command name)
    if len(sys.argv) == 2:
        print("Reading from file " + sys.argv[1])
        with open(sys.argv[1], newline='') as f:
            for row in csv.DictReader(f):
                save_review_from_row(row)

        print("There are {} reviews in DB".format(Review.objects.count()))
    else:
        print("Please provide Reviews file path.")
