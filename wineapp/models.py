import statistics

from django.db import models


class Wine(models.Model):
    name = models.CharField(max_length=200)

    def average_rating(self):
        if self.review_set.all():
            all_ratings = map(lambda x: x.rating, self.review_set.all())
            return statistics.mean(all_ratings)
        else:
            return None

    def __str__(self):
        return self.name


class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    wine = models.ForeignKey(Wine)
    pub_date = models.DateTimeField('date published')
    user_name = models.CharField(max_length=100)
    comment = models.CharField(max_length=200)
    rating = models.IntegerField(choices=RATING_CHOICES)


class Post(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=1000)
    pub_date = models.DateTimeField('date published')
    user_name = models.CharField(max_length=200)
