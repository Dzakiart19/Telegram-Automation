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
MATCH_FOUND_TEXT = "Pasangan telah ditemukan!"
GREETING_TEXT = "Katakan, Hai untuk membalas pasangan anda 😊"
PARTNER_LEFT_TEXT = "Lawan bicara telah meninggalkan percakapan"
SEARCH_AGAIN_TEXT = "Ketik /search untuk mencari obrolan baru"

client = TelegramClient('tele', API_ID, API_HASH)

async def start_searching():
    """Mengirim perintah /search ke bot target"""
    logger.info(f"Mengirim /search ke @{TARGET_BOT}")
    await client.send_message(TARGET_BOT, '/search')

@client.on(events.NewMessage(from_users=TARGET_BOT, incoming=True))
async def handle_bot_messages(event):
    message_text = event.message.message
    logger.info(f"Pesan dari bot: {message_text[:80]}")

    # Cek jika pasangan ditemukan
    if MATCH_FOUND_TEXT in message_text or GREETING_TEXT in message_text:
        logger.info("Pasangan ditemukan! Mengirim link promo...")
        await asyncio.sleep(2)
        await client.send_message(TARGET_BOT, LINK_PESAN)
        logger.info(f"Link promo terkirim: {LINK_PESAN}")

        # Setelah kirim pesan, tunggu lalu /next untuk cari baru
        await asyncio.sleep(5)
        logger.info("Mencari pasangan baru dengan /next...")
        await client.send_message(TARGET_BOT, '/next')

    # Lawan bicara pergi atau diminta /search lagi
    elif PARTNER_LEFT_TEXT in message_text or SEARCH_AGAIN_TEXT in message_text:
        logger.info("Lawan bicara pergi. Mencari lagi...")
        await asyncio.sleep(3)
        await start_searching()

    # Sedang mencari
    elif "sedang mencari" in message_text.lower() or "mencari obrolan" in message_text.lower():
        logger.info("Sedang mencari pasangan...")

    # Obrolan berhenti
    elif "berhenti" in message_text.lower() or "meninggalkan" in message_text.lower():
        logger.info("Obrolan berhenti, mencari lagi...")
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
