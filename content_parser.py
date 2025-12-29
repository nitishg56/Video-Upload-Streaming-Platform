def extract_clean_text(soup):
    """
    Robust content extractor for:
    - WordPress
    - Zluri
    - Chargebee
    - Zendesk (Neo)
    """

    # ✅ Try multiple known documentation containers
    main = (
        soup.find("article") or
        soup.find("main") or
        soup.find("section", {"role": "main"}) or
        soup.find("div", class_="article-body") or
        soup.find("div", class_="article-content") or
        soup.find("body")
    )

    if not main:
        return []

    # ❌ Remove noise
    for tag in main(["nav", "footer", "header", "aside", "script", "style", "form"]):
        tag.decompose()

    content = []

    for tag in main.find_all(["h1", "h2", "h3", "p", "li"], recursive=True):
        text = tag.get_text(" ", strip=True)

        if len(text) < 30:
            continue

        # Ignore cookie banners & auth noise
        noise = ["cookie", "privacy policy", "sign in", "log in"]
        if any(n in text.lower() for n in noise):
            continue

        content.append((tag.name, text))

    return content
