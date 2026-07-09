import asyncio
import logging
import stats
from telethon import events

logger = logging.getLogger(__name__)

TARGET = 'chatbot'
LINK   = 'free bokep update setiap hari 👀 https://vidorey.web.app'

MATCH_TEXT   = "Teman bicara ditemukan"
LEFT_TEXT    = "Pasanganmu telah menghentikan obrolan"
SEARCH_TEXT  = "Ketik /search untuk menemukan pasangan baru"
THANKS_TEXT  = "Terima kasih atas tanggapan Anda"
SEARCHING    = "sedang mencari teman bicara baru"


def register(client):
    """Daftarkan handler @chatbot, kembalikan coroutine start()."""

    state = {"promo_sent": False, "busy": False}

    async def next_partner():
        logger.info("[Bot3] /next → cari teman baru")
        state["promo_sent"] = False
        await client.send_message(TARGET, '/next')

    async def do_start():
        logger.info("[Bot3] /start → memulai")
        state["promo_sent"] = False
        await client.send_message(TARGET, '/start')

    @client.on(events.NewMessage(from_users=TARGET, incoming=True))
    async def handle(event):
        if state["busy"]:
            return
        msg = event.message.message
        logger.info(f"[Bot3] {msg[:90]}")

        # Teman ditemukan → kirim promo
        if MATCH_TEXT in msg:
            if state["promo_sent"]:
                return
            state["busy"] = True
            try:
                logger.info("[Bot3] Match! Jeda 5 detik...")
                await asyncio.sleep(5)
                await client.send_message(TARGET, LINK)
                state["promo_sent"] = True
                stats.increment('chatbot')
                logger.info("[Bot3] Promo terkirim!")
                await asyncio.sleep(10)
                await next_partner()
            finally:
                state["busy"] = False

        # Partner pergi sebelum/sesudah promo → /next
        elif LEFT_TEXT in msg or SEARCH_TEXT in msg:
            logger.info("[Bot3] Partner pergi. /next...")
            await asyncio.sleep(3)
            state["promo_sent"] = False
            await next_partner()

        # Konfirmasi atau sedang mencari → abaikan
        elif THANKS_TEXT in msg or SEARCHING in msg.lower():
            logger.info("[Bot3] Sedang mencari / konfirmasi, tunggu...")

    async def start():
        await do_start()

    return start
