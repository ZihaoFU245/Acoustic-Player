import { useEffect, useState } from 'react'
import type { Track } from '../api'
import { getTracks, scanDirectory, playTrack } from '../api'
import '../demo-style.css'

function MainUI() {
  const [tracks, setTracks] = useState<Track[]>([])
  const [scanPath, setScanPath] = useState('')
  const [loading, setLoading] = useState(false)
  const [currentTrack, setCurrentTrack] = useState<Track | null>(null)

  useEffect(() => {
    loadLibrary()
  }, [])

  async function loadLibrary() {
    try {
      const data = await getTracks()
      setTracks(data)
    } catch (err) {
      console.error('Failed to load tracks', err)
    }
  }

  async function handleScan() {
    if (!scanPath) return
    setLoading(true)
    try {
      await scanDirectory(scanPath)
      await loadLibrary()
    } catch (err) {
      console.error('Failed to scan folder', err)
    } finally {
      setLoading(false)
    }
  }

  async function handlePlay(t: Track) {
    try {
      await playTrack(t.path)
      setCurrentTrack(t)
    } catch (err) {
      console.error('Failed to play track', err)
    }
  }

  return (
    <div className="app-container main-layout">
      <nav className="sidebar left">
        <div className="logo">
          <span>Acoustic Player</span>
        </div>
        <ul>
          <li className="active">Home</li>
          <li>New</li>
          <li>Recently Played</li>
        </ul>
      </nav>

      <div className="content-area">
        <header className="topbar">
          <div className="search-wrap">
            <input
              type="text"
              placeholder="Path to music folder"
              className="search-input"
              value={scanPath}
              onChange={(e) => setScanPath(e.target.value)}
            />
          </div>
          <div className="topbar-actions">
            <button className="notif-btn" title="Scan" onClick={handleScan}>
              {loading ? 'Scanning...' : 'Scan'}
            </button>
          </div>
        </header>

        <main className="main-content color-bg" style={{ paddingBottom: '64px' }}>
          <div className="content-grid">
            <div className="now-playing-section section">
              <div className="now-playing-card">
                <div className="album-art large" />
                <div className="track-info">
                  <h2 className="track-title">
                    {currentTrack ? currentTrack.title : 'Nothing Playing'}
                  </h2>
                  <div className="artist-name">
                    {currentTrack?.artist ?? ''}
                  </div>
                </div>
              </div>
            </div>

            <div className="lyrics-section section">
              <div className="lyrics-header">
                <h3 className="section-title">Lyrics</h3>
              </div>
              <div className="lyrics-content">
                <div className="lyrics-scroll">
                  <p>Select a track to play</p>
                </div>
              </div>
            </div>

            <div className="music-library-section section">
              <div className="section-header">
                <h3 className="section-title">Library</h3>
              </div>
              <div className="track-list">
                {tracks.map((t) => (
                  <div
                    key={t.id}
                    className="track-item"
                    onClick={() => handlePlay(t)}
                  >
                    <div className="track-item-art" />
                    <div className="track-item-info">
                      <span className="track-name">{t.title}</span>
                      <span className="track-artist">{t.artist}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </main>
      </div>

      <aside className="sidebar right">
        <div className="tab-switch">
          <button className="active">Queue</button>
        </div>
        <div className="tab-content">
          <div className="queue-view">
            {currentTrack && (
              <div className="current-playing">
                <div className="album-art small" />
                <div className="current-track-info">
                  <h4>{currentTrack.title}</h4>
                  <div className="artist">{currentTrack.artist}</div>
                </div>
              </div>
            )}
          </div>
        </div>
      </aside>

      <footer className="player-bar">
        {currentTrack && (
          <div className="player-info">
            <div className="album-art tiny" />
            <div className="player-track-info">
              <div className="track-title">{currentTrack.title}</div>
              <div className="track-artist">{currentTrack.artist}</div>
            </div>
          </div>
        )}
      </footer>
    </div>
  )
}

export default MainUI
