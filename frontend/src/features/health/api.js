// Use relative paths by default so Vite dev proxy can forward to the backend without CORS.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

export async function healthCheck() {
  const res = await fetch(`${API_BASE_URL}/api/health`);
  return res.json();
}
