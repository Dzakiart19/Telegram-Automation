# Overview

Ini adalah tool otomasi Telegram (Python + Telethon) yang:
1. Auto-chat ke beberapa bot "cari teman/pasangan" (`@random_pacar_bot`, `@AnonyMeetBot`, `@chatbot`), lalu otomatis kirim pesan promo begitu dapat match.
2. Auto-post pesan promo secara bergilir ke daftar grup Telegram.
3. Auto-balas pesan pribadi yang masuk ke akun (dengan cooldown per pengirim).
4. Dashboard monitoring sederhana lewat Flask (`keep_alive.py`) untuk melihat statistik pengiriman.

# Struktur Project

- `main.py` — entry point, menghubungkan client Telegram, mendaftarkan semua handler dari `lib/`, dan menjalankan loop restart otomatis kalau crash.
- `keep_alive.py` — server Flask untuk dashboard monitoring.
- `stats.py` — penyimpanan statistik di memori.
- `lib/` — semua logic otomasi:
  - `bot_random_pacar.py`, `bot_anony_meet.py`, `bot_chatbot.py` — logic per bot target.
  - `group_sender.py` — daftar & loop pengirim pesan ke grup.
  - `auto_reply.py` — auto-balas pesan pribadi masuk.

# User preferences

- **Wajib buat modul baru di `lib/` untuk setiap penambahan bot, grup pengirim, atau fitur otomasi baru** — jangan menaruh logic baru langsung di `main.py`. `main.py` hanya boleh melakukan import + registrasi (memanggil fungsi `register()`/`run()` dari modul `lib/`), sama seperti pola bot dan group_sender yang sudah ada.
- Setiap grup di `group_sender.py` boleh punya pesan sendiri-sendiri (lihat `GROUPS` sebagai list of tuple `(nama_grup, pesan)`).
