# Quick Commands for Hugo Blog

## Development Server

```bash
hugo server --bind 0.0.0.0 --port 1313 --buildDrafts --buildFuture
```

## Check Build Stats

```bash
hugo --buildDrafts --buildFuture --templateMetrics
```

## Git Commit Template

```bash
git add .
git commit -m "feat(blog): add [topic] articles (YYYY-MM-DD)

- Add Portuguese and English posts for [topic]
- Include N images/diagrams: [list]
- Add CSS styling with .[topic]-img class (Npx max-width)
- Update Hugo builds to X EN + Y PT pages

Content covers: [description]"
```

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
