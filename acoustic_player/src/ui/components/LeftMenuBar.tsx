import React from 'react'

export interface LeftMenuBarProps {
  currentPage: string
  onNavigate: (page: string) => void
}

const pages = [
  { key: 'home', label: 'Home' },
  { key: 'new', label: 'New' },
  { key: 'recent', label: 'Recently Played' }
]

export default function LeftMenuBar({ currentPage, onNavigate }: LeftMenuBarProps) {
  return (
    <nav className="sidebar left">
      <div className="logo">
        <span>Acoustic Player</span>
      </div>
      <ul>
        {pages.map((p) => (
          <li
            key={p.key}
            className={currentPage === p.key ? 'active' : ''}
            onClick={() => onNavigate(p.key)}
          >
            {p.label}
          </li>
        ))}
      </ul>
    </nav>
  )
}
