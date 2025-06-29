import React from 'react'
import type { Track } from '../api/playerApi'

export interface BottomPlayerBarProps {
  currentTrack: Track | null
  isPlaying: boolean
  onPlay: () => void
  onPause: () => void
  onNext: () => void
  onPrev: () => void
  onSeek: (pos: number) => void
  onVolumeChange: (vol: number) => void
}

export default function BottomPlayerBar({
  currentTrack,
  isPlaying,
  onPlay,
  onPause,
  onNext,
  onPrev,
  onSeek,
  onVolumeChange
}: BottomPlayerBarProps) {
  function handleSeek(e: React.ChangeEvent<HTMLInputElement>) {
    onSeek(Number(e.target.value))
  }
  function handleVolume(e: React.ChangeEvent<HTMLInputElement>) {
    onVolumeChange(Number(e.target.value))
  }
  return (
    <footer className="bg-white border-t border-gray-200 px-6 py-4 flex items-center justify-between fixed left-0 right-0 bottom-0 z-50" style={{minHeight:'88px'}}>
      <div className="flex items-center">
        {currentTrack && (
          <>
            <div className="w-12 h-12 bg-gray-300 rounded-lg mr-4" />
            <div>
              <p className="font-medium text-gray-900">{currentTrack.title}</p>
              <p className="text-sm text-gray-500">{currentTrack.artist}</p>
            </div>
          </>
        )}
      </div>
      <div className="flex flex-col items-center flex-1 max-w-md">
        <div className="flex items-center space-x-6 mb-2">
          <button onClick={onPrev} className="text-gray-500 hover:text-black">&#9664;&#9664;</button>
          {isPlaying ? (
            <button onClick={onPause} className="bg-white text-black p-3 rounded-full shadow-md border border-gray-300 hover:bg-gray-100">||</button>
          ) : (
            <button onClick={onPlay} className="bg-white text-black p-3 rounded-full shadow-md border border-gray-300 hover:bg-gray-100">&#9654;</button>
          )}
          <button onClick={onNext} className="text-gray-500 hover:text-black">&#9654;&#9654;</button>
        </div>
        <div className="flex items-center w-full">
          <span className="text-xs text-gray-500 mr-2">0:00</span>
          <input type="range" min="0" max="100" className="w-full" onChange={handleSeek} />
          <span className="text-xs text-gray-500 ml-2">3:00</span>
        </div>
      </div>
      <div className="flex items-center space-x-4">
        <input type="range" min="0" max="100" onChange={handleVolume} />
      </div>
    </footer>
  )
}
