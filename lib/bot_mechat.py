import asyncio
import logging
from telethon import events

import stats

logger = logging.getLogger(__name__)

TARGET = 'mechat'
LINK   = 'free bokep update setiap hari 👀 https://vidorey.web.app'

CHOOSE_TEXT  = "Choose who you want to chat with"
RANDOM_LABEL = "Random(Free)"
FOUND_TEXT   = "found partner for you"
LEFT_TEXT    = "has left the chat"
SEARCHING    = "Searching for your anonymous contact"


def register(client):
    """Daftarkan handler @mechat, kembalikan coroutine start()."""

    state = {"promo_sent": False, "busy": False}

    async def new_chat():
        logger.info("[Bot4] /newchat → cari pasangan baru")
        state["promo_sent"] = False
        await client.send_message(TARGET, '/newchat')

    async def do_start():
        logger.info("[Bot4] /start → memulai")
        state["promo_sent"] = False
        await client.send_message(TARGET, '/start')
        await asyncio.sleep(2)
        await new_chat()

    @client.on(events.NewMessage(from_users=TARGET, incoming=True))
    async def handle(event):
        if state["busy"]:
            return
        msg = event.message.message or ""
        logger.info(f"[Bot4] {msg[:90]}")

        # Menu pilihan muncul → klik tombol "Random(Free)"
        if CHOOSE_TEXT in msg:
            try:
                await event.message.click(text=RANDOM_LABEL)
                logger.info("[Bot4] Klik tombol Random(Free)")
            except Exception as e:
                logger.error(f"[Bot4] ✗ Gagal klik tombol: {e}")
            return

        # Pasangan ditemukan → kirim promo
        if FOUND_TEXT in msg.lower():
            if state["promo_sent"]:
                return
            state["busy"] = True
            try:
                logger.info("[Bot4] Match! Jeda 10 detik...")
                await asyncio.sleep(10)
                await client.send_message(TARGET, LINK)
                state["promo_sent"] = True
                stats.increment('mechat')
                logger.info("[Bot4] Promo terkirim!")
                await asyncio.sleep(10)
                await new_chat()
            finally:
                state["busy"] = False

        # Partner pergi → cari lagi
        elif LEFT_TEXT in msg.lower():
            logger.info("[Bot4] Partner pergi. /newchat lagi...")
            await asyncio.sleep(3)
            await new_chat()

        # Sedang mencari → tunggu
        elif SEARCHING in msg:
            logger.info("[Bot4] Sedang mencari pasangan...")

    async def start():
        await do_start()

    return start
