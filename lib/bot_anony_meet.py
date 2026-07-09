import asyncio
import logging
import stats

logger = logging.getLogger(__name__)

TARGET = 'AnonyMeetBot'
LINK   = 'https://vidorey.web.app update setiap hari 👀'

MATCH_TEXT      = "It's a match!"
LEFT_BY_THEM    = "Your partner closed the conversation"
LEFT_BY_YOU     = "You have closed the conversation"
NOT_IN_CONV     = "You are not in conversation"
ALREADY_IN_CHAT = "You are already in chat"
IN_QUEUE        = "already in the matching queue"
CAPTCHA_TEXT    = "solve the captcha"


def register(client):
    """Daftarkan event handler dan kembalikan fungsi start."""

    state = {"promo_sent": False, "busy": False, "started": False}

    async def next_partner():
        logger.info("[Bot2] /next → cari pasangan baru")
        state["promo_sent"] = False
        await client.send_message(TARGET, '/next')

    async def do_start():
        logger.info("[Bot2] /start → memulai")
        state["promo_sent"] = False
        state["started"] = True
        await client.send_message(TARGET, '/start')

    @client.on(__import__('telethon').events.NewMessage(from_users=TARGET, incoming=True))
    async def handle(event):
        if state["busy"]:
            return
        msg = event.message.message
        logger.info(f"[Bot2] {msg[:90]}")

        # Match ditemukan → kirim promo
        if MATCH_TEXT in msg:
            if state["promo_sent"]:
                return
            state["busy"] = True
            try:
                logger.info("[Bot2] Match! Jeda 5 detik...")
                await asyncio.sleep(5)
                await client.send_message(TARGET, LINK)
                state["promo_sent"] = True
                stats.increment('AnonyMeetBot')
                logger.info("[Bot2] Promo terkirim!")
                await asyncio.sleep(5)
                await next_partner()
            finally:
                state["busy"] = False

        # Partner pergi SEBELUM promo sempat dikirim → /next
        elif LEFT_BY_THEM in msg:
            if not state["promo_sent"]:
                logger.info("[Bot2] Partner pergi sebelum promo. /next...")
                await asyncio.sleep(3)
                await next_partner()
            else:
                logger.info("[Bot2] Partner pergi (promo sudah dikirim). /next...")
                await asyncio.sleep(3)
                await next_partner()

        # Kamu yang menutup → /next saja
        elif LEFT_BY_YOU in msg:
            logger.info("[Bot2] Percakapan ditutup. /next...")
            await asyncio.sleep(3)
            await next_partner()

        # Belum dalam percakapan (awal/reset) → /start
        elif NOT_IN_CONV in msg:
            logger.info("[Bot2] Tidak dalam percakapan. /start...")
            await asyncio.sleep(3)
            await do_start()

        # Captcha → jeda panjang lalu /next
        elif CAPTCHA_TEXT in msg.lower():
            logger.info("[Bot2] Captcha terdeteksi! Jeda 30 detik...")
            await asyncio.sleep(30)
            await next_partner()

        # Sudah di queue → abaikan
        elif IN_QUEUE in msg or ALREADY_IN_CHAT in msg:
            logger.info("[Bot2] Sudah dalam antrian, abaikan.")

    async def start():
        await do_start()

    return start
