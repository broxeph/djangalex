import statistics

from django.db import models


class Wine(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(null=True, upload_to='images', blank=True)
    variety = models.CharField(max_length=50, blank=True)
    abv = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    description = models.TextField(max_length=1000, blank=True)

    def average_rating(self):
        if self.review_set.all():
            all_ratings = map(lambda x: x.rating, self.review_set.all())
            return statistics.mean(all_ratings)
        else:
            return 0

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
    wine = models.ForeignKey(Wine, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published')
    user_name = models.CharField(max_length=100)
    comment = models.CharField(max_length=200)
    rating = models.IntegerField(choices=RATING_CHOICES)


class Post(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=1000)
    pub_date = models.DateTimeField('date published')
    user_name = models.CharField(max_length=200)
