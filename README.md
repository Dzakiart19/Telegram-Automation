# Telegram Automation - @random_pacar_bot

Otomatisasi interaksi dengan bot anonymous Telegram `@random_pacar_bot`.

## Fitur
- Otomatis mengirim perintah `/search` saat dijalankan.
- Mendeteksi pasangan baru ("Balasan Pasangan telah ditemukan!").
- Mengirim pesan promosi link secara otomatis.
- Otomatis mencari pasangan baru dengan perintah `/next`.

## Persyaratan
- Python 3.8+
- Library Telethon (`pip install telethon`)

## Konfigurasi
Atur variabel lingkungan (Environment Variables) berikut:
- `API_ID`: Ambil dari [my.telegram.org](https://my.telegram.org)
- `API_HASH`: Ambil dari [my.telegram.org](https://my.telegram.org)
- `PHONE`: Nomor telepon akun Telegram Anda (contoh: +628123456789)

## Cara Menjalankan
```bash
python main.py
```

## Disclaimer
Gunakan dengan bijak. Risiko akun terkena limit atau ban dari Telegram adalah tanggung jawab pengguna.
