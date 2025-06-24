# Google Analytics 4 Setup for Hugo Blog

## Overview

This blog uses Google Analytics 4 (GA4) with enhanced topic tracking to understand which content resonates most with readers. The analytics setup provides comprehensive insights into content performance, user navigation patterns, and topic preferences.

## Measurement Configuration

- **GA4 Property ID**: G-GL0Q1PNV4W
- **Cross-subdomain tracking**: Enabled for heliomedeiros.com domain
- **Privacy-focused**: IP anonymization, no ad personalization
- **Enhanced measurement**: Enabled for automatic event tracking

## Topic Tracking Features

### 1. Content Classification

Every page view is automatically tagged with:

- **Content Type**: home, article, section, other
- **Language**: en (English) or pt (Portuguese)
- **Author**: Post author information
- **Category**: Primary category for articles
- **Tags**: All tags associated with content
- **Reading Time**: Estimated reading time for articles
- **Word Count**: Article length metrics

### 2. Topic Interest Tracking

For every article page, the system automatically tracks:

- **Category Views**: Each category gets a separate event
- **Tag Views**: Each tag gets a separate event
- **Content Engagement**: Detailed article-level metrics

### 3. Navigation Pattern Analysis

The analytics tracks how users navigate between content:

- **Post-to-Post Navigation**: When users click from one article to another
- **Topic Exploration**: When users browse category or tag pages
- **External Link Clicks**: With source context (which category they came from)

### 4. Engagement Depth Measurement

Multiple layers of engagement tracking:

- **Scroll Depth**: 25%, 50%, 75%, 90%, 100% milestones
- **Time Engagement**: 30s, 60s, 2min, 5min milestones
- **Session Completion**: Total time spent when leaving

## Analytics Reports You Can Create

### Most Popular Topics

In Google Analytics, you can create reports to see:

1. **Top Categories** → Events → category_view (event_label shows category names)
2. **Top Tags** → Events → tag_view (event_label shows tag names)
3. **Content Performance** → Events → content_view (shows individual articles)

### Navigation Insights

Track how users discover content:

1. **Topic Exploration** → Events → topic_navigation (users browsing categories/tags)
2. **Post Discovery** → Events → internal_navigation (post-to-post movement)
3. **External Referrals** → Events → click (outbound links with source context)

### Engagement Quality

Measure content quality and reader satisfaction:

1. **Reading Completion** → Events → scroll (100% completion rate)
2. **Deep Engagement** → Events → timing_complete (time milestones)
3. **Content Stickiness** → Events → session_complete (total session time)

## Setting Up Custom Reports

### 1. Most Searched Topics Report

- **Primary dimension**: Event name (category_view, tag_view)
- **Secondary dimension**: Event label (shows specific topics)
- **Metric**: Event count
- **Filter**: Event category = "topic_tracking"

### 2. Content Performance by Language

- **Primary dimension**: Page title or content_category
- **Secondary dimension**: Language (en/pt)
- **Metrics**: Page views, scroll depth, session duration

### 3. Navigation Flow Analysis

- **Primary dimension**: Event name (internal_navigation, topic_navigation)
- **Secondary dimension**: Source category
- **Metric**: Event count

## Advanced Analytics Setup

### Custom Dimensions (Already Configured)

- **custom_parameter_1**: content_type
- **custom_parameter_2**: content_category
- **custom_parameter_3**: content_tags

### Goals and Conversions

You can set up goals for:

- **Deep Reading**: Users who scroll 75%+ and spend 2+ minutes
- **Topic Exploration**: Users who visit 3+ category/tag pages
- **Content Discovery**: Users who navigate between 3+ articles

## Privacy and Compliance

- **IP Anonymization**: Enabled
- **Google Signals**: Disabled
- **Ad Personalization**: Disabled
- **Cookie Consent**: 2-year expiration
- **Production Only**: Analytics only loads on live site

## Viewing Your Data

### Real-time Reports

- **Active Users**: See current readers and what they're reading
- **Page Views**: Which articles are being read right now
- **Events**: Live topic tracking and navigation events

### Historical Analysis

- **Most Popular Categories**: Leadership, Development, Architecture, etc.
- **Language Preferences**: EN vs PT content performance
- **Seasonal Trends**: Topic interest over time
- **Reading Patterns**: Which topics lead to deeper engagement

### Content Strategy Insights

Use the data to:

1. **Identify High-Performing Topics**: Focus on categories with most engagement
2. **Optimize Content Mix**: Balance between popular and niche topics
3. **Improve Navigation**: Enhance pathways to your best content
4. **Language Strategy**: Optimize content distribution between EN/PT

## Implementation Details

- **File**: `layouts/partials/analytics.html`
- **Template Engine**: Hugo with Go templates
- **Event Tracking**: JavaScript-based with Hugo context
- **Cross-subdomain**: Configured for heliomedeiros.com
- **Privacy**: GDPR-compliant settings

## Troubleshooting

- **No Data**: Check browser console for errors
- **Missing Events**: Verify JavaScript execution
- **Cross-subdomain Issues**: Confirm cookie domain settings
- **Template Errors**: Check Hugo build logs

This comprehensive setup gives you deep insights into which topics resonate most with your audience, helping you create more targeted and engaging content.
