# Email Priority Rubric

The scoring math for `operations-email-report`. SKILL.md reads this at runtime — edit here, no rebuild needed.

Every email gets a **Priority Score** (integer). Score = sum of the 5 signals below, capped at 8. Higher = more important.

**Score is independent of bucket.** Score decides surfacing order; bucket decides which section the email goes in.

---

## Signals

### 1. Sender match — who is it from?

| +3 | +2 | +1 | 0 |
|----|----|----|---|
| Active client (has open rows in Notion Client Deliverables DB) **OR** VIP correspondent (3+ threads in last 30 days from a non-bulk-mail sender — see "VIP rule" below) | Prospect already in Notion CRM People DB | Known company domain (matches `context/business-profile.md`) | Unknown sender |

### 2. Subject signal — what is it about?

| +2 | +1 | 0 |
|----|----|---|
| "proposal", "invoice", "blocked", "deadline", "urgent", "ASAP" in subject | "pricing", "call", "meeting", "schedule", "question", "follow-up" | None of the above |

### 3. Time-sensitivity — when do they need a reply?

| +2 | +1 | 0 |
|----|----|---|
| Asks for response today / tomorrow / by EOD ("today", "by EOD", "tomorrow", "ASAP", "urgent", "deadline" in body) | Asks for response this week ("this week", "by Friday") | No deadline mentioned |

### 4. Thread state — who's holding the ball?

| +2 | +1 | 0 | -1 |
|----|----|---|-----|
| Other side last replied — you are holding the ball | Other side last replied — but it's been < 24h | First message in thread / no clear history | you last replied — awaiting their response |

### 5. Q2 priority bonus

+1 to any email tied to a current Q2 priority from `context/current-priorities.md` (mentions priority keywords or named projects).

---

## Special-case scoring overrides

These trump the additive rubric. Apply BEFORE running steps 1-5.

| Pattern | Override |
|---|---|
| Reply from outbound prospect (sender not in CRM, but you sent the first message in thread) | Min score = 3, bucket = REVENUE, badge = 🔴 minimum. Don't let "unknown sender" suppress a warm reply. |
| Inbound form submission (matched in `content-patterns.md`) | Force score = 6 (🔥), bucket = INBOUND. New leads are always top of report. |
| Inbound booking notification (any provider) | Force score = 5 (🔴), bucket = INBOUND. |
| Time-bombed renewal (subscription renewing in ≤ 5 days) | Force score = 3 (🟡), bucket = ADMIN, sub-bucket = "time-bombed". |
| Sender on noise blocklist (`noise-blocklist.md`) | Force score = 0, bucket = FYI. Do not run the rubric. |
| SaaS-drip-pretending-to-be-human (sender like `firstname@mail.*` / `firstname@email.*` / `firstname@notifications.*`) | Force score = 0, bucket = FYI. Even if subject has signal keywords. |
| Your own newsletter (`your-email@substack.com`) | Suppress entirely — don't include in report. |

---

## VIP rule (frequent correspondent)

When pre-loading clients/CRM (SKILL.md context steps 3-4), also run a Gmail query: `from:* newer_than:30d` and count thread participants by email address.

A sender qualifies as **VIP** when ALL of these are true:
1. They appear in **3+ separate threads** in the last 30 days (not 3 messages in one thread — 3 distinct threads).
2. Their domain is **not** a bulk-mail subdomain (skip if domain matches `mail.*`, `email.*`, `notifications.*`, `noreply.*`, `no-reply.*`, `notification.*`).
3. They are not you.

VIP gets +3 sender match (same as active client). This catches recurring prospects/clients before they're in CRM (e.g. Dan/Chris booking back-and-forth, Alice across two email addresses).

---

## Badge mapping

After computing the score (capped at 8):

- 🔥 **score ≥ 6** — drop everything
- 🔴 **score 4–5** — same-day priority
- 🟠 **dropped ball** — you last replied >3 days ago, no response (assigned by separate detection, not score)
- 🟡 **score 2–3** — this week
- ⚪ **score 0–1** — low / informational

Score determines inline display:
- 🔥 / 🔴 / 🟠 → always shown inline with preview
- 🟡 → summarized (no preview)
- ⚪ → counted but hidden

---

## Q2 priority bonus — how to detect

Read `context/current-priorities.md`. Extract:
1. Named priorities (e.g. "Offer 2 launch", "Cowork OS build")
2. Named clients/projects on those priorities
3. Keywords tied to the priority work

If subject OR first 200 chars of body contains any of those → +1 bonus. Cap at 8.
