import React from 'react'

export interface Album {
  id: number
  title: string
  artist: string
  art?: string
}

export interface AlbumWidgetProps {
  album: Album
  onClick: (album: Album) => void
}

export default function AlbumWidget({ album, onClick }: AlbumWidgetProps) {
  return (
    <div className="album-widget" onClick={() => onClick(album)}>
      <div className="album-art small" />
      <div className="album-info">
        <div className="album-title">{album.title}</div>
        <div className="album-artist">{album.artist}</div>
      </div>
    </div>
  )
}
