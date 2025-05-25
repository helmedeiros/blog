#!/usr/bin/env python3
"""
Convert translated markdown files to Hugo content structure

This script takes our translated English markdown files and creates proper
Hugo content files that can be used to regenerate the HTML blog structure.
"""

import os
import re
from pathlib import Path
import shutil

def parse_frontmatter(content):
    """Parse YAML frontmatter from markdown"""
    if not content.startswith('---'):
        return {}, content

    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content

    frontmatter_text = parts[1].strip()
    body = parts[2].strip()

    # Simple YAML parsing for our use case
    frontmatter = {}
    for line in frontmatter_text.split('\n'):
        line = line.strip()
        if ':' in line and not line.startswith('-'):
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"\'')
            frontmatter[key] = value

    return frontmatter, body

def create_hugo_frontmatter(frontmatter, body):
    """Create Hugo-compatible frontmatter"""

    # Extract first paragraph for description
    lines = body.split('\n')
    description_lines = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#'):
            description_lines.append(line)
            if len(' '.join(description_lines)) > 100:  # Reasonable description length
                break

    description = ' '.join(description_lines)[:150] + ('...' if len(' '.join(description_lines)) > 150 else '')

    # Create Hugo frontmatter
    hugo_frontmatter = f'''---
title: {frontmatter.get('title', '""')}
date: {frontmatter.get('date', '')}
slug: {frontmatter.get('slug', '')}
draft: false
description: "{description}"
language: en
tags: []
---'''

    return hugo_frontmatter

def convert_markdown_file(md_file_path, content_dir):
    """Convert a single markdown file to Hugo content structure"""

    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse frontmatter and body
    frontmatter, body = parse_frontmatter(content)

    if not frontmatter.get('slug'):
        print(f"  ⚠ No slug found in {md_file_path.name}, skipping")
        return None

    slug = frontmatter['slug']

    # Create Hugo frontmatter
    hugo_frontmatter = create_hugo_frontmatter(frontmatter, body)

    # Create Hugo-compatible content
    hugo_content = f"{hugo_frontmatter}\n\n{body}"

    # Create content file path (Hugo expects .md files in content directory)
    content_file = content_dir / f"{slug}.md"

    with open(content_file, 'w', encoding='utf-8') as f:
        f.write(hugo_content)

    return content_file

def backup_existing_content(backup_dir):
    """Backup existing content before replacing"""
    posts_dir = Path('content/posts')
    if posts_dir.exists():
        backup_dir.mkdir(exist_ok=True)
        if (backup_dir / 'posts').exists():
            shutil.rmtree(backup_dir / 'posts')
        shutil.copytree(posts_dir, backup_dir / 'posts')
        print(f"✓ Backed up existing content to {backup_dir}")

def main():
    """Convert all translated markdown files to Hugo content structure"""

    input_dir = Path('markdown_posts_en')
    content_dir = Path('content/posts')
    backup_dir = Path('content_backup')

    if not input_dir.exists():
        print(f"Error: Input directory {input_dir} not found")
        return

    # Create content directory structure
    content_dir.mkdir(parents=True, exist_ok=True)

    # Backup existing content
    backup_existing_content(backup_dir)

    # Get list of markdown files
    md_files = sorted([f for f in input_dir.glob('*.md') if not f.name.endswith('.backup')])

    if not md_files:
        print("No markdown files found to convert")
        return

    print(f"Converting {len(md_files)} markdown files to Hugo content structure")
    print(f"Output directory: {content_dir}")

    converted_count = 0
    for md_file in md_files:
        print(f"Converting: {md_file.name}")

        try:
            content_file = convert_markdown_file(md_file, content_dir)
            if content_file:
                print(f"  ✓ Created: {content_file}")
                converted_count += 1
            else:
                print(f"  ✗ Failed to convert")

        except Exception as e:
            print(f"  ✗ Error: {e}")

    print(f"\nConversion complete!")
    print(f"Converted: {converted_count}/{len(md_files)} files")
    print(f"Hugo content files saved to: {content_dir}")
    print(f"\nNext steps:")
    print(f"1. Run 'hugo server' to test the site")
    print(f"2. Run 'hugo' to build static files")
    print(f"3. Deploy the generated public/ directory")

if __name__ == "__main__":
    main()
