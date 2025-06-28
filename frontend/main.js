import { initApi } from './js/api.js';

const { libraryApi, playerApi } = initApi();

document.addEventListener('DOMContentLoaded', () => {
    loadLibrary();
});

async function loadLibrary() {
    try {
        const tracks = await libraryApi.getTracks();
        const list = document.getElementById('track-list');
        list.innerHTML = '';
        tracks.forEach(track => {
            const li = document.createElement('li');
            li.className = 'collection-item';
            li.textContent = `${track.artist} - ${track.title}`;
            li.addEventListener('click', () => playerApi.play(track.path));
            list.appendChild(li);
        });
    } catch (err) {
        console.error('Failed to load tracks', err);
    }
}
