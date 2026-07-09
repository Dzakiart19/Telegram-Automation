import os
import sys
import asyncio
import logging
from telethon import TelegramClient
from keep_alive import keep_alive
from lib.bot_random_pacar import register as register_bot1
from lib.bot_anony_meet import register as register_bot2
from lib.bot_chatbot import register as register_bot3
from lib.bot_mechat import register as register_bot4
from lib.bot_anon_chat import register as register_bot5
from lib import group_sender
from lib import auto_reply


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

API_ID   = os.getenv('API_ID',   '26372402')
API_HASH = os.getenv('API_HASH', 'a2732d77a9abc513db065170f563a603')
PHONE    = os.getenv('PHONE',    '+6285962694573')

IS_DEPLOYMENT = bool(os.getenv('REPLIT_DEPLOYMENT'))
SESSION_NAME  = 'tele_prod' if IS_DEPLOYMENT else 'tele_dev'


async def run_bot():
    logger.info(f"Menggunakan session: {SESSION_NAME} (deployment={IS_DEPLOYMENT})")
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

    # Daftarkan semua bot, dapatkan fungsi start masing-masing
    start_bot1 = register_bot1(client)
    start_bot2 = register_bot2(client)
    start_bot3 = register_bot3(client)
    start_bot4 = register_bot4(client)
    start_bot5 = register_bot5(client)
    auto_reply.register(client)

    logger.info("Menghubungkan ke Telegram...")
    await client.connect()

    if not await client.is_user_authorized():
        logger.error("Sesi tidak valid! Harap login ulang.")
        return

    me = await client.get_me()
    logger.info(f"Login: {me.first_name} (@{me.username})")

    # Bot mulai bergantian dengan jeda agar tidak bersamaan
    await start_bot1()
    await asyncio.sleep(8)
    await start_bot2()
    await asyncio.sleep(8)
    await start_bot3()
    await asyncio.sleep(8)
    await start_bot4()
    await asyncio.sleep(8)
    await start_bot5()

    asyncio.create_task(group_sender.run(client))

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
