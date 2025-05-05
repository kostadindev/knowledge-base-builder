import requests
from typing import List
from bs4 import BeautifulSoup

class WebsiteProcessor:
    """Handle website content processing."""
    @staticmethod
    def get_urls_from_sitemap(sitemap_url: str) -> List[str]:
        """Extract URLs from a sitemap XML file."""
        response = requests.get(sitemap_url)
        if response.status_code != 200:
            raise Exception(f"Failed to load sitemap: {response.status_code}")
        soup = BeautifulSoup(response.text, "xml")
        return [loc.text for loc in soup.find_all("loc")]

    @staticmethod
    def download_and_clean_html(url: str) -> str:
        """Download HTML from a URL and clean it for processing."""
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to download HTML: {response.status_code}")
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        return soup.get_text(separator="\n", strip=True) 