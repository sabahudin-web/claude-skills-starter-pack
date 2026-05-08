---
name: operations-check-recent-calls
description: Reads the Notion Transcripts & Recordings DB for coaching/sales/nurturing calls in the last 72 hours, parses each transcript for commitments and next steps, auto-creates high-confidence Client Deliverables rows, and flags low-confidence candidates in the briefing. Use this skill when the user says "check recent calls", "what did I commit on calls yesterday", "any new tasks from coaching calls". Also trigger at position #4 in the /morning routine.
---

# operations-check-recent-calls

One job: scan ALL call transcripts from the last 3 days (every call type — coaching, sales, nurturing, collaboration, friendly) and capture every commitment / next step / missing task into Client Deliverables — automatically.

Without this skill, you would have to manually remember "I said I'd send the workflow diagram by Wednesday" and translate it into a task row. With this skill, /morning captures that automatically across all call types — high-confidence commitments are auto-created, ambiguous ones are flagged in the briefing for you to glance at.

**Automation level:** AUTONOMOUS — auto-creates high-confidence rows. Surfaces low-confidence candidates in the briefing as "⚠ Possible commitment — not auto-created" so you can manually create if needed. All auto-created rows tagged `Source = "Auto from transcript {date}"` for easy audit/cleanup.

**Routine position:** /morning step #4. Runs after operations-check-tasks (step #3) so dedup can compare against existing rows and skip duplicates.

---

## Setup Required

Replace these placeholders in the Constants table below with your actual Notion database IDs before running:

| Placeholder | How to find your ID |
|-------------|-------------------|
| `YOUR_TRANSCRIPTS_RECORDINGS_NOTION_DB_ID` | Open the database in Notion → copy the URL → the UUID after the last `/` |
| `YOUR_CLIENT_DELIVERABLES_NOTION_DB_ID` | Same method for your Client Deliverables database |
| `YOUR_PEOPLE_CRM_NOTION_DB_ID` | Same method for your People/CRM database |
| `YOUR_DEALS_NOTION_DB_ID` | Same method for your Deals database (optional — used for gap-fill window) |

---

## Constants

| Thing | ID / URL |
|-------|----------|
| Transcripts & Recordings data source | `collection://YOUR_TRANSCRIPTS_RECORDINGS_NOTION_DB_ID` |
| Client Deliverables data source | `collection://YOUR_CLIENT_DELIVERABLES_NOTION_DB_ID` |
| People (CRM) data source | `collection://YOUR_PEOPLE_CRM_NOTION_DB_ID` |
| Deals (CRM) data source | `collection://YOUR_DEALS_NOTION_DB_ID` |
| Default lookback window | 3 days (72 hours — covers daily runs and Mon–Fri schedule) |
| Gap-fill lookback window | 7 days, applied to clients with an active deal in the Deals DB (catches missed days for paying clients specifically) |
| Eligible Call Purposes | ALL call types — Coaching Call, Sales Call, Nurturing Call, Collaboration Call, Friendly Call. Every call can produce commitments. |
| "Active deal" filter | Any Deals row whose Status is NOT one of: `Won`, `Lost`, `Closed`, `Cancelled`, `Archived`. If the actual Deals schema uses different terminal status names, treat any non-terminal Status as active. |

---

## Steps

### Part 1 — Pull recent eligible call transcripts (72h default, 7d gap-fill for active-deal clients)

1. **Identify active-deal clients first** (this controls the window per client):
   - Tool: `mcp__claude_ai_Notion__notion-search`
   - data_source_url: `collection://YOUR_DEALS_NOTION_DB_ID` (Deals)
   - query: `"a"` (stub)
   - page_size: 50
   - For each Deals row, call `notion-fetch` if needed to read Status. Keep rows whose Status is NOT terminal (per Constants). For each active deal, capture the linked People row(s) (Client relation) → build a set `active_client_ids`.
   - If Deals DB unreachable: log "Deals DB unavailable — gap-fill disabled, falling back to 72h window for all clients" and continue.

2. **Pull recent transcripts:**
   - Tool: `mcp__claude_ai_Notion__notion-search`
   - data_source_url: `collection://YOUR_TRANSCRIPTS_RECORDINGS_NOTION_DB_ID`
   - query: `"a"` (stub — `notion-search` requires query length ≥1)
   - page_size: 25

3. For each returned row, call `notion-fetch` to get the full properties + the call body. Apply per-client window:
   - If the call's Client relation is in `active_client_ids` → keep if Call Date is within last **7 days** (gap-fill window).
   - Otherwise → keep if Call Date is within last **3 days** (default 72h window).
   - Include ALL call types: Coaching, Sales, Nurturing, Collaboration, Friendly. Every call type can surface commitments.

4. If no rows match either window, output "No calls in the last 3-7 days — nothing to surface." and stop.

### Part 2 — Resolve client identity

4. For each kept call, identify the client:
   - **Preferred:** Read the `Client` relation property. If set → fetch the People page → extract Name. Done.
   - **Fallback if Client relation is empty:** Parse the Call Name title for a known client name. Compare against the active People DB pages. If unique match → tentatively assign that client + flag "Client relation missing on this transcript — please add in Notion."
   - **Last resort:** If no client can be inferred → skip the call with a note "Could not resolve client for [Call Name]. Add Client relation in Notion to surface commitments next time."

### Part 3 — Read and parse the transcript for commitments

5. For each kept call with a resolved client, read the transcript in two passes:

   **Pass 1 — Key takeaways / summary section (fast):** Most transcription tools include a structured "Key Takeaways", "Action Items", or "Summary" section near the top of the page body. Read that section first. If it contains clear commitments and action items, that's enough — don't read the full transcript.

   **Pass 2 — Full transcript (only if needed):** If the key takeaways section is missing, empty, or unclear, read the full transcript body. Scan for commitment patterns:
   - "I'll [verb] [object] by [date]" — e.g. "I'll send you the workflow diagram by Wednesday."
   - "Next step is [thing]" / "Next steps:"
   - "Action items:" lists
   - "you will [verb]" / "[Name] will [verb]"
   - "We agreed [thing]"
   - Date-bearing phrases: "by Friday", "next week", "before our next session"
   - Any task, deliverable, or follow-up mentioned — even from collaboration or friendly calls

6. Extract each commitment as a candidate row, AND assign a confidence score:
   - **Task:** the verb + object phrase, normalized to a 5-10 word task title.
   - **Client:** from step 4.
   - **Offer:** infer from the People page Status (if Client) and the call's context.
   - **Phase:** infer from the most recent in-progress Phase in their existing Client Deliverables rows.
   - **Due Date:** parse the date phrase. "by Wednesday" → next Wednesday. "next week" → 7 days out. "by EOD" → today. If no date → leave empty.
   - **Priority:** "must / urgent / blocker" in surrounding context → High. "would be great / nice to have" → Low. Default → Medium.
   - **Source:** `Auto from transcript {YYYY-MM-DD}` — date is the call date. This tag is how you find and bulk-delete any bad auto-creates in Notion.
   - **Notes:** quote the exact transcript phrase that triggered the extraction so you can verify in one glance.

   **Confidence score (HIGH vs LOW):**
   - **HIGH** = explicit commitment with named owner + clear action + parseable date.
     Examples: "I'll send you the workflow diagram by Wednesday", "Action item: prepare the v2 proposal by Friday".
   - **LOW** = implicit, vague, no owner, no date, or topic-as-action.
     Examples: "let's discuss pricing", "we should look into integrations", "next steps include considering Apollo".

   Only HIGH-confidence candidates get auto-created in Part 5. LOW-confidence candidates are surfaced in the briefing as flagged items, not created.

### Part 4 — Dedupe against existing Client Deliverables

7. For each candidate row, query Client Deliverables for any existing row with the same Client AND a similar Task title (use case-insensitive substring match).

8. Skip candidates that already exist as a not-Done row in Client Deliverables. Note in the output: "Already tracked: [task] for [client]."

