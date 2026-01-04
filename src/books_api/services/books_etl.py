import re
import asyncio
import requests
from requests.exceptions import HTTPError
import httpx
from bs4 import BeautifulSoup, Tag

from src.books_api.models.persistent_storage.interfaces.books_repository_interface import IBooksRepository


BASE_URL = "https://books.toscrape.com"


async def fetch_book(httpx_async_client: httpx.AsyncClient, book_info: Tag) -> dict:
    book_id = book_info.find("h3").find("a").get("href")
    book_title = book_info.find("h3").find("a").get("title")
    book_price = book_info.select_one(".product_price .price_color").text
    book_rating = book_info.select_one(".star-rating").get("class")[1]
    book_image = book_info.find(class_="image_container").find("img").get("src")

    book_url = f'{BASE_URL}/catalogue/{book_id}'
    book_response = await httpx_async_client.get(book_url)
    book_html = BeautifulSoup(book_response.text, "lxml")

    book_availability = book_html.select_one(".availability").text
    book_category = book_html.find("ul", class_="breadcrumb").find_all("li")[2].find("a").text

    return {
        "book_id": book_id,
        "book_title": book_title,
        "book_price": book_price,
        "book_rating": book_rating,
        "book_image": book_image,
        "book_availability": book_availability,
        "book_category": book_category,
    }


async def extract_books() -> list[dict]:
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
            async with httpx.AsyncClient() as client:
                tasks = [fetch_book(client, book_info) for book_info in books_info]
                books_raw_current_page = await asyncio.gather(*tasks)
                books_raw.extend(books_raw_current_page)

            # next_page = books_html.find(class_="pager").find(class_="next")
            next_page = books_html.select_one(".pager .next")
            CONTINUE = next_page is not None
            if CONTINUE:
                books_url = f'{BASE_URL}/catalogue/{next_page.find("a").get("href")}'

    return books_raw


def transform_books(books_raw: list[dict]) -> list[dict]:
    books_transformed = []

    book_id_pattern = re.compile(r"(?P<book_id>\d*)/index.html$")
    book_availability_pattern = re.compile(r"(?P<book_availability>\d*)\s+available")

    ratings_map = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5,
    }

    for book_raw in books_raw:
        book_id = int(
            book_id_pattern
            .search(book_raw["book_id"])
            .group("book_id")
        )
        book_price = float(book_raw["book_price"][2:])
        book_rating = ratings_map.get(book_raw["book_rating"], 0)
        book_availability = int(
            book_availability_pattern
            .search(book_raw["book_availability"])
            .group("book_availability")
        )
        book_image = f'{BASE_URL}/{book_raw["book_image"][3:]}'

        books_transformed.append({
            "book_id": book_id,
            "titulo": book_raw["book_title"],
            "preco": book_price,
            "rating": book_rating,
            "disponibilidade": book_availability,
            "categoria": book_raw["book_category"],
            "url_imagem": book_image,
        })

    return books_transformed


def load_books(books_repo: IBooksRepository, books_transformed: list[dict], dry_run: bool) -> None:
    if dry_run:
        conn = books_repo.get_db_connection()
        if not conn.is_connected():
            raise ConnectionError("Conexão com BD não estabelecida.")
    else:
        books_repo.insert_books(books_transformed)


async def run_etl(books_repo: IBooksRepository, dry_run: bool = False) -> None:
    books_raw = await extract_books()
    books_transformed = transform_books(books_raw)
    books_transformed.sort(key=lambda x: x["book_id"])
    load_books(books_repo, books_transformed, dry_run=dry_run)
