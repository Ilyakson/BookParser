from django.db import models


class ISBN(models.Model):
    isbn = models.CharField(max_length=255, unique=True)
    publisher = models.CharField(max_length=255, blank=True)
    edition = models.CharField(max_length=255, blank=True)
    language = models.CharField(max_length=255, blank=True)
    rating = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    author = models.CharField(max_length=255, blank=True)
    seller = models.CharField(max_length=255, blank=True)
    price = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=25, default='New')
