import React, { useEffect, useState } from 'react'
import LeftSidebar from './components/new/LeftSidebar'
import TopBar from './components/new/TopBar'
import RightSidebar from './components/new/RightSidebar'
import BottomPlayerBar from './components/BottomPlayerBar'
import MainContent from './components/new/MainContent'
import { connect } from './socket'
import type { Album, Track } from './api/playerApi'
import {
  getAlbums,
  play,
  pause,
  getCurrentTrack,
  searchMusic,
  addFolder
} from './api/playerApi'

function App() {
  const [albums, setAlbums] = useState<Album[]>([])
  const [currentTrack, setCurrentTrack] = useState<Track | null>(null)
  const [isPlaying, setIsPlaying] = useState(false)
  const [page, setPage] = useState('home')

  useEffect(() => {
    loadInitial()
    const sock = connect((st) => {
      setCurrentTrack(st.track)
      setIsPlaying(st.is_playing)
    })
    return () => {
      sock.disconnect()
    }
  }, [])

  async function loadInitial() {
    try {
      const albumData = await getAlbums()
      setAlbums(albumData)
      const status = await getCurrentTrack()
      setCurrentTrack(status.track)
      setIsPlaying(status.is_playing)
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
    <div className="relative flex min-h-screen flex-col bg-white overflow-x-hidden">
      <div className="flex flex-1 h-0 min-h-0 grow">
        <LeftSidebar currentPage={page} onNavigate={setPage} />
        <div className="flex-1 flex flex-col min-h-0 ml-64 mr-80" style={{minWidth:0}}>
          <TopBar onSearch={handleSearch} onAddFolder={handleAddFolder} />
          <MainContent albums={albums} onSelectAlbum={() => {}} />
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
        <RightSidebar currentTrack={currentTrack} />
      </div>
    </div>
  )
}

export default App
