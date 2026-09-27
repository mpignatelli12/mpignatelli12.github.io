#!/usr/bin/env python3
"""
Adds (or updates) a <link rel="canonical" href="..."> tag in every top-level
HTML page, pointing at the matching URL on michaelpignatelli.com.

Run from the repo root. Safe to re-run — it replaces an existing canonical
tag rather than duplicating it, so it's fine to run on every CI build.
"""
import re
from pathlib import Path

DOMAIN = "https://michaelpignatelli.com"
ROOT = Path(__file__).resolve().parent.parent

CANONICAL_RE = re.compile(
    r'^[ \t]*<link\s+rel="canonical"[^>]*>[ \t]*\n?', re.IGNORECASE | re.MULTILINE
)


def canonical_url(html_path: Path) -> str:
    name = html_path.name
    if name == "index.html":
        return f"{DOMAIN}/"
    return f"{DOMAIN}/{name}"


def process(html_path: Path) -> bool:
    text = html_path.read_text(encoding="utf-8")
    url = canonical_url(html_path)
    tag = f'    <link rel="canonical" href="{url}" />\n'

    # Strip any existing canonical tag first, so re-runs don't duplicate.
    text_no_canonical = CANONICAL_RE.sub("", text)

    # Insert right after the <head> tag.
    head_match = re.search(r"(<head[^>]*>\s*\n)", text_no_canonical, re.IGNORECASE)
    if not head_match:
        print(f"  SKIPPED (no <head> found): {html_path.name}")
        return False

    insert_at = head_match.end()
    new_text = text_no_canonical[:insert_at] + tag + text_no_canonical[insert_at:]

    if new_text != text:
        html_path.write_text(new_text, encoding="utf-8")
        print(f"  updated: {html_path.name} -> {url}")
        return True

    print(f"  unchanged: {html_path.name}")
    return False


def main():
    html_files = sorted(ROOT.glob("*.html"))
    if not html_files:
        print("No .html files found at repo root.")
        return

    print(f"Adding canonical tags pointing at {DOMAIN} ...")
    for f in html_files:
        process(f)


if __name__ == "__main__":
    main()