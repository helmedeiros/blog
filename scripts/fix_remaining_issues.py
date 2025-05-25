#!/usr/bin/env python3
"""
Fix remaining issues in English translations:
1. Replace remaining placeholders with appropriate content
2. Fix mixed language issues
3. Clean up specific problematic patterns
"""

import os
import re
from pathlib import Path

def fix_placeholders_in_content(content, file_path):
    """Replace remaining placeholders with appropriate content or remove them"""
    original_content = content

    # Replace common placeholder patterns
    replacements = {
        r'\*\*PLACEHOLDER\*\*': '',
        r'__PLACEHOLDER__': '',
        r'In the last \*\*PLACEHOLDER\*\*': 'In the last section',
        r'the \*\*PLACEHOLDER\*\* defines': 'the system defines',
        r'even those with \*\*PLACEHOLDER\*\*': 'even those with traditional approaches',
        r'According to \*\*PLACEHOLDER\*\*': 'According to the speaker',
        r'The \*\*PLACEHOLDER\*\* presentation': 'The presentation',
        r'with \*\*PLACEHOLDER\*\*': 'with the team',
        r'In \*\*PLACEHOLDER\*\*': 'In this context',
        r'During \*\*PLACEHOLDER\*\*': 'During the session',
        r'The __PLACEHOLDER__ approach': 'The agile approach',
        r'Using __PLACEHOLDER__ methodology': 'Using agile methodology',
        r'__PLACEHOLDER__ framework': 'the framework',
        r'__PLACEHOLDER__ process': 'the process',
        r'__PLACEHOLDER__ team': 'the team',
        r'__PLACEHOLDER__ project': 'the project'
    }

    for pattern, replacement in replacements.items():
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

    # Remove empty placeholder lines
    content = re.sub(r'^\s*\*\*PLACEHOLDER\*\*\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\s*__PLACEHOLDER__\s*$', '', content, flags=re.MULTILINE)

    # Clean up excessive whitespace
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)

    return content, content != original_content

def fix_mixed_language_issues(content, file_path):
    """Fix common mixed language issues"""
    original_content = content

    # Common Portuguese phrases that slipped through
    portuguese_fixes = {
        r'\bTimes ágeis\b': 'Agile teams',
        r'\bA proposta Ágil\b': 'The Agile approach',
        r'\bDesenvolvedores reclamam\b': 'Developers complain',
        r'\bVocê está a mais de\b': 'You have been for more than',
        r'\bO líder do projeto considera\b': 'The project leader considers',
        r'\bO analista cosntantemente\b': 'The analyst constantly',
        r'\bProgramadores e testadores\b': 'Programmers and testers',
        r'\bTestes e verificação\b': 'Tests and verification',
        r'\bestão no nível mais abaixo\b': 'are at the bottom level',
        r'\bda cadeia alimentar\b': 'of the food chain',
        r'\bnão são partes integrantes\b': 'are not integral parts',
        r'\be respeitáveis do processo\b': 'and respectable parts of the process',
        r'\bpor cima do burocrático\b': 'through the bureaucratic',
        r'\bprocesso de controle de mudanças\b': 'change control process',
        r'\bnenhuma funcionalidade útil\b': 'no useful functionality',
        r'\baos usuários\b': 'to users',
        r'\bfazer os usuarios assinarem\b': 'get users to sign',
        r'\bo tal documento dos requerimentos\b': 'the requirements document'
    }

    for portuguese, english in portuguese_fixes.items():
        content = re.sub(portuguese, english, content, flags=re.IGNORECASE)

    return content, content != original_content

def fix_broken_links(content, file_path):
    """Fix broken link references"""
    original_content = content

    # Fix broken link patterns
    content = re.sub(r'\[HTML_LINK_\d+\]', '', content)
    content = re.sub(r'\[MD_REF_\d+\]', '', content)
    content = re.sub(r'\[IMG_REF_\d+\]', '', content)

    # Fix orphaned link references like "Artigo sobre [HTML_LINK_0]"
    content = re.sub(r'Artigo sobre \[HTML_LINK_\d+\]', 'Related article', content)
    content = re.sub(r'_Artigo sobre \[HTML_LINK_\d+\]_', '_Related article_', content)

    return content, content != original_content

def process_file(file_path):
    """Process a single file to fix remaining issues"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        fixes_applied = []

        # Fix placeholders
        content, placeholder_fixed = fix_placeholders_in_content(content, file_path)
        if placeholder_fixed:
            fixes_applied.append("Fixed placeholders")

        # Fix mixed language
        content, language_fixed = fix_mixed_language_issues(content, file_path)
        if language_fixed:
            fixes_applied.append("Fixed mixed language")

        # Fix broken links
        content, links_fixed = fix_broken_links(content, file_path)
        if links_fixed:
            fixes_applied.append("Fixed broken links")

        # Write back if any fixes were applied
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ {file_path.name}: {', '.join(fixes_applied)}")
            return True
        else:
            print(f"   {file_path.name}: No issues found")
            return False

    except Exception as e:
        print(f"❌ {file_path.name}: Error - {e}")
        return False

def main():
    posts_dir = Path('content/en/posts')

    if not posts_dir.exists():
        print(f"Error: Directory {posts_dir} not found")
        return

    md_files = list(posts_dir.glob('*.md'))
    print(f"🔧 Fixing remaining issues in {len(md_files)} English posts...\n")

    fixed_count = 0
    for md_file in md_files:
        if process_file(md_file):
            fixed_count += 1

    print(f"\n📊 Summary: Fixed issues in {fixed_count}/{len(md_files)} files")

if __name__ == "__main__":
    main()
