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

- Generate proper Hugo front matter with timestamp
- Convert markdown content for Hugo compatibility
- Place files in correct language directories:
  - `content/en/posts/YYYY-MM-DD-filename.md`
  - `content/pt/posts/YYYY-MM-DD-filename.md`

### Step 3: Handle Images

- Create image placeholder files in `/static/uploads/YYYY/MM/`
- Convert image references to Hugo format
- Generate appropriate CSS class for topic
- Update `static/css/custom-layout.css` with responsive styling

### Step 4: Test and Verify

- Ensure Hugo development server is running
- Verify posts appear in build statistics
- Check both language versions are accessible
- Confirm multilingual linking works

### Step 5: Git Commit

- Stage all changes
- Create conventional commit with detailed body
- Include build statistics and content summary

## Success Criteria

- ✅ Hugo detects new posts immediately
- ✅ Both language versions accessible at localhost:1313
- ✅ Images have responsive styling
- ✅ Page count increases in build stats
- ✅ Clean git commit with conventional format

## Example Output

```
feat(blog): add design patterns articles (2008-07-08)

- Add Portuguese and English posts for behavioral patterns
- Include 10 UML diagrams: chain-of-responsibility.png, command.png, ...
- Add CSS styling with .behavioral-pattern-img class (800px max-width)
- Update Hugo builds to 550 EN + 554 PT pages

Content covers: 10 Gang of Four behavioral design patterns including
Chain of Responsibility, Command, Interpreter, Iterator, Mediator,
Memento, Observer, State, Strategy, and Template Method
```
