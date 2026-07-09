# Telegram Automation - @random_pacar_bot

Repositori ini telah diperbarui untuk mengotomatisasi pengiriman pesan ke bot anonymous Telegram `@random_pacar_bot`.

## Fitur Baru
- Otomatis mengirim `/search` saat dijalankan.
- Mendeteksi ketika pasangan ditemukan ("Balasan Pasangan telah ditemukan!").
- Otomatis mengirim link `https://vidorey.web.app`.
- Otomatis mengirim `/next` setelah mengirim link untuk mencari pasangan baru secara terus-menerus.

## Cara Penggunaan

1. **Persyaratan**:
   - Python 3.8+
   - `telethon` library (`pip install telethon`)

2. **Konfigurasi**:
   Set variabel lingkungan berikut:
   - `API_ID`: Ambil dari [my.telegram.org](https://my.telegram.org)
   - `API_HASH`: Ambil dari [my.telegram.org](https://my.telegram.org)
   - `PHONE`: Nomor telepon akun Telegram Anda (dengan kode negara, misal: +628123456789)

3. **Menjalankan**:
   ```bash
   python main_v2.py
   ```

4. **Catatan Keamanan**:
   Gunakan dengan bijak. Terlalu sering mengirim pesan atau `/next` dalam waktu singkat dapat menyebabkan akun Anda di-banned oleh Telegram atau diblokir oleh bot target.
