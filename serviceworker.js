self.addEventListener('install', (e) => {
    e.waitUntil(
      caches.open('install-store').then((cache) => cache.addAll([
        '/img/logo.png',
        '/img/favicon.png',
        '/img/avatar.png',
        '/img/daily_pic.png',
        '/img/sidebar_header.png',
        'https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@100;300;400;500;700;900&display=swap',
        'https://fonts.googleapis.com/css?family=Material+Icons|Material+Icons+Outlined|Material+Icons+Two+Tone|Material+Icons+Round|Material+Icons+Sharp',
        '/img/random/material-1.webp',
        '/img/random/material-2.webp',
        '/img/random/material-3.webp',
        '/img/random/material-4.webp',
        '/img/random/material-5.webp',
        '/img/random/material-6.webp',
        '/img/random/material-7.webp',
        '/img/random/material-8.webp',
        '/img/random/material-9.webp',
        '/img/random/material-10.webp',
        '/img/random/material-11.webp',
        '/img/random/material-12.webp',
        '/img/random/material-13.webp',
        '/img/random/material-14.webp',
        '/img/random/material-15.webp',
        '/img/random/material-16.webp',
        '/img/random/material-17.webp',
        '/img/random/material-18.webp',
        '/img/random/material-19.webp',
        '/img/random/material-20.webp',
        '/img/random/material-21.webp',
        '/img/random/material-22.webp',
        '/img/random/material-23.webp',
        '/img/random/material-24.webp',
        '/img/random/material-25.webp',
        '/img/random/material-26.webp',
        '/img/random/material-27.webp',
        '/img/random/material-28.webp',
        '/img/random/material-29.webp',
        '/img/random/material-30.webp',
        '/img/random/material-31.webp',
        '/img/random/material-32.webp',
        '/page/2',
        '/page/3',
        '/page/4',
        '/page/5',
      ])),
    );
  });
  
  self.addEventListener('fetch', (e) => {
    console.log(e.request.url);
    e.respondWith(
      caches.match(e.request).then((response) => response || fetch(e.request)),
    );
  });