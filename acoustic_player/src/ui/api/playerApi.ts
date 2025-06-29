export interface Track {
  id: number
  title: string
  artist: string
  album?: string
  path: string
}

export interface PlayerStatus {
  track: Track | null
  is_playing: boolean
}

export interface Album {
  id: number
  title: string
  artist: string
  art?: string
}

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:5000/api'

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(url, options)
  if (!res.ok) throw new Error('Request failed')
  return res.json() as Promise<T>
}

export async function play(path: string) {
  return request<PlayerStatus>(`${API_BASE_URL}/player/play`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ path })
  })
}

export async function pause() {
  return request<PlayerStatus>(`${API_BASE_URL}/player/pause`, { method: 'POST' })
}

export async function next() {
  return request<PlayerStatus>(`${API_BASE_URL}/player/next`, { method: 'POST' })
}

export async function prev() {
  return request<PlayerStatus>(`${API_BASE_URL}/player/previous`, { method: 'POST' })
}

export async function seek(position: number) {
  return request<PlayerStatus>(`${API_BASE_URL}/player/seek`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ position })
  })
}

export async function setVolume(level: number) {
  return request<PlayerStatus>(`${API_BASE_URL}/player/volume`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ level })
  })
}

export async function getCurrentTrack() {
  return request<PlayerStatus>(`${API_BASE_URL}/player/status`)
}

export async function getQueue() {
  return request<Track[]>(`${API_BASE_URL}/player/queue`)
}

export async function searchMusic(query: string) {
  return request<Track[]>(`${API_BASE_URL}/library/search?query=${encodeURIComponent(query)}`)
}

export async function addFolder(path: string) {
  return request(`${API_BASE_URL}/library/scan`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ path })
  })
}

export async function getAlbums() {
  return request<Album[]>(`${API_BASE_URL}/library/albums`)
}
