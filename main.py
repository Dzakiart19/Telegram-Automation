import os
import sys
import asyncio
import logging
from telethon import TelegramClient
from keep_alive import keep_alive
from lib.bot_random_pacar import register as register_bot1
from lib.bot_anony_meet import register as register_bot2

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

API_ID   = os.getenv('API_ID',   '26372402')
API_HASH = os.getenv('API_HASH', 'a2732d77a9abc513db065170f563a603')
PHONE    = os.getenv('PHONE',    '+6285962694573')


async def run_bot():
    client = TelegramClient('tele', API_ID, API_HASH)

    # Daftarkan kedua bot, dapatkan fungsi start masing-masing
    start_bot1 = register_bot1(client)
    start_bot2 = register_bot2(client)

    logger.info("Menghubungkan ke Telegram...")
    await client.connect()

    if not await client.is_user_authorized():
        logger.error("Sesi tidak valid! Harap login ulang.")
        return

    me = await client.get_me()
    logger.info(f"Login: {me.first_name} (@{me.username})")

    # Bot1 mulai duluan, Bot2 menyusul 8 detik kemudian
    await start_bot1()
    await asyncio.sleep(8)
    await start_bot2()

    await client.run_until_disconnected()


if __name__ == '__main__':
    keep_alive()
    import time
    while True:
        try:
            logger.info("=== Bot dimulai ===")
            asyncio.run(run_bot())
            logger.info("Disconnect. Restart dalam 5 detik...")
        except Exception as e:
            logger.error(f"ERROR: {e}", exc_info=True)
            logger.info("Restart dalam 5 detik...")
        time.sleep(5)
