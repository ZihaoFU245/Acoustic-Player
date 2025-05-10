# Album Art Storage Strategy

## Overview

The Acoustic Player implements a hybrid approach for album art storage, balancing performance and user experience:
1. Full-size album art is stored on the filesystem
2. Thumbnail versions are stored directly in the database

## Implementation Details

### Database Structure

The `Track` model in `database.py` contains two fields for album art:

```python
album_art_path = Column(String(255), nullable=True)  # Path to full-size album art file
album_art_thumbnail = Column(LargeBinary, nullable=True)  # Small thumbnail stored directly in DB
```

### Metadata Extraction

When scanning the music library, we:
1. Extract embedded album art from audio files
2. Save full-size images to the filesystem (in `~/.acoustic_player/album_art` by default)
3. Generate small thumbnails (max 150px) and store them directly in the database
4. Associate both with the track record

### API Access

The backend provides multiple ways to access album art:

1. **Track data includes thumbnail info**: Each track record indicates whether a thumbnail is available
   ```json
   {
     "id": 1,
     "title": "Song Title",
     "has_thumbnail": true,
     "album_art_path": "/path/to/full/album_art.jpg"
   }
   ```

2. **Dedicated thumbnail endpoint**: Frontend can fetch thumbnails on-demand
   ```
   GET /api/library/tracks/{track_id}/thumbnail
   ```
   Returns thumbnail data as a base64-encoded data URL ready to use in HTML/CSS

3. **Full-size access**: Frontend can access full-size images using the path

## Benefits of This Approach

1. **Performance optimization**:
   - Small thumbnails (~5-20KB) in the database enable fast loading of album art in track lists
   - Thumbnails are directly usable without additional disk I/O
   - Base64-encoding eliminates the need for separate HTTP requests for images

2. **Full-size access**:
   - Full-size album art remains on the filesystem where it's more efficiently served
   - Reduces database bloat from storing large files
   - Easier to manage (backup, cache, serve) through traditional file operations

3. **User experience**:
   - Fast loading of track lists with thumbnails for responsive UI
   - High-quality full-size images available for currently playing track or album view

## Usage in Frontend

```javascript
// Example: Get and display a track thumbnail
const thumbnail = await libraryApi.getThumbnail(track.id);
if (thumbnail) {
  // thumbnail is a data URL, can be used directly in img src
  trackElement.style.backgroundImage = `url(${thumbnail})`;
}
```

## Technical Considerations

- Thumbnails are limited to 150px in the largest dimension
- JPEG format is used for thumbnails to minimize size
- The database stores the raw binary data, which is converted to base64 only when sent to the frontend
- If no embedded album art is found, both fields will be NULL
