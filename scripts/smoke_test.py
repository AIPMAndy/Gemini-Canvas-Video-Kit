#!/usr/bin/env python3
"""Check static HTML links before publishing (stdlib only)."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
ROOT = Path(__file__).resolve().parents[1]
FILES = [ROOT / "index.html", *sorted((ROOT / "examples").glob("*.html"))]
REQUIRED = [ROOT / "index.html", ROOT / "examples/launch-showcase.html", ROOT / "examples/knowledge-explainer.html", ROOT / ".nojekyll"]

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids = [], set()
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        for key in ("href", "src"):
            if attrs.get(key):
                self.links.append(attrs[key])

errors = []
for required in REQUIRED:
    if not required.is_file():
        errors.append(f"Missing required: {required.relative_to(ROOT)}")
for page in FILES:
    if not page.is_file():
        continue
    parser = LinkParser()
    parser.feed(page.read_text(encoding="utf-8"))
    for link in parser.links:
        parsed = urlparse(link)
        if parsed.scheme or parsed.netloc or link.startswith("//") or parsed.path.startswith("/"):
            continue
        target = (page.parent / unquote(parsed.path)).resolve() if parsed.path else page
        if not target.is_relative_to(ROOT):
            errors.append(f"Unsafe URL {page.name}: {link}")
        elif not target.is_file():
            errors.append(f"Broken relative link {page.relative_to(ROOT)} -> {link}")
        elif parsed.fragment and target == page and parsed.fragment not in parser.ids:
            errors.append(f"Broken anchor {page.relative_to(ROOT)} -> {link}")
if errors:
    raise SystemExit("\n".join(errors))
print(f"PASS: {len(FILES)} HTML files; all relative URLs and required pages valid")
