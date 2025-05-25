#!/usr/bin/env python3
"""
Test script to translate a single blog post
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
            return response.stdout.strip()
        else:
            print(f"Error from ollama: {response.stderr}")
            return None
    except subprocess.TimeoutExpired:
        print("Translation timed out")
        return None
    except Exception as e:
        print(f"Error calling ollama: {e}")
        return None

def main():
    """Test translation on a single post"""
    # Test with the hello-world post
    test_post = 'pt/posts/2008-06-12-hello-world/index.html'

    if not os.path.exists(test_post):
        print(f"Test post not found: {test_post}")
        return

    print("Testing translation on hello-world post...")
    print("=" * 50)

    # Extract content
    title, content = extract_content_from_html(test_post)

    print(f"Original Title: {title}")
    print(f"Original Content:\n{content}")
    print("=" * 50)

    # Translate title
    print("Translating title...")
    translated_title = translate_with_ollama(title)
    print(f"Translated Title: {translated_title}")
    print("=" * 50)

    # Translate content
    print("Translating content...")
    translated_content = translate_with_ollama(content)
    print(f"Translated Content:\n{translated_content}")
    print("=" * 50)

    print("Test completed!")

if __name__ == "__main__":
    main()
