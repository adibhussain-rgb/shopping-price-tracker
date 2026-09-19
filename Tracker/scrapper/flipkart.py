import requests
from bs4 import BeautifulSoup
from .base import BaseScraper


class FlipkartScraper(BaseScraper):
    def fetch(self, url):
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        price_tag = soup.find("div", class_="v1zwn21n v1zwn20 _1psv1zeb9 _1psv1ze0")
        if not price_tag:
            raise ValueError("Price not found on page")

        price_text = price_tag.text.replace("₹", "").replace(",", "")
        price = float(price_text)

        return {
            "price": price,
            "availability": True,
        }