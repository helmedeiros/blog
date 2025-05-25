# Domain Migration Checklist: old-blog → blog.heliomedeiros.com

## ✅ Completed (Code Changes)

- [x] Updated `config.toml` baseurl
- [x] Updated `static/CNAME` file
- [x] Updated `content/pt/posts/config.yaml`
- [x] Updated `README.md` references
- [x] Committed changes to git

## 🔧 DNS & Hosting Setup Required

### 1. DNS Configuration

- [ ] **Create CNAME record**: `blog.heliomedeiros.com` → `[your-github-username].github.io`
- [ ] **Verify DNS propagation**: Use `dig blog.heliomedeiros.com` or online DNS checker
- [ ] **Wait for propagation**: Can take up to 24-48 hours

### 2. GitHub Pages Configuration

- [ ] **Push changes** to your GitHub repository
- [ ] **Go to repository Settings** → Pages
- [ ] **Update custom domain** from `old-blog.heliomedeiros.com` to `blog.heliomedeiros.com`
- [ ] **Enable "Enforce HTTPS"** (after DNS propagation)

### 3. SSL Certificate

- [ ] **Wait for GitHub to provision** SSL certificate for new domain
- [ ] **Test HTTPS access**: `https://blog.heliomedeiros.com`

### 4. Redirects (Optional but Recommended)

- [ ] **Set up redirect** from `old-blog.heliomedeiros.com` to `blog.heliomedeiros.com`
- [ ] **Update any external links** pointing to old domain
- [ ] **Update social media profiles** with new domain

### 5. SEO Considerations

- [ ] **Submit new sitemap** to Google Search Console: `https://blog.heliomedeiros.com/sitemap.xml`
- [ ] **Set up 301 redirects** from old domain (if possible)
- [ ] **Update canonical URLs** (Hugo will handle this automatically)

### 6. Testing Checklist

- [ ] **Homepage loads**: `https://blog.heliomedeiros.com`
- [ ] **Portuguese version**: `https://blog.heliomedeiros.com/pt`
- [ ] **Posts listing**: `https://blog.heliomedeiros.com/posts/`
- [ ] **Individual posts**: Test a few post URLs
- [ ] **Language switching**: Verify EN ↔ PT links work
- [ ] **RSS feeds**: `https://blog.heliomedeiros.com/index.xml`

### 7. Analytics & Tools Update

- [ ] **Google Analytics**: Update property URL (if using)
- [ ] **Search Console**: Add new property for new domain
- [ ] **Social sharing**: Test sharing buttons work with new domain

## 🚀 Ready to Write!

Once the domain migration is complete:

- [ ] **Create your first new post**: `hugo new posts/2024-01-15-back-to-blogging.md`
- [ ] **Test the complete workflow**: Write → Preview → Publish
- [ ] **Share your return**: Announce on social media with new domain

## 📝 Notes

- The new domain `blog.heliomedeiros.com` is much cleaner and professional
- All your existing content and SEO value will be preserved
- The bilingual setup will continue working seamlessly
- Modern Hugo setup is ready for years of blogging

---

**Estimated total time**: 2-4 hours (mostly waiting for DNS propagation)
