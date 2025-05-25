#!/usr/bin/env python3
"""
Script to update a single SlideShare embed.
"""

import json
import os

def update_slideshare_embed(old_id, new_key, title=""):
    """Update a single SlideShare embed."""

    # Load the analysis data
    with open('slideshare_embed_analysis.json', 'r') as f:
        analysis = json.load(f)

    if old_id not in analysis:
        print(f"❌ ID {old_id} not found in analysis")
        return False

    info = analysis[old_id]
    new_embed_url = f"https://www.slideshare.net/slideshow/embed_code/key/{new_key}"

    print(f"🔄 Updating SlideShare embed:")
    print(f"   📋 ID: {old_id}")
    print(f"   🎯 Title: {title}")
    print(f"   🔗 New Key: {new_key}")
    print(f"   📁 Files: {len(info['files'])}")
    print()

    # Create the new iframe embed
    new_iframe = f'<iframe src="{new_embed_url}" width="597" height="486" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen></iframe>'

    # Update each file
    updated_files = 0
    for file_path in info['files']:
        if os.path.exists(file_path):
            print(f"   📝 Updating: {file_path}")

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Replace the old embed with the new one
            old_embed = info['old_embed']
            if old_embed in content:
                content = content.replace(old_embed, new_iframe)

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                print(f"   ✅ Updated successfully")
                updated_files += 1
            else:
                print(f"   ⚠️  Old embed not found in file")
        else:
            print(f"   ❌ File not found: {file_path}")

    # Update the analysis file
    analysis[old_id]['new_embed_url'] = new_embed_url
    analysis[old_id]['title'] = title

    with open('slideshare_embed_analysis.json', 'w') as f:
        json.dump(analysis, f, indent=2)

    print(f"   💾 Updated analysis file")
    print()
    print(f"📊 Summary: Updated {updated_files} files")

    return updated_files > 0

if __name__ == "__main__":
    # Update the Test Driven Development - Em busca de feedback util e concreto presentation
    success = update_slideshare_embed("14055677", "ePHVpNd1rPPUEh", "Test Driven Development - Em busca de feedback util e concreto")

    if success:
        print("✅ Update completed successfully!")
    else:
        print("❌ Update failed!")
