#!/usr/bin/env python3
"""
Translate Hugo Portuguese posts to English while preserving links and formatting

This script improves upon the original translation by:
1. Preserving markdown reference-style links
2. Preserving HTML links with all attributes
3. Preserving HTML formatting tags
4. Better handling of mixed content
"""

import os
import re
import subprocess
from pathlib import Path
import argparse
import time

def extract_and_preserve_links(text):
    """Extract links and replace with placeholders to preserve them during translation"""

    # Store extracted elements
    preserved_elements = {}
    counter = 0

    # 1. Preserve HTML links with all attributes
    html_link_pattern = r'<a\s+[^>]*href=[^>]*>.*?</a>'
    html_links = re.findall(html_link_pattern, text, re.IGNORECASE | re.DOTALL)
    for link in html_links:
        placeholder = f"__HTML_LINK_{counter}__"
        preserved_elements[placeholder] = link
        text = text.replace(link, placeholder, 1)
        counter += 1

    # 2. Preserve markdown reference-style links [text][ref]
    md_ref_pattern = r'\[([^\]]+)\]\[(\d+)\]'
    md_refs = re.findall(md_ref_pattern, text)
    for match in md_refs:
        full_match = f"[{match[0]}][{match[1]}]"
        placeholder = f"__MD_REF_{counter}__"
        preserved_elements[placeholder] = full_match
        text = text.replace(full_match, placeholder, 1)
        counter += 1

    # 3. Preserve image references ![alt][ref]
    img_ref_pattern = r'!\[([^\]]*)\]\[(\d+)\]'
    img_refs = re.findall(img_ref_pattern, text)
    for match in img_refs:
        full_match = f"![{match[0]}][{match[1]}]"
        placeholder = f"__IMG_REF_{counter}__"
        preserved_elements[placeholder] = full_match
        text = text.replace(full_match, placeholder, 1)
        counter += 1

    # 4. Preserve link reference definitions [1]: http://...
    ref_def_pattern = r'^\s*\[(\d+)\]:\s+(.+)$'
    ref_defs = re.findall(ref_def_pattern, text, re.MULTILINE)
    for match in ref_defs:
        full_match = f" [{match[0]}]: {match[1]}"
        placeholder = f"__REF_DEF_{counter}__"
        preserved_elements[placeholder] = full_match
        # Remove from text (will be added back at the end)
        text = re.sub(r'^\s*\[' + re.escape(match[0]) + r'\]:\s+' + re.escape(match[1]) + r'$', '', text, flags=re.MULTILINE)
        counter += 1

    return text, preserved_elements

def restore_preserved_elements(text, preserved_elements):
    """Restore preserved elements back into the translated text"""
    for placeholder, original in preserved_elements.items():
        text = text.replace(placeholder, original)
    return text

def translate_with_ollama(text, model='llama3:latest'):
    """Translate text using ollama with link preservation"""

    # Extract and preserve links/formatting
    text_to_translate, preserved_elements = extract_and_preserve_links(text)

    prompt = f"""Translate this Portuguese text to English. Keep all __PLACEHOLDER__ text exactly as written.

{text_to_translate}"""

    try:
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

            # Restore preserved elements
            result = restore_preserved_elements(result, preserved_elements)

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

def parse_hugo_frontmatter(content):
    """Parse YAML frontmatter from Hugo markdown"""
    if not content.startswith('---'):
        return [], content

    parts = content.split('---', 2)
    if len(parts) < 3:
        return [], content

    frontmatter_text = parts[1].strip()
    body = parts[2].strip()

    # Parse Hugo frontmatter (preserving original structure)
    frontmatter_lines = []
    for line in frontmatter_text.split('\n'):
        frontmatter_lines.append(line)

    return frontmatter_lines, body

def create_english_hugo_frontmatter(original_frontmatter_lines, translated_title):
    """Create English Hugo frontmatter preserving original structure"""
    english_lines = []

    for line in original_frontmatter_lines:
        if line.strip().startswith('title:'):
            # Replace title with translated version
            english_lines.append(f'title: "{translated_title}"')
        else:
            # Keep all other frontmatter as-is (author, date, layout, url, categories, etc.)
            english_lines.append(line)

    return '\n'.join(english_lines)

