self.addEventListener('install', (e) => {
    e.waitUntil(
      caches.open('fox-store').then((cache) => cache.addAll([
        '/img/logo.png',
        '/img/favicon.png',
        '/img/avatar.png',
        '/img/daily_pic.png',
        '/img/sidebar_header.png',
        'https://cdn.jsdelivr.net/npm/noto-sans-sc@11.0.1/all.css',
      ])),
    );
  });
  
  self.addEventListener('fetch', (e) => {
    console.log(e.request.url);
    e.respondWith(
      caches.match(e.request).then((response) => response || fetch(e.request)),
    );
  });