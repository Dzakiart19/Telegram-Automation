import asyncio
import logging
import stats

logger = logging.getLogger(__name__)

GROUP    = 'cari_teman_online_sejati'
LINK     = 'https://vidorey.web.app update setiap hari 👀'
INTERVAL = 15  # detik


async def run(client):
    """Loop kirim pesan ke grup setiap INTERVAL detik."""
    logger.info(f"[Grup] Mulai kirim ke @{GROUP} setiap {INTERVAL} detik")
    while True:
        try:
            await client.send_message(GROUP, LINK)
            stats.increment('grup_' + GROUP)
            logger.info(f"[Grup] Pesan terkirim ke @{GROUP}")
        except Exception as e:
            logger.error(f"[Grup] Gagal kirim: {e}")
        await asyncio.sleep(INTERVAL)
