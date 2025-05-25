#!/usr/bin/env python3
"""
Fix broken title quotes in YAML frontmatter
"""

import re
from pathlib import Path

def fix_yaml_title(content):
    """Fix broken title quotes in YAML frontmatter"""

    lines = content.split('\n')
    fixed_lines = []
    in_frontmatter = False

    for line in lines:
        if line.strip() == '---':
            if not in_frontmatter:
                in_frontmatter = True
            else:
                in_frontmatter = False
            fixed_lines.append(line)
        elif in_frontmatter and line.startswith('title:'):
            # Check if title has opening quote but no closing quote
            if line.count('"') == 1 and line.strip().endswith('"') == False:
                # Add closing quote
                fixed_line = line + '"'
                fixed_lines.append(fixed_line)
                print(f"  Fixed title: {line} -> {fixed_line}")
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)

    return '\n'.join(fixed_lines)

def process_file(file_path):
    """Process a single file to fix YAML titles"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        fixed_content = fix_yaml_title(content)

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
    print(f"🔧 Fixing YAML title quotes in {len(md_files)} English posts...\n")

    fixed_count = 0
    for md_file in md_files:
        if process_file(md_file):
            fixed_count += 1

    print(f"\n📊 Summary: Fixed YAML titles in {fixed_count}/{len(md_files)} files")

if __name__ == "__main__":
    main()
