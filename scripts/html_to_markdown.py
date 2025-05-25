#!/usr/bin/env python3
"""
Extract blog content from HTML to markdown format

This script extracts the content from Portuguese HTML files and creates
clean markdown files that can be easily translated.
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime

def extract_date_from_path(post_path):
    """Extract date from post directory name"""
    match = re.match(r'(\d{4}-\d{2}-\d{2})', post_path.name)
    if match:
        return match.group(1)
    return None

def extract_slug_from_path(post_path):
    """Extract slug from post directory name"""
    match = re.match(r'\d{4}-\d{2}-\d{2}-(.*)', post_path.name)
    if match:
        return match.group(1)
    return post_path.name

def extract_content_to_markdown(html_file_path):
    """Extract title and content from HTML file and convert to markdown"""
    with open(html_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    soup = BeautifulSoup(content, 'html.parser')

    # Extract title from h1 tag in posts-heading
    title = ""
    title_element = soup.find('div', class_='posts-heading')
    if title_element:
        h1 = title_element.find('h1')
        if h1:
            title = h1.get_text().strip()

    # Extract tags if available (look in the HTML for tag links)
    tags = []
    tag_links = soup.find_all('a', href=re.compile(r'/tags/'))
    for tag_link in tag_links:
        tag_text = tag_link.get_text().strip()
        if tag_text and tag_text not in tags:
            tags.append(tag_text)

    # Extract main content from blog-post article
    markdown_content = []
    article = soup.find('article', class_='blog-post')

    if article:
        # Remove sharing links and other non-content elements
        for element in article.find_all(['ul', 'h4'], string=re.compile('See also|share', re.I)):
            element.decompose()

        # Process content elements
        for element in article.children:
            if hasattr(element, 'name'):
                if element.name == 'p':
                    text = element.get_text().strip()
                    if text and not text.startswith('__'):  # Skip social media icons
                        markdown_content.append(text + '\n')

                elif element.name == 'blockquote':
                    quote_text = element.get_text().strip()
                    if quote_text:
                        # Convert to markdown blockquote
                        quote_lines = quote_text.split('\n')
                        for line in quote_lines:
                            if line.strip():
                                markdown_content.append(f"> {line.strip()}\n")
                        markdown_content.append('\n')

                elif element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    heading_text = element.get_text().strip()
                    if heading_text:
                        level = int(element.name[1])
                        markdown_content.append(f"{'#' * level} {heading_text}\n\n")

                elif element.name == 'ul':
                    for li in element.find_all('li'):
                        li_text = li.get_text().strip()
                        if li_text:
                            markdown_content.append(f"- {li_text}\n")
                    markdown_content.append('\n')

                elif element.name == 'ol':
                    for i, li in enumerate(element.find_all('li'), 1):
                        li_text = li.get_text().strip()
                        if li_text:
                            markdown_content.append(f"{i}. {li_text}\n")
                    markdown_content.append('\n')

                elif element.name == 'img':
                    src = element.get('src', '')
                    alt = element.get('alt', '')
                    if src:
                        markdown_content.append(f"![{alt}]({src})\n\n")

                elif element.name == 'a':
                    href = element.get('href', '')
                    link_text = element.get_text().strip()
                    if href and link_text:
                        markdown_content.append(f"[{link_text}]({href})")

    content_text = ''.join(markdown_content).strip()

    return title, content_text, tags

def create_markdown_file(post_path, output_dir):
    """Create markdown file from HTML post"""
    html_file = post_path / 'index.html'

    if not html_file.exists():
        return None

    # Extract content
    title, content, tags = extract_content_to_markdown(html_file)

    if not title:
        return None

    # Extract metadata
    date = extract_date_from_path(post_path)
    slug = extract_slug_from_path(post_path)

    # Create frontmatter
    frontmatter = []
    frontmatter.append('---')
    frontmatter.append(f'title: "{title}"')
    if date:
        frontmatter.append(f'date: {date}')
    frontmatter.append(f'slug: {slug}')
    if tags:
        frontmatter.append('tags:')
        for tag in tags:
            frontmatter.append(f'  - {tag}')
    frontmatter.append('draft: false')
    frontmatter.append('language: pt')
    frontmatter.append('---')
    frontmatter.append('')

    # Combine frontmatter and content
    full_content = '\n'.join(frontmatter) + '\n' + content

    # Create output file
    output_file = output_dir / f'{post_path.name}.md'

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_content)

    return output_file

def main():
    """Convert all Portuguese HTML posts to markdown"""
    pt_posts_dir = Path('pt/posts')
    output_dir = Path('markdown_posts_pt')

    # Create output directory
    output_dir.mkdir(exist_ok=True)

    # Get list of Portuguese posts
    pt_post_dirs = [d for d in pt_posts_dir.iterdir() if d.is_dir()]
    pt_post_dirs.sort()

    print(f"Converting {len(pt_post_dirs)} Portuguese posts to markdown...")

    success_count = 0

    for pt_post_dir in pt_post_dirs:
        print(f"Processing: {pt_post_dir.name}")

        try:
            output_file = create_markdown_file(pt_post_dir, output_dir)
            if output_file:
                print(f"  ✓ Created: {output_file}")
                success_count += 1
            else:
                print(f"  ✗ Failed to extract content")
        except Exception as e:
            print(f"  ✗ Error: {e}")

    print(f"\nConversion complete! {success_count}/{len(pt_post_dirs)} posts converted.")
    print(f"Markdown files saved to: {output_dir}")

if __name__ == "__main__":
    main()
