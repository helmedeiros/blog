#!/usr/bin/env python3
"""
Clean up translated posts by fixing YAML frontmatter and removing LLM artifacts
"""

import os
import re
from pathlib import Path

def clean_frontmatter_title(content):
    """Clean up title field in YAML frontmatter"""
    lines = content.split('\n')
    cleaned_lines = []
    in_frontmatter = False
    title_started = False

    for i, line in enumerate(lines):
        if line.strip() == '---':
            if not in_frontmatter:
                in_frontmatter = True
                cleaned_lines.append(line)
            else:
                # End of frontmatter
                in_frontmatter = False
                cleaned_lines.append(line)
                title_started = False
        elif in_frontmatter:
            if line.startswith('title:'):
                # Extract title content
                title_match = re.match(r'title:\s*["\']?(.*?)["\']?\s*$', line)
                if title_match:
                    title = title_match.group(1)
                    # Clean up common LLM artifacts
                    title = re.sub(r'^Here is the translation.*?:', '', title, flags=re.IGNORECASE).strip()
                    title = re.sub(r'^Translation.*?:', '', title, flags=re.IGNORECASE).strip()
                    title = re.sub(r'\(Note:.*?\)', '', title, flags=re.IGNORECASE).strip()
                    title = re.sub(r'Note:.*', '', title, flags=re.IGNORECASE).strip()
                    title = re.sub(r'Let me know.*', '', title, flags=re.IGNORECASE).strip()

                    # Remove quotes if they exist and re-add them properly
                    title = title.strip('"\'')
                    cleaned_lines.append(f'title: "{title}"')
                    title_started = True
                else:
                    title_started = True
                    cleaned_lines.append(line)
            elif title_started and not line.startswith(('author:', 'layout:', 'date:', 'url:', 'categories:', 'tags:', 'dsq_thread_id:', 'embed:', 'seo_follow:', 'seo_noindex:')):
                # This might be a continuation of a multi-line title, skip it
                continue
            else:
                title_started = False
                cleaned_lines.append(line)
        else:
            # Content after frontmatter
            # Remove common LLM artifacts
            if re.match(r'^Here is the translation.*?:', line.strip(), re.IGNORECASE):
                continue
            if re.match(r'^Translation.*?:', line.strip(), re.IGNORECASE):
                continue
            if re.match(r'^Note:.*', line.strip(), re.IGNORECASE):
                continue
            if re.match(r'^Let me know.*', line.strip(), re.IGNORECASE):
                continue
            if line.strip() == 'Note: The "__PLACEHOLDER__" text remains unchanged as per your request.':
                continue
            if line.strip().startswith('(Note:') and line.strip().endswith(')'):
                continue

            cleaned_lines.append(line)

    return '\n'.join(cleaned_lines)

def clean_post_file(file_path):
    """Clean up a single post file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Clean frontmatter and content
        cleaned_content = clean_frontmatter_title(content)

        # Write back the cleaned content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)

        return True
    except Exception as e:
        print(f"Error cleaning {file_path}: {e}")
        return False

def main():
    """Clean up all translated posts"""
    posts_dir = Path('content/en/posts')

    if not posts_dir.exists():
        print(f"Directory {posts_dir} not found")
        return

    md_files = list(posts_dir.glob('*.md'))
    print(f"Found {len(md_files)} posts to clean up")

    cleaned_count = 0
    for md_file in md_files:
        print(f"Cleaning: {md_file.name}")
        if clean_post_file(md_file):
            cleaned_count += 1
        else:
            print(f"  ✗ Failed to clean {md_file.name}")

    print(f"\nCleaned {cleaned_count}/{len(md_files)} posts successfully")

if __name__ == "__main__":
    main()
