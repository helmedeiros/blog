const CACHE_NAME = 'helio-blog-v1';
const STATIC_CACHE_URLS = [
  '/',
  '/css/main.css',
  '/css/syntax.css',
  '/css/codeblock.css',
  '/css/custom-layout.css',
  '/css/blog-style.css',
  '/js/main.js',
  '/js/load-photoswipe.js',
  '/favicon.svg'
];

// Helper function to check if request should be cached
function shouldCache(request) {
  // Only cache HTTP/HTTPS requests
  if (!request.url.startsWith('http://') && !request.url.startsWith('https://')) {
    return false;
  }

  // Don't cache chrome-extension or other unsupported schemes
  if (request.url.startsWith('chrome-extension://') ||
      request.url.startsWith('moz-extension://') ||
      request.url.startsWith('safari-extension://')) {
    return false;
  }

  // Only cache GET requests
  if (request.method !== 'GET') {
    return false;
  }

  return true;
}

// Install event
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        return cache.addAll(STATIC_CACHE_URLS);
      })
      .then(() => {
        return self.skipWaiting();
      })
  );
});

// Activate event
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => {
      return self.clients.claim();
    })
  );
});

// Fetch event
self.addEventListener('fetch', (event) => {
  // Filter out unsupported requests early
  if (!shouldCache(event.request)) {
    return;
  }

  // Handle static assets
  if (event.request.url.includes('/css/') ||
      event.request.url.includes('/js/') ||
      event.request.url.includes('/favicon') ||
      event.request.url.includes('/fonts/')) {

    event.respondWith(
      caches.match(event.request)
        .then((response) => {
          if (response) {
            return response;
          }
          return fetch(event.request)
            .then((response) => {
              // Don't cache non-successful responses
              if (!response || response.status !== 200 || response.type !== 'basic') {
                return response;
              }

              const responseToCache = response.clone();
              caches.open(CACHE_NAME)
                .then((cache) => {
                  cache.put(event.request, responseToCache)
                    .catch((error) => {
                      console.log('Cache put failed:', error);
                    });
                });

              return response;
            });
        })
    );
  }

  // Handle HTML pages with network-first strategy
  else if (event.request.headers.get('accept') && event.request.headers.get('accept').includes('text/html')) {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          const responseToCache = response.clone();
          caches.open(CACHE_NAME)
            .then((cache) => {
              cache.put(event.request, responseToCache)
                .catch((error) => {
                  console.log('Cache put failed:', error);
                });
            });
          return response;
        })
        .catch(() => {
          return caches.match(event.request)
            .then((response) => {
              return response || caches.match('/');
            });
        })
    );
  }
});
