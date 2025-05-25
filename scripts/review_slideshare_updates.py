#!/usr/bin/env python3
"""
Script to review all SlideShare updates and verify both language versions.
"""

import json
import os

def review_slideshare_updates():
    """Review all SlideShare updates and check both language versions."""

    # Load the analysis data
    with open('slideshare_embed_analysis.json', 'r') as f:
        analysis = json.load(f)

    print("🔍 SLIDESHARE EMBED UPDATE REVIEW")
    print("=" * 50)
    print()

    updated_count = 0
    pending_count = 0
    total_files_updated = 0

    for slide_id, info in analysis.items():
        has_new_embed = info.get('new_embed_url') is not None
        title = info.get('title', 'Unknown')
        files = info.get('files', [])

        print(f"📋 ID: {slide_id}")
        print(f"   🎯 Title: {title}")
        print(f"   📁 Files: {len(files)}")

        if has_new_embed:
            print(f"   ✅ Status: UPDATED")
            print(f"   🔗 New Key: {info['new_embed_url'].split('/')[-1]}")
            updated_count += 1
            total_files_updated += len(files)

            # Check if both PT and EN versions exist
            pt_files = [f for f in files if '/pt/' in f]
            en_files = [f for f in files if '/en/' in f]

            if pt_files and en_files:
                print(f"   🌐 Languages: PT ✅ EN ✅")
            elif pt_files:
                print(f"   🌐 Languages: PT ✅ EN ❌ (PT only)")
            elif en_files:
                print(f"   🌐 Languages: PT ❌ EN ✅ (EN only)")
            else:
                print(f"   🌐 Languages: Unknown structure")

            # Verify files exist
            missing_files = []
            for file_path in files:
                if not os.path.exists(file_path):
                    missing_files.append(file_path)

            if missing_files:
                print(f"   ⚠️  Missing files: {len(missing_files)}")
                for missing in missing_files:
                    print(f"      - {missing}")
            else:
                print(f"   📂 All files exist: ✅")

        else:
            print(f"   ❌ Status: PENDING")
            pending_count += 1

        print()

    print("📊 SUMMARY")
    print("=" * 30)
    print(f"✅ Updated presentations: {updated_count}")
    print(f"❌ Pending presentations: {pending_count}")
    print(f"📁 Total files updated: {total_files_updated}")
    print(f"📈 Progress: {updated_count}/{len(analysis)} ({updated_count/len(analysis)*100:.1f}%)")
    print()

    if pending_count > 0:
        print("🔄 PENDING PRESENTATIONS:")
        print("-" * 25)
        for slide_id, info in analysis.items():
            if info.get('new_embed_url') is None:
                print(f"   • ID {slide_id}: {info.get('title', 'Unknown')}")
        print()

    # Test a few random embeds to verify they're working
    print("🧪 TESTING RANDOM EMBEDS:")
    print("-" * 25)

    updated_presentations = [(k, v) for k, v in analysis.items() if v.get('new_embed_url')]
    if updated_presentations:
        import random
        test_samples = random.sample(updated_presentations, min(3, len(updated_presentations)))

        for slide_id, info in test_samples:
            files = info.get('files', [])
            if files:
                # Test the first file
                test_file = files[0]
                if os.path.exists(test_file):
                    with open(test_file, 'r', encoding='utf-8') as f:
                        content = f.read()

                    new_key = info['new_embed_url'].split('/')[-1]
                    if new_key in content:
                        print(f"   ✅ ID {slide_id}: Embed key found in {test_file}")
                    else:
                        print(f"   ❌ ID {slide_id}: Embed key NOT found in {test_file}")
                else:
                    print(f"   ⚠️  ID {slide_id}: File not found {test_file}")

    return updated_count, pending_count, total_files_updated

if __name__ == "__main__":
    review_slideshare_updates()
