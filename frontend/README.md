# Acoustic Player Frontend

This folder contains the web-based UI for Acoustic Player. The interface uses
[Materialize CSS](https://materializecss.com/) to provide a clean, material design
style and communicates with the Flask backend through the `api.js` module.

## Running

1. Start the backend server:
   ```bash
   cd ../backend
   python main.py
   ```
2. Open `index.html` in a browser or load it inside an Electron renderer process.

The page will request the track list from the backend and display it. Clicking a
track will start playback using the backend player API.

## Files

- `index.html` – basic layout with Material design components
- `style.css` – custom styles
- `main.js` – loads tracks and wires up simple playback actions
