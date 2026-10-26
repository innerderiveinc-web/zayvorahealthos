// ZMIE Progressive Web App (PWA) Offline-First Service Worker
// Version 8.0 - Hardened (Zero Private API Caching & Verified Precache URLs)
const CACHE_NAME = 'zmie-v8-offline-cache';
const PRECACHE_URLS = [
  '/',
  '/index.html',
  '/workbench',
  '/catalog_seed.json'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(PRECACHE_URLS).catch((err) => {
        console.warn('[PWA SW] Precache warning:', err);
      });
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((k) => {
          if (k !== CACHE_NAME) return caches.delete(k);
        })
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
  
  // Skip non-http schemes (e.g. chrome-extension, data:)
  if (!event.request.url.startsWith('http')) return;

  const url = new URL(event.request.url);

  // SECURITY: Strictly exclude dynamic/authenticated API routes from offline browser cache
  // Prevents private research projects, patient notes, or audit records from being cached
  if (url.pathname.startsWith('/v1/') || url.pathname.startsWith('/api/')) {
    return;
  }

  event.respondWith(
    fetch(event.request)
      .then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200 && event.request.url.startsWith(self.location.origin)) {
          const clone = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
        }
        return networkResponse;
      })
      .catch(() => {
        return caches.match(event.request).then((cachedResponse) => {
          return cachedResponse || caches.match('/index.html') || caches.match('/workbench');
        });
      })
  );
});
