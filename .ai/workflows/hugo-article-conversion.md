# Hugo Article Conversion Workflow

## Trigger

When user provides content with format: "Please convert these articles for [date]: @english-file.md @portuguese-file.md"

**Alternative trigger**: "@.ai/workflows/hugo-article-conversion.md Please convert these articles for [date]: @english-file.md @portuguese-file.md"

## Input Requirements

1. **Date**: DD-MM-YYYY format
2. **Files**: Two attached markdown files with identical names
3. **Images**: List of referenced images (if any)
4. **Content Type**: Technical/Tutorial/Conceptual

## Execution Steps

### Step 1: Parse Input

- Extract date and convert to YYYY-MM-DD
- Identify base filename from attachments
- Validate both files have identical names
- Extract image references from content

### Step 2: Create Hugo Posts

- Generate proper Hugo front matter using `.ai/templates/hugo-front-matter.yaml`
- Convert markdown content for Hugo compatibility
- Place files in correct language directories:
  - `content/en/posts/YYYY-MM-DD-filename.md`
  - `content/pt/posts/YYYY-MM-DD-filename.md`

### Step 3: Handle Images

- Create image placeholder files in `/static/uploads/YYYY/MM/`
- Convert image references to Hugo format: `![Alt](/uploads/YYYY/MM/image.png)`
- Generate appropriate CSS class using `.ai/templates/css-image-class.css`
- Update `static/css/custom-layout.css` with responsive styling

### Step 4: Test and Verify

- Ensure Hugo development server is running
- Verify posts appear in build statistics
- Check both language versions are accessible at localhost:1313
- Confirm multilingual linking works (identical filenames)

### Step 5: Git Commit

- Stage all changes with `git add .`
- Create commit following `.cursor-rules` Git Commit Standards
- Include technical metrics and Hugo build stats
- Verify commit message follows Technical Conventional format

## Success Criteria

- ✅ Hugo detects new posts immediately
- ✅ Both language versions accessible at localhost:1313
- ✅ Images have responsive styling with topic-appropriate CSS
- ✅ Page count increases in build stats (EN + PT)
- ✅ Clean git commit with conventional format
- ✅ Multilingual linking functional with identical filenames

## Templates Used

- Front matter: `.ai/templates/hugo-front-matter.yaml`
- CSS styling: `.ai/templates/css-image-class.css`
- Commit format: Defined in `.cursor-rules` Git Commit Standards
