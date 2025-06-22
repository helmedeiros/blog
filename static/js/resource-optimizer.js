// Resource Optimizer - Load non-critical CSS asynchronously
document.addEventListener('DOMContentLoaded', function() {

  // Function to load CSS asynchronously
  function loadCSS(href, media = 'all') {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = href;
    link.media = 'print'; // Load as print first to avoid blocking
    link.onload = function() {
      this.media = media; // Switch to target media once loaded
    };
    document.head.appendChild(link);
    return link;
  }

  // Load non-critical CSS
  const nonCriticalCSS = [
    '/css/photoswipe.min.css',
    '/css/default-skin.min.css'
  ];

  nonCriticalCSS.forEach(css => {
    const link = document.querySelector(`link[href="${css}"]`);
    if (!link) {
      loadCSS(css);
    }
  });

  // Preload next page resources on hover
  let prefetchedPages = new Set();

  function prefetchPage(url) {
    if (prefetchedPages.has(url)) return;

    const link = document.createElement('link');
    link.rel = 'prefetch';
    link.href = url;
    document.head.appendChild(link);
    prefetchedPages.add(url);
  }

  // Add hover prefetching to internal links
  document.querySelectorAll('a[href^="/"], a[href^="./"], a:not([href^="http"]):not([href^="mailto"]):not([href^="tel"])').forEach(link => {
    if (link.hostname === window.location.hostname) {
      link.addEventListener('mouseenter', function(e) {
        prefetchPage(this.href);
      }, { once: true });
    }
  });

  // Remove unused CSS after page load
  setTimeout(() => {
    const unusedSelectors = [
      '.fa-stack', // Remove if not using FontAwesome stacks
      '.post-image', // Remove if no post images
      '.staticman' // Remove if not using staticman
    ];

    unusedSelectors.forEach(selector => {
      const elements = document.querySelectorAll(selector);
      if (elements.length === 0) {
        // Could remove related CSS rules if needed
        console.log(`Unused selector detected: ${selector}`);
      }
    });
  }, 2000);
});

// Performance monitoring
if ('performance' in window && 'getEntriesByType' in window.performance) {
  window.addEventListener('load', function() {
    setTimeout(() => {
      const navigation = performance.getEntriesByType('navigation')[0];
      const paintEntries = performance.getEntriesByType('paint');

      const metrics = {
        domContentLoaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
        loadComplete: navigation.loadEventEnd - navigation.loadEventStart,
        firstPaint: paintEntries.find(entry => entry.name === 'first-paint')?.startTime,
        firstContentfulPaint: paintEntries.find(entry => entry.name === 'first-contentful-paint')?.startTime
      };

      // Log performance metrics (could send to analytics)
      console.log('Performance Metrics:', metrics);

      // Alert if performance is poor
      if (metrics.firstContentfulPaint > 2500) {
        console.warn('Slow First Contentful Paint detected:', metrics.firstContentfulPaint + 'ms');
      }
    }, 100);
  });
}
