import io
import wave
import numpy as np
import matplotlib.pyplot as plt

class AudioVisualizer:
    """Utility class to generate basic audio visualizations."""

    def _read_wav(self, file_path):
        """Read PCM data from a WAV file."""
        with wave.open(file_path, 'rb') as wf:
            sample_rate = wf.getframerate()
            frames = wf.readframes(wf.getnframes())
            channels = wf.getnchannels()
            sample_width = wf.getsampwidth()

        dtype = np.int16 if sample_width == 2 else np.uint8
        data = np.frombuffer(frames, dtype=dtype)
        if channels > 1:
            data = data[::channels]
        return sample_rate, data

    def waveform_bytes(self, file_path):
        """Return waveform image bytes (PNG). Only supports WAV files."""
        sr, data = self._read_wav(file_path)
        fig, ax = plt.subplots(figsize=(8, 2))
        ax.plot(np.linspace(0, len(data)/sr, num=len(data)), data, linewidth=0.5)
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Amplitude')
        ax.set_title('Waveform')
        fig.tight_layout()
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        plt.close(fig)
        buffer.seek(0)
        return buffer.getvalue()

    def spectrogram_bytes(self, file_path):
        """Return spectrogram image bytes (PNG). Only supports WAV files."""
        sr, data = self._read_wav(file_path)
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.specgram(data, Fs=sr, NFFT=1024, noverlap=512)
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Frequency (Hz)')
        ax.set_title('Spectrogram')
        fig.tight_layout()
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        plt.close(fig)
        buffer.seek(0)
        return buffer.getvalue()
