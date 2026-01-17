# Ajasendiri Bot

Bot Discord yang mendeteksi berbagai wordlist dan merespons dengan gambar.

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

## Contoh Konfigurasi

Bot akan mendeteksi pesan yang mengandung semua keyword dalam wordlist, baik melalui pattern matching maupun fuzzy matching.

## Dependencies

Install dengan: `pip install -r requirements.txt`

## Setup

1. Buat file `.env` dengan `DISCORD_TOKEN=your_token_here`
2. Jalankan dengan `python bot.py`