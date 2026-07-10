import asyncio
import logging
import stats
from telethon.errors import AuthKeyDuplicatedError, UserBannedInChannelError
from lib.telegram_safety import safe_send_message

logger = logging.getLogger(__name__)

LINK    = 'free bokep update setiap hari 👀 https://vidorey.web.app'
PC_LINK = 'pc sini'

GROUPS = [
    ('cari_teman_kenalan_pacar2', PC_LINK),
    ('BEBAS_SHARE_Link_Apk', LINK),
    ('cari_teman_kenalan_pacar', PC_LINK),
    ('cari_pacar_temen_online', LINK),
    ('CARI_PACAR_TEMEN_BESTIE', LINK),
    ('Cari_Kenalan_Bestie_Online', LINK),
    ('Cari_Teman_Online_Pacar_Sahabat', LINK),
    ('cari_teman_sahabat_chat', LINK),
]

INTERVAL = 15  # detik antar kirim (per grup)


async def run(client):
    """Loop kirim pesan ke semua grup bergantian setiap INTERVAL detik."""
    logger.info(f"[Grup] Aktif — {len(GROUPS)} grup, interval {INTERVAL} detik")
    while True:
        for group, message in GROUPS:
            try:
                ok = await safe_send_message(client, group, message, label='Grup')
                if ok:
                    stats.increment('grup_' + group)
                    logger.info(f"[Grup] ✓ Terkirim ke @{group}")
            except UserBannedInChannelError:
                logger.critical(
                    "[Grup] Akun kena restriksi 'banned from sending messages in supergroups/"
                    "channels' (berlaku akun-wide, bukan per-grup). Menghentikan loop grup "
                    "selama 30 menit agar tidak memperparah restriksi."
                )
                await asyncio.sleep(1800)
                break
            except AuthKeyDuplicatedError:
                logger.critical("[Grup] AuthKeyDuplicatedError, menghentikan loop grup.")
                return
            await asyncio.sleep(INTERVAL)
