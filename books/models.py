from django.db import models


class Book(models.Model):
    isbn = models.CharField(max_length=255, unique=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    edition = models.CharField(max_length=255, blank=True, null=True)
    language = models.CharField(max_length=255, blank=True, null=True)
    rating = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=25, default='New')

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def __str__(self):
        return self.isbn


class Seller(models.Model):
    seller = models.CharField(max_length=255, blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)
    price = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="sellers")

    class Meta:
        verbose_name = 'Seller'
        verbose_name_plural = 'Sellers'

    def __str__(self):
        return self.link
