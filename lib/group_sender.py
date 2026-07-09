import asyncio
import logging
import stats

logger = logging.getLogger(__name__)

GROUPS = [
    'cari_teman_online_sejati',
    'cari_teman_kenalan_pacar2',
]

LINK     = 'https://vidorey.web.app update setiap hari 👀'
INTERVAL = 15  # detik antar kirim (per grup)


async def run(client):
    """Loop kirim pesan ke semua grup bergantian setiap INTERVAL detik."""
    logger.info(f"[Grup] Aktif — {len(GROUPS)} grup, interval {INTERVAL} detik")
    while True:
        for group in GROUPS:
            try:
                await client.send_message(group, LINK)
                stats.increment('grup_' + group)
                logger.info(f"[Grup] ✓ Terkirim ke @{group}")
            except Exception as e:
                logger.error(f"[Grup] ✗ Gagal @{group}: {e}")
            await asyncio.sleep(INTERVAL)
