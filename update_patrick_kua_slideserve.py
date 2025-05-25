#!/usr/bin/env python3
"""
Script to update Patrick Kua's presentation with SlideServe embed.
"""

import json
import os

def update_patrick_kua_slideserve():
    """Update Patrick Kua's presentation with SlideServe embed."""

    slide_id = "23530373"
    title = "Agile: Unlocking our human potential - Patrick Kua"
    slideserve_url = "https://www.slideserve.com/thekua/agile-unlocking-our-human-potential-7318736"

    # Load the analysis data
    with open('slideshare_embed_analysis.json', 'r') as f:
        analysis = json.load(f)

    if slide_id not in analysis:
        print(f"❌ ID {slide_id} not found in analysis")
        return False

    info = analysis[slide_id]

    print(f"🔄 Updating Patrick Kua's presentation:")
    print(f"   📋 ID: {slide_id}")
    print(f"   🎯 Title: {title}")
    print(f"   🔗 SlideServe URL: {slideserve_url}")
    print(f"   📁 Files: {len(info['files'])}")
    print()

    # Create the new SlideServe embed
    new_embed = f'''<div style="margin-bottom: 20px;">
<iframe src="https://www.slideserve.com/embed/7318736"
        width="597" height="486" frameborder="0" marginwidth="0" marginheight="0"
        scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;"
        allowfullscreen></iframe>
<div style="margin-bottom:5px">
    <strong><a href="{slideserve_url}" target="_blank">Agile: Unlocking our human potential by Patrick Kua</a></strong>
</div>
</div>'''

    # Update each file
    updated_files = 0
    for file_path in info['files']:
        if os.path.exists(file_path):
            print(f"   📝 Updating: {file_path}")

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Find and replace the old embed section
            old_embed_start = '<div style="margin-bottom: 20px;">'
            old_embed_end = '</div>\n</div>'

            start_idx = content.find(old_embed_start)
            if start_idx != -1:
                # Find the end of the embed section
                end_idx = content.find(old_embed_end, start_idx)
                if end_idx != -1:
                    end_idx += len(old_embed_end)

                    # Replace the old embed with the new one
                    new_content = content[:start_idx] + new_embed + content[end_idx:]

                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)

                    print(f"   ✅ Updated successfully")
                    updated_files += 1
                else:
                    print(f"   ⚠️  Could not find embed end in file")
            else:
                print(f"   ⚠️  Could not find embed start in file")
        else:
            print(f"   ❌ File not found: {file_path}")

    # Update the analysis file
    analysis[slide_id]['new_embed_url'] = slideserve_url
    analysis[slide_id]['title'] = title
    analysis[slide_id]['platform'] = 'slideserve'

    with open('slideshare_embed_analysis.json', 'w') as f:
        json.dump(analysis, f, indent=2)

    print(f"   💾 Updated analysis file")
    print()
    print(f"📊 Summary: Updated {updated_files} files")

    return updated_files > 0

if __name__ == "__main__":
    success = update_patrick_kua_slideserve()

    if success:
        print("✅ Patrick Kua's presentation updated successfully!")
        print("🔗 Now using SlideServe embed instead of SlideShare")
    else:
        print("❌ Update failed!")
