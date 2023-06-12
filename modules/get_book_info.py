import requests
from bs4 import BeautifulSoup
from django.db import transaction

from django_setup import *
from books.models import Book, Seller


class BookSearcher:
    def __init__(self):
        self.base_url = "https://www.bookfinder.com"

    def get_book_info(self, book_obj):
        url = f"{self.base_url}/isbn/{book_obj.isbn}/?used=1"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Помилка при отриманні сторінки товару: {response.status_code}")
            return
        soup = BeautifulSoup(response.content, "html.parser")

        try:
            title_element = soup.find("h1", class_="bf-content-header-book-title")
            title = title_element.text.strip()
        except AttributeError:
            title = None

        try:
            author_element = soup.find(
                "div", class_="bf-content-header-book-author"
            )
            author = author_element.find("a").text
        except AttributeError:
            author = None

        try:
            rating_element = soup.find(
                "span", class_="book-rating-average text-muted"
            )
            rating = rating_element.text.split()[0].strip()

        except AttributeError:
            rating = None

        try:
            publisher_element = soup.find("strong", string="Publisher:")
            publisher = " ".join(publisher_element.next_sibling.split())
        except AttributeError:
            publisher = None

        try:
            edition_element = soup.find("strong", string="Edition:")
            edition = edition_element.next_sibling.split()[0]
        except AttributeError:
            edition = None

        try:
            language_element = soup.find("strong", string="Language:")
            language = language_element.next_sibling.split()[0]
        except AttributeError:
            language = None

        defaults = {
            "publisher": publisher,
            "edition": edition,
            "language": language,
            "rating": rating,
            "title": title,
            "author": author,
        }
        with transaction.atomic():
            Book.objects.filter(pk=book_obj.pk).update(**defaults)

        book_obj.refresh_from_db()

    def get_seller_info(self, book_obj):
        url = f"{self.base_url}/isbnresults/{book_obj.isbn}/?used=1"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Помилка при отриманні сторінки товару: {response.status_code}")
            return

        soup = BeautifulSoup(response.content, "html.parser")
        sellers_section = soup.find("div", class_="hidden-xs hidden-sm")
        sellers = sellers_section.find_all("li", class_="bf-search-result-wrapper")
        seller_list = []

        for seller in sellers:

            try:
                seller_name_element = seller.find(
                    "div", class_="marketplace-seller-name"
                )
                seller_name = seller_name_element.text.strip()
            except AttributeError:
                seller_name = None

            try:
                link_element = seller.find("a", class_="clickout-logger")["href"]
            except AttributeError:
                link_element = None

            try:
                price_element = seller.find("span", class_="tooltiptext-custom")
                total_price_element = price_element.find("th", string="Total price ")
                total_price = total_price_element.find_next_sibling("th").get_text(strip=True).strip()
            except AttributeError:
                total_price = None

            try:
                description_element = seller.find("div", class_="bf-search-result-col-info").get_text().split()
                description_text = " ".join(description_element)
            except AttributeError:
                description_text = None

            seller_obj = Seller(
                seller=seller_name,
                link=link_element,
                price=total_price,
                description=description_text,
                book=book_obj
            )
            seller_list.append(seller_obj)

        Seller.objects.bulk_create(seller_list)
        book_obj.status = "Done"
        book_obj.save()


book_searcher = BookSearcher()
new_books = Book.objects.filter(status="New")
for book in new_books:
    book_searcher.get_book_info(book)
    book_searcher.get_seller_info(book)
