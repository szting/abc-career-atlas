"""
PWA Injector for Streamlit
Injects PWA scripts and meta tags into Streamlit pages
"""

import streamlit as st
import streamlit.components.v1 as components

def inject_pwa_meta():
    """Inject PWA meta tags and scripts into the Streamlit app"""
    
    # PWA meta tags
    pwa_meta = """
    <meta name="theme-color" content="#1e3a8a">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <meta name="apple-mobile-web-app-title" content="Career Atlas">
    <link rel="apple-touch-icon" href="/static/icon-192.png">
    <link rel="manifest" href="/static/manifest.json">
    
    <!-- PWA Scripts -->
    <script src="/static/pwa-register.js" defer></script>
    
    <!-- Install button (hidden by default) -->
    <style>
        #install-button {
            display: none;
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: #3b82f6;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            z-index: 1000;
        }
        
        #install-button:hover {
            background-color: #2563eb;
        }
        
        #connection-status {
            position: fixed;
            top: 10px;
            right: 10px;
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 12px;
            z-index: 1000;
        }
        
        .status-online {
            background-color: #10b981;
            color: white;
        }
        
        .status-offline {
            background-color: #ef4444;
            color: white;
        }
    </style>
    
    <button id="install-button">Install Career Atlas</button>
    <div id="connection-status"></div>
    """
    
    # Inject the meta tags and scripts
    st.markdown(pwa_meta, unsafe_allow_html=True)
    
    # Also inject using components for better compatibility
    components.html("""
    <script>
        // Additional PWA initialization
        if ('serviceWorker' in navigator && 'SyncManager' in window) {
            navigator.serviceWorker.ready.then(registration => {
                console.log('Service Worker ready for background sync');
            });
        }
        
        // Handle standalone mode
        if (window.matchMedia('(display-mode: standalone)').matches) {
            console.log('Running in standalone mode');
        }
    </script>
    """, height=0)

def check_pwa_support():
    """Check if the browser supports PWA features"""
    components.html("""
    <script>
        const pwaSupport = {
            serviceWorker: 'serviceWorker' in navigator,
            cache: 'caches' in window,
            backgroundSync: 'SyncManager' in window,
            notifications: 'Notification' in window,
            install: 'BeforeInstallPromptEvent' in window
        };
        
        console.log('PWA Support:', pwaSupport);
        
        // Store in session storage for Python access
        sessionStorage.setItem('pwaSupport', JSON.stringify(pwaSupport));
    </script>
    """, height=0)
