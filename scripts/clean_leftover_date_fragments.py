#!/usr/bin/env python3
"""
Clean up leftover date fragments in English translation files
"""

import re
from pathlib import Path

def clean_date_fragments(content):
    """Remove leftover date fragments from frontmatter"""

    lines = content.split('\n')
    cleaned_lines = []
    in_frontmatter = False

    for line in lines:
        if line.strip() == '---':
            if not in_frontmatter:
                in_frontmatter = True
            else:
                in_frontmatter = False
            cleaned_lines.append(line)
        elif in_frontmatter:
            # Skip lines that look like leftover date fragments
            line_stripped = line.strip()
            if (re.match(r'^\d{2}T\d{2}:\s*$', line_stripped) or  # "12T20: "
                re.match(r'^\d{2}:\s*\d{2}\+\s*$', line_stripped) or  # "16: 38+ "
                re.match(r'^\d{2}:\s*\d{2}\s*$', line_stripped) or   # "00: 00"
                re.match(r'^T\d{2}:\s*$', line_stripped) or         # "T20: "
                re.match(r'^\d{2}:\s*$', line_stripped) or          # "16: "
                re.match(r'^\d{2}\+\s*$', line_stripped) or         # "38+ "
                re.match(r'^\d{2}\s*$', line_stripped)):            # "00"
                continue  # Skip this line
            else:
                cleaned_lines.append(line)
        else:
            cleaned_lines.append(line)

    return '\n'.join(cleaned_lines)

def process_file(file_path):
    """Process a single file to clean date fragments"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        cleaned_content = clean_date_fragments(content)

        if cleaned_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            print(f"🔧 Cleaned: {file_path.name}")
            return True
        else:
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
    print(f"🔧 Cleaning date fragments in {len(md_files)} English posts...\n")

    cleaned_count = 0
    for md_file in md_files:
        if process_file(md_file):
            cleaned_count += 1

    print(f"\n📊 Summary: Cleaned date fragments in {cleaned_count}/{len(md_files)} files")

if __name__ == "__main__":
    main()
