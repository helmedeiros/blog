# Helio Medeiros - Technology Blog

This is a bilingual technology blog covering agile development, software engineering, and technology insights spanning from 2008-2014.

## 🌍 Languages

- **Portuguese** (original): Available at `/pt/posts/`
- **English** (translated): Available at `/posts/`

## 🚀 Translation Project

This blog was successfully translated from Brazilian Portuguese to English using **local LLM technology** (ollama/llama3) in May 2025.

### Translation Results

- ✅ **67 blog posts** fully translated
- ✅ **Authentic tone preserved** from original Portuguese
- ✅ **Technical accuracy maintained**
- ✅ **All metadata updated** (SEO, social sharing, structured data)
- ✅ **Site structure intact** (navigation, styling, features)

### How It Was Done

The translation was accomplished using a sophisticated workflow with local AI:

1. **Content Extraction**: HTML posts converted to clean markdown
2. **AI Translation**: Local llama3 model via ollama for authentic translations
3. **Quality Control**: Automated cleanup of translation artifacts
4. **Seamless Integration**: Content replaced while preserving all site functionality

For technical details and scripts used, see [`scripts/README.md`](scripts/README.md).

## 📚 Content Topics

The blog covers various technology topics including:

- **Agile Methodologies** (SCRUM, XP, Kanban)
- **Software Development** practices and patterns
- **Project Management** experiences
- **Technology Events** and conference reports
- **Programming Languages** and tools
- **Data Science** and Big Data

## 🏗 Technical Setup

This is a Hugo-generated static site with:

- **Hugo Static Site Generator** with Beautiful Hugo theme
- **Bilingual Support**: English and Portuguese content
- **GitHub Actions**: Automated build and deployment
- **Custom Domain**: `old-blog.heliomedeiros.com`
- **Responsive design** with SEO optimization
- **Social sharing integration**

## 🚀 Deployment

The site is automatically deployed using GitHub Actions:

1. **Source files** are stored in this repository
2. **GitHub Actions** builds the Hugo site on every push to `main`/`master`
3. **Generated static files** are deployed to GitHub Pages
4. **Custom domain** `old-blog.heliomedeiros.com` serves the content

### Local Development

```bash
# Install Hugo (macOS)
brew install hugo

# Clone the repository
git clone [repository-url]
cd blog

# Start local development server
hugo server -D

# Build for production
hugo --minify
```

### Manual Deployment

If needed, you can manually trigger deployment:

1. Go to the **Actions** tab in GitHub
2. Select **Deploy Hugo site to Pages**
3. Click **Run workflow**

## 📖 Reading

- **Browse in English**: [old-blog.heliomedeiros.com](https://old-blog.heliomedeiros.com)
- **Ler em Português**: [old-blog.heliomedeiros.com/pt](https://old-blog.heliomedeiros.com/pt)

---

_This bilingual blog represents years of technology insights made accessible to both Portuguese and English-speaking audiences through the power of local AI translation._
