#!/usr/bin/env python3
"""
Fix all YAML frontmatter issues in English translation files
"""

import re
from pathlib import Path

def fix_yaml_frontmatter(content, file_path):
    """Fix YAML frontmatter issues"""

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

        # Handle title field specially
        if line.startswith('title:'):
            # Extract title content
            title_content = line[6:].strip()

            # Remove quotes if present
            title_content = title_content.strip('"\'')

            # Clean up common issues
            if title_content.startswith('**Original'):
                # This is a broken title, try to extract meaningful content
                if 'Hadoop' in title_content or 'Big Data' in title_content:
                    title_content = "Hadoop and the Big Data Ecosystem"
                elif 'Impala' in title_content:
                    title_content = "How Impala has Pushed HDFS in New Ways"
                elif 'Data Science' in title_content:
                    title_content = "Building a Data Science Program at NASA/JPL"
                else:
                    # Use filename as fallback
                    title_content = file_path.stem.replace('-', ' ').title()

            # Skip continuation lines that are part of broken title
            j = i + 1
            while j < len(lines):
                next_line = lines[j].strip()
                if (next_line.startswith('Text:') or
                    next_line.startswith('**') or
                    'translated' in next_line.lower() or
                    'placeholder' in next_line.lower() or
                    not next_line.endswith(':') and ':' not in next_line):
                    j += 1
                else:
                    break

            fixed_lines.append(f'title: "{title_content}"')
            i = j
            continue

        # Skip invalid fields
        if (line.startswith('Note:') or
            line.startswith('Text:') or
            line.startswith('**') or
            'translated' in line.lower() or
            'placeholder' in line.lower()):
            i += 1
            continue

        # Handle other valid fields
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
    """Process a single file to fix YAML issues"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        fixed_content = fix_yaml_frontmatter(content, file_path)

        if fixed_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print(f"🔧 Fixed: {file_path.name}")
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
    print(f"🔧 Fixing YAML issues in {len(md_files)} English posts...\n")

    fixed_count = 0
    for md_file in md_files:
        if process_file(md_file):
            fixed_count += 1

    print(f"\n📊 Summary: Fixed YAML issues in {fixed_count}/{len(md_files)} files")

if __name__ == "__main__":
    main()
