---
name: operations-email-report
description: Scans Gmail for the last 24 hours of emails, categorizes each by content pattern (INBOUND / CLIENT / REVENUE / ADMIN / FYI / UNKNOWN), scores priority, surfaces dropped-ball threads, and outputs action items. Use this skill when the user says "check my email", "email report", "what emails came in", "scan my inbox", or "morning emails". Also trigger at position #1 in the morning routine.
---

# operations-email-report

Three jobs, in this order:

**Job 1 — Categorize:** Search Gmail for unread + important emails from the last 24 hours. Categorize each one using `references/content-patterns.md` (matches by content fingerprint, not sender domain — survives tool swaps). Buckets: INBOUND / CLIENT / REVENUE / ADMIN / FYI / UNKNOWN.

**Job 2 — Score:** Apply `references/email-rubric.md` to assign a Priority Score (0-8) and badge (🔥 / 🔴 / 🟡 / ⚪). Score decides surfacing order; bucket decides which section.

**Job 3 — Surface dropped balls:** Separate query — find threads where you last replied >3 days ago and the other side hasn't responded. Surface in 🟠 Dropped Balls section.

**Automation level:** AUTONOMOUS — read-only. Nothing is sent, labeled, or modified in Gmail.

**Routine position:** Morning routine #1 — feeds operations-compile-daily-plan (skill #6).

---

## Setup Required

Replace these placeholders in the context steps below with your actual Notion database IDs:

| Placeholder | What it's for |
|-------------|--------------|
| `YOUR_CLIENT_DELIVERABLES_NOTION_DB_ID` | Your active clients database (powers the +3 sender bonus) |
| `YOUR_PEOPLE_CRM_NOTION_DB_ID` | Your CRM prospects database (powers the +2 sender bonus) |

Also update `references/sender-aliases.md` with your own contacts and `references/noise-blocklist.md` with your own noise domains.

---

## Context to read before running

1. Read `context/current-priorities.md` — current priorities. An email tied to a current priority gets +1 to score (see rubric).
2. Read `context/business-profile.md` — known client/prospect company domains.
3. Read `context/icp.md` — for the form submission ICP mini-score.
4. Read **all four reference files** in this skill:
   - `references/email-rubric.md` — scoring math
   - `references/content-patterns.md` — bucket-detection rules
   - `references/sender-aliases.md` — alias mapping
   - `references/noise-blocklist.md` — auto-FYI domains and self-suppress
5. Query the Notion **Client Deliverables** data source (`collection://YOUR_CLIENT_DELIVERABLES_NOTION_DB_ID`) — list of active clients (page IDs and names). Powers "Active client = +3" sender match.
6. Query the Notion **People** data source (`collection://YOUR_PEOPLE_CRM_NOTION_DB_ID`) — prospects in CRM (Status ≠ Lost / Cold). Powers "CRM prospect = +2" sender match.

---

## Steps

### Part 1 — Search Gmail

1. Three Gmail queries in parallel using `mcp__claude_ai_Gmail__search_threads`:
   - **Unread (24h):** `query: "is:unread newer_than:1d"`, pageSize: 30
   - **Important unread (24h):** `query: "is:important is:unread newer_than:1d"`, pageSize: 20
   - **Dropped balls (you last replied 3-14d ago):** `query: "from:me older_than:3d newer_than:14d"`, pageSize: 30

2. Merge results from queries 1 + 2. Deduplicate by thread ID. Keep 30 most recent if total exceeds 30.

3. For each thread in the merged list, call `mcp__claude_ai_Gmail__get_thread` with `messageFormat: FULL_CONTENT`. Extract:
   - sender name + sender email + sender domain
   - subject
   - first 200 chars of body
   - thread length
   - who sent the most recent message
   - first sender in thread (to detect "you sent first → reply from prospect" override)

### Part 2 — Pre-filter (suppress + blocklist)

4. For each email, check `references/noise-blocklist.md`:
   - **Self-suppress matches** → drop entirely. Don't include in counts or report.
   - **Domain blocklist matches** → force bucket = FYI, score = 0. Skip to Part 5.

