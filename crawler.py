import requests
from bs4 import BeautifulSoup
from utils import normalize_url, is_same_domain


def crawl_site(start_url, max_pages=50):
    """
    Recursively crawl ONLY documentation-related pages
    and ignore homepage / marketing / UI sections.
    """
    visited = set()
    pages = {}

    def is_documentation_url(url: str) -> bool:
        """
        Allow only documentation-like URLs
        """
        doc_keywords = [
            "/documentation",
            "/docs",
            "/doc",
            "/support",
            "/hc/"
        ]
        return any(keyword in url.lower() for keyword in doc_keywords)

    def crawl(url):
        if url in visited or len(visited) >= max_pages:
            return

        # 🚫 Skip non-documentation URLs
        if not is_documentation_url(url):
            return

        visited.add(url)

        try:
            response = requests.get(
                url,
                timeout=10,
                headers={
                    "User-Agent": "Mozilla/5.0 (ModuleExtractorBot)"
                }
            )

            if response.status_code != 200:
                return

            soup = BeautifulSoup(response.text, "lxml")
            pages[url] = soup

            for a in soup.find_all("a", href=True):
                next_url = normalize_url(url, a["href"])
                if is_same_domain(start_url, next_url):
                    crawl(next_url)

        except requests.RequestException:
            pass

    crawl(start_url)
    return pages
