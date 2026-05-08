# Noise Blocklist

Senders that auto-file to FYI with **no scoring** — they're confirmed noise and we don't want to spend cycles on them.

**To add a sender:** Confirm it's noise → add the domain or full email below with a one-line reason. The skill checks this file on every run.

**When to audit:** Quarterly, or when high-frequency senders start cluttering the morning briefing despite being non-actionable.

---

## Domain blocklist (auto-FYI, no scoring)

Add your own noise domains here. Examples below are a starting template — customize to your own tools and subscriptions.

| Domain pattern | Reason |
|---|---|
| `apollo.io` | Apollo product/marketing emails — if you use Apollo but don't act on these |
| `mail.apollo.io` | Apollo marketing subdomain |
| `notifications.trigify.io` | Trigify onboarding sequence (if already onboarded) |
| `featurebase.app` | Product update marketing |
| `payments-noreply@google.com` | Google Workspace monthly invoice receipts |

---

## Self-suppress (drop entirely, don't show in any bucket)

Add your own email addresses here — so your own outbound notifications don't appear in your inbox triage.

| Sender | Reason |
|---|---|
| `your-email@substack.com` | Your own Substack — should not appear in your own inbox triage |

---

## Senders explicitly KEPT IN scoring (signal, not noise)

These look automated but are high-signal — never block:

| Sender | Why it's signal |
|---|---|
| `hello@cal.com` | New Cal.com bookings (Discovery Calls, coaching). Drives meeting prep. |
| `notifications@tally.so` | Tally form submissions = inbound leads |
| `no-reply@fathom.video` | Call recaps. Transcripts feed commitment mining. |

Adjust this list to match your own booking, form, and call recording tools.

---

## How to use this file

The skill reads this on every run. For each incoming email:

1. Check `Self-suppress` first — if matched, drop the email entirely (don't include in counts or report).
2. Check `Domain blocklist` — if sender domain matches, force bucket = FYI, score = 0, no action item.
3. Otherwise → continue to content-pattern matching.

This file replaces what used to be hardcoded in SKILL.md. Edit here, no rebuild needed.
