import React from 'react'

export interface LeftSidebarProps {
  currentPage: string
  onNavigate: (p: string) => void
}

const items = [
  { key: 'home', label: 'Home' },
  { key: 'search', label: 'Search' },
  { key: 'library', label: 'Your Library' },
  { key: 'create', label: 'Create Playlist' },
  { key: 'liked', label: 'Liked Songs' },
]

export default function LeftSidebar({ currentPage, onNavigate }: LeftSidebarProps) {
  return (
    <aside className="w-64 bg-gray-100 p-6 flex flex-col gap-4 fixed left-0 top-0 bottom-0" style={{height:'calc(100vh - 88px)'}}>
      <div className="flex items-center gap-3 mb-8 text-gray-900">
        <svg viewBox="0 0 48 48" fill="currentColor" className="w-6 h-6"><path d="M4 42.4379C4 42.4379 14.0962 36.0744 24 41.1692C35.0664 46.8624 44 42.2078 44 42.2078L44 7.01134C44 7.01134 35.068 11.6577 24.0031 5.96913C14.0971 0.876274 4 7.27094 4 7.27094L4 42.4379Z"/></svg>
        <h1 className="font-bold text-xl">Acoustic Player</h1>
      </div>
      <nav className="space-y-2">
        {items.map(i => (
          <button key={i.key} onClick={() => onNavigate(i.key)} className={`flex items-center gap-3 px-3 py-2 rounded-full ${currentPage===i.key?'bg-orange-100 text-orange-500':'text-gray-900 hover:text-orange-500'}`}>{i.label}</button>
        ))}
      </nav>
    </aside>
  )
}
