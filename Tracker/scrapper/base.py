class BaseScraper:
    def fetch(self, url):
        raise NotImplementedError("Each scraper must implement its own fetch method")