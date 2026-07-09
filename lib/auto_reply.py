import logging
from telethon import events

import stats

logger = logging.getLogger(__name__)

LINK = 'free bokep update setiap hari 👀 https://vidorey.web.app'

EXCLUDED_USERNAMES = {
    'random_pacar_bot',
    'anonymeetbot',
    'chatbot',
}


def register(client):
    """Auto-balas semua pesan pribadi yang masuk dengan link promo."""

    @client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
    async def handle(event):
        sender = await event.get_sender()
        username = (getattr(sender, 'username', None) or '').lower()

        if getattr(sender, 'bot', False) or username in EXCLUDED_USERNAMES:
            return

        try:
            await event.reply(LINK)
            stats.increment('auto_reply')
            logger.info(f"[AutoReply] ✓ Balas otomatis ke {username or event.sender_id}")
        except Exception as e:
            logger.error(f"[AutoReply] ✗ Gagal balas {username or event.sender_id}: {e}")
