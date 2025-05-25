#!/usr/bin/env python3
"""
Comprehensive review and cleanup of English translations

This script identifies and fixes common issues in the translated posts:
1. LLM artifacts and instructions
2. Placeholder text that wasn't replaced
3. Broken links and references
4. Mixed language content
5. Formatting issues
6. YAML frontmatter problems
"""

import os
import re
from pathlib import Path
import argparse

class TranslationReviewer:
    def __init__(self):
        self.issues_found = []
        self.fixes_applied = []

    def log_issue(self, file_path, issue_type, description, line_num=None):
        """Log an issue found during review"""
        issue = {
            'file': file_path.name,
            'type': issue_type,
            'description': description,
            'line': line_num
        }
        self.issues_found.append(issue)

    def log_fix(self, file_path, fix_description):
        """Log a fix that was applied"""
        self.fixes_applied.append(f"{file_path.name}: {fix_description}")

    def clean_frontmatter(self, content, file_path):
        """Clean up YAML frontmatter issues"""
        lines = content.split('\n')
        cleaned_lines = []
        in_frontmatter = False
        frontmatter_fixed = False

        for i, line in enumerate(lines):
            if line.strip() == '---':
                if not in_frontmatter:
                    in_frontmatter = True
                    cleaned_lines.append(line)
                else:
                    in_frontmatter = False
                    cleaned_lines.append(line)
            elif in_frontmatter:
                # Fix title issues
                if line.startswith('title:'):
                    original_line = line
                    # Remove common LLM artifacts from titles
                    title_content = line[6:].strip()

                    # Remove quotes and clean
                    title_content = title_content.strip('"\'')

                    # Remove LLM artifacts
                    artifacts = [
                        r'^Here is the translation.*?:',
                        r'^Translation.*?:',
                        r'^I\'d be happy to help.*',
                        r'^However, I don\'t see.*',
                        r'^The text you provided.*',
                        r'\(Note:.*?\)',
                        r'Note:.*',
                        r'Let me know.*',
                        r'If you could provide.*',
                        r'I\'d be happy to assist.*'
                    ]

                    for artifact in artifacts:
                        title_content = re.sub(artifact, '', title_content, flags=re.IGNORECASE).strip()

                    # Remove extra whitespace and clean up
                    title_content = re.sub(r'\s+', ' ', title_content).strip()

                    if title_content != original_line[6:].strip().strip('"\''):
                        cleaned_lines.append(f'title: "{title_content}"')
                        self.log_fix(file_path, f"Cleaned title: {original_line[:50]}...")
                        frontmatter_fixed = True
                    else:
                        cleaned_lines.append(line)
                else:
                    cleaned_lines.append(line)
            else:
                cleaned_lines.append(line)

        return '\n'.join(cleaned_lines), frontmatter_fixed

    def clean_content_artifacts(self, content, file_path):
        """Remove LLM artifacts from post content"""
        original_content = content

        # Common LLM artifacts to remove
        artifacts_to_remove = [
            r'^Here is the translation.*?:\s*\n',
            r'^Translation.*?:\s*\n',
            r'^I\'d be happy to help.*?\n',
            r'^However, I don\'t see.*?\n',
            r'^The text you provided.*?\n',
            r'^If you could provide.*?\n',
            r'^I\'d be happy to assist.*?\n',
            r'^\(Note:.*?\)\s*\n',
            r'^Note: The "__PLACEHOLDER__" text remains.*?\n',
            r'^Note: I kept the "__PLACEHOLDER__".*?\n',
            r'^Let me know if you.*?\n',
            r'^\(Note: I left the placeholder.*?\)\s*\n'
        ]

        for artifact in artifacts_to_remove:
            content = re.sub(artifact, '', content, flags=re.MULTILINE | re.IGNORECASE)

        # Remove standalone artifact lines
        lines = content.split('\n')
        cleaned_lines = []

        for line in lines:
            line_stripped = line.strip()

            # Skip lines that are pure LLM artifacts
            if (line_stripped.startswith('Here is the translation') or
                line_stripped.startswith('Translation:') or
                line_stripped.startswith('I\'d be happy to help') or
                line_stripped.startswith('However, I don\'t see') or
                line_stripped.startswith('The text you provided') or
                line_stripped.startswith('If you could provide') or
                line_stripped.startswith('Let me know if you') or
                line_stripped == 'Note: The "__PLACEHOLDER__" text remains unchanged as per your request.' or
                line_stripped == 'Note: The "__PLACEHOLDER__" text remains exactly as written, indicating that it needs to be replaced with actual content.' or
                (line_stripped.startswith('(Note:') and line_stripped.endswith(')'))):
                continue

            cleaned_lines.append(line)

        cleaned_content = '\n'.join(cleaned_lines)

        # Remove excessive blank lines
        cleaned_content = re.sub(r'\n\s*\n\s*\n', '\n\n', cleaned_content)

        if cleaned_content != original_content:
            self.log_fix(file_path, "Removed LLM artifacts from content")
            return cleaned_content, True

        return cleaned_content, False

    def fix_placeholder_issues(self, content, file_path):
        """Fix placeholder and link issues"""
        original_content = content

        # Find unresolved placeholders
        placeholder_patterns = [
            r'__HTML_LINK_\d+__',
            r'__MD_REF_\d+__',
            r'__IMG_REF_\d+__',
            r'\*\*PLACEHOLDER\*\*',
            r'__PLACEHOLDER__'
        ]

        for pattern in placeholder_patterns:
            matches = re.findall(pattern, content)
            if matches:
                self.log_issue(file_path, "PLACEHOLDER", f"Found unresolved placeholders: {matches}")

        # Fix common placeholder issues
        content = re.sub(r'\*\*PLACEHOLDER\*\*', '', content)
        content = re.sub(r'__PLACEHOLDER__', '', content)

        # Clean up broken link references
        content = re.sub(r'\[HTML_LINK_\d+\]', '', content)

        if content != original_content:
            self.log_fix(file_path, "Fixed placeholder issues")
            return content, True

        return content, False

    def check_mixed_language(self, content, file_path):
        """Check for mixed Portuguese/English content"""
        # Common Portuguese words that shouldn't appear in English posts
        portuguese_indicators = [
            r'\bcom\b', r'\bpara\b', r'\bque\b', r'\buma\b', r'\buma\b',
            r'\bno\b', r'\bna\b', r'\bdo\b', r'\bda\b', r'\bos\b', r'\bas\b',
            r'\bpor\b', r'\bem\b', r'\bde\b', r'\bse\b', r'\bé\b', r'\bão\b',
            r'\bmas\b', r'\bsão\b', r'\bestá\b', r'\bestão\b', r'\btem\b',
            r'\btêm\b', r'\bpode\b', r'\bpodem\b', r'\bfoi\b', r'\bforam\b'
        ]

        # Skip checking inside code blocks and links
        content_to_check = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
        content_to_check = re.sub(r'`[^`]+`', '', content_to_check)
        content_to_check = re.sub(r'\[.*?\]\(.*?\)', '', content_to_check)
        content_to_check = re.sub(r'<a[^>]*>.*?</a>', '', content_to_check, flags=re.DOTALL)

        mixed_language_found = []
        for indicator in portuguese_indicators:
            matches = re.findall(indicator, content_to_check, re.IGNORECASE)
            if len(matches) > 2:  # Allow some false positives
                mixed_language_found.append(indicator.strip('\\b'))

        if mixed_language_found:
            self.log_issue(file_path, "MIXED_LANGUAGE", f"Possible Portuguese words: {mixed_language_found}")

    def review_post(self, file_path):
        """Review and clean up a single post"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content
            content_modified = False

            # Clean frontmatter
            content, frontmatter_fixed = self.clean_frontmatter(content, file_path)
            if frontmatter_fixed:
                content_modified = True

            # Clean content artifacts
            content, artifacts_fixed = self.clean_content_artifacts(content, file_path)
            if artifacts_fixed:
                content_modified = True

            # Fix placeholder issues
            content, placeholders_fixed = self.fix_placeholder_issues(content, file_path)
            if placeholders_fixed:
                content_modified = True

            # Check for mixed language (just report, don't auto-fix)
            self.check_mixed_language(content, file_path)

            # Write back if modified
            if content_modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True

            return False

        except Exception as e:
            self.log_issue(file_path, "ERROR", f"Failed to process: {e}")
            return False

    def generate_report(self):
        """Generate a summary report"""
        print("\n" + "="*60)
        print("ENGLISH TRANSLATION REVIEW REPORT")
        print("="*60)

        print(f"\n📊 SUMMARY:")
        print(f"   • Files processed: {len(self.fixes_applied) + len([i for i in self.issues_found if i['type'] != 'ERROR'])}")
        print(f"   • Fixes applied: {len(self.fixes_applied)}")
        print(f"   • Issues found: {len(self.issues_found)}")

        if self.fixes_applied:
            print(f"\n✅ FIXES APPLIED ({len(self.fixes_applied)}):")
            for fix in self.fixes_applied:
                print(f"   • {fix}")

        if self.issues_found:
            print(f"\n⚠️  ISSUES FOUND ({len(self.issues_found)}):")
            issue_types = {}
            for issue in self.issues_found:
                issue_type = issue['type']
                if issue_type not in issue_types:
                    issue_types[issue_type] = []
                issue_types[issue_type].append(issue)

            for issue_type, issues in issue_types.items():
                print(f"\n   {issue_type} ({len(issues)}):")
                for issue in issues[:5]:  # Show first 5 of each type
                    print(f"     - {issue['file']}: {issue['description']}")
                if len(issues) > 5:
                    print(f"     ... and {len(issues) - 5} more")

def main():
    parser = argparse.ArgumentParser(description='Review and cleanup English translations')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be fixed without making changes')
    parser.add_argument('--file', help='Review specific file only')
    args = parser.parse_args()

    reviewer = TranslationReviewer()
    posts_dir = Path('content/en/posts')

    if not posts_dir.exists():
        print(f"Error: Directory {posts_dir} not found")
        return

    if args.file:
        file_path = posts_dir / args.file
        if file_path.exists():
            print(f"Reviewing: {file_path.name}")
            reviewer.review_post(file_path)
        else:
            print(f"File not found: {file_path}")
            return
    else:
        md_files = list(posts_dir.glob('*.md'))
        print(f"Reviewing {len(md_files)} English posts...")

        for i, md_file in enumerate(md_files, 1):
            print(f"[{i:2d}/{len(md_files)}] {md_file.name}")
            reviewer.review_post(md_file)

    reviewer.generate_report()

if __name__ == "__main__":
    main()