### Part 5 — Auto-create high-confidence rows; flag low-confidence

9. **For every HIGH-confidence candidate** (from step 6), create the row immediately in Client Deliverables:
   - Tool: `mcp__claude_ai_Notion__notion-create-pages`
   - parent: `{"type": "data_source_id", "data_source_id": "YOUR_CLIENT_DELIVERABLES_NOTION_DB_ID"}`
   - Properties: Task, Client (relation), Offer, Phase, Status = "Not started", date:Due Date:start, Priority, Source = `Auto from transcript {YYYY-MM-DD}`, Notes = quote.
   - If the create fails (Notion error), record the failed row to `inbox/outputs/md/YYYY-MM-DD-operations-check-recent-calls-pending.md` so it can be retried — don't lose the candidate.

10. **For every LOW-confidence candidate**, do NOT create. Add to a "Possible commitments — flagged for review" section in the output. You can manually create in Notion if any are real.

### Part 6 — Build the output

11. Render output:

```markdown
## Calls processed (X)

### Coaching Call — [Client Name] — YYYY-MM-DD
**Call:** [Call Name] | [Call Link]

**✅ Auto-created in Client Deliverables (2):**
1. **Send workflow diagram** — Due YYYY-MM-DD — Priority: High
   _Quote: "I'll send you the v2 workflow diagram by Wednesday so you can review before Session 4."_
   _Notion row: [link]_
2. **Set up outbound campaign** — Due YYYY-MM-DD — Priority: Medium
   _Quote: "Next step is getting Apollo wired up so the team can start campaigns."_
   _Notion row: [link]_

**⚠ Possible commitments — flagged, NOT auto-created (1):**
- "Look into team training options for Q3" — vague, no date, no clear owner.

**⏭ Already tracked (1):**
- "Schedule Session 4" — existing row in Client Deliverables.
```

12. Save the report to `inbox/outputs/md/YYYY-MM-DD-operations-check-recent-calls.md` using today's date.

13. Print a short summary inline:
    - "Recent calls scanned: X eligible. Auto-created: Y rows. Flagged for review: Z. All auto-created rows tagged Source=`Auto from transcript {date}` for cleanup."

---

## Edge Cases

- **Transcripts & Recordings DB unreachable:** Log "Transcripts DB unavailable — skipping recent calls scan." Continue /morning.
- **No calls in 3-day window:** Output "No calls in the last 3 days — nothing to surface."
- **Call body is empty / transcript missing:** Skip the call. Note "Transcript missing for [Call Name] — propose nothing."
- **Call has no Client relation AND name doesn't match any active client:** Skip with the message in step 4. Don't guess.
- **Commitment phrase is ambiguous:** Don't propose it. Only extract concrete commitments with verbs + objects.
- **Duplicate detected across multiple calls in the same window:** Propose once, with a note "Mentioned in calls A + B."
- **Auto-created row turns out to be wrong:** Filter Client Deliverables by `Source contains "Auto from transcript"` and bulk-delete. The Source tag makes the cleanup pass trivial.
- **`notion-create-pages` fails on a candidate:** Save that candidate to `inbox/outputs/md/YYYY-MM-DD-operations-check-recent-calls-pending.md` so it can be retried manually.

---

## Why this design (the why behind autonomous + confidence threshold)

The whole point of going AUTONOMOUS is that the routine runs at a scheduled time whether you're at your desk or not. Asking for approval on every commitment defeats that — you'd arrive to a backlog of pending approvals.

The confidence threshold exists to prevent Notion bloat:

1. **Transcript noise stays out of tasks.** Tools like Fathom over-extract — they'll mark "let's discuss pricing" as an action item when it's just a topic. The HIGH/LOW threshold catches those.

2. **Phantom obligations are recoverable.** If a transcript says "[Name] will send the deck" but it was already sent, the row gets auto-created — but it's tagged `Source = Auto from transcript {date}`. Filter by that source and bulk-delete any phantom rows. One filter, one click, gone.
