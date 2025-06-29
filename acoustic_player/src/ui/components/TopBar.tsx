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
    <header className="topbar">
      <form className="search-wrap" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Search"
          className="search-input"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
      </form>
      <div className="topbar-actions">
        <button className="notif-btn" title="Add" onClick={onAddFolder}>
          Add
        </button>
      </div>
    </header>
  )
}
