from django.db import models


class Tag(models.Model):
    tagname = models.CharField(max_length=100)

    def __str__(self):
        return self.tagname


class Advert(models.Model):
    name = models.CharField(max_length=200)
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(upload_to='image/')
    ad_url = models.CharField(max_length=500)

    def __str__(self):
        return self.name
