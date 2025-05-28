# Hugo Posts Visibility Issue - Empty Titles Fix

## Problem Identified

Some Hugo blog posts were not visible because they had empty titles in their front matter (`title: ""`).

## Root Cause

Hugo requires posts to have valid titles to properly display them. Posts with empty titles (`title: ""`) were being filtered out or not displayed correctly.

## Posts Fixed

We identified and fixed **10 posts** with empty titles:

### English Posts Fixed:

1. `2013-06-26-agile-unlocking-our-human-potential-patrick-kua.md` → "Agile: Unlocking Our Human Potential - Patrick Kua"
2. `2012-08-24-1a-semana-de-lightningtalks-e-fishbowls-no-tecnopuc.md` → "First Week of Lightning Talks and Fishbowls at TecnoPUC"
3. `2009-08-05-yuml-por-que-escrever-um-blog.md` → "yUML: Why Write a Blog?"
4. `2008-07-11-minicenario-classificados-na-web.md` → "Mini-scenario: Web Classifieds"
5. `2010-04-11-materializando-os-valores-xp-aula-13.md` → "Materializing XP Values - Class 13"
6. `2008-07-12-minicenario-controle-de-obras.md` → "Mini-scenario: Construction Control"
7. `2009-11-11-rod-johnson-tendencias-em-java-ee-como-serao-os-proximos-5-anos.md` → "Rod Johnson: Trends in Java EE - What Will the Next 5 Years Look Like?"
8. `2008-07-12-minicenario-controle-de-bolao.md` → "Mini-scenario: Lottery Pool Control System"
9. `2012-08-01-slides-gerando-valor-desafios-no-lancamentdo-conteudo-pago.md` → "Generating Value – Challenges in Launching Paid Content"
10. `2012-09-06-keynote-growing-into-fluency-and-excellence-james-shore.md` → "Growing Fluency and Excellence"

## Solution Applied

1. **Identified** all posts with `title: ""` using grep search
2. **Created scripts** to automatically fix titles:
   - `fix_empty_titles.py` - Analysis script to identify issues
   - `fix_all_titles.py` - Automated fix script with predefined mappings
3. **Generated appropriate titles** based on:
   - Content analysis
   - Filename parsing
   - Manual curation for better readability
4. **Verified the fix** by running Hugo build and listing all content

## Results

- **Before**: Some posts were invisible due to empty titles
- **After**: All posts are now properly recognized by Hugo
- **Hugo build**: Successfully shows 539 EN pages and 543 PT pages
- **Verification**: All fixed posts now appear in `hugo list all` output

## Scripts Created

- `scripts/fix_empty_titles.py` - Diagnostic script
- `scripts/fix_all_titles.py` - Automated fix script

## Verification Commands Used

```bash
# Check for empty titles
grep 'title: ""' content/**/*.md

# Build site and verify
hugo --buildDrafts --buildFuture

# List all content to verify posts are recognized
hugo list all

# Check specific fixed posts
hugo list all | grep "Mini-scenario\|Generating Value\|yUML\|Lightning Talks"
```

## Date: January 2025

## Status: ✅ RESOLVED
