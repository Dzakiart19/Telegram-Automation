---
name: Deployment target for this bot
description: Correct deployment target for the Telegram automation bot and a gotcha about it reverting
---

This project runs a persistent Telethon client (long-lived Telegram connection) plus an in-memory Flask stats dashboard and a local SQLite session file. It must be deployed as `vm` (Reserved VM / always-on), never `cloudrun` (autoscale/stateless) — autoscale can spin multiple/ephemeral instances that don't preserve the persistent connection, in-memory stats, or session file consistency.

**Why:** `.replit` was observed to have reverted to `deploymentTarget = "cloudrun"` after being explicitly set to `vm` in an earlier session, which contributed to a production crash loop.

**How to apply:** Before troubleshooting a production-only crash on this project, check `.replit`'s `[deployment]` section for `deploymentTarget` and correct it back to `vm` if it has drifted.
