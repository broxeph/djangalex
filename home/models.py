from django.db import models

# Create your models here.


class Box(models.Model):
    name = models.CharField(max_length=50)
    logo_url = models.URLField()
    link_url = models.URLField()

    def __str__(self):
        return self.name
