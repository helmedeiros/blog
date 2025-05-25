# Blog Translation Scripts

This directory contains all the Python scripts used to translate the blog from Portuguese to English using local LLM (ollama/llama3).

## 📋 Table of Contents

- [Workflow Overview](#workflow-overview)
- [Core Scripts](#core-scripts)
- [Utility Scripts](#utility-scripts)
- [Legacy Scripts](#legacy-scripts)
- [Usage Examples](#usage-examples)
- [Requirements](#requirements)

## 🔄 Workflow Overview

The complete translation workflow consists of these steps:

1. **Extract** HTML content to clean markdown
2. **Translate** Portuguese markdown to English
3. **Clean** unwanted prefixes from translations
4. **Replace** HTML content with translated versions
5. **Fix** any remaining title issues

## 🎯 Core Scripts

### 1. `html_to_markdown.py`

**Purpose**: Extract content from Portuguese HTML files and convert to clean markdown.

- Extracts 67 blog posts from `pt/posts/*/index.html`
- Creates clean markdown files in `markdown_posts_pt/`
- Preserves frontmatter (title, date, slug, tags)
- Removes HTML artifacts and social sharing buttons

**Usage**: `python3 html_to_markdown.py`

### 2. `translate_markdown.py`

**Purpose**: Translate Portuguese markdown files to English using ollama/llama3.

- Processes files in `markdown_posts_pt/`
- Creates English versions in `markdown_posts_en/`
- Supports batch processing and resume functionality
- Automatic cleanup of LLM response prefixes

**Usage**:

```bash
python3 translate_markdown.py --batch-size 5 --start-from 0
python3 translate_markdown.py --dry-run  # Preview files to process
```

### 3. `translate_all_with_cleanup.py`

**Purpose**: Automated batch translation with progress tracking.

- Automatically processes all files in batches
- Runs cleanup after each batch
- Progress tracking and error recovery
- Resume capability

**Usage**: `python3 translate_all_with_cleanup.py`

### 4. `replace_html_content.py`

**Purpose**: Replace HTML content with translated markdown while preserving structure.

- Updates all 67 HTML files in `posts/*/index.html`
- Preserves metadata, navigation, and site structure
- Updates SEO tags, Open Graph, and JSON-LD data
- Converts markdown to HTML automatically

**Usage**: `python3 replace_html_content.py`

### 5. `fix_remaining_titles.py`

**Purpose**: Clean up any remaining title issues from translation artifacts.

- Fixes titles with unwanted LLM prefixes
- Updates all metadata consistently
- Final cleanup step

**Usage**: `python3 fix_remaining_titles.py`

## 🛠 Utility Scripts

### `clean_translated_files.py`

**Purpose**: Remove unwanted prefixes from translated markdown files.

- Cleans common LLM response prefixes
- Can be run standalone or as part of batch process
- Processes files in `markdown_posts_en/`

**Usage**: `python3 clean_translated_files.py`

### `test_single_translation.py`

**Purpose**: Test translation on a single file for quality checking.

- Useful for testing prompts and LLM responses
- Quick preview before batch processing

**Usage**: `python3 test_single_translation.py filename.md`

### `markdown_to_hugo.py`

**Purpose**: Convert markdown files to Hugo content structure (alternative approach).

- Creates Hugo-compatible content files
- Alternative to direct HTML replacement
- Not used in final workflow but available for Hugo rebuilds

**Usage**: `python3 markdown_to_hugo.py`

## 📦 Legacy Scripts

### `backup_and_translate.py`

Early version that attempted direct HTML-to-HTML translation. Had issues with mixed language content.

### `translate_blog.py`

Another early version with similar approach. Superseded by the markdown-first workflow.

## 💡 Usage Examples

### Complete Translation Workflow

```bash
# 1. Extract HTML to markdown
python3 html_to_markdown.py

# 2. Translate all content
python3 translate_all_with_cleanup.py

# 3. Replace HTML content
python3 replace_html_content.py

# 4. Fix any remaining issues
python3 fix_remaining_titles.py
```

### Resume Interrupted Translation

```bash
# Check progress and resume from specific point
python3 translate_markdown.py --start-from 25 --batch-size 5
```

### Test Individual Translation

```bash
# Test on a single file first
python3 test_single_translation.py 2008-06-12-hello-world.md
```

## 📋 Requirements

### Python Packages

```bash
pip install beautifulsoup4 markdown
```

### System Requirements

- Python 3.9+
- ollama installed and running
- llama3 model available (`ollama pull llama3`)

### Directory Structure Expected

```
old-blog/
├── pt/posts/           # Portuguese HTML source
├── posts/              # English HTML target
├── markdown_posts_pt/  # Extracted Portuguese markdown
├── markdown_posts_en/  # Translated English markdown
└── scripts/            # These scripts
```

## 🎯 Results

- **67/67 blog posts successfully translated**
- **Authentic tone preserved** from original Portuguese
- **All metadata updated** (SEO, social sharing, structured data)
- **Site structure maintained** (navigation, styling, features)
- **Clean, deployment-ready** English blog

## 🚀 Next Steps

After running these scripts:

1. Test a few translated posts in browser
2. Deploy to hosting platform
3. Update any external links if needed
4. Celebrate your bilingual blog! 🎉
