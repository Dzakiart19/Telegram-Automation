import asyncio
import logging
import stats

logger = logging.getLogger(__name__)

TARGET = 'random_pacar_bot'
LINK   = 'https://vidorey.web.app update setiap hari 👀'

MATCH_TEXT   = "Pasangan telah ditemukan!"
GREET_TEXT   = "Katakan, Hai untuk membalas pasangan anda 😊"
LEFT_TEXT    = "Lawan bicara telah meninggalkan percakapan"
SEARCH_TEXT  = "Ketik /search untuk mencari obrolan baru"


def register(client):
    """Daftarkan event handler dan kembalikan fungsi start."""

    state = {"promo_sent": False, "busy": False}

    async def next_partner():
        logger.info("[Bot1] /next → cari pasangan baru")
        state["promo_sent"] = False
        await client.send_message(TARGET, '/next')

    async def search():
        logger.info("[Bot1] /search → mulai mencari")
        state["promo_sent"] = False
        await client.send_message(TARGET, '/search')

    @client.on(__import__('telethon').events.NewMessage(from_users=TARGET, incoming=True))
    async def handle(event):
        if state["busy"]:
            return
        msg = event.message.message
        logger.info(f"[Bot1] {msg[:90]}")

        # Pasangan ditemukan → kirim promo
        if MATCH_TEXT in msg or GREET_TEXT in msg:
            if state["promo_sent"]:
                return
            state["busy"] = True
            try:
                logger.info("[Bot1] Match! Jeda 5 detik...")
                await asyncio.sleep(5)
                await client.send_message(TARGET, LINK)
                state["promo_sent"] = True
                stats.increment('random_pacar_bot')
                logger.info("[Bot1] Promo terkirim!")
                await asyncio.sleep(5)
                await next_partner()
            finally:
                state["busy"] = False

        # Partner pergi sebelum promo sempat dikirim → /next lagi
        elif LEFT_TEXT in msg or SEARCH_TEXT in msg or "meninggalkan" in msg.lower():
            logger.info("[Bot1] Lawan pergi. /next lagi...")
            await asyncio.sleep(3)
            await next_partner()

        elif "berhenti" in msg.lower():
            logger.info("[Bot1] Obrolan berhenti. /next lagi...")
            await asyncio.sleep(3)
            await next_partner()

    async def start():
        await search()

    return start
