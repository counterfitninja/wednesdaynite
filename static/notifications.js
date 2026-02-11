// PWA and Notification Manager
class WNFCNotificationManager {
  constructor() {
    this.checkNotificationSettings();
  }

  async checkNotificationSettings() {
    // Check if notifications are enabled in admin settings
    try {
      const response = await fetch('/api/settings/notifications');
      const data = await response.json();
      
      if (data.enabled) {
        this.checkWednesdayReminder();
      } else {
        console.log('Notifications disabled in admin settings');
      }
    } catch (error) {
      console.error('Failed to check notification settings:', error);
    }
  }

  async requestNotificationPermission() {
    if (!('Notification' in window)) {
      console.log('This browser does not support notifications');
      return false;
    }

    if (Notification.permission === 'granted') {
      return true;
    }

    if (Notification.permission !== 'denied') {
      const permission = await Notification.requestPermission();
      return permission === 'granted';
    }

    return false;
  }

  async registerServiceWorker() {
    if ('serviceWorker' in navigator) {
      try {
        const registration = await navigator.serviceWorker.register('/static/service-worker.js');
        console.log('Service Worker registered:', registration);
        return registration;
      } catch (error) {
        console.error('Service Worker registration failed:', error);
      }
    }
  }

  checkWednesdayReminder() {
    // Check every hour if we should show the Wednesday reminder
    this.scheduleNextCheck();
  }

  scheduleNextCheck() {
    const now = new Date();
    const nextCheck = new Date(now);
    
    // Check at the next hour
    nextCheck.setHours(now.getHours() + 1, 0, 0, 0);
    
    const timeUntilCheck = nextCheck - now;
    
    setTimeout(() => {
      this.checkAndNotify();
      this.scheduleNextCheck();
    }, timeUntilCheck);
  }

  async checkAndNotify() {
    // First check if notifications are enabled in settings
    try {
      const response = await fetch('/api/settings/notifications');
      const data = await response.json();
      
      if (!data.enabled) {
        console.log('Notifications disabled by admin - skipping reminder');
        return;
      }
    } catch (error) {
      console.error('Failed to check notification settings:', error);
      return;
    }

    const now = new Date();
    const day = now.getDay(); // 0 = Sunday, 3 = Wednesday
    const hour = now.getHours();

    // Wednesday between 12:00 and 13:00
    if (day === 3 && hour === 12) {
      await this.showWednesdayReminder();
    }
  }

  async showWednesdayReminder() {
    const hasPermission = await this.requestNotificationPermission();
    
    if (!hasPermission) {
      console.log('Notification permission not granted');
      return;
    }

    // Check if we already notified today
    const lastNotification = localStorage.getItem('lastWednesdayNotification');
    const today = new Date().toDateString();
    
    if (lastNotification === today) {
      console.log('Already notified today');
      return;
    }

    // Show notification
    if ('serviceWorker' in navigator && navigator.serviceWorker.controller) {
      // Use service worker notification (works in background)
      const registration = await navigator.serviceWorker.ready;
      await registration.showNotification('Wednesday Night FC Reminder', {
        body: '⚽ Time to set up the Wednesday night poll!',
        icon: '/static/wn.png',
        badge: '/static/wn.png',
        vibrate: [200, 100, 200],
        tag: 'wednesday-reminder',
        requireInteraction: true,
        actions: [
          {
            action: 'open',
            title: 'Open App'
          }
        ]
      });
    } else {
      // Fallback to regular notification
      new Notification('Wednesday Night FC Reminder', {
        body: '⚽ Time to set up the Wednesday night poll!',
        icon: '/static/wn.png',
        vibrate: [200, 100, 200]
      });
    }

    // Mark as notified
    localStorage.setItem('lastWednesdayNotification', today);
  }

  // Manual trigger for testing
  async testNotification() {
    const hasPermission = await this.requestNotificationPermission();
    if (hasPermission) {
      new Notification('Test Notification', {
        body: 'This is a test notification from Wednesday Night FC',
        icon: '/static/wn.png'
      });
    }
  }
}

// Initialize notification manager
let notificationManager;

document.addEventListener('DOMContentLoaded', () => {
  notificationManager = new WNFCNotificationManager();
  notificationManager.registerServiceWorker();
});

// Add install prompt
let deferredPrompt;

window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredPrompt = e;
  
  // Show install button if not already installed
  const installBtn = document.getElementById('install-btn');
  if (installBtn) {
    installBtn.style.display = 'block';
    installBtn.addEventListener('click', async () => {
      if (deferredPrompt) {
        deferredPrompt.prompt();
        const { outcome } = await deferredPrompt.userChoice;
        console.log(`User response: ${outcome}`);
        deferredPrompt = null;
        installBtn.style.display = 'none';
      }
    });
  }
});
