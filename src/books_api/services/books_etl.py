import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup


def extract_books() -> list[dict]:
    BASE_URL = "https://books.toscrape.com"

    books_raw = []

    CONTINUE = True
    books_url = f"{BASE_URL}/catalogue/page-1.html"
    while CONTINUE:
        try:
            books_response = requests.get(books_url)
            books_response.raise_for_status()
        except HTTPError as http_err:
            CONTINUE = False
            print(http_err)
        else:
            books_html = BeautifulSoup(books_response.text, "lxml")

            books_info = books_html.find_all("article", class_="product_pod")
            for book_info in books_info:
                book_id = book_info.find("h3").find("a").get("href")
                book_title = book_info.find("h3").find("a").get("title")
                book_price = book_info.select_one(".product_price .price_color").text
                book_rating = book_info.select_one(".star-rating").get("class")[1]
                book_image = book_info.find(class_="image_container").find("img").get("src")

                book_url = f'{BASE_URL}/catalogue/{book_id}'
                book_response = requests.get(book_url)
                book_html = BeautifulSoup(book_response.text, "lxml")

                book_availability = book_html.select_one(".availability").text
                book_category = book_html.find("ul", class_="breadcrumb").find_all("li")[2].find("a").text

                books_raw.append({
                    "book_id": book_id,
                    "book_title": book_title,
                    "book_price": book_price,
                    "book_rating": book_rating,
                    "book_image": book_image,
                    "book_availability": book_availability,
                    "book_category": book_category,
                })

            # next_page = books_html.find(class_="pager").find(class_="next")
            next_page = books_html.select_one(".pager .next")
            CONTINUE = next_page is not None
            if CONTINUE:
                books_url = f'{BASE_URL}/catalogue/{next_page.find("a").get("href")}'

    return books_raw


def transform_books(books_raw: list[dict]) -> list[dict]:
    books_transformed = []

    return books_transformed


def load_books(books_transformed: list[dict], dry_run: bool = False) -> None:
    pass


if __name__ == "__main__":
    books_raw = extract_books()
    books_transformed = transform_books(books_raw)
    load_books(books_transformed, dry_run=True)
