import os
import sys
import asyncio
import logging
from telethon import TelegramClient, events
from keep_alive import keep_alive
import stats

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

API_ID = os.getenv('API_ID', '26372402')
API_HASH = os.getenv('API_HASH', 'a2732d77a9abc513db065170f563a603')
PHONE = os.getenv('PHONE', '+6285962694573')

LINK_PESAN = 'https://vidorey.web.app update setiap hari 👀'

# ── Bot 1: @random_pacar_bot ──────────────────────────────────
BOT1 = 'random_pacar_bot'
BOT1_MATCH      = "Pasangan telah ditemukan!"
BOT1_GREETING   = "Katakan, Hai untuk membalas pasangan anda 😊"
BOT1_LEFT       = "Lawan bicara telah meninggalkan percakapan"
BOT1_SEARCH_TXT = "Ketik /search untuk mencari obrolan baru"

# ── Bot 2: @AnonyMeetBot ──────────────────────────────────────
BOT2 = 'AnonyMeetBot'
BOT2_MATCH      = "It's a match!"
BOT2_LEFT_THEM  = "Your partner closed the conversation"
BOT2_LEFT_YOU   = "You have closed the conversation"
BOT2_SEARCHING  = "Start looking for a partner"

async def run_bot():
    client = TelegramClient('tele', API_ID, API_HASH)

    # ── Handler Bot 1 ─────────────────────────────────────────
    @client.on(events.NewMessage(from_users=BOT1, incoming=True))
    async def handle_bot1(event):
        msg = event.message.message
        logger.info(f"[Bot1] {msg[:80]}")

        if BOT1_MATCH in msg or BOT1_GREETING in msg:
            logger.info("[Bot1] Match! Jeda 5 detik...")
            await asyncio.sleep(5)
            await client.send_message(BOT1, LINK_PESAN)
            stats.increment('random_pacar_bot')
            logger.info("[Bot1] Promo terkirim!")
            await asyncio.sleep(5)
            logger.info("[Bot1] /next...")
            await client.send_message(BOT1, '/next')

        elif BOT1_LEFT in msg or BOT1_SEARCH_TXT in msg:
            logger.info("[Bot1] Lawan pergi, /search lagi...")
            await asyncio.sleep(5)
            await client.send_message(BOT1, '/search')

        elif "berhenti" in msg.lower() or "meninggalkan" in msg.lower():
            logger.info("[Bot1] Berhenti, /search lagi...")
            await asyncio.sleep(5)
            await client.send_message(BOT1, '/search')

    # ── Handler Bot 2 ─────────────────────────────────────────
    @client.on(events.NewMessage(from_users=BOT2, incoming=True))
    async def handle_bot2(event):
        msg = event.message.message
        logger.info(f"[Bot2] {msg[:80]}")

        if BOT2_MATCH in msg:
            logger.info("[Bot2] Match! Jeda 5 detik...")
            await asyncio.sleep(5)
            await client.send_message(BOT2, LINK_PESAN)
            stats.increment('AnonyMeetBot')
            logger.info("[Bot2] Promo terkirim!")
            await asyncio.sleep(5)
            logger.info("[Bot2] /next...")
            await client.send_message(BOT2, '/next')

        elif BOT2_LEFT_THEM in msg:
            logger.info("[Bot2] Partner pergi, /start lagi...")
            await asyncio.sleep(5)
            await client.send_message(BOT2, '/start')

        elif BOT2_LEFT_YOU in msg:
            logger.info("[Bot2] Obrolan ditutup, /start lagi...")
            await asyncio.sleep(5)
            await client.send_message(BOT2, '/start')

    # ── Connect ───────────────────────────────────────────────
    logger.info("Menghubungkan ke Telegram...")
    await client.connect()

    if not await client.is_user_authorized():
        logger.error("Sesi tidak valid!")
        return

    me = await client.get_me()
    logger.info(f"Login: {me.first_name} (@{me.username})")

    # Mulai Bot1 dulu, Bot2 dengan jeda 8 detik agar tidak bersamaan
    logger.info("[Bot1] Memulai /search...")
    await client.send_message(BOT1, '/search')

    await asyncio.sleep(8)

    logger.info("[Bot2] Memulai /start...")
    await client.send_message(BOT2, '/start')

    await client.run_until_disconnected()

if __name__ == '__main__':
    keep_alive()
    while True:
        try:
            logger.info("=== Bot dimulai ===")
            asyncio.run(run_bot())
            logger.info("Disconnect. Restart dalam 5 detik...")
        except Exception as e:
            logger.error(f"ERROR: {e}", exc_info=True)
            logger.info("Restart dalam 5 detik...")
        import time
        time.sleep(5)
