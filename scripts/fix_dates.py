#!/usr/bin/env python3
"""
Fix broken date fields in English translation files
"""

import re
from pathlib import Path

def fix_date_field(content):
    """Fix broken date fields in YAML frontmatter"""

    # Pattern to match broken date fields
    # Look for date: followed by broken date components
    pattern = r'date:\s*(\d{4}-\d{2}-\d{2})\s*T(\d{2}):\s*(\d{2}):\s*(\d{2})\+(\d{2}):\s*(\d{2})'

    def date_replacer(match):
        year_month_day = match.group(1)
        hour = match.group(2)
        minute = match.group(3)
        second = match.group(4)
        tz_hour = match.group(5)
        tz_minute = match.group(6)

        return f'date: {year_month_day}T{hour}:{minute}:{second}+{tz_hour}:{tz_minute}'

    # Fix the broken date pattern
    content = re.sub(pattern, date_replacer, content, flags=re.MULTILINE)

    # Also fix cases where the date got split across multiple lines
    # Pattern: date: YYYY-MM-DD\nT\nHH:\nMM:\nSS+\nTZ:\nTZ
    lines = content.split('\n')
    fixed_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Check if this is a broken date line
        if re.match(r'date:\s*\d{4}-\d{2}-\d{2}$', line.strip()):
            # This is the start of a broken date, collect all parts
            date_parts = [line.strip()]
            j = i + 1

            # Collect continuation lines that look like date parts
            while j < len(lines):
                next_line = lines[j].strip()
                if (re.match(r'^\d{2}T\d{2}:$', next_line) or  # "12T20:"
                    re.match(r'^\d{2}:\s*\d{2}\+$', next_line) or  # "16: 38+"
                    re.match(r'^\d{2}:\s*\d{2}$', next_line) or   # "00: 00"
                    re.match(r'^T\d{2}:$', next_line) or         # "T20:"
                    re.match(r'^\d{2}:\s*$', next_line) or       # "16: "
                    re.match(r'^\d{2}\+$', next_line) or         # "38+"
                    re.match(r'^\d{2}$', next_line)):            # "00"
                    date_parts.append(next_line)
                    j += 1
                else:
                    break

            # Reconstruct the date
            if len(date_parts) > 1:
                # Extract the date from the first part
                date_match = re.search(r'date:\s*(\d{4}-\d{2}-\d{2})', date_parts[0])
                if date_match:
                    date_base = date_match.group(1)

                    # Try to reconstruct time from the parts
                    all_parts = ' '.join(date_parts[1:])

                    # Default time if we can't parse it
                    time_part = "T00:00:00+00:00"

                    # Try to extract time components
                    time_match = re.search(r'(\d{2})T(\d{2}):.*?(\d{2}):\s*(\d{2})\+.*?(\d{2}):\s*(\d{2})', all_parts)
                    if time_match:
                        time_part = f"T{time_match.group(2)}:{time_match.group(3)}:{time_match.group(4)}+{time_match.group(5)}:{time_match.group(6)}"
                    else:
                        # Try simpler patterns
                        hour_match = re.search(r'T(\d{2}):', all_parts)
                        if hour_match:
                            hour = hour_match.group(1)
                            minute_match = re.search(r'(\d{2}):\s*(\d{2})', all_parts)
                            if minute_match:
                                minute = minute_match.group(1)
                                second = minute_match.group(2)
                                time_part = f"T{hour}:{minute}:{second}+00:00"

                    fixed_lines.append(f'date: {date_base}{time_part}')
                    i = j
                    continue

            # If we couldn't reconstruct, just use the original
            fixed_lines.append(line)
            i += 1
        else:
            fixed_lines.append(line)
            i += 1

    return '\n'.join(fixed_lines)

def process_file(file_path):
    """Process a single file to fix date fields"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        fixed_content = fix_date_field(content)

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
    print(f"🔧 Fixing date fields in {len(md_files)} English posts...\n")

    fixed_count = 0
    for md_file in md_files:
        if process_file(md_file):
            fixed_count += 1

    print(f"\n📊 Summary: Fixed date fields in {fixed_count}/{len(md_files)} files")

if __name__ == "__main__":
    main()
