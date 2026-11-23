#!/usr/bin/env python3
"""Check static HTML links before publishing (stdlib only)."""
from html.parser import HTMLParser
from pathlib import Path
import hashlib, json, re, xml.etree.ElementTree as ET
from urllib.parse import urlparse, unquote
ROOT = Path(__file__).resolve().parents[1]
FILES = [ROOT / "index.html", ROOT / "review.html", *sorted((ROOT / "examples").glob("*.html"))]
REQUIRED = [ROOT / "index.html", ROOT / "review.html", ROOT / "robots.txt", ROOT / "sitemap.xml", ROOT / "pdf/Gemini-Canvas-Video-Kit-guide.pdf", ROOT / "examples/launch-showcase.html", ROOT / "examples/knowledge-explainer.html", ROOT / ".nojekyll"]

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
# Enforce verifiable SEO data; no invented WebApplication claims.
base = "https://aipmandy.github.io/Gemini-Canvas-Video-Kit/"
sitemap = ET.parse(ROOT / "sitemap.xml").getroot()
urls = [item.text for item in sitemap.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
if base not in urls or base + "review.html" not in urls:
    errors.append("Sitemap missing homepage or review workbench")
if "Sitemap: " + base + "sitemap.xml" not in (ROOT / "robots.txt").read_text(encoding="utf-8"):
    errors.append("Robots sitemap mismatch")
review = (ROOT / "review.html").read_text(encoding="utf-8")
if '<link rel="canonical" href="' + base + 'review.html">' not in review:
    errors.append("Wrong review canonical")
if review.count("<h1") != 1:
    errors.append("Review workbench must have exactly one H1")
for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', review, re.S):
    try:
        obj = json.loads(block)
        if obj.get("@type") != "WebApplication" or obj.get("url") != base + "review.html":
            errors.append("Invalid review structured data")
    except ValueError:
        errors.append("Invalid JSON-LD")
if 'review.html' not in (ROOT / "index.html").read_text(encoding="utf-8"):
    errors.append("Missing homepage tool entry")
edition = json.loads((ROOT / "pdf/edition.json").read_text(encoding="utf-8"))
pdf = ROOT / edition["pdf_path"]
if not pdf.is_file() or hashlib.sha256(pdf.read_bytes()).hexdigest() != edition["sha256"]:
    errors.append("Original PDF SHA does not match edition; do not silently replace")
for required_brand in ("AIPMAndy", "https://metaver.vip/", "https://metaver.vip/services", "https://www.a6no1.cn/"):
    if required_brand not in review:
        errors.append("Missing approved contact: " + required_brand)
if errors:
    raise SystemExit("\n".join(errors))
print(f"PASS: {len(FILES)} HTML files; all relative URLs and required pages valid")