def translate_hugo_post(md_file_path, output_dir):
    """Translate a single Hugo markdown file with link preservation"""
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse frontmatter and body
    frontmatter_lines, body = parse_hugo_frontmatter(content)

    if not frontmatter_lines:
        print(f"  ✗ No frontmatter found in {md_file_path}")
        return None

    # Extract title for translation
    original_title = None
    for line in frontmatter_lines:
        if line.strip().startswith('title:'):
            title_match = re.search(r"title:\s*['\"]?(.*?)['\"]?\s*$", line)
            if title_match:
                original_title = title_match.group(1)
                break

    if not original_title:
        print(f"  ✗ No title found in {md_file_path}")
        return None

    # Translate title (simple text, no links expected)
    print(f"  → Translating title: {original_title[:50]}...")
    translated_title = translate_with_ollama(original_title)
    if not translated_title:
        print(f"  ✗ Could not translate title")
        return None

    # Translate body content with link preservation
    print(f"  → Translating content ({len(body)} chars) with link preservation...")
    translated_body = translate_with_ollama(body)
    if not translated_body:
        print(f"  ✗ Could not translate content")
        return None

    # Create English frontmatter
    english_frontmatter = create_english_hugo_frontmatter(frontmatter_lines, translated_title)

    # Combine translated content
    translated_content = f"---\n{english_frontmatter}\n---\n\n{translated_body}"

    # Save translated file
    output_file = output_dir / md_file_path.name
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(translated_content)

    return output_file

def main():
    parser = argparse.ArgumentParser(description='Translate Hugo Portuguese posts to English with link preservation')
    parser.add_argument('--batch-size', type=int, default=3, help='Number of files to process in each batch')
    parser.add_argument('--start-from', type=int, default=0, help='Index to start from')
    parser.add_argument('--dry-run', action='store_true', help='Show files to be processed')
    parser.add_argument('--single', type=str, help='Translate single file by name')
    parser.add_argument('--test', action='store_true', help='Test link preservation on a sample')

    args = parser.parse_args()

    if args.test:
        # Test the link preservation function
        test_text = """
        This is a test with [a link][1] and <a href="http://example.com" title="Example" target="_blank">HTML link</a>.
        Also has ![image][2] and some <u>formatting</u>.

        [1]: http://test.com
        [2]: http://image.com
        """
        print("Original text:")
        print(test_text)
        print("\nAfter extraction:")
        extracted, preserved = extract_and_preserve_links(test_text)
        print(extracted)
        print("\nPreserved elements:")
        for k, v in preserved.items():
            print(f"{k}: {v}")
        print("\nAfter restoration:")
        restored = restore_preserved_elements(extracted, preserved)
        print(restored)
        return

    input_dir = Path('content/pt/posts')
    output_dir = Path('content/en/posts')

    if not input_dir.exists():
        print(f"Error: Input directory {input_dir} not found")
        return

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get list of markdown files
    if args.single:
        md_files = [input_dir / args.single]
        if not md_files[0].exists():
            print(f"Error: File {args.single} not found in {input_dir}")
            return
    else:
        md_files = sorted([f for f in input_dir.glob('*.md')])

    if not md_files:
        print("No markdown files found to translate")
        return

    print(f"Found {len(md_files)} Hugo post(s) to translate with link preservation")

    if args.dry_run:
        print("\nFiles to be processed:")
        for i, md_file in enumerate(md_files):
            print(f"  {i+1:2d}. {md_file.name}")
        return

    # Process in batches
    log_file = 'scripts/translation_links_progress.log'
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
                output_file = translate_hugo_post(md_file, output_dir)
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

            # Small delay between translations
            time.sleep(2)

        start_idx = end_idx

        if start_idx < len(md_files):
            response = input(f"\nBatch complete. Continue with next batch? (y/n/q to quit): ")
            if response.lower() in ['n', 'q', 'quit']:
                print(f"Stopping. Resume with: --start-from {start_idx}")
                break

    print(f"\nTranslation complete! Translated files saved to: {output_dir}")

if __name__ == "__main__":
    main()
