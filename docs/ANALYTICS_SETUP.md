# Analytics Setup Guide 📊

**For Personal Blog Tracking at blog.heliomedeiros.com**

## 🎯 **Recommended Free Analytics Solutions**

### 1. **Google Analytics 4 (GA4)** - _Most Popular & Comprehensive_

**✅ Pros:**

- Completely free with generous limits
- Excellent blog analytics and insights
- Rich reporting and real-time data
- Integration with Google tools
- Mobile app for monitoring
- Bilingual content tracking (EN/PT)

**❌ Cons:**

- Google data collection (privacy concerns)
- Complex interface
- Requires Google account

**Setup Steps:**

1. Go to [Google Analytics](https://analytics.google.com/)
2. Create a new GA4 property for "blog.heliomedeiros.com"
3. Set up Enhanced Measurement
4. Enable blog-specific tracking
5. Replace `G-XXXXXXXXXX` in `config.toml` with your Measurement ID

**Blog Configuration:**

```javascript
// Already configured in your head_custom.html
gtag("config", "G-XXXXXXXXXX", {
  anonymize_ip: true,
  allow_google_signals: false,
  enhanced_measurement: true,
  // Blog-specific tracking
  custom_map: {
    custom_parameter_1: "content_type",
  },
});
```

---

### 2. **Plausible Analytics** - _Privacy-Focused_

**✅ Pros:**

- Privacy-focused (no cookies, GDPR compliant)
- Simple, beautiful dashboard
- Lightweight script (< 1KB)
- Open source
- Real-time data
- 30-day free trial

**❌ Cons:**

- Paid after trial ($9/month for 10K pageviews)
- Limited advanced features
- No demographic data

**Setup:**

```html
<!-- Add to head_custom.html -->
<script
  defer
  data-domain="blog.heliomedeiros.com"
  src="https://plausible.io/js/script.js"
></script>
```

---

### 3. **Umami Analytics** - _Self-Hosted & Free_

**✅ Pros:**

- Completely free (self-hosted)
- Privacy-focused
- Simple interface
- Real-time data
- No data limits
- Perfect for personal blogs

**❌ Cons:**

- Requires server setup
- Technical knowledge needed
- You manage infrastructure

**Setup Options:**

- Deploy on Vercel/Netlify (free tier)
- Use Railway/PlanetScale (free databases)
- Docker self-hosting

---

### 4. **Fathom Analytics** - _Simple & Privacy-First_

**✅ Pros:**

- Privacy-focused
- Simple interface
- GDPR compliant
- 100K pageviews free tier

**❌ Cons:**

- Limited free tier
- Expensive for growth ($14/month)

---

## 🚀 **Quick Start with GA4 (Recommended)**

### Step 1: Get Your GA4 Measurement ID

1. Visit [Google Analytics](https://analytics.google.com/)
2. Create account → Create Property
3. Enter "blog.heliomedeiros.com" as your website
4. Choose "Web" platform
5. Copy your Measurement ID (format: G-XXXXXXXXXX)

### Step 2: Update Configuration

Replace `G-XXXXXXXXXX` in your `config.toml`:

```toml
[services]
  [services.googleAnalytics]
    id = "G-YOUR-ACTUAL-ID"
```

### Step 3: Set Up Goals & Events

Track important blog actions:

- Article reads (scroll depth)
- Popular content engagement
- External link clicks
- Language switching (EN/PT)

---

## 🔧 **Advanced Blog Configuration**

### Blog-Specific Events Already Configured

Your setup automatically tracks:

```javascript
// Content type tracking
gtag("event", "page_view", {
  content_type: "article|home|section",
  language: "en|pt",
});

// Reading engagement
gtag("event", "scroll", {
  event_category: "engagement",
  event_label: "25%|50%|75%|100%",
});

// External link clicks
gtag("event", "click", {
  event_category: "outbound",
  event_label: "external_url",
});
```

---

## 🔒 **Privacy-First Alternative: Umami Self-Host**

### Deploy Umami on Vercel (Free)

1. Fork [Umami repository](https://github.com/umami-software/umami)
2. Deploy to Vercel
3. Connect to PlanetScale database (free tier)
4. Add tracking script:

```html
<script
  defer
  src="https://your-umami.vercel.app/script.js"
  data-website-id="your-website-id"
></script>
```

---

## 📈 **What to Track for Your Blog**

### Essential Blog Metrics

- **Page views** - Most popular articles
- **User sessions** - Reader engagement
- **Traffic sources** - How people find your content
- **Device types** - Mobile vs desktop readers
- **Geographic data** - Global reach of your content

### Content Performance

- **Reading time** - Article engagement depth
- **Bounce rate** - Content quality indicator
- **Popular series** - OKRA, Leadership, Development content
- **Language preferences** - EN vs PT content performance
- **Search queries** - SEO opportunities

### Blog Growth Tracking

- **Returning visitors** - Building audience
- **Social shares** - Content virality
- **Newsletter signups** - Audience building
- **Comment engagement** - Community building

---

## 🎨 **GA4 Dashboard for Your Blog**

### Custom Reports to Create

- **Content Performance** - Top articles by category
- **Audience Insights** - Reader demographics and behavior
- **Language Analysis** - EN vs PT content performance
- **Series Tracking** - OKRA, Leadership content engagement
- **Mobile Experience** - Mobile vs desktop reading patterns

### Real-time Monitoring

Set up mobile app alerts for:

- Traffic spikes on new articles
- Popular content alerts
- Unusual traffic patterns

---

## 🛡️ **Privacy Compliance**

### GDPR/Privacy Settings

```javascript
// Privacy-focused GA4 configuration
gtag("config", "G-XXXXXXXXXX", {
  anonymize_ip: true,
  allow_google_signals: false,
  allow_ad_personalization_signals: false,
});
```

### Cookie Consent (Optional)

For EU readers, consider adding a simple consent banner:

```html
<!-- Simple cookie notice -->
<div id="cookie-notice">
  This blog uses analytics cookies to improve reader experience.
  <button onclick="acceptCookies()">Accept</button>
</div>
```

---

## 🚀 **Deployment**

After configuration:

1. Test locally: `hugo server`
2. Deploy to your hosting platform
3. Verify tracking in GA4 Real-time reports
4. Check both English and Portuguese pages

**Total setup time**: 15-30 minutes
**Cost**: $0 (GA4 free tier perfect for personal blogs)

---

## 📋 **Checklist**

- [ ] GA4 property created for blog.heliomedeiros.com
- [ ] Measurement ID added to config.toml
- [ ] Blog-specific tracking configured
- [ ] Enhanced measurement enabled
- [ ] Content type tracking set up
- [ ] Privacy settings configured
- [ ] Real-time tracking verified
- [ ] Both EN and PT content tracking tested
- [ ] Mobile app configured for monitoring

**🎉 Your blog analytics are ready to track your excellent content!**

Perfect for tracking your leadership insights, OKRA series, development posts, and architectural content across both English and Portuguese languages.
