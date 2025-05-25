#!/usr/bin/env python3
"""
Blog Post Translation Script

This script translates Portuguese blog posts to English using ollama with llama3.
It extracts content from HTML files, translates them, and creates new English versions.
"""

import os
import re
import json
import subprocess
from pathlib import Path
from bs4 import BeautifulSoup

def extract_content_from_html(html_file_path):
    """Extract title and content from HTML file"""
    with open(html_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    soup = BeautifulSoup(content, 'html.parser')

    # Extract title from h1 tag in posts-heading
    title_element = soup.find('div', class_='posts-heading')
    title = ""
    if title_element:
        h1 = title_element.find('h1')
        if h1:
            title = h1.get_text().strip()

    # Extract main content from blog-post article
    article = soup.find('article', class_='blog-post')
    content_text = ""
    if article:
        # Remove sharing links and other non-content elements
        for element in article.find_all(['ul', 'h4'], string=re.compile('See also|share', re.I)):
            element.decompose()

        # Get text content while preserving paragraph structure
        paragraphs = article.find_all(['p', 'blockquote', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        content_parts = []
        for p in paragraphs:
            text = p.get_text().strip()
            if text and not text.startswith('__'):  # Skip social media icons
                content_parts.append(text)

        content_text = '\n\n'.join(content_parts)

    return title, content_text

def translate_with_ollama(text, model='llama3:latest'):
    """Translate text using ollama"""
    prompt = f"""Please translate the following Brazilian Portuguese text to English. Maintain the original meaning, tone, and technical accuracy. Preserve any technical terms appropriately. Do not add explanations, just provide the translation:

{text}"""

    try:
        # Use ollama API
        response = subprocess.run([
            'ollama', 'run', model, prompt
        ], capture_output=True, text=True, timeout=300)

        if response.returncode == 0:
            result = response.stdout.strip()
            # Clean up common prefixes that the model might add
            prefixes_to_remove = [
                "Here is the translation:",
                "Translation:",
                "Here's the translation:",
                "The translation is:",
            ]
            for prefix in prefixes_to_remove:
                if result.startswith(prefix):
                    result = result[len(prefix):].strip()
            return result
        else:
            print(f"Error from ollama: {response.stderr}")
            return None
    except subprocess.TimeoutExpired:
        print("Translation timed out")
        return None
    except Exception as e:
        print(f"Error calling ollama: {e}")
        return None

def create_english_html(original_html_path, translated_title, translated_content, english_post_dir):
    """Create English version of HTML file with translated content"""
    with open(original_html_path, 'r', encoding='utf-8') as file:
        content = file.read()

    soup = BeautifulSoup(content, 'html.parser')

    # Update language
    html_tag = soup.find('html')
    if html_tag:
        html_tag['lang'] = 'en'

    # Update title in head
    title_tag = soup.find('title')
    if title_tag:
        title_tag.string = f"{translated_title} - Helio Medeiros"

    # Update meta description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc:
        # Use first paragraph of translated content as description
        first_para = translated_content.split('\n\n')[0][:160] + "..."
        meta_desc['content'] = first_para

    # Update Open Graph tags
    og_title = soup.find('meta', attrs={'property': 'og:title'})
    if og_title:
        og_title['content'] = translated_title

    og_desc = soup.find('meta', attrs={'property': 'og:description'})
    if og_desc:
        first_para = translated_content.split('\n\n')[0][:200] + "..."
        og_desc['content'] = first_para

    # Update URLs to point to English version
    og_url = soup.find('meta', attrs={'property': 'og:url'})
    if og_url:
        url = og_url['content']
        url = url.replace('/pt/posts/', '/posts/')
        og_url['content'] = url

    # Update breadcrumb JSON-LD
    scripts = soup.find_all('script', type='application/ld+json')
    for script in scripts:
        try:
            data = json.loads(script.string)
            if data.get('@type') == 'BreadcrumbList':
                for item in data.get('itemListElement', []):
                    if 'item' in item and '@id' in item['item']:
                        item['item']['@id'] = item['item']['@id'].replace('/pt/posts/', '/posts/')
            elif data.get('@type') == 'Article':
                data['headline'] = translated_title
                data['description'] = translated_content.split('\n\n')[0]
                data['mainEntityOfPage'] = data['mainEntityOfPage'].replace('/pt/posts/', '/posts/')
            script.string = json.dumps(data, ensure_ascii=False)
        except:
            continue

    # Update title in posts-heading
    title_element = soup.find('div', class_='posts-heading')
    if title_element:
        h1 = title_element.find('h1')
        if h1:
            h1.string = translated_title

    # Update main content
    article = soup.find('article', class_='blog-post')
    if article:
        # Clear existing content
        article.clear()

        # Add translated content as paragraphs
        for paragraph in translated_content.split('\n\n'):
            if paragraph.strip():
                p_tag = soup.new_tag('p')
                p_tag.string = paragraph.strip()
                article.append(p_tag)

    # Update navigation links
    navbar_links = soup.find_all('a', title=True)
    for link in navbar_links:
        if link.get('title') == 'Início':
            link['title'] = 'Home'
            link.string = 'Home'
        elif link.get('title') == 'Sobre':
            link['title'] = 'About'
            link.string = 'About'
        elif link.get('title') == 'Posts':
            link['title'] = 'Posts'
            link.string = 'Posts'

    # Update links to point to English version
    for link in soup.find_all('a', href=True):
        href = link['href']
        if '/pt/' in href:
            link['href'] = href.replace('/pt/', '/')

    # Update brand link
    brand_link = soup.find('a', class_='navbar-brand')
    if brand_link:
        brand_link.string = 'Helio Medeiros - Technology Blog'
        brand_link['href'] = brand_link['href'].replace('/pt/', '/')

    # Save the translated HTML
    os.makedirs(english_post_dir, exist_ok=True)
    english_html_path = os.path.join(english_post_dir, 'index.html')

    with open(english_html_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))

    return english_html_path

def main():
    """Main translation process"""
    pt_posts_dir = Path('pt/posts')
    en_posts_dir = Path('posts')

    # Get list of Portuguese posts
    pt_post_dirs = [d for d in pt_posts_dir.iterdir() if d.is_dir()]
    pt_post_dirs.sort()  # Process in order

    print(f"Found {len(pt_post_dirs)} Portuguese posts to translate")

    # Log file to track progress
    log_file = 'translation_progress.log'

    for i, pt_post_dir in enumerate(pt_post_dirs, 1):
        post_name = pt_post_dir.name
        pt_html_file = pt_post_dir / 'index.html'
        en_post_dir = en_posts_dir / post_name
        en_html_file = en_post_dir / 'index.html'

        print(f"[{i}/{len(pt_post_dirs)}] Processing: {post_name}")

        # Skip if English version already exists (unless forced)
        if en_html_file.exists():
            print(f"  ✓ English version already exists, skipping...")
            continue

        if not pt_html_file.exists():
            print(f"  ✗ Portuguese HTML file not found, skipping...")
            continue

        try:
            # Extract content
            print(f"  → Extracting content...")
            title, content = extract_content_from_html(pt_html_file)

            if not title or not content:
                print(f"  ✗ Could not extract content, skipping...")
                continue

            print(f"  → Title: {title[:50]}...")
            print(f"  → Content: {len(content)} characters")

            # Translate title
            print(f"  → Translating title...")
            translated_title = translate_with_ollama(title)
            if not translated_title:
                print(f"  ✗ Could not translate title, skipping...")
                continue

            # Translate content
            print(f"  → Translating content...")
            translated_content = translate_with_ollama(content)
            if not translated_content:
                print(f"  ✗ Could not translate content, skipping...")
                continue

            # Create English HTML
            print(f"  → Creating English HTML...")
            english_html_path = create_english_html(
                pt_html_file, translated_title, translated_content, en_post_dir
            )

            print(f"  ✓ Complete: {english_html_path}")

            # Log progress
            with open(log_file, 'a', encoding='utf-8') as log:
                log.write(f"SUCCESS: {post_name}\n")

        except Exception as e:
            print(f"  ✗ Error processing {post_name}: {e}")
            with open(log_file, 'a', encoding='utf-8') as log:
                log.write(f"ERROR: {post_name} - {e}\n")
            continue

    print(f"\nTranslation process complete! Check {log_file} for details.")

if __name__ == "__main__":
    main()
