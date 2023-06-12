from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from books.models import Book, Seller


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [
        "isbn", "publisher", "edition",
        "language", "rating", "title",
        "author", "status"
    ]


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ["seller", "price", "book_link", "description"]
    list_display_links = ['seller']  # Поле 'book_link' будет ссылкой

    def book_link(self, obj):
        book = obj.book
        book_admin_url = reverse('admin:books_book_change', args=[book.id])
        return format_html('<a href="{}">{}</a>', book_admin_url, book.title)

    book_link.short_description = 'Book'
