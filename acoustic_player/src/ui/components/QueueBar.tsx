import React from 'react'
import type { Track } from '../api/playerApi'

export interface QueueBarProps {
  queue: Track[]
  currentTrack: Track | null
}

export default function QueueBar({ queue, currentTrack }: QueueBarProps) {
  return (
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
          <div className="queue-list">
            {queue.map((t) => (
              <div key={t.id} className="queue-item">
                <div className="queue-item-art" />
                <div className="queue-item-info">
                  <div className="queue-track-name">{t.title}</div>
                  <div className="queue-track-artist">{t.artist}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </aside>
  )
}
