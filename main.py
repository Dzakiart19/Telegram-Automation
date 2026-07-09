import os
import asyncio
import logging
from telethon import TelegramClient, events
from keep_alive import keep_alive

# Konfigurasi Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Konfigurasi API (Pastikan ENV ini diset)
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE = os.getenv('PHONE')

# Target Bot
TARGET_BOT = 'random_pacar_bot'
LINK_PESAN = 'https://vidorey.web.app update setiap hari 👀'

# Kata kunci balasan bot
MATCH_FOUND_TEXT = "Balasan Pasangan telah ditemukan!"
GREETING_TEXT = "Katakan, Hai untuk membalas pasangan anda 😊"

client = TelegramClient('tele', API_ID, API_HASH)

async def start_searching():
    """Mengirim perintah /search ke bot target"""
    logger.info(f"Mengirim /search ke @{TARGET_BOT}")
    await client.send_message(TARGET_BOT, '/search')

@client.on(events.NewMessage(from_users=TARGET_BOT, incoming=True))
async def handle_bot_messages(event):
    message_text = event.message.message
    
    # Cek jika pasangan ditemukan
    if MATCH_FOUND_TEXT in message_text or GREETING_TEXT in message_text:
        logger.info("Pasangan ditemukan! Mengirim link...")
        # Tunggu sebentar agar terlihat natural
        await asyncio.sleep(2)
        await client.send_message(TARGET_BOT, LINK_PESAN)
        
        # Setelah kirim pesan, tunggu sebentar lalu /next untuk cari baru
        await asyncio.sleep(5)
        logger.info("Mencari pasangan baru...")
        await client.send_message(TARGET_BOT, '/next')

    # Cek jika tidak ada orang online atau bot berhenti
    elif "mencari pasangan" in message_text.lower():
        logger.info("Sedang mencari...")
    
    elif "berhenti" in message_text.lower():
        logger.info("Obrolan berhenti, mencoba mencari lagi...")
        await asyncio.sleep(3)
        await start_searching()

async def main():
    await client.connect()
    
    if not await client.is_user_authorized():
        logger.error("Sesi tidak valid! Harap login ulang.")
        return
    
    logger.info("Bot User Automation Aktif!")
    
    # Memulai pencarian pertama kali
    await start_searching()
    
    # Tetap berjalan
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        keep_alive()
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot dihentikan.")