### Part 3 — Categorize by content pattern

5. For each remaining email, walk through `references/content-patterns.md` in this order:
   - INBOUND patterns (1-5)
   - CLIENT patterns (1-5)
   - REVENUE patterns (1-5)
   - ADMIN patterns (1-5)
   - FYI patterns (1-6)
   - If none match → bucket = UNKNOWN

   First match wins. Record which pattern matched (used for action-item template).

6. Resolve sender aliases via `references/sender-aliases.md` before checking active-client / CRM lookup. (Same person across 2 emails should count once.)

### Part 4 — Score with rubric

7. Apply `references/email-rubric.md`:
   - **Special-case overrides FIRST.** If a content pattern matches a special override (inbound form = score 6, inbound booking = score 5, reply-to-outbound = min 3, time-bombed renewal = 3, SaaS-drip-pretending-to-be-human = 0, etc.) — apply it and skip the additive rubric.
   - Otherwise, sum the 5 signals (sender match + subject + time-sensitivity + thread state + priority bonus). Cap at 8.

8. **VIP check** — for each non-suppressed, non-blocklisted email:
   - Run a Gmail query: `from:<sender> newer_than:30d` (cache results across the run — don't re-query for the same sender).
   - Count distinct threads. If ≥ 3 AND domain is not bulk-mail (not `mail.*`, `email.*`, `notifications.*`, `noreply.*`) → apply +3 sender match (overrides "unknown sender" 0).

9. Assign badge from final score: 🔥 ≥ 6 / 🔴 4–5 / 🟡 2–3 / ⚪ 0–1.

### Part 5 — Detect dropped balls

10. From the dropped-balls query (Part 1, query 3): for each thread:
    - Read full thread.
    - Check: did anyone reply AFTER your most recent message?
    - If no → it's a dropped ball.
    - Skip if your last message contained closure language: "ttyl", "no rush", "fyi", "thanks!", "no need to reply".
    - For each true dropped ball, record: who, subject, days dormant, last action.

### Part 6 — Action items

11. For each email scoring ≥ 2 in INBOUND, CLIENT, or REVENUE buckets, write one action item using the template from the matched content pattern.
    - Format: "[Verb]: [topic] — from [Name]"
    - Keep under 15 words.
    - INBOUND form submissions get a parsed ICP mini-score appended: "ICP fit: HIGH/MEDIUM/LOW — [reason]"
    - Call recap CLIENT emails get one action item per commitment extracted from the body.

12. ⚪ emails (score 0–1) get no action item — informational only.

13. Add one action item per dropped ball: "Followup: [subject] — [Name] (X days dormant)"

### Part 7 — Build and save output

14. Sort each bucket internally by score descending.

15. Save to `inbox/outputs/md/YYYY-MM-DD-operations-email-report.md`. If a file for today already exists, append with a `### Check — HH:MM` header.

16. Print short summary inline (not the full report):
    - "Email report done: X INBOUND, X CLIENT (Y action), X REVENUE (Y action), X ADMIN, X FYI, X UNKNOWN, X dropped balls. Top score: [score] — [subject]."

17. If UNKNOWN section has entries, also print: "X emails couldn't be categorized — check the UNKNOWN section in the report and tell me what they are so I can add a rule to `references/content-patterns.md`."

---

## Output Format

```
# Email Report — YYYY-MM-DD HH:MM

> X total scanned. INBOUND X, CLIENT X, REVENUE X, ADMIN X, FYI X, UNKNOWN X. Dropped balls: X. Action items: Y.

---

## Priority rubric (recap)
- 🔥 ≥6 / 🔴 4–5 / 🟡 2–3 / ⚪ 0–1 / 🟠 Dropped ball (separate)
- Active client or VIP (3+ threads/30d): +3 / CRM prospect: +2 / Known company: +1
- Subject "proposal/invoice/blocked/urgent": +2 / "pricing/call/follow-up": +1
- Body "today/EOD/ASAP": +2 / "this week": +1
- You holding the ball: +2 / You last replied: -1
- Priority bonus: +1
- Special overrides (form = 6, booking = 5, reply-to-outbound = min 3, blocklist = 0)

---

## 🆕 INBOUND (X)
| Score | From | Subject | Pattern matched | Action |
|-------|------|---------|-----------------|--------|
| 🔥 6 | [Contact Name] | Free Audit Call | Tally form submission | Reply within 24h. ICP fit: HIGH — [reason] |
| 🔴 5 | [Contact Name] | New booking | Cal.com | Meeting booked: [Name] on YYYY-MM-DD — run meeting prep 24h before. |

---

## 👥 CLIENT (X)
| Score | From | Subject | Preview | Action |
|-------|------|---------|---------|--------|
| 🔥 7 | [Client Name] | Re: project update | "When can I expect..." | Reply: ETA update — from [Client] |

---

## 💰 REVENUE (X)
| Score | From | Subject | Preview | Action |
|-------|------|---------|---------|--------|
| 🔴 4 | [Prospect Name] | Re: proposal | "...may still need your help..." | Warm reply — review thread, draft response |

---

## 🟠 Dropped Balls (X)
| Days dormant | Who | Subject | Last action |
|--------------|-----|---------|-------------|
| 5 | [Name] | [Subject] | You sent proposal v1, no response |

---

## ⚙️ ADMIN (X)
| Score | From | Subject | Preview | Note |
|-------|------|---------|---------|------|
| 🟡 3 | Excalidraw | Subscription renews | "..." | Time-bombed: 3 days. Keep or cancel? |

---

## 📌 FYI (X)
| Score | From | Subject | Note |
|-------|------|---------|------|
| ⚪ 0 | Apollo | [Subject] | Blocklist |

---

## ❓ UNKNOWN (X) — review and tell me how to categorize
| From | Subject | Why unclassified |
|------|---------|------------------|
| [Sender] | [Subject] | Not in CRM, no known pattern matched |

---

## Action Items for Today (top-scored only)
- [ ] 🔥 Reply within 24h: [Name] submission (HIGH ICP fit)
- [ ] 🔴 Meeting booked: [Name] on [Date] — run meeting prep 24h before
- [ ] 🟠 Followup: [proposal subject] — [Name] (5 days dormant)
```

---

## Edge Cases

- **Inbox empty / no unread emails:** Output "Inbox clear — no unread emails in last 24h." Pass forward to daily plan.
- **Gmail API fails or times out:** Log "Gmail unavailable — email report skipped." Continue morning routine.
- **Notion query for active clients fails:** Skip the +3 sender bonus from active clients (VIP detection still works as fallback).
- **Can't read full email body:** Score sender + subject only. Time-sensitivity and thread state default to 0.
- **Reference file missing or empty:** Treat all emails as UNKNOWN (don't crash). Print "Reference file `[name]` is empty — fill it before next run."
- **More than 30 emails in 24h:** Process the 30 most recent. Note "X additional unread not scored — check inbox directly."
- **Two emails from the same thread:** Score both, but only generate one action item (use the most recent message).
- **UNKNOWN bucket has more than 5:** Show 5 most recent. Note "X more unclassified — review in inbox."
- **VIP query times out:** Skip VIP detection for that sender, fall back to standard scoring.
- **Form parsing fails:** Surface the email as INBOUND with action "Form received — couldn't parse fields, check inbox."

---

## What good looks like

A finished email report is a **decision aid**, not a copy of the inbox. After reading it, you know in <60 seconds:

1. Which 1-3 emails to reply to right now (🔥 / 🔴 in INBOUND, CLIENT, REVENUE).
2. Which meetings need prep this week (INBOUND bookings).
3. Which threads you've dropped the ball on (🟠).
4. Which subscriptions are about to auto-renew (ADMIN time-bombed).
5. Whether anything new appeared that the system doesn't recognize (UNKNOWN).

The UNKNOWN section is the feedback loop — every entry there is a chance to make the skill smarter for next run.
