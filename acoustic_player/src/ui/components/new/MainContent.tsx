import React from 'react'
import type { Album } from '../../api/playerApi'

export interface MainContentProps {
  albums: Album[]
  onSelectAlbum: (a: Album) => void
}

export default function MainContent({ albums, onSelectAlbum }: MainContentProps) {
  return (
    <main className="flex-1 p-6 overflow-y-auto" style={{height:'calc(100vh - 88px)'}}>
      <h2 className="text-2xl font-bold pb-3">Good evening</h2>
      <div className="flex overflow-x-auto gap-3 mb-8">
        {albums.map((a) => (
          <div key={a.id} className="min-w-40 flex flex-col gap-2" onClick={() => onSelectAlbum(a)}>
            <div className="w-full aspect-square rounded-xl bg-cover" style={{backgroundImage:'linear-gradient(to bottom right,#fbc2eb,#a6c1ee)'}}></div>
            <p className="text-gray-900 text-base font-medium">{a.title}</p>
          </div>
        ))}
      </div>
    </main>
  )
}
