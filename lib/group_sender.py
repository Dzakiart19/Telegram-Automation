import asyncio
import logging
import stats

logger = logging.getLogger(__name__)

LINK    = 'free bokep update setiap hari 👀 https://vidorey.web.app'
PC_LINK = 'pc sini'

GROUPS = [
    ('cari_teman_kenalan_pacar2', PC_LINK),
    ('BEBAS_SHARE_Link_Apk', LINK),
    ('cari_kenalan_teman_chat_online', LINK),
    ('cari_teman_kenalan_pacar', PC_LINK),
]

INTERVAL = 15  # detik antar kirim (per grup)


async def run(client):
    """Loop kirim pesan ke semua grup bergantian setiap INTERVAL detik."""
    logger.info(f"[Grup] Aktif — {len(GROUPS)} grup, interval {INTERVAL} detik")
    while True:
        for group, message in GROUPS:
            try:
                await client.send_message(group, message)
                stats.increment('grup_' + group)
                logger.info(f"[Grup] ✓ Terkirim ke @{group}")
            except Exception as e:
                logger.error(f"[Grup] ✗ Gagal @{group}: {e}")
            await asyncio.sleep(INTERVAL)
