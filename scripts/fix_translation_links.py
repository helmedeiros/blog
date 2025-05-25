#!/usr/bin/env python3
"""
Fix translation linking issues by removing conflicting URL parameters.

This script removes 'url' parameters from post front matter that prevent
Hugo from properly detecting translations between EN and PT versions.
"""

import os
import re
from pathlib import Path

def process_markdown_file(file_path):
    """Process a single markdown file to remove url parameter from front matter."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if file has front matter
        if not content.startswith('---'):
            return False

        # Find the end of front matter
        end_marker = content.find('---', 3)
        if end_marker == -1:
            return False

        front_matter = content[3:end_marker]
        post_content = content[end_marker:]

        # Check if url parameter exists
        url_pattern = r'^url:\s*.*$'
        if re.search(url_pattern, front_matter, re.MULTILINE):
            # Remove the url line
            new_front_matter = re.sub(url_pattern, '', front_matter, flags=re.MULTILINE)
            # Clean up any double newlines
            new_front_matter = re.sub(r'\n\n+', '\n', new_front_matter)

            # Reconstruct file
            new_content = f"---{new_front_matter}{post_content}"

            # Write back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            print(f"Removed 'url' parameter from {file_path}")
            return True

        return False

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main function to process all markdown files."""
    base_dir = Path('.')

    # Process both EN and PT content directories
    content_dirs = [
        'content/en/posts',
        'content/pt/posts'
    ]

    total_processed = 0
    total_modified = 0

    for content_dir in content_dirs:
        content_path = base_dir / content_dir

        if not content_path.exists():
            print(f"Directory {content_dir} does not exist, skipping...")
            continue

        print(f"\nProcessing {content_dir}...")

        # Find all markdown files
        md_files = list(content_path.glob('*.md'))

        for md_file in md_files:
            total_processed += 1
            if process_markdown_file(md_file):
                total_modified += 1

    print(f"\n=== Summary ===")
    print(f"Total files processed: {total_processed}")
    print(f"Total files modified: {total_modified}")
    print(f"Translation linking should now work properly!")

if __name__ == "__main__":
    main()
