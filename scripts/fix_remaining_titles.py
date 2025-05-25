#!/usr/bin/env python3
"""
Fix remaining title issues in HTML files

This script fixes any titles that still contain unwanted prefixes from the translation.
"""

import re
from pathlib import Path
from bs4 import BeautifulSoup

def clean_title(title):
    """Clean unwanted prefixes from titles"""
    prefixes_to_remove = [
        "Here is the translation of the text from Brazilian Portuguese to English:",
        "Here's the translation of the text from Brazilian Portuguese to English:",
        "Here is the translation from Brazilian Portuguese to English:",
        "Here's the translation from Brazilian Portuguese to English:",
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
    ]

    cleaned_title = title
    for prefix in prefixes_to_remove:
        if cleaned_title.lower().startswith(prefix.lower()):
            cleaned_title = cleaned_title[len(prefix):].strip()
            break

    return cleaned_title

def fix_html_file(html_file_path):
    """Fix title issues in a single HTML file"""
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # Get current title
    title_tag = soup.find('title')
    if not title_tag:
        return False

    current_title = title_tag.string
    if not current_title:
        return False

    # Extract the blog title part (before " - Helio Medeiros")
    title_parts = current_title.split(' - ')
    if len(title_parts) < 2:
        return False

    blog_title = title_parts[0]
    cleaned_title = clean_title(blog_title)

    if cleaned_title == blog_title:
        return False  # No change needed

    # Update title tag
    new_full_title = f"{cleaned_title} - Helio Medeiros"
    title_tag.string = new_full_title

    # Update Open Graph title
    og_title = soup.find('meta', attrs={'property': 'og:title'})
    if og_title:
        og_title['content'] = cleaned_title

    # Update Twitter title
    twitter_title = soup.find('meta', attrs={'name': 'twitter:title'})
    if twitter_title:
        twitter_title['content'] = cleaned_title

    # Update the main heading (h1 in posts-heading)
    posts_heading = soup.find('div', class_='posts-heading')
    if posts_heading:
        h1 = posts_heading.find('h1')
        if h1:
            h1.string = cleaned_title

    # Update JSON-LD structured data
    json_scripts = soup.find_all('script', type='application/ld+json')
    for script in json_scripts:
        if script.string:
            try:
                import json
                data = json.loads(script.string)

                # Update various JSON-LD objects
                if '@type' in data:
                    if data['@type'] == 'Article':
                        data['headline'] = cleaned_title
                    elif data['@type'] == 'BreadcrumbList':
                        # Update breadcrumb for the current page
                        if 'itemListElement' in data:
                            for item in data['itemListElement']:
                                if item.get('@type') == 'ListItem' and 'item' in item:
                                    item_data = item['item']
                                    if html_file_path.name in str(item_data.get('@id', '')):
                                        item_data['name'] = cleaned_title

                script.string = json.dumps(data)
            except:
                # If JSON parsing fails, skip this script
                pass

    # Write updated HTML
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    return True

def main():
    """Fix remaining title issues in all HTML files"""
    posts_dir = Path('posts')

    if not posts_dir.exists():
        print(f"Error: Posts directory {posts_dir} not found")
        return

    print("Checking for title issues in HTML files...")

    fixed_count = 0
    total_files = 0

    for post_dir in posts_dir.iterdir():
        if post_dir.is_dir():
            html_file = post_dir / 'index.html'
            if html_file.exists():
                total_files += 1
                try:
                    if fix_html_file(html_file):
                        print(f"✓ Fixed title in: {post_dir.name}")
                        fixed_count += 1
                except Exception as e:
                    print(f"✗ Error processing {post_dir.name}: {e}")

    print(f"\nTitle cleanup complete!")
    print(f"Files checked: {total_files}")
    print(f"Files fixed: {fixed_count}")

if __name__ == "__main__":
    main()
