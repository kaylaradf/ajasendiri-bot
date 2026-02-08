# Ajasendiri Bot

Bot Discord yang mendeteksi berbagai wordlist dan merespons dengan gambar, plus fitur voice channel dengan audio looping.

## Fitur

### 1. Wordlist Detection
Bot mendeteksi kata-kata tertentu dalam pesan dan merespons dengan gambar.

### 2. Voice Channel Audio Loop
Bot bisa join voice channel dan play audio secara loop dengan kualitas tinggi.

**Slash Commands:**
- `/join` - Join voice channel dan mulai play audio loop
- `/stop` - Stop audio tapi tetap di channel (nunggu)
- `/play` - Resume audio loop
- `/volume <level>` - Set volume (0.0 - 1.0, contoh: 0.15 untuk background)
- `/leave` - Keluar dari voice channel

## Cara Menambah Wordlist Baru

1. Tambahkan gambar ke folder `assets/`
2. Edit `config.py` dan tambahkan entry baru di `WORDLIST_CONFIG`:

```python
"nama_wordlist": {
    "keywords": ["kata1", "kata2"],  # Kata kunci yang harus ada
    "image": "assets/nama-gambar.jpg",  # Path ke gambar
    "pattern": r'.*k.*a.*t.*a.*1.*k.*a.*t.*a.*2.*',  # Pattern regex
    "fuzzy_words": {
        "kata1": ["kata1", "kt1", "kata", "kat1"],  # Variasi kata1
        "kata2": ["kata2", "kt2", "kata", "kat2"]   # Variasi kata2
    }
}
```

## Setup Voice Feature

1. Tambahkan audio file ke `assets/loop-audio.mp3`
2. Edit `config.py` di bagian `VOICE_CONFIG` untuk mengatur:
   - `audio_file`: Path ke audio file
   - `bitrate`: Kualitas audio (64-320 kbps, default 128)
   - `volume`: Volume level (0.0 - 1.0, default 0.15 untuk background opacity)

## Dependencies

Install dengan: `pip install -r requirements.txt`

**Catatan:** Untuk voice feature, kamu perlu install FFmpeg:
- Windows: Download dari https://ffmpeg.org/download.html dan tambahkan ke PATH
- Linux: `sudo apt install ffmpeg`
- macOS: `brew install ffmpeg`

## Setup

1. Buat file `.env` dengan `DISCORD_TOKEN=your_token_here`
2. Jalankan dengan `python bot.py`