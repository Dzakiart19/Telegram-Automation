---
name: Telethon session/version pinning
description: Why prod crashed with "too many values to unpack" reading tele.session, and how to prevent it
---

The SQLite session file format used by Telethon (`*.session`) is version-specific. If the dev environment has a newer/older Telethon installed than what `pyproject.toml`/`poetry.lock` pins, production will install the pinned (stale) version and fail to read a session file created by the dev version, with `ValueError: too many values to unpack (expected 5)` in `SQLiteSession`.

**Why:** Dev environments can drift from the lockfile (e.g. packages installed directly bypassing poetry), so the lockfile silently goes stale relative to what's actually running and being used to create session files.

**How to apply:** Whenever debugging a working-in-dev-broken-in-prod Telethon crash, first compare `pip show telethon` (actual installed version) against the version pinned in `pyproject.toml`/`poetry.lock`. Re-lock to match before assuming it's a code bug.
