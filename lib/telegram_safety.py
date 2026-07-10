import asyncio
import logging
import random

from telethon.errors import FloodWaitError, AuthKeyDuplicatedError

import control

logger = logging.getLogger(__name__)


async def safe_send_message(client, target, message, *, label="?"):
    """Kirim pesan dengan penanganan error yang aman untuk dipakai berulang di runtime
    (bukan cuma saat startup).

    - FloodWaitError: benar-benar menunggu durasi yang diminta Telegram (+ jitter kecil)
      sebelum melanjutkan, alih-alih langsung mencoba lagi/lanjut ke target berikutnya.
    - AuthKeyDuplicatedError: session ini sudah dicabut Telegram (dipakai dari 2 tempat
      sekaligus). Retry tidak akan membantu, jadi error ini diangkat ulang supaya
      pemanggil (main.py) bisa berhenti dengan bersih alih-alih crash-loop cepat.
    - Exception lain: dicatat sebagai error dan dianggap gagal terkirim.

    Return True jika berhasil terkirim, False jika gagal (selain AuthKeyDuplicatedError).
    """
    try:
        await client.send_message(target, message)
        return True
    except FloodWaitError as e:
        wait = e.seconds + random.randint(1, 5)
        logger.warning(f"[{label}] Flood-wait {e.seconds}s pada @{target}, menunggu {wait}s sebelum lanjut...")
        await asyncio.sleep(wait)
        return False
    except AuthKeyDuplicatedError:
        logger.critical(
            f"[{label}] AuthKeyDuplicatedError saat kirim ke @{target} — session sudah dicabut Telegram "
            "(dipakai dari 2 tempat sekaligus). Memutus koneksi, TIDAK retry dengan session yang sama."
        )
        control.mark_auth_key_dead()
        try:
            await client.disconnect()
        except Exception:
            pass
        raise
    except Exception as e:
        logger.error(f"[{label}] Gagal kirim ke @{target}: {e}")
        return False
