#!/usr/bin/env python3
import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
OUT = ROOT / "assets" / "diagrams"
STYLE = OUT / "style.puml"
SHORTCODE = re.compile(r"\{\{<\s*plantuml\b[^>]*>\}\}(.*?)\{\{<\s*/plantuml\s*>\}\}", re.S)


def diagrams():
    style = STYLE.read_text(encoding="utf-8")
    found = {}
    for page in sorted(CONTENT.rglob("*.md")):
        for match in SHORTCODE.finditer(page.read_text(encoding="utf-8")):
            source = match.group(1).strip()
            key = hashlib.md5((style + source).encode("utf-8")).hexdigest()
            styled = re.sub(r"^@startuml[^\n]*\n", lambda m: m.group(0) + style, source, count=1)
            found.setdefault(key, (styled, page.relative_to(ROOT).as_posix()))
    return found


def plantuml_command():
    if os.environ.get("PLANTUML_JAR"):
        return ["java", "-Djava.awt.headless=true", "-jar", os.environ["PLANTUML_JAR"]]
    if shutil.which("plantuml"):
        return ["plantuml", "-Djava.awt.headless=true"]
    sys.exit("render_diagrams: install PlantUML (brew install plantuml) or set PLANTUML_JAR")


def render(command, source, page):
    result = subprocess.run([*command, "-tsvg", "-pipe", "-charset", "UTF-8"], input=source.encode("utf-8"), capture_output=True)
    svg = result.stdout.decode("utf-8")
    if result.returncode != 0 or "<svg" not in svg:
        sys.exit(f"render_diagrams: PlantUML failed for a diagram in {page}:\n{result.stderr.decode('utf-8', 'replace')}{svg[:500]}")
    return svg


def main():
    parser = argparse.ArgumentParser(description="Render the PlantUML diagrams in content/ with assets/diagrams/style.puml to assets/diagrams/<md5 of style and source>.svg")
    parser.add_argument("--check", action="store_true", help="only report missing or unused SVGs")
    parser.add_argument("--force", action="store_true", help="re-render every diagram")
    args = parser.parse_args()

    found = diagrams()
    existing = {p.stem for p in OUT.glob("*.svg")}
    missing = sorted(set(found) - existing) if not args.force else sorted(found)
    unused = sorted(existing - set(found))

    if args.check:
        for key in missing:
            print(f"missing: assets/diagrams/{key}.svg (diagram in {found[key][1]})")
        for key in unused:
            print(f"unused: assets/diagrams/{key}.svg")
        print(f"render_diagrams: {len(found)} diagrams, {len(missing)} missing, {len(unused)} unused")
        if missing or unused:
            print("render_diagrams: run python3 scripts/render_diagrams.py and commit assets/diagrams/")
            return 1
        return 0

    OUT.mkdir(parents=True, exist_ok=True)
    command = plantuml_command() if missing else None
    for key in missing:
        source, page = found[key]
        (OUT / f"{key}.svg").write_text(render(command, source, page), encoding="utf-8")
    for key in unused:
        (OUT / f"{key}.svg").unlink()
    print(f"render_diagrams: {len(found)} diagrams, {len(missing)} rendered, {len(unused)} removed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
