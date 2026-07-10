---
name: Single-process bot crash isolation
description: Why a flood-wait or error in one Telethon bot handler must not crash the whole main.py process
---

The bot runners (Bot1-6) all share one `TelegramClient` and one asyncio event loop in `main.py`, wrapped in an outer `while True: asyncio.run(run_bot())` restart loop.

**Why:** early on, a single bot hitting `FloodWaitError` during its startup sequence (`await start_botN()`) propagated up and crashed `run_bot()` entirely. The outer loop then reconnected the *same* client immediately, which could still be mid-teardown, causing `sqlite3.OperationalError: database is locked` on the session file, and repeating in a tight 5s crash loop — during which the still-active flood-wait window meant it kept crashing without ever actually waiting it out.

**How to apply:** any per-bot startup/send call in `main.py` must be wrapped (see `safe_start` helper) to catch `FloodWaitError`/generic exceptions per-bot and log+continue, not let it bubble up. Also always `await client.disconnect()` in a `finally` around the whole `run_bot()` body before the outer loop retries, so the SQLite session file isn't left locked by a half-torn-down client.
