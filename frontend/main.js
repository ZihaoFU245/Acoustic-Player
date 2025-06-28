import { initApi } from './js/api.js';

const { libraryApi, playerApi } = initApi();

document.addEventListener('DOMContentLoaded', () => {
    loadLibrary();
    const scanBtn = document.getElementById('scan-btn');
    if (scanBtn) {
        scanBtn.addEventListener('click', scanLibrary);
    }
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

async function scanLibrary() {
    const input = document.getElementById('scan-path');
    const path = input.value.trim();
    if (!path) return;

    try {
        await libraryApi.scanDirectory(path);
        if (window.M && M.toast) {
            M.toast({ html: 'Scan completed' });
        }
        loadLibrary();
    } catch (err) {
        console.error('Failed to scan folder', err);
        if (window.M && M.toast) {
            M.toast({ html: 'Scan failed' });
        }
    }
}
