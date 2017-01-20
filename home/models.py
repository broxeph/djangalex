from django.db import models


class Box(models.Model):
    name = models.CharField(max_length=50)
    logo_url = models.CharField(max_length=50)
    link_url = models.URLField()
    sort_order = models.IntegerField(null=True)

    def logo_url_static(self):
        return 'home/' + self.logo_url

    def __str__(self):
        return self.name


class Subtitle(models.Model):
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text
