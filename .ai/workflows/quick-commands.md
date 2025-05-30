# Quick Commands for Hugo Blog

## Development Server

```bash
hugo server --bind 0.0.0.0 --port 1313 --buildDrafts --buildFuture
```

## Check Build Stats

```bash
hugo --buildDrafts --buildFuture --templateMetrics
```

## Git Commit Template (CRITICAL PATTERN)

```bash
git add .
git commit -m "type(scope): short description

Detailed changes in this commit:
- Specific file: purpose and functionality
- Technical metrics: X files changed, Y insertions
- Hugo build stats: X EN + Y PT pages
- CSS classes: .class-name-img (Npx max-width)
- Image handling: N diagrams in /static/uploads/YYYY/MM/

Summary: What this commit enables and its impact."
```

### Commit Types

- `feat(blog):` - New blog posts or content
- `feat(automation):` - Workflow or tool improvements
- `fix(css):` - Styling corrections
- `docs():` - Documentation updates
- `refactor():` - Code reorganization

### Required Elements

- ✅ Only describe changes in THIS commit
- ✅ Include technical metrics and file counts
- ✅ Hugo page count changes when applicable
- ✅ Specific CSS class names and dimensions
- ✅ Professional, comprehensive documentation
- ❌ No references to previous commits
- ❌ No vague or generic descriptions

## File Structure Check

```bash
# Verify posts exist in both languages
ls -la content/en/posts/YYYY-MM-DD-*
ls -la content/pt/posts/YYYY-MM-DD-*

# Check image uploads
ls -la static/uploads/YYYY/MM/
```

## CSS Class Generator Pattern

```css
.{topic}-pattern-img {
    max-width: {600-800}px;
    width: 100%;
    height: auto;
    margin: 20px 0;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    display: block;
    margin-left: auto;
    margin-right: auto;
}
```

## Hugo Image Reference Format

```markdown
![Image Alt Text](/uploads/YYYY/MM/image-name.png)
{: .css-class-name}
```

## Multilingual File Validation

Both files must exist with identical names:

- `content/en/posts/YYYY-MM-DD-filename.md`
- `content/pt/posts/YYYY-MM-DD-filename.md`
