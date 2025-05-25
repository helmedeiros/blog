#!/usr/bin/env python3
"""
Translate Portuguese markdown files to English

This script translates the extracted Portuguese markdown files to English
using ollama with llama3, creating clean English versions.
"""

import os
import re
import subprocess
from pathlib import Path
import argparse

def clean_markdown_content(content):
    """Clean up markdown content by removing artifacts"""
    lines = content.split('\n')
    cleaned_lines = []

    skip_patterns = [
        r'^- __+$',  # Social media share buttons
        r'^__+$',    # Social media share buttons
        r'^\s*$',    # Empty lines (will be re-added properly)
    ]

    for line in lines:
        # Skip lines that match cleanup patterns
        skip_line = False
        for pattern in skip_patterns:
            if re.match(pattern, line.strip()):
                skip_line = True
                break

        if not skip_line:
            cleaned_lines.append(line)

    # Remove excessive whitespace
    cleaned_content = '\n'.join(cleaned_lines)
    # Remove multiple consecutive empty lines
    cleaned_content = re.sub(r'\n\s*\n\s*\n', '\n\n', cleaned_content)

    return cleaned_content.strip()

def translate_with_ollama(text, model='llama3:latest'):
    """Translate text using ollama with improved prompts"""

    # Clean the text first
    text = clean_markdown_content(text)

    prompt = f"""Translate this Brazilian Portuguese text to English. Do NOT add any prefixes, introductions, explanations, or comments. Only output the translated text directly.

{text}"""

    try:
        # Use ollama CLI
        response = subprocess.run([
            'ollama', 'run', model, prompt
        ], capture_output=True, text=True, timeout=600)

        if response.returncode == 0:
            result = response.stdout.strip()

            # Clean up common prefixes that the model might add
            prefixes_to_remove = [
                "Here is the translation of the text from Brazilian Portuguese to English:",
                "Here is the translation from Brazilian Portuguese to English:",
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
                "Here is the translation of the Brazilian Portuguese text to English:",
                "Translation from Portuguese to English:",
                "The English translation is:",
            ]

            for prefix in prefixes_to_remove:
                if result.lower().startswith(prefix.lower()):
                    result = result[len(prefix):].strip()
                    break

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
        elif line.startswith('-') and 'tags' in str(frontmatter.get('last_key', '')):
            # Handle tags array
            if 'tags' not in frontmatter:
                frontmatter['tags'] = []
            tag = line.strip('- ').strip()
            if tag:
                frontmatter.setdefault('tags', []).append(tag)

    return frontmatter, body

def create_english_frontmatter(original_frontmatter, translated_title):
    """Create English frontmatter"""
    english_frontmatter = original_frontmatter.copy()
    english_frontmatter['title'] = f'"{translated_title}"'
    english_frontmatter['language'] = 'en'

    # Build frontmatter text
    lines = ['---']
    lines.append(f'title: {english_frontmatter["title"]}')

    if 'date' in english_frontmatter:
        lines.append(f'date: {english_frontmatter["date"]}')

    if 'slug' in english_frontmatter:
        lines.append(f'slug: {english_frontmatter["slug"]}')

    if 'tags' in english_frontmatter and english_frontmatter['tags']:
        lines.append('tags:')
        if isinstance(english_frontmatter['tags'], list):
            for tag in english_frontmatter['tags']:
                lines.append(f'  - {tag}')
        else:
            lines.append(f'  - {english_frontmatter["tags"]}')

    lines.append('draft: false')
    lines.append('language: en')
    lines.append('---')

    return '\n'.join(lines)

def translate_markdown_file(md_file_path, output_dir):
    """Translate a single markdown file"""
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse frontmatter and body
    frontmatter, body = parse_frontmatter(content)

    if not frontmatter.get('title'):
        print(f"  ✗ No title found in {md_file_path}")
        return None

    original_title = frontmatter['title']

    # Translate title
    print(f"  → Translating title: {original_title[:50]}...")
    translated_title = translate_with_ollama(original_title)
    if not translated_title:
        print(f"  ✗ Could not translate title")
        return None

    # Translate body content
    print(f"  → Translating content ({len(body)} chars)...")
    translated_body = translate_with_ollama(body)
    if not translated_body:
        print(f"  ✗ Could not translate content")
        return None

    # Create English frontmatter
    english_frontmatter = create_english_frontmatter(frontmatter, translated_title)

    # Combine translated content
    translated_content = english_frontmatter + '\n\n' + translated_body

    # Save translated file
    output_file = output_dir / md_file_path.name
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(translated_content)

    return output_file

def main():
    parser = argparse.ArgumentParser(description='Translate Portuguese markdown files to English')
    parser.add_argument('--batch-size', type=int, default=5, help='Number of files to process in each batch')
    parser.add_argument('--start-from', type=int, default=0, help='Index to start from')
    parser.add_argument('--dry-run', action='store_true', help='Show files to be processed')

    args = parser.parse_args()

    input_dir = Path('markdown_posts_pt')
    output_dir = Path('markdown_posts_en')

    if not input_dir.exists():
        print(f"Error: Input directory {input_dir} not found")
        return

    # Create output directory
    output_dir.mkdir(exist_ok=True)

    # Get list of markdown files
    md_files = sorted([f for f in input_dir.glob('*.md')])

    if not md_files:
        print("No markdown files found to translate")
        return

    print(f"Found {len(md_files)} markdown files to translate")

    if args.dry_run:
        print("\nFiles to be processed:")
        for i, md_file in enumerate(md_files):
            print(f"  {i+1:2d}. {md_file.name}")
        return

    # Process in batches
    log_file = 'translation_markdown_progress.log'
    start_idx = args.start_from
    batch_size = args.batch_size

    while start_idx < len(md_files):
        end_idx = min(start_idx + batch_size, len(md_files))
        batch = md_files[start_idx:end_idx]

        print(f"\n{'='*60}")
        print(f"Processing batch {start_idx//batch_size + 1}: files {start_idx+1}-{end_idx}")
        print(f"{'='*60}")

        for i, md_file in enumerate(batch, start_idx + 1):
            print(f"[{i}/{len(md_files)}] Processing: {md_file.name}")

            try:
                output_file = translate_markdown_file(md_file, output_dir)
                if output_file:
                    print(f"  ✓ Complete: {output_file}")
                    with open(log_file, 'a', encoding='utf-8') as log:
                        log.write(f"SUCCESS: {md_file.name}\n")
                else:
                    print(f"  ✗ Failed to translate")
                    with open(log_file, 'a', encoding='utf-8') as log:
                        log.write(f"ERROR: {md_file.name}\n")

            except Exception as e:
                print(f"  ✗ Error: {e}")
                with open(log_file, 'a', encoding='utf-8') as log:
                    log.write(f"ERROR: {md_file.name} - {e}\n")

        start_idx = end_idx

        if start_idx < len(md_files):
            response = input(f"\nBatch complete. Continue with next batch? (y/n/q to quit): ")
            if response.lower() in ['n', 'q', 'quit']:
                print(f"Stopping. Resume with: --start-from {start_idx}")
                break

    print(f"\nTranslation complete! Translated files saved to: {output_dir}")

if __name__ == "__main__":
    main()
