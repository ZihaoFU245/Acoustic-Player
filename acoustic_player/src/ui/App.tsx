import { useEffect, useState } from 'react';
import './App.css';
import type { Track } from './api.ts';
import { getTracks, scanDirectory, playTrack } from './api.ts';

function App() {
  const [tracks, setTracks] = useState<Track[]>([]);
  const [scanPath, setScanPath] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadLibrary();
  }, []);

  async function loadLibrary() {
    try {
      const data = await getTracks();
      setTracks(data);
    } catch (err) {
      console.error('Failed to load tracks', err);
    }
  }

  async function handleScan() {
    if (!scanPath) return;
    setLoading(true);
    try {
      await scanDirectory(scanPath);
      await loadLibrary();
    } catch (err) {
      console.error('Failed to scan folder', err);
    } finally {
      setLoading(false);
    }
  }

  async function handlePlay(path: string) {
    try {
      await playTrack(path);
    } catch (err) {
      console.error('Failed to play track', err);
    }
  }

  return (
    <div className="container" id="content">
      <div className="section" id="library-section">
        <h5>Library</h5>
        <div className="row">
          <div className="input-field col s9">
            <input
              id="scan-path"
              type="text"
              value={scanPath}
              onChange={(e) => setScanPath(e.target.value)}
              placeholder="Path to music folder"
            />
          </div>
          <div className="input-field col s3">
            <button
              id="scan-btn"
              className="btn waves-effect waves-light"
              onClick={handleScan}
              disabled={loading}
            >
              {loading ? 'Scanning...' : 'Scan'}
            </button>
          </div>
        </div>
        <ul id="track-list" className="collection">
          {tracks.map((t) => (
            <li
              key={t.id}
              className="collection-item"
              onClick={() => handlePlay(t.path)}
              style={{ cursor: 'pointer' }}
            >
              {t.artist} - {t.title}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;
