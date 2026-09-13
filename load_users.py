import csv
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangalex.settings")

import django
django.setup()

from django.contrib.auth.models import User


def save_user_from_row(row):
    user = User()
    user.id = int(row['id'])
    user.username = row['name']
    user.save()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        print("Reading from file " + sys.argv[1])
        with open(sys.argv[1], newline='') as f:
            for row in csv.DictReader(f):
                save_user_from_row(row)

        print("There are {} users".format(User.objects.count()))
    else:
        print("Please provide User file path.")
