from django.contrib import admin

from books.models import ISBN


@admin.register(ISBN)
class ISBNAdmin(admin.ModelAdmin):
    list_display = [
        "isbn", "publisher", "edition",
        "language", "rating", "title",
        "author", "seller", "price",
        "status"
    ]
