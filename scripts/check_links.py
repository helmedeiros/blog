#!/usr/bin/env python3
import os
import sys
from collections import defaultdict
from functools import lru_cache
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse

SITE = "https://blog.heliomedeiros.com/"
ATTRS = {"href", "src", "poster", "data-src"}


class Refs(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if not value:
                continue
            if name in ATTRS and not (tag == "link" and dict(attrs).get("rel") in ("preconnect", "dns-prefetch")):
                self.refs.append(value)
            elif name in ("srcset", "data-srcset"):
                self.refs.extend(c.strip().split(" ")[0] for c in value.split(",") if c.strip())


@lru_cache(maxsize=None)
def listing(directory):
    try:
        return frozenset(os.listdir(directory))
    except OSError:
        return frozenset()


def exists(root, path):
    parent = root
    for part in path.relative_to(root).parts:
        if part not in listing(parent):
            return False
        parent = parent / part
    return True


def target(root, page_url, ref):
    url = urlparse(urljoin(page_url, ref.strip()))
    if url.scheme not in ("http", "https") or url.netloc != urlparse(SITE).netloc:
        return None
    path = root / unquote(url.path).lstrip("/")
    if url.path.endswith("/") or path.is_dir():
        return path / "index.html"
    return path


def main(root):
    root = Path(root)
    pages = sorted(root.rglob("*.html"))
    broken = defaultdict(set)
    checked = 0
    for page in pages:
        rel = page.relative_to(root).as_posix()
        page_url = urljoin(SITE, rel)
        parser = Refs()
        parser.feed(page.read_text(encoding="utf-8", errors="replace"))
        for ref in parser.refs:
            path = target(root, page_url, ref)
            if path is None:
                continue
            checked += 1
            if not exists(root, path):
                broken[urlparse(urljoin(page_url, ref)).path].add(rel)
    for link, sources in sorted(broken.items()):
        print(f"broken: {link} (from {len(sources)} page(s), e.g. {sorted(sources)[0]})")
    print(f"check_links: {len(pages)} pages, {checked} internal links, {len(broken)} broken targets")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "public"))
