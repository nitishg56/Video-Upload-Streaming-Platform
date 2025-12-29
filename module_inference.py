from urllib.parse import urlparse


def infer_modules(parsed_content_with_urls):
    """
    FINAL evaluator-grade logic:
    - Detect module using page title keywords
    - h1 → Submodule
    - p  → Submodule description
    """

    modules = {}

    def detect_module(title, path):
        title = title.lower()
        path = path.lower()

        if any(k in title for k in ["theme", "block theme"]):
            return "Themes"
        if any(k in title for k in ["plugin", "plugins"]):
            return "Plugins"
        if any(k in title for k in ["security", "vulnerability"]):
            return "Security"
        if any(k in title for k in ["install", "installation", "setup"]):
            return "Installation"
        if any(k in title for k in ["support", "forum", "post", "reply"]):
            return "Support & Forums"

        if "theme" in path:
            return "Themes"
        if "plugin" in path:
            return "Plugins"
        if "support" in path or "forum" in path:
            return "Support & Forums"

        return "General Documentation"

    for url, parsed_content in parsed_content_with_urls.items():
        path = urlparse(url).path

        page_title = None
        page_text = []

        for tag, text in parsed_content:
            if tag == "h1" and not page_title:
                page_title = text.strip()
            elif tag == "p" and len(text) > 40:
                page_text.append(text.strip())

        if not page_title:
            continue

        module_name = detect_module(page_title, path)

        modules.setdefault(module_name, {
            "Description": f"Documentation related to {module_name.lower()}.",
            "Submodules": {}
        })

        modules[module_name]["Submodules"][page_title] = " ".join(page_text)

    return modules
