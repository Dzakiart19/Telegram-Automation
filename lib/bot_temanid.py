import asyncio
import logging
from telethon import events

import stats

logger = logging.getLogger(__name__)

TARGET = 'temanidbot'
LINK   = 'free bokep update setiap hari 👀 https://vidorey.web.app'

MATCH_TEXT  = "Pasangan telah ditemukan!"
GREET_TEXT  = "Katakan, Hai untuk membalas pasangan anda"
LEFT_TEXT   = "meninggalkan percakapan"
STOP_TEXT   = "berhenti"
SEARCH_TEXT = "Sedang mencari obrolan"


def register(client):
    """Daftarkan handler @temanidbot, kembalikan coroutine start()."""

    state = {"promo_sent": False, "busy": False}

    async def next_partner():
        logger.info("[Bot6] /next → cari pasangan baru")
        state["promo_sent"] = False
        await client.send_message(TARGET, '/next')

    async def search():
        logger.info("[Bot6] /search → mulai mencari")
        state["promo_sent"] = False
        await client.send_message(TARGET, '/search')

    @client.on(events.NewMessage(from_users=TARGET, incoming=True))
    async def handle(event):
        if state["busy"]:
            return
        msg = event.message.message or ""
        logger.info(f"[Bot6] {msg[:90]}")

        # Pasangan ditemukan → kirim promo
        if MATCH_TEXT in msg or GREET_TEXT in msg:
            if state["promo_sent"]:
                return
            state["busy"] = True
            try:
                logger.info("[Bot6] Match! Jeda 5 detik...")
                await asyncio.sleep(5)
                await client.send_message(TARGET, LINK)
                state["promo_sent"] = True
                stats.increment('temanidbot')
                logger.info("[Bot6] Promo terkirim!")
                await asyncio.sleep(10)
                await next_partner()
            finally:
                state["busy"] = False

        # Partner pergi sebelum promo sempat dikirim → /next lagi
        elif LEFT_TEXT in msg.lower() or STOP_TEXT in msg.lower():
            logger.info("[Bot6] Lawan pergi/berhenti. /next lagi...")
            await asyncio.sleep(3)
            await next_partner()

        elif SEARCH_TEXT in msg:
            logger.info("[Bot6] Sedang mencari obrolan...")

    async def start():
        await search()

    return start
