#!/usr/bin/env python3
"""
Clean up already translated markdown files by removing unwanted prefixes
"""

import re
from pathlib import Path

def clean_translation_prefixes(content):
    """Remove translation prefixes from content"""
    prefixes_to_remove = [
        "Here is the translation of the text from Brazilian Portuguese to English:",
        "Here is the translation from Brazilian Portuguese to English:",
        "Here is the translation:",
        "Here's the translation:",
        "Translation:",
        "The translation is:",
        "Here is the English translation:",
        "Here's the English translation:",
        "English translation:",
        "Translated text:",
        "Here is the translated text:",
        "Here's the translated text:",
        "Here is the translation of the Brazilian Portuguese text to English:",
        "Translation from Portuguese to English:",
        "The English translation is:",
    ]

    for prefix in prefixes_to_remove:
        if content.strip().lower().startswith(prefix.lower()):
            content = content[len(prefix):].strip()
            break

    return content

def clean_markdown_file(file_path):
    """Clean a single markdown file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split frontmatter and body
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = '---' + parts[1] + '---'
            body = parts[2].strip()

            # Clean the body content
            cleaned_body = clean_translation_prefixes(body)

            # Check if cleaning was needed
            if cleaned_body != body:
                print(f"  → Cleaned prefixes from {file_path.name}")

                # Write back the cleaned content
                cleaned_content = frontmatter + '\n\n' + cleaned_body
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(cleaned_content)
                return True

    return False

def main():
    """Clean all translated markdown files"""
    input_dir = Path('markdown_posts_en')

    if not input_dir.exists():
        print("No translated files directory found")
        return

    md_files = list(input_dir.glob('*.md'))

    if not md_files:
        print("No translated markdown files found")
        return

    print(f"Checking {len(md_files)} translated markdown files for prefixes...")

    cleaned_count = 0

    for md_file in md_files:
        if clean_markdown_file(md_file):
            cleaned_count += 1

    print(f"\nCleaning complete! Fixed {cleaned_count} files.")

if __name__ == "__main__":
    main()
