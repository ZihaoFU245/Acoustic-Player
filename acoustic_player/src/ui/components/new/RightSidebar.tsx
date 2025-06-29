import React from 'react'
import type { Track } from '../../api/playerApi'

export interface RightSidebarProps {
  currentTrack: Track | null
}

export default function RightSidebar({ currentTrack }: RightSidebarProps) {
  return (
    <aside className="w-80 bg-gray-100 p-6 flex flex-col gap-6 fixed right-0 top-0 bottom-0" style={{height:'calc(100vh - 88px)'}}>
      {currentTrack && (
        <div className="bg-gradient-to-br from-orange-300 via-pink-300 to-purple-300 p-6 rounded-xl text-center">
          <div className="w-48 h-48 bg-white rounded-lg mx-auto mb-6" />
          <h3 className="text-2xl font-semibold text-white">{currentTrack.title}</h3>
          <p className="text-gray-100 mb-1">{currentTrack.artist}</p>
        </div>
      )}
    </aside>
  )
}
