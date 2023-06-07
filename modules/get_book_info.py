import requests
from bs4 import BeautifulSoup
from django_setup import *
from books.models import ISBN


class BookSearcher:
    def __init__(self):
        self.base_url = "https://www.bookfinder.com"

    def search_books(self):
        for isbn in ISBN.objects.filter(status="New"):
            url = f"{self.base_url}/isbn/{isbn.isbn}/?used=1"
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

            url = f"https://www.bookfinder.com/isbnresults/{isbn.isbn}/?used=1"
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Помилка при отриманні сторінки товару: {response.status_code}")
                return

            soup = BeautifulSoup(response.content, "html.parser")
            seller = soup.find("li", class_="bf-search-result-wrapper")

            try:
                seller_name_element = seller.find(
                    "div", class_="marketplace-seller-name"
                )
                seller_name = seller_name_element.text
            except AttributeError:
                seller_name = None

            try:
                link = seller.find("a", class_="clickout-logger")["href"]
            except AttributeError:
                link = None

            try:
                price = seller.find("span", class_="tooltiptext-custom")
                total_element = price.find("th", string="Total price ")
                total_price = total_element.find_next_sibling("th").get_text(strip=True)
            except AttributeError:
                total_price = None

            defaults = {
                "publisher": publisher,
                "edition": edition,
                "language": language,
                "rating": rating,
                "title": title,
                "author": author,
                "seller": f"Name: {seller_name}, link: {link}",
                "price": total_price,
            }

            isbn_object, created = ISBN.objects.update_or_create(
                isbn=isbn.isbn, defaults=defaults
            )

            isbn_object.status = "Done"
            isbn_object.save()


book_searcher = BookSearcher()
book_searcher.search_books()
