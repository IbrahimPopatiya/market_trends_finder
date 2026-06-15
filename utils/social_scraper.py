from system.base_scraper import BaseScraper
import json

class SocialScraper(BaseScraper):
    def scrape(self, query):
        """
        Simulated TikTok/Reddit scraping for trends.
        """
        print(f"[SocialScraper] Searching for related hashtags/posts for: {query}")
        # In a real scenario, this would use BeautifulSoup or an internal tool
        mock_raw_data = [
            {"product": "GlowStick", "views": "1.2M", "mentions": "TikTok"},
            {"product": "SkinShield", "views": "800K", "mentions": "Reddit"}
        ]
        return mock_raw_data

    def parse(self, raw_data):
        """
        Turns raw JSON into structured Trend objects.
        """
        trends = []
        for item in raw_data:
            trends.append({
                "platform": item["mentions"],
                "topic": item["product"],
                "viral_score": float(item["views"].replace("M", "")) * 100 if "M" in item["views"] else float(item["views"].replace("K", "")),
                "description": f"Trending Product: {item['product']} on {item['mentions']}",
                "url": f"https://{item['mentions'].lower()}.com/search?q={item['product']}"
            })
        return trends
