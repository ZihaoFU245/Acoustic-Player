import React, { useState } from 'react'

export interface TopBarProps {
  onSearch: (q: string) => void
  onAddFolder: () => void
}

export default function TopBar({ onSearch, onAddFolder }: TopBarProps) {
  const [query, setQuery] = useState('')

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    onSearch(query)
  }

  return (
    <div className="flex items-center mb-6">
      <div className="flex-1 flex justify-center">
        <form onSubmit={handleSubmit} className="w-full max-w-80">
          <input
            placeholder="Search for songs, artists...."
            className="w-full h-10 rounded-xl px-4 bg-gray-100 text-gray-900"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </form>
      </div>
      <div className="flex gap-2 ml-4">
        <button onClick={onAddFolder} className="h-10 w-10 flex items-center justify-center rounded-full bg-gray-100 text-gray-900">
          +
        </button>
      </div>
    </div>
  )
}
