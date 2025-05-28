#!/usr/bin/env python3
import os
import re
import glob

# Mapping of filenames to appropriate titles
TITLE_MAPPINGS = {
    "2013-06-26-agile-unlocking-our-human-potential-patrick-kua.md": "Agile: Unlocking Our Human Potential - Patrick Kua",
    "2012-08-24-1a-semana-de-lightningtalks-e-fishbowls-no-tecnopuc.md": "First Week of Lightning Talks and Fishbowls at TecnoPUC",
    "2009-08-05-yuml-por-que-escrever-um-blog.md": "yUML: Why Write a Blog?",
    "2008-07-11-minicenario-classificados-na-web.md": "Mini-scenario: Web Classifieds",
    "2010-04-11-materializando-os-valores-xp-aula-13.md": "Materializing XP Values - Class 13",
    "2008-07-12-minicenario-controle-de-obras.md": "Mini-scenario: Construction Control",
    "2009-11-11-rod-johnson-tendencias-em-java-ee-como-serao-os-proximos-5-anos.md": "Rod Johnson: Trends in Java EE - What Will the Next 5 Years Look Like?"
}

def fix_post_title(filepath):
    """Fix a single post's empty title"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        if 'title: ""' not in content:
            return False

        filename = os.path.basename(filepath)

        # Check if we have a predefined title
        if filename in TITLE_MAPPINGS:
            new_title = TITLE_MAPPINGS[filename]
        else:
            # Generate title from filename
            name_without_ext = os.path.splitext(filename)[0]
            title_part = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', name_without_ext)
            new_title = title_part.replace('-', ' ').replace('_', ' ')
            new_title = ' '.join(word.capitalize() for word in new_title.split())

        # Replace the empty title
        new_content = content.replace('title: ""', f'title: "{new_title}"')

        # Write back the file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"Fixed: {filepath}")
        print(f"  New title: {new_title}")
        return True

    except Exception as e:
        print(f"Error fixing {filepath}: {e}")
        return False

def main():
    """Fix all posts with empty titles"""
    fixed_count = 0

    # Find all markdown files in content directories
    for pattern in ['content/en/posts/*.md', 'content/pt/posts/*.md']:
        for filepath in glob.glob(pattern):
            if fix_post_title(filepath):
                fixed_count += 1

    print(f"\nFixed {fixed_count} posts with empty titles.")

if __name__ == "__main__":
    main()
