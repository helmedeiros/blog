#!/usr/bin/env python3
"""
Replace HTML content with translated markdown

This script takes our translated English markdown files and replaces the content
in the existing HTML files while preserving all metadata, navigation, and structure.
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
import markdown

def parse_frontmatter(content):
    """Parse YAML frontmatter from markdown"""
    if not content.startswith('---'):
        return {}, content

    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content

    frontmatter_text = parts[1].strip()
    body = parts[2].strip()

    # Simple YAML parsing for our use case
    frontmatter = {}
    for line in frontmatter_text.split('\n'):
        line = line.strip()
        if ':' in line and not line.startswith('-'):
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"\'')
            frontmatter[key] = value

    return frontmatter, body

def markdown_to_html(markdown_text):
    """Convert markdown to HTML"""
    # Configure markdown with extensions for better HTML output
    md = markdown.Markdown(extensions=['extra', 'codehilite', 'toc'])
    html = md.convert(markdown_text)
    return html

def extract_description(body_text):
    """Extract a description from the body text"""
    # Remove markdown syntax for description
    clean_text = re.sub(r'[*_`#\[\]()]+', '', body_text)
    lines = clean_text.split('\n')
    description_lines = []

    for line in lines:
        line = line.strip()
        if line:
            description_lines.append(line)
            if len(' '.join(description_lines)) > 100:
                break

    description = ' '.join(description_lines)[:150]
    if len(' '.join(description_lines)) > 150:
        description += '...'

    return description

def update_html_file(html_file_path, markdown_content, translated_title):
    """Update HTML file with translated content"""

    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # Parse markdown content
    frontmatter, body = parse_frontmatter(markdown_content)

    # Convert markdown body to HTML
    body_html = markdown_to_html(body)

    # Extract description for meta tags
    description = extract_description(body)

    # Update title tags
    title_tag = soup.find('title')
    if title_tag:
        # Keep the format " - Helio Medeiros"
        base_title = title_tag.string.split(' - ')[:-1]  # Remove author part
        title_tag.string = f"{translated_title} - Helio Medeiros"

    # Update meta description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc:
        meta_desc['content'] = description

    # Update Open Graph title
    og_title = soup.find('meta', attrs={'property': 'og:title'})
    if og_title:
        og_title['content'] = translated_title

    # Update Open Graph description
    og_desc = soup.find('meta', attrs={'property': 'og:description'})
    if og_desc:
        og_desc['content'] = description

    # Update Twitter title
    twitter_title = soup.find('meta', attrs={'name': 'twitter:title'})
    if twitter_title:
        twitter_title['content'] = translated_title

    # Update Twitter description
    twitter_desc = soup.find('meta', attrs={'name': 'twitter:description'})
    if twitter_desc:
        twitter_desc['content'] = description

    # Update the main heading (h1 in posts-heading)
    posts_heading = soup.find('div', class_='posts-heading')
    if posts_heading:
        h1 = posts_heading.find('h1')
        if h1:
            h1.string = translated_title

    # Update the main article content
    article = soup.find('article', class_='blog-post')
    if article:
        # Clear existing content but preserve attributes
        article.clear()
        # Add new content
        article.append(BeautifulSoup(body_html, 'html.parser'))

    # Update language attribute in html tag
    html_tag = soup.find('html')
    if html_tag:
        html_tag['lang'] = 'en'

    # Update JSON-LD structured data if present
    json_scripts = soup.find_all('script', type='application/ld+json')
    for script in json_scripts:
        if script.string:
            try:
                import json
                data = json.loads(script.string)

                # Update various JSON-LD objects
                if '@type' in data:
                    if data['@type'] == 'Article':
                        data['headline'] = translated_title
                        data['description'] = description
                        data['inLanguage'] = 'en'
                    elif data['@type'] == 'BreadcrumbList':
                        # Update breadcrumb for the current page
                        if 'itemListElement' in data:
                            for item in data['itemListElement']:
                                if item.get('@type') == 'ListItem' and 'item' in item:
                                    item_data = item['item']
                                    if html_file_path.name in str(item_data.get('@id', '')):
                                        item_data['name'] = translated_title

                script.string = json.dumps(data)
            except:
                # If JSON parsing fails, skip this script
                pass

    # Write updated HTML
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))

def find_html_file_for_markdown(md_file_path, posts_dir):
    """Find the corresponding HTML file for a markdown file"""
    # Extract the date and slug from the markdown filename
    # Format: YYYY-MM-DD-slug.md
    filename = md_file_path.stem

    # Look for a directory with this name in posts/
    html_dir = posts_dir / filename
    if html_dir.exists() and html_dir.is_dir():
        html_file = html_dir / 'index.html'
        if html_file.exists():
            return html_file

    return None

def main():
    """Replace HTML content with translated markdown"""

    input_dir = Path('markdown_posts_en')
    posts_dir = Path('posts')

    if not input_dir.exists():
        print(f"Error: Input directory {input_dir} not found")
        return

    if not posts_dir.exists():
        print(f"Error: Posts directory {posts_dir} not found")
        return

    # Get list of markdown files
    md_files = sorted([f for f in input_dir.glob('*.md') if not f.name.endswith('.backup')])

    if not md_files:
        print("No markdown files found to process")
        return

    print(f"Processing {len(md_files)} translated markdown files")

    updated_count = 0
    for md_file in md_files:
        print(f"Processing: {md_file.name}")

        # Find corresponding HTML file
        html_file = find_html_file_for_markdown(md_file, posts_dir)
        if not html_file:
            print(f"  ⚠ No HTML file found for {md_file.name}")
            continue

        try:
            # Read markdown content
            with open(md_file, 'r', encoding='utf-8') as f:
                markdown_content = f.read()

            # Parse to get title
            frontmatter, body = parse_frontmatter(markdown_content)
            translated_title = frontmatter.get('title', '').strip('"\'')

            if not translated_title:
                print(f"  ⚠ No title found in {md_file.name}")
                continue

            # Update HTML file
            print(f"  → Updating: {html_file}")
            update_html_file(html_file, markdown_content, translated_title)
            print(f"  ✓ Updated with title: {translated_title}")

            updated_count += 1

        except Exception as e:
            print(f"  ✗ Error: {e}")

    print(f"\nUpdate complete!")
    print(f"Updated: {updated_count}/{len(md_files)} files")
    print(f"\nYour blog posts have been updated with the English translations!")

if __name__ == "__main__":
    main()
