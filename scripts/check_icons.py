#!/usr/bin/env python3
import re
import sys
from collections import defaultdict
from pathlib import Path

ICONS_CSS = Path(__file__).resolve().parent.parent / "assets" / "css" / "icons.css"
MODIFIERS = {"fa-stack", "fa-stack-1x", "fa-stack-2x", "fa-inverse", "fa-lg", "fa-fw", "fa-solid", "fa-regular", "fa-brands"}
CLASS = re.compile(r'class=(?:"([^"]*)"|([^\s>]+))')


def main(root):
    available = set(re.findall(r"\.fa-([a-z0-9-]+):before", ICONS_CSS.read_text()))
    missing = defaultdict(set)
    styles = defaultdict(set)
    pages = 0
    for page in Path(root).rglob("*.html"):
        pages += 1
        body = page.read_text(encoding="utf-8", errors="replace").partition("</head>")[2]
        for match in CLASS.finditer(body):
            classes = (match.group(1) or match.group(2)).split()
            if not ({"fa", "fas", "far", "fab"} & set(classes)):
                continue
            rel = page.relative_to(root).as_posix()
            for style in {"far", "fab"} & set(classes):
                styles[style].add(rel)
            for cls in classes:
                if cls.startswith("fa-") and cls not in MODIFIERS and cls[3:] not in available:
                    missing[cls].add(rel)
    for cls, sources in sorted(missing.items()):
        print(f"missing icon: {cls} (on {len(sources)} page(s), e.g. {sorted(sources)[0]}); add it to {ICONS_CSS.name} and the font subset")
    for style, sources in sorted(styles.items()):
        print(f"unsupported icon style: {style} (on {len(sources)} page(s), e.g. {sorted(sources)[0]}); only solid icons are bundled")
    print(f"check_icons: {pages} pages, {len(available)} bundled icons, {len(missing)} missing, {len(styles)} unsupported styles")
    return 1 if missing or styles else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "public"))
