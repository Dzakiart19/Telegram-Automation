import os
import sys
import asyncio
import logging
from telethon import TelegramClient, events
from keep_alive import keep_alive

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

API_ID = os.getenv('API_ID', '26372402')
API_HASH = os.getenv('API_HASH', 'a2732d77a9abc513db065170f563a603')
PHONE = os.getenv('PHONE', '+6285962694573')

TARGET_BOT = 'random_pacar_bot'
LINK_PESAN = 'https://vidorey.web.app update setiap hari 👀'

MATCH_FOUND_TEXT = "Pasangan telah ditemukan!"
GREETING_TEXT = "Katakan, Hai untuk membalas pasangan anda 😊"
PARTNER_LEFT_TEXT = "Lawan bicara telah meninggalkan percakapan"
SEARCH_AGAIN_TEXT = "Ketik /search untuk mencari obrolan baru"

async def run_bot():
    client = TelegramClient('tele', API_ID, API_HASH)

    async def start_searching():
        logger.info(f"Mengirim /search ke @{TARGET_BOT}")
        await client.send_message(TARGET_BOT, '/search')

    @client.on(events.NewMessage(from_users=TARGET_BOT, incoming=True))
    async def handle_bot_messages(event):
        message_text = event.message.message
        logger.info(f"Pesan masuk: {message_text[:100]}")

        if MATCH_FOUND_TEXT in message_text or GREETING_TEXT in message_text:
            logger.info("Pasangan ditemukan! Mengirim link promo...")
            await asyncio.sleep(2)
            await client.send_message(TARGET_BOT, LINK_PESAN)
            logger.info(f"Link promo terkirim!")
            await asyncio.sleep(5)
            logger.info("Mencari pasangan baru dengan /next...")
            await client.send_message(TARGET_BOT, '/next')

        elif PARTNER_LEFT_TEXT in message_text or SEARCH_AGAIN_TEXT in message_text:
            logger.info("Lawan pergi. Mencari lagi...")
            await asyncio.sleep(3)
            await start_searching()

        elif "sedang mencari" in message_text.lower() or "mencari obrolan" in message_text.lower():
            logger.info("Sedang mencari pasangan...")

        elif "berhenti" in message_text.lower() or "meninggalkan" in message_text.lower():
            logger.info("Obrolan berhenti, mencari lagi...")
            await asyncio.sleep(3)
            await start_searching()

    logger.info("Menghubungkan ke Telegram...")
    await client.connect()
    logger.info("Terhubung!")

    auth = await client.is_user_authorized()
    logger.info(f"Status auth: {auth}")

    if not auth:
        logger.error("Sesi tidak valid! Harap login ulang.")
        return

    me = await client.get_me()
    logger.info(f"Login sebagai: {me.first_name} (@{me.username})")

    await start_searching()
    await client.run_until_disconnected()

if __name__ == '__main__':
    keep_alive()
    while True:
        try:
            logger.info("=== Bot dimulai ===")
            asyncio.run(run_bot())
            logger.info("Bot disconnect, restart dalam 5 detik...")
        except Exception as e:
            logger.error(f"ERROR: {e}", exc_info=True)
            logger.info("Restart dalam 5 detik...")
        import time
        time.sleep(5)
