// Minimal API client for the React frontend
export interface Track {
  id: number;
  title: string;
  artist: string;
  path: string;
}

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:5000/api';

export async function getTracks(): Promise<Track[]> {
  const res = await fetch(`${API_BASE_URL}/library/tracks`);
  if (!res.ok) throw new Error('Failed to get library tracks');
  return res.json();
}

export async function scanDirectory(path: string): Promise<void> {
  const res = await fetch(`${API_BASE_URL}/library/scan`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ path })
  });
  if (!res.ok) throw new Error('Failed to scan directory');
}

export async function playTrack(trackPath: string): Promise<void> {
  const res = await fetch(`${API_BASE_URL}/player/play`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ path: trackPath })
  });
  if (!res.ok) throw new Error('Failed to play track');
}
