#!/usr/bin/env python3
"""
Blog Translation Script with Backup and Batch Control

This script provides options to:
1. Backup existing English posts
2. Process posts in batches
3. Resume from where you left off
4. Selective translation
"""

import os
import shutil
import argparse
from datetime import datetime
from pathlib import Path
from translate_blog import extract_content_from_html, translate_with_ollama, create_english_html

def backup_existing_posts():
    """Create backup of existing English posts"""
    posts_dir = Path('posts')
    backup_dir = Path(f'posts_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}')

    if posts_dir.exists() and any(posts_dir.iterdir()):
        print(f"Backing up existing English posts to {backup_dir}")
        shutil.copytree(posts_dir, backup_dir)
        print(f"✓ Backup created: {backup_dir}")
        return backup_dir
    else:
        print("No existing English posts found to backup")
        return None

def get_posts_to_process(pt_posts_dir, force_overwrite=False):
    """Get list of posts that need translation"""
    pt_post_dirs = [d for d in pt_posts_dir.iterdir() if d.is_dir()]
    pt_post_dirs.sort()

    if force_overwrite:
        return pt_post_dirs

    # Filter out posts that already have English versions
    posts_to_process = []
    for pt_post_dir in pt_post_dirs:
        en_post_dir = Path('posts') / pt_post_dir.name
        en_html_file = en_post_dir / 'index.html'

        if not en_html_file.exists():
            posts_to_process.append(pt_post_dir)

    return posts_to_process

def translate_batch(posts_batch, start_index=0):
    """Translate a batch of posts"""
    log_file = 'translation_progress.log'

    for i, pt_post_dir in enumerate(posts_batch, start_index + 1):
        post_name = pt_post_dir.name
        pt_html_file = pt_post_dir / 'index.html'
        en_post_dir = Path('posts') / post_name

        print(f"[{i}/{start_index + len(posts_batch)}] Processing: {post_name}")

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

def main():
    parser = argparse.ArgumentParser(description='Translate blog posts with backup and batch control')
    parser.add_argument('--backup', action='store_true', help='Create backup of existing English posts')
    parser.add_argument('--batch-size', type=int, default=10, help='Number of posts to process in each batch (default: 10)')
    parser.add_argument('--start-from', type=int, default=0, help='Index to start from (default: 0)')
    parser.add_argument('--force-overwrite', action='store_true', help='Overwrite existing English posts')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be processed without doing it')

    args = parser.parse_args()

    pt_posts_dir = Path('pt/posts')

    if not pt_posts_dir.exists():
        print("Error: Portuguese posts directory not found")
        return

    # Create backup if requested
    backup_dir = None
    if args.backup:
        backup_dir = backup_existing_posts()

    # Get posts to process
    posts_to_process = get_posts_to_process(pt_posts_dir, args.force_overwrite)

    if not posts_to_process:
        print("No posts need translation. Use --force-overwrite to retranslate existing posts.")
        return

    print(f"\nFound {len(posts_to_process)} posts to translate")

    if args.dry_run:
        print("\nDRY RUN - Posts that would be processed:")
        for i, post_dir in enumerate(posts_to_process):
            print(f"  {i+1:2d}. {post_dir.name}")
        return

    # Process in batches
    start_idx = args.start_from
    batch_size = args.batch_size

    while start_idx < len(posts_to_process):
        end_idx = min(start_idx + batch_size, len(posts_to_process))
        batch = posts_to_process[start_idx:end_idx]

        print(f"\n{'='*60}")
        print(f"Processing batch {start_idx//batch_size + 1}: posts {start_idx+1}-{end_idx}")
        print(f"{'='*60}")

        translate_batch(batch, start_idx)

        start_idx = end_idx

        if start_idx < len(posts_to_process):
            response = input(f"\nBatch complete. Continue with next batch? (y/n/q to quit): ")
            if response.lower() in ['n', 'q', 'quit']:
                print(f"Stopping. Resume with: --start-from {start_idx}")
                break

    print(f"\nTranslation process complete!")
    if backup_dir:
        print(f"Original English posts backed up to: {backup_dir}")

if __name__ == "__main__":
    main()
