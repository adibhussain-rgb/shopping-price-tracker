from .models import Product, PriceRecord, CollectionLog
from .scrapper.flipkart import FlipkartScraper

SCRAPER_REGISTRY = {
    "Flipkart": FlipkartScraper,
}


def collect_price(product):
    scraper_class = SCRAPER_REGISTRY.get(product.store)
    if not scraper_class:
        raise ValueError(f"No scraper registered for store: {product.store}")

    scraper = scraper_class()

    try:
        result = scraper.fetch(product.url)
        PriceRecord.objects.create(
            product=product,
            price=result["price"],
            availability=result["availability"],
        )
        CollectionLog.objects.create(
            product=product,
            status="success",
        )
    except Exception as e:
        CollectionLog.objects.create(
            product=product,
            status="failed",
            error_message=str(e),
        )