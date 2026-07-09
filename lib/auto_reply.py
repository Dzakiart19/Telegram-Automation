import logging
import time
from telethon import events

import stats

logger = logging.getLogger(__name__)

LINK = 'free bokep update setiap hari 👀 https://vidorey.web.app'

EXCLUDED_USERNAMES = {
    'random_pacar_bot',
    'anonymeetbot',
    'chatbot',
}

COOLDOWN = 3600  # detik (1 jam) sebelum boleh membalas orang yang sama lagi


def register(client):
    """Auto-balas semua pesan pribadi yang masuk dengan link promo, dengan cooldown per pengirim."""

    last_replied = {}

    @client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
    async def handle(event):
        sender = await event.get_sender()
        username = (getattr(sender, 'username', None) or '').lower()

        if getattr(sender, 'bot', False) or username in EXCLUDED_USERNAMES:
            return

        now = time.time()
        last = last_replied.get(event.sender_id)
        if last is not None and (now - last) < COOLDOWN:
            logger.info(f"[AutoReply] ⏳ Cooldown aktif, lewati {username or event.sender_id}")
            return

        try:
            await event.reply(LINK)
            last_replied[event.sender_id] = now
            stats.increment('auto_reply')
            logger.info(f"[AutoReply] ✓ Balas otomatis ke {username or event.sender_id}")
        except Exception as e:
            logger.error(f"[AutoReply] ✗ Gagal balas {username or event.sender_id}: {e}")
