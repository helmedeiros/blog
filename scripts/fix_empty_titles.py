#!/usr/bin/env python3
import os
import re
import glob

def extract_title_from_filename(filename):
    """Extract a meaningful title from the filename"""
    # Remove path and extension
    basename = os.path.basename(filename)
    name_without_ext = os.path.splitext(basename)[0]

    # Remove date prefix (YYYY-MM-DD-)
    title_part = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', name_without_ext)

    # Replace hyphens and underscores with spaces
    title = title_part.replace('-', ' ').replace('_', ' ')

    # Capitalize words
    title = ' '.join(word.capitalize() for word in title.split())

    return title

def extract_title_from_content(content):
    """Try to extract a title from the content"""
    lines = content.split('\n')

    # Look for first heading
    for line in lines:
        line = line.strip()
        if line.startswith('# '):
            return line[2:].strip()
        elif line.startswith('## '):
            return line[3:].strip()

    # Look for first sentence that might be a title
    for line in lines:
        line = line.strip()
        if line and not line.startswith('---') and not line.startswith('<') and len(line) < 100:
            # Clean up HTML tags
            clean_line = re.sub(r'<[^>]+>', '', line)
            if clean_line and len(clean_line.split()) <= 10:
                return clean_line

    return None

def fix_empty_titles():
    """Find and fix posts with empty titles"""
    posts_with_empty_titles = []

    # Find all markdown files in content directories
    for pattern in ['content/en/posts/*.md', 'content/pt/posts/*.md']:
        for filepath in glob.glob(pattern):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Check if title is empty
                if 'title: ""' in content:
                    posts_with_empty_titles.append(filepath)

                    # Generate a title
                    filename_title = extract_title_from_filename(filepath)
                    content_title = extract_title_from_content(content)

                    suggested_title = content_title if content_title else filename_title

                    print(f"\nFile: {filepath}")
                    print(f"Suggested title from filename: {filename_title}")
                    if content_title:
                        print(f"Suggested title from content: {content_title}")
                    print(f"Recommended title: {suggested_title}")

                    # Show first few lines of content for context
                    lines = content.split('\n')
                    print("Content preview:")
                    for i, line in enumerate(lines[10:20]):  # Skip front matter
                        if line.strip():
                            print(f"  {line[:100]}...")
                            break

            except Exception as e:
                print(f"Error processing {filepath}: {e}")

    print(f"\nFound {len(posts_with_empty_titles)} posts with empty titles.")
    return posts_with_empty_titles

if __name__ == "__main__":
    fix_empty_titles()
