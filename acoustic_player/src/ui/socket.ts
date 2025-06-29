import { io, Socket } from 'socket.io-client'
import type { PlayerStatus } from './api/playerApi'

let socket: Socket | null = null

export function connect(onStatus: (st: PlayerStatus) => void) {
  if (!socket) {
    const base = (import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:5000/api').replace(/\/api$/, '')
    socket = io(base)
    socket.on('player_status_update', onStatus)
  }
  return socket!
}
