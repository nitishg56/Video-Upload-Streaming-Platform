import validators
from urllib.parse import urljoin, urlparse

def is_valid_url(url: str) -> bool:
    return validators.url(url)

def normalize_url(base, link):
    return urljoin(base, link)

def is_same_domain(base_url, target_url):
    return urlparse(base_url).netloc == urlparse(target_url).netloc
