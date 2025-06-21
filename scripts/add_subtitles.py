#!/usr/bin/env python3
"""
Add subtitles to blog posts that don't have them.
Keeps English and Portuguese versions in sync.
"""

import os
import re
import yaml
from pathlib import Path

# Subtitle mappings for posts based on their titles and content
SUBTITLES = {
    # Hello World and Early Posts
    "2008-05-12-hello-world": {
        "en": "My first steps into the world of blogging and sharing knowledge",
        "pt": "Meus primeiros passos no mundo dos blogs e compartilhamento de conhecimento"
    },

    # UML and Design Patterns
    "2008-06-10-uml-introducao-minicenarios": {
        "en": "Introduction to UML modeling through practical mini-scenarios",
        "pt": "Introdução à modelagem UML através de mini-cenários práticos"
    },
    "2008-06-13-minicenario-classificados-na-web": {
        "en": "Modeling web classifieds system using UML mini-scenarios",
        "pt": "Modelando sistema de classificados web usando mini-cenários UML"
    },
    "2008-06-17-minicenario-controle-de-bolao": {
        "en": "UML modeling for betting pool management systems",
        "pt": "Modelagem UML para sistemas de controle de bolão"
    },
    "2008-06-25-minicenario-estacionamento": {
        "en": "Parking management system design through UML scenarios",
        "pt": "Design de sistema de estacionamento através de cenários UML"
    }
}

def extract_frontmatter(content):
    """Extract YAML frontmatter from markdown content."""
    if not content.startswith('---'):
        return {}, content

    try:
        parts = content.split('---', 2)
        if len(parts) < 3:
            return {}, content

        frontmatter = yaml.safe_load(parts[1])
        body = parts[2].strip()
        return frontmatter, body
    except:
        return {}, content

def update_frontmatter(frontmatter, body, subtitle):
    """Update frontmatter with subtitle if not present."""
    if 'subtitle' not in frontmatter and 'description' not in frontmatter:
        frontmatter['subtitle'] = subtitle

    # Convert frontmatter back to YAML
    yaml_content = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)
    return f"---\n{yaml_content}---\n\n{body}"

def process_post(file_path, language):
    """Process a single post file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        frontmatter, body = extract_frontmatter(content)

        # Skip if already has subtitle or description
        if 'subtitle' in frontmatter or 'description' in frontmatter:
            print(f"✓ {file_path.name} already has subtitle/description")
            return False

        # Extract filename without extension for lookup
        filename_base = file_path.stem

        # Look up subtitle
        if filename_base in SUBTITLES:
            subtitle = SUBTITLES[filename_base][language]
            updated_content = update_frontmatter(frontmatter, body, subtitle)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)

            print(f"✓ Added subtitle to {file_path.name}: {subtitle}")
            return True
        else:
            print(f"⚠ No subtitle defined for {filename_base}")
            return False

    except Exception as e:
        print(f"✗ Error processing {file_path}: {e}")
        return False

def main():
    """Main function to process all posts."""
    script_dir = Path(__file__).parent
    content_dir = script_dir.parent / "content"

    en_posts_dir = content_dir / "en" / "posts"
    pt_posts_dir = content_dir / "pt" / "posts"

    updated_count = 0

    print("Processing English posts...")
    for post_file in en_posts_dir.glob("*.md"):
        if post_file.name != "_index.md":
            if process_post(post_file, "en"):
                updated_count += 1

    print("\nProcessing Portuguese posts...")
    for post_file in pt_posts_dir.glob("*.md"):
        if post_file.name != "_index.md":
            if process_post(post_file, "pt"):
                updated_count += 1

    print(f"\n✅ Updated {updated_count} posts with subtitles")

if __name__ == "__main__":
    main()
