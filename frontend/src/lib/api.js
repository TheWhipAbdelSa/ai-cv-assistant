export const apiBase = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/$/, '');

export async function api(path, options = {}) {
  const response = await fetch(`${apiBase}${path}`, { ...options, cache: 'no-store' });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(typeof data.detail === 'string' ? data.detail : 'Kontroller feltene og prøv igjen.');
  }
  return data;
}
