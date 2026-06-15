from abc import ABC, abstractmethod
import requests

class BaseScraper(ABC):
    def __init__(self, name, source_type):
        """
        :param name: Name of the scraper (e.g., 'TikTokSkincare')
        :param source_type: Type of source ('social', 'news', 'marketplace')
        """
        self.name = name
        self.source_type = source_type
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        })

    @abstractmethod
    def scrape(self, query):
        """
        Executes the raw data extraction.
        """
        pass

    @abstractmethod
    def parse(self, raw_data):
        """
        Parses raw data into structured Trend objects.
        """
        pass

    def run_full_flow(self, query):
        print(f"[{self.name}] Starting scrape for: {query}")
        raw = self.scrape(query)
        if raw:
            structured = self.parse(raw)
            print(f"[{self.name}] Successfully parsed {len(structured)} trends.")
            return structured
        return []
