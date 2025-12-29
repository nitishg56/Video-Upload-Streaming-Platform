from crawler import crawl_site
from content_parser import extract_clean_text
from module_inference import infer_modules


def extract_modules_from_url(start_url):
    """
    Extract modules while preserving page-level context.
    """

    pages = crawl_site(start_url)

    # ✅ Keep URL → parsed content mapping
    parsed_content_with_urls = {}

    for page_url, soup in pages.items():
        content = extract_clean_text(soup)

        # Ignore empty or junk pages
        if content and len(content) > 3:
            parsed_content_with_urls[page_url] = content

    # ✅ Pass URL-aware content to inference layer
    modules = infer_modules(parsed_content_with_urls)

    # ✅ Convert to required output format
    output = []
    for module_name, data in modules.items():
        output.append({
            "module": module_name,
            "Description": data.get("Description", "").strip(),
            "Submodules": data.get("Submodules", {})
        })

    return output
