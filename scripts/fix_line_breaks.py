#!/usr/bin/env python3
"""
Fix corrupted line breaks in English translation files

The English files have been corrupted and lost their line breaks,
making them single-line files. This script restores proper formatting.
"""

import re
from pathlib import Path

def fix_line_breaks(content):
    """Restore proper line breaks to markdown content"""

    # First, let's identify the frontmatter section
    if content.startswith('---'):
        # Find the end of frontmatter
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            body = parts[2]

            # Fix frontmatter - add line breaks after each field
            frontmatter = re.sub(r'(\w+:)', r'\n\1', frontmatter)
            frontmatter = re.sub(r'^\n', '', frontmatter)  # Remove leading newline
            frontmatter = re.sub(r'(\s+)-\s+', r'\n  - ', frontmatter)  # Fix list items

            # Fix body content
            body = fix_body_content(body)

            return f"---{frontmatter}\n---\n{body}"

    # If no frontmatter, just fix the body
    return fix_body_content(content)

def fix_body_content(content):
    """Fix line breaks in the body content"""

    # Add line breaks after common sentence endings
    content = re.sub(r'(\.) ([A-Z])', r'\1\n\n\2', content)
    content = re.sub(r'(\!) ([A-Z])', r'\1\n\n\2', content)
    content = re.sub(r'(\?) ([A-Z])', r'\1\n\n\2', content)

    # Add line breaks after colons when followed by uppercase
    content = re.sub(r'(:) ([A-Z])', r'\1\n\n\2', content)

    # Fix markdown headers (add line breaks before #)
    content = re.sub(r'([^#])(\s*#{1,6}\s+)', r'\1\n\n\2', content)

    # Fix markdown lists (add line breaks before list items)
    content = re.sub(r'([^-\n])(\s*-\s+)', r'\1\n\n\2', content)
    content = re.sub(r'([^*\n])(\s*\*\s+)', r'\1\n\n\2', content)
    content = re.sub(r'([^\d\n])(\s*\d+\.\s+)', r'\1\n\n\2', content)

    # Fix markdown links and images (ensure proper spacing)
    content = re.sub(r'(\]\([^)]+\))([A-Z])', r'\1\n\n\2', content)

    # Fix HTML tags (add line breaks around block elements)
    content = re.sub(r'(</?(?:div|p|h[1-6]|blockquote|pre|ul|ol|li)[^>]*>)', r'\n\1\n', content)

    # Clean up excessive whitespace
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    content = re.sub(r'^\s+', '', content)  # Remove leading whitespace
    content = re.sub(r'\s+$', '', content)  # Remove trailing whitespace

    return content

def process_file(file_path):
    """Process a single file to fix line breaks"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if file needs fixing (single line with lots of content)
        lines = content.split('\n')
        if len(lines) <= 3 and len(content) > 200:
            print(f"🔧 Fixing: {file_path.name}")

            fixed_content = fix_line_breaks(content)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)

            return True
        else:
            print(f"✅ OK: {file_path.name}")
            return False

    except Exception as e:
        print(f"❌ Error processing {file_path.name}: {e}")
        return False

def main():
    posts_dir = Path('content/en/posts')

    if not posts_dir.exists():
        print(f"Error: Directory {posts_dir} not found")
        return

    md_files = list(posts_dir.glob('*.md'))
    print(f"🔧 Fixing line breaks in {len(md_files)} English posts...\n")

    fixed_count = 0
    for md_file in md_files:
        if process_file(md_file):
            fixed_count += 1

    print(f"\n📊 Summary: Fixed line breaks in {fixed_count}/{len(md_files)} files")

if __name__ == "__main__":
    main()
