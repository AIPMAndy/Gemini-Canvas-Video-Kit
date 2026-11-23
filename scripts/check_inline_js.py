#!/usr/bin/env python3
"""Parse inline JavaScript from the public source pages and run node --check."""
from html.parser import HTMLParser
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
class Scripts(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active = False
        self.parts = []
        self.scripts = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.active = tag == "script" and "src" not in attrs and attrs.get("type", "text/javascript") in ("text/javascript", "module")
        if self.active:
            self.parts = []
    def handle_data(self, data):
        if self.active:
            self.parts.append(data)
    def handle_endtag(self, tag):
        if tag == "script" and self.active:
            self.scripts.append("".join(self.parts))
            self.active = False

for path in (ROOT / "index.html", ROOT / "review.html"):
    parser = Scripts()
    parser.feed(path.read_text(encoding="utf-8"))
    assert parser.scripts, f"{path.name}: no inline JS detected"
    for i, code in enumerate(parser.scripts, 1):
        with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8") as tmp:
            tmp.write(code)
            tmp.flush()
            subprocess.run(["node", "--check", tmp.name], check=True)
            print(f"PASS: {path.name} inline script {i}")
