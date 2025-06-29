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
      <div className="player-controls">
        <div className="control-buttons">
          <button onClick={onPrev}>Prev</button>
          {isPlaying ? (
            <button className="play-pause-btn" onClick={onPause}>
              ||
            </button>
          ) : (
            <button className="play-pause-btn" onClick={onPlay}>
              ▶
            </button>
          )}
          <button onClick={onNext}>Next</button>
        </div>
        <div className="progress-bar">
          <span className="time-current" />
          <input type="range" min="0" max="100" className="progress" onChange={handleSeek} />
          <span className="time-total" />
        </div>
      </div>
      <div className="player-actions">
        <div className="player-volume">
          <input type="range" min="0" max="100" onChange={handleVolume} />
        </div>
      </div>
    </footer>
  )
}
