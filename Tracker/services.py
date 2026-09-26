from django.db.models import Min, Max
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


def get_current_price(product):
    latest_record = PriceRecord.objects.filter(product=product).order_by("-collected_at").first()
    return latest_record.price if latest_record else None


def get_lowest_price(product):
    result = PriceRecord.objects.filter(product=product).aggregate(Min("price"))
    return result["price__min"]


def get_highest_price(product):
    result = PriceRecord.objects.filter(product=product).aggregate(Max("price"))
    return result["price__max"]


def get_price_change(product):
    records = PriceRecord.objects.filter(product=product).order_by("-collected_at")[:2]
    if len(records) < 2:
        return None

    latest, previous = records[0], records[1]
    return latest.price - previous.price


def get_best_price_comparison(product_name):
    matching_products = Product.objects.filter(name=product_name, is_active=True)

    comparison = []
    for product in matching_products:
        current = get_current_price(product)
        if current is not None:
            comparison.append({"store": product.store, "price": current})

    comparison.sort(key=lambda x: x["price"])
    return comparison


def check_price_alert(product):
    if product.target_price is None:
        return False

    current = get_current_price(product)
    if current is None:
        return False

    return current <= product.target_price