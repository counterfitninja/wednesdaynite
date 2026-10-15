const CACHE_NAME = 'wnfc-v2';
const urlsToCache = [
  '/',
  '/static/wn.png'
];

// Install service worker
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
      .then(() => self.skipWaiting())
  );
});

// Remove old app caches before taking over existing tabs.
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(names => Promise.all(
        names.filter(name => name.startsWith('wnfc-') && name !== CACHE_NAME)
          .map(name => caches.delete(name))
      ))
      .then(() => self.clients.claim())
  );
});

// Fetch from cache
self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;

  // Pages contain live match data and must not use an old cached build.
  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request).catch(error =>
        caches.open(CACHE_NAME)
          .then(cache => cache.match(event.request))
          .then(response => {
            if (response) return response;
            throw error;
          })
      )
    );
    return;
  }

  event.respondWith(
    caches.open(CACHE_NAME)
      .then(cache => cache.match(event.request))
      .then(response => response || fetch(event.request))
  );
});

// Handle push notifications
self.addEventListener('push', event => {
  const options = {
    body: event.data ? event.data.text() : 'Time to set up the Wednesday night poll!',
    icon: '/static/wn.png',
    badge: '/static/wn.png',
    vibrate: [200, 100, 200],
    tag: 'wednesday-reminder',
    requireInteraction: true,
    actions: [
      {
        action: 'open',
        title: 'Open App'
      },
      {
        action: 'close',
        title: 'Dismiss'
      }
    ]
  };

  event.waitUntil(
    self.registration.showNotification('Wednesday Night FC Reminder', options)
  );
});

// Handle notification clicks
self.addEventListener('notificationclick', event => {
  event.notification.close();

  if (event.action === 'open') {
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});
