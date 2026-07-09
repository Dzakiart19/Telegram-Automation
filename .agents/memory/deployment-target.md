---
name: Deployment target for this bot
description: Deployment target tradeoff for the Telegram automation bot (VM vs autoscale) given free-tier budget constraint
---

Ideally this bot (persistent Telethon client, in-memory Flask stats, local SQLite session file) should run on `vm` (Reserved VM / always-on), since autoscale can spin up multiple/ephemeral instances that don't preserve the persistent connection, in-memory stats, or session file consistency.

**Why:** The user is on Replit's free tier and Reserved VM deployments require a paid plan. Per explicit user decision, the project is deployed on `autoscale` instead, accepting the tradeoff (the process may be scaled to zero when idle and lose its live Telegram connection/in-memory stats until the next incoming request wakes it; the `/health` endpoint + external cronjob ping is used to mitigate this).

**How to apply:** Do not "fix" the deployment target back to `vm` on this project — `autoscale` is the deliberate, budget-driven choice. Only revisit if the user upgrades their plan or explicitly asks to reconsider. If debugging production crashes, keep in mind autoscale's cold-start/scale-to-zero behavior as a likely factor (e.g. bot state resetting, session reconnect churn).
