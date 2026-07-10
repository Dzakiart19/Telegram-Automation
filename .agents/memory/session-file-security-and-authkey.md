---
name: Telethon session file security & AuthKeyDuplicatedError recovery
description: Why *.session files must never be git-tracked, and why AuthKeyDuplicatedError needs session regen, not just a restart
---

This project's `*.session`/`*.session-journal` files were tracked in git and pushed to a **public** GitHub remote (`origin`). A Telethon `.session` file is a live, authenticated login credential — equivalent to a password. Anyone who clones/views a public repo containing it can log into the Telegram account directly, no OTP/2FA needed.

**Why this matters:** `AuthKeyDuplicatedError` ("used under two different IP addresses simultaneously") can be caused not just by the app's own multiple instances (e.g. autoscale running >1 machine sharing one session file), but also by an outside party using a leaked session concurrently. Since the repo here was confirmed public, leaked-credential use is a real candidate cause, not just a autoscale/instance-count issue.

**How to apply:**
- `.gitignore` must always include `*.session` and `*.session-journal`; `git rm --cached` any already-tracked ones. This repo's `.gitignore` now has this — don't remove it.
- If a session file was ever pushed to a public/shared remote, treat the account as **potentially compromised**: advise the user to terminate all other active Telegram sessions (Telegram app → Settings → Devices → "Terminate all other sessions") and regenerate the session (fresh login) rather than assuming a restart/backoff fixes it.
- Once `AuthKeyDuplicatedError` fires, that specific auth key is generally dead permanently — restarting with the *same* session file will keep failing forever. The only real fix is a fresh interactive login (send_code_request + sign_in) to produce a brand-new session file, then redeploy so production picks it up (dev-container session regen does not affect an already-running deployment until republished).
- `UserBannedInChannelError` ("You're banned from sending messages in supergroups/channels") is an **account-wide** restriction, not per-group — retrying other groups will all fail the same way; back off broadly instead of cycling through the group list.
- Runtime send calls (not just startup) should go through a shared safe-send helper that respects `FloodWaitError.seconds` (sleep, don't hammer) and treats `AuthKeyDuplicatedError` as unrecoverable (disconnect, stop, don't retry).
