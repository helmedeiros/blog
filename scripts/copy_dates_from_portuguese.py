#!/usr/bin/env python3
"""
Copy correct date fields from Portuguese files to English files
"""

import re
from pathlib import Path

def extract_date_from_file(file_path):
    """Extract the date field from a markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Look for date field in frontmatter
        match = re.search(r'^date:\s*(.+)$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()

        return None
    except:
        return None

def fix_date_in_english_file(en_file_path, correct_date):
    """Fix the date field in an English file"""
    try:
        with open(en_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Replace the broken date field with the correct one
        # First, try to match the broken multi-line date pattern
        pattern = r'date:\s*\d{4}-\d{2}-\d{2}(?:\s*T\d{2}:\s*\d{2}:\s*\d{2}\+\d{2}:\s*\d{2}|[^\n]*(?:\n[^\n:]*)*?(?=\n\w+:|$))'

        if re.search(pattern, content, re.MULTILINE):
            content = re.sub(pattern, f'date: {correct_date}', content, flags=re.MULTILINE)
        else:
            # Try simpler pattern
            content = re.sub(r'^date:.*$', f'date: {correct_date}', content, flags=re.MULTILINE)

        with open(en_file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return True
    except Exception as e:
        print(f"Error fixing {en_file_path.name}: {e}")
        return False

def main():
    pt_dir = Path('content/pt/posts')
    en_dir = Path('content/en/posts')

    if not pt_dir.exists() or not en_dir.exists():
        print("Error: Portuguese or English posts directory not found")
        return

    pt_files = list(pt_dir.glob('*.md'))
    fixed_count = 0

    print(f"🔧 Copying dates from {len(pt_files)} Portuguese files to English files...\n")

    for pt_file in pt_files:
        # Find corresponding English file
        en_file = en_dir / pt_file.name

        if en_file.exists():
            # Extract date from Portuguese file
            correct_date = extract_date_from_file(pt_file)

            if correct_date:
                # Fix date in English file
                if fix_date_in_english_file(en_file, correct_date):
                    print(f"✅ Fixed: {en_file.name}")
                    fixed_count += 1
                else:
                    print(f"❌ Failed: {en_file.name}")
            else:
                print(f"⚠️  No date found in: {pt_file.name}")
        else:
            print(f"⚠️  No English file for: {pt_file.name}")

    print(f"\n📊 Summary: Fixed dates in {fixed_count} files")

if __name__ == "__main__":
    main()
