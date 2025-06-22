// Lazy Loading for Images - Improved Performance
document.addEventListener('DOMContentLoaded', function() {
  const images = document.querySelectorAll('img[data-src]');

  // Use Intersection Observer if supported, fallback to scroll for older browsers
  if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.classList.remove('lazy');
          imageObserver.unobserve(img);

          // Add fade-in effect
          img.addEventListener('load', function() {
            img.style.opacity = '1';
          });
        }
      });
    }, {
      rootMargin: '50px 0px',
      threshold: 0.01
    });

    images.forEach(img => {
      img.style.opacity = '0';
      img.style.transition = 'opacity 0.3s';
      imageObserver.observe(img);
    });
  } else {
    // Fallback for older browsers
    function loadImagesInView() {
      images.forEach(img => {
        if (img.getBoundingClientRect().top <= window.innerHeight + 50) {
          img.src = img.dataset.src;
          img.classList.remove('lazy');
        }
      });
    }

    window.addEventListener('scroll', loadImagesInView);
    window.addEventListener('resize', loadImagesInView);
    loadImagesInView(); // Load initial images
  }
});

// Optimize images with modern formats
function optimizeImages() {
  const images = document.querySelectorAll('img');

  images.forEach(img => {
    // Add loading="lazy" for native lazy loading support
    if (!img.hasAttribute('loading')) {
      img.setAttribute('loading', 'lazy');
    }

    // Add decoding="async" for better performance
    if (!img.hasAttribute('decoding')) {
      img.setAttribute('decoding', 'async');
    }
  });
}

// Run optimization after DOM is loaded
document.addEventListener('DOMContentLoaded', optimizeImages);
