import { loadConfig, ConfigError } from '../src/config.js';
import { createApp } from '../src/app.js';

// Instance dibuat sekali per container (cold start), dipakai ulang antar request.
let appPromise = null;

function getApp() {
  if (!appPromise) {
    appPromise = Promise.resolve().then(() => {
      const config = loadConfig(process.env);
      return createApp({ config });
    });
  }
  return appPromise;
}

export default async function handler(req, res) {
  let app;
  try {
    app = await getApp();
  } catch (err) {
    // Konfigurasi salah: jangan coba jalankan apa pun.
    appPromise = null;
    res.statusCode = err instanceof ConfigError ? 503 : 500;
    res.setHeader('content-type', 'application/json; charset=utf-8');
    res.setHeader('cache-control', 'no-store');
    res.end(
      JSON.stringify({
        error: 'config_error',
        message: err?.message ?? 'Konfigurasi broker tidak valid',
      }),
    );
    return;
  }
  return app(req, res);
}
