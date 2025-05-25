#!/usr/bin/env python3
"""
Fix YAML frontmatter formatting in English translation files
"""

import re
from pathlib import Path

def fix_frontmatter(content):
    """Fix YAML frontmatter formatting"""

    if not content.startswith('---'):
        return content

    # Split content into frontmatter and body
    parts = content.split('---', 2)
    if len(parts) < 3:
        return content

    frontmatter = parts[1].strip()
    body = parts[2].strip()

    # Fix common frontmatter issues
    lines = frontmatter.split('\n')
    fixed_lines = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if not line:
            i += 1
            continue

        # Handle date field specially
        if line.startswith('date:'):
            # Reconstruct the date if it was broken across lines
            date_value = line[5:].strip()

            # Look ahead for continuation of date
            j = i + 1
            while j < len(lines) and not lines[j].strip().endswith(':') and lines[j].strip():
                date_value += lines[j].strip()
                j += 1

            # Fix common date format issues
            date_value = re.sub(r'(\d{4}-\d{2}-\d{2})T(\d{2}):(\d{2}):(\d{2})\+(\d{2}):(\d{2})',
                               r'\1T\2:\3:\4+\5:\6', date_value)

            fixed_lines.append(f'date: {date_value}')
            i = j
            continue

        # Handle other fields
        if ':' in line:
            field_name = line.split(':')[0].strip()
            field_value = ':'.join(line.split(':')[1:]).strip()

            # Handle categories and tags (list fields)
            if field_name in ['categories', 'tags']:
                fixed_lines.append(f'{field_name}:')

                # Look for list items
                j = i + 1
                while j < len(lines):
                    next_line = lines[j].strip()
                    if next_line.startswith('-'):
                        fixed_lines.append(f'  {next_line}')
                        j += 1
                    elif next_line and ':' in next_line:
                        break
                    elif next_line:
                        # Single item, convert to list
                        fixed_lines.append(f'  - {next_line}')
                        j += 1
                    else:
                        j += 1
                        break

                i = j
                continue

            # Regular field
            fixed_lines.append(f'{field_name}: {field_value}')

        i += 1

    # Reconstruct the file
    fixed_frontmatter = '\n'.join(fixed_lines)
    return f'---\n{fixed_frontmatter}\n---\n\n{body}'

def process_file(file_path):
    """Process a single file to fix frontmatter"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        fixed_content = fix_frontmatter(content)

        if fixed_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print(f"🔧 Fixed: {file_path.name}")
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
    print(f"🔧 Fixing frontmatter in {len(md_files)} English posts...\n")

    fixed_count = 0
    for md_file in md_files:
        if process_file(md_file):
            fixed_count += 1

    print(f"\n📊 Summary: Fixed frontmatter in {fixed_count}/{len(md_files)} files")

if __name__ == "__main__":
    main()
