#!/usr/bin/env python3
"""
Translate all remaining markdown files with automatic cleanup

This script translates files and automatically runs cleanup after each batch
to ensure no prefixes slip through.
"""

import subprocess
import time
from pathlib import Path

def run_cleanup():
    """Run the cleanup script"""
    try:
        result = subprocess.run(['python3', 'scripts/clean_translated_files.py'],
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Cleanup completed")
            return True
        else:
            print(f"✗ Cleanup failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Cleanup error: {e}")
        return False

def count_translated_files():
    """Count how many files have been translated"""
    output_dir = Path('markdown_posts_en')
    if output_dir.exists():
        return len(list(output_dir.glob('*.md')))
    return 0

def main():
    """Translate all remaining files with cleanup"""

    # Check current progress
    current_count = count_translated_files()
    total_files = 67

    print(f"Current progress: {current_count}/{total_files} files translated")

    if current_count >= total_files:
        print("All files already translated!")
        return

    # Start from current count
    start_from = current_count
    batch_size = 5  # Smaller batches for better monitoring

    while start_from < total_files:
        print(f"\n{'='*60}")
        print(f"Translating batch starting from index {start_from}")
        print(f"{'='*60}")

        # Run translation for this batch
        try:
            # Use timeout to prevent hanging
            result = subprocess.run([
                'python3', 'scripts/translate_markdown.py',
                '--start-from', str(start_from),
                '--batch-size', str(batch_size)
            ], input='q\n', text=True, timeout=1800)  # 30 min timeout

        except subprocess.TimeoutExpired:
            print("⚠ Translation batch timed out, continuing...")
        except KeyboardInterrupt:
            print("\n⚠ Translation interrupted by user")
            break
        except Exception as e:
            print(f"✗ Translation error: {e}")
            break

        # Always run cleanup after each batch
        print("\nRunning cleanup...")
        run_cleanup()

        # Check progress
        new_count = count_translated_files()
        if new_count > current_count:
            print(f"✓ Progress: {new_count}/{total_files} files translated")
            current_count = new_count
            start_from = new_count
        else:
            print("⚠ No new files translated, stopping")
            break

        # Small delay to prevent overwhelming the system
        time.sleep(2)

    # Final cleanup
    print("\nRunning final cleanup...")
    run_cleanup()

    final_count = count_translated_files()
    print(f"\nTranslation complete! {final_count}/{total_files} files translated")

if __name__ == "__main__":
    main()
