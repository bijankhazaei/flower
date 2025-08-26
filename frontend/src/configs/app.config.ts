export const AppConfig = {
  app: {
    name: 'Flower',
    version: '1.0.0',
    description: 'Visual Flow Builder'
  },
  api: {
    baseUrl: import.meta.env.VITE_API_URL || 'http://localhost:8022/api',
    timeout: parseInt(import.meta.env.VITE_API_TIMEOUT || '10000'),
    retryAttempts: 3
  },
  auth: {
    tokenKey: 'flower_auth_token',
    refreshTokenKey: 'flower_refresh_token',
    tokenExpiry: 24 * 60 * 60 * 1000 // 24 hours
  },
  canvas: {
    defaultZoom: 1,
    minZoom: 0.1,
    maxZoom: 3,
    gridSize: 20,
    nodeSnapThreshold: 10
  },
  ui: {
    sidebarWidth: 280,
    toolbarHeight: 60,
    animationDuration: 200
  },
  features: {
    realTimeCollaboration: import.meta.env.VITE_ENABLE_COLLABORATION === 'true',
    analytics: import.meta.env.VITE_ENABLE_ANALYTICS === 'true',
    debugMode: import.meta.env.DEV
  }
} as const;