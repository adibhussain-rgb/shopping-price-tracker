import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management.base import BaseCommand
from Tracker.models import Product
from Tracker.services import collect_price

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_price_collection():
    active_products = Product.objects.filter(is_active=True)
    logger.info(f"Starting price collection for {active_products.count()} products")

    for product in active_products:
        try:
            collect_price(product)
            logger.info(f"Collected price for {product.name}")
        except Exception as e:
            logger.error(f"Failed to collect price for {product.name}: {e}")


class Command(BaseCommand):
    help = "Runs the price collection job every 4 hours"

    def handle(self, *args, **options):
        scheduler = BlockingScheduler()
        scheduler.add_job(run_price_collection, "interval", hours=4)

        self.stdout.write("Scheduler started. Checking prices every 4 hours...")

        run_price_collection()  # run once immediately on startup

        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            self.stdout.write("Scheduler stopped.")