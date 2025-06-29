import React, { useEffect, useState } from 'react'
import './demo-style.css'
import LeftMenuBar from './components/LeftMenuBar'
import TopBar from './components/TopBar'
import QueueBar from './components/QueueBar'
import BottomPlayerBar from './components/BottomPlayerBar'
import MainArea from './components/MainArea'
import type { Album, Track } from './api/playerApi'
import {
  getAlbums,
  play,
  pause,
  getCurrentTrack,
  getQueue,
  searchMusic,
  addFolder
} from './api/playerApi'

function App() {
  const [albums, setAlbums] = useState<Album[]>([])
  const [queue, setQueue] = useState<Track[]>([])
  const [currentTrack, setCurrentTrack] = useState<Track | null>(null)
  const [isPlaying, setIsPlaying] = useState(false)
  const [page, setPage] = useState('home')

  useEffect(() => {
    loadInitial()
  }, [])

  async function loadInitial() {
    try {
      const albumData = await getAlbums()
      setAlbums(albumData)
      const status = await getCurrentTrack()
      setCurrentTrack(status.track)
      setIsPlaying(status.is_playing)
      const q = await getQueue()
      setQueue(q)
    } catch (err) {
      console.error('Failed to load data', err)
    }
  }

  async function handlePlay(path: string) {
    const status = await play(path)
    setCurrentTrack(status.track)
    setIsPlaying(status.is_playing)
  }

  async function handlePause() {
    const status = await pause()
    setCurrentTrack(status.track)
    setIsPlaying(status.is_playing)
  }

  async function handleSearch(q: string) {
    try {
      const results = await searchMusic(q)
      setAlbums(results.map((t, idx) => ({ id: idx, title: t.title, artist: t.artist })))
    } catch (err) {
      console.error(err)
    }
  }

  async function handleAddFolder() {
    const path = prompt('Folder path to scan:')
    if (!path) return
    try {
      await addFolder(path)
      const albumData = await getAlbums()
      setAlbums(albumData)
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <div className="app-container">
      <LeftMenuBar currentPage={page} onNavigate={setPage} />
      <div className="content-area">
        <TopBar onSearch={handleSearch} onAddFolder={handleAddFolder} />
        <MainArea albums={albums} onSelectAlbum={() => {}} />
      </div>
      <QueueBar queue={queue} currentTrack={currentTrack} />
      <BottomPlayerBar
        currentTrack={currentTrack}
        isPlaying={isPlaying}
        onPlay={() => currentTrack && handlePlay(currentTrack.path)}
        onPause={handlePause}
        onNext={() => {}}
        onPrev={() => {}}
        onSeek={() => {}}
        onVolumeChange={() => {}}
      />
    </div>
  )
}

export default App
