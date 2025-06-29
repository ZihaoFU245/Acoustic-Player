import React from 'react'
import AlbumWidget from './AlbumWidget'
import type { Album } from './AlbumWidget'

export interface MainAreaProps {
  albums: Album[]
  onSelectAlbum: (album: Album) => void
}

export default function MainArea({ albums, onSelectAlbum }: MainAreaProps) {
  return (
    <main className="main-content color-bg">
      <div className="music-library-section">
        <div className="section-header">
          <h3>Library</h3>
        </div>
        <div className="track-list">
          {albums.map((a) => (
            <AlbumWidget key={a.id} album={a} onClick={onSelectAlbum} />
          ))}
        </div>
      </div>
    </main>
  )
}
