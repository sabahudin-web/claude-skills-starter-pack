---
name: operations-meeting-prep
description: Researches a meeting attendee, builds a personalized 12-step sales script, and generates a value-driven pitch deck as PDF. Use this skill when the user says "prep for my meeting", "research [name]", "meeting prep", "get ready for my call with [name]", or provides a name after the morning routine asks about meetings. Triggered as optional last step in /morning after the user confirms a meeting.
---

# operations-meeting-prep

One job: walk into every sales call fully prepared. That means deep LinkedIn enrichment + 30-day web research on the person, a personalized 12-step sales script, and a value-driven pitch deck tailored to that specific person — all stored in Notion under "Meeting Prep Report & Sales Script".

**Automation level:** AUTONOMOUS — runs end-to-end without pausing. When inputs come from a calendar booking (via `/morning`), the LinkedIn URL and meeting time are auto-extracted. Offer fit is auto-picked using the scoring rubric below, with ambiguity flagged in the output rather than gated on user confirmation.

**Routine position:** /morning step 7. Auto-runs once per Discovery Call booked for today. Also runs standalone when called directly with a name + LinkedIn URL.

---

## Setup Required

Replace these placeholders before running:

| Placeholder | What to replace it with |
|-------------|------------------------|
| `YOUR_MEETING_PREP_NOTION_DB_ID` | Your "Meeting Prep" Notion database ID |
| `[YOUR_PROJECT_PATH]` | Your local project root path (e.g. `/Users/yourname/Documents/my-claude-os`) |

---

## Context to read before running

1. Read `context/offers.md` — know all your offers, their ideal clients, pricing, and positioning angles.
2. Read `context/icp.md` — know the ICP profile so you can spot fit or misfit quickly.
3. Read `references/sales-script-template.md` — the 12-step framework you'll personalize.

---

## Steps

### Part 1 — Get the person's name, LinkedIn URL, and conversation history

**Routine mode (called by /morning step 7):** Inputs are pre-extracted from a calendar booking. The orchestrator passes:
- `name` (attendee full name)
- `linkedin_url` (from the booking form's LinkedIn URL field)
- `scheduled_time` (today's call time)
- `dm_conversation` (full DM history with this lead, if available via your LinkedIn outreach tool)

If `dm_conversation` is non-empty, treat it as primary context — the lead's own words from DMs are the strongest signal for "why did they book the call".

**Standalone mode (user calls skill directly):**

1. Take the name (and LinkedIn URL if provided) from the user.
   - If no name: ask "Who are you meeting with? Give me their name — and their LinkedIn URL if you have it."
   - If LinkedIn URL is provided: skip Part 2, go straight to Part 3.

### Part 2 — Find their LinkedIn profile (only if no URL given)

2. Try Playwright first:
   - Tool: `mcp__playwright__browser_navigate`
   - URL: `https://www.linkedin.com/search/results/people/?keywords=[FirstName LastName]`
   - Tool: `mcp__playwright__browser_snapshot`
   - Extract the most likely profile URL by name match.

3. If Playwright fails: use Relay as fallback:
   - Tool: `mcp__claude_ai_Relay_APP_Claude_Code__search_linkedin_for_profile`
   - firstName, lastName, company (if known)
   - Extract the profile URL from the result.

4. If no profile found: note "LinkedIn profile not found — enrichment limited" and continue with name-only context.

### Part 3 — Enrich the person (LinkedIn enrichment tool)

5. Get their full LinkedIn profile using your LinkedIn enrichment tool (e.g. Trigify CLI: `trigify profile enrich --profile-url <linkedin_url>`).
   - Extract: current role, company, headline, about/summary, experience, education, certifications.
   - If this returns empty or errors: note the failure and continue with whatever partial data is available.

6. Get their company profile:
   - Extract from the enrichment output above. If company fields are missing: note "Company profile unavailable" and continue.

7. Get their recent LinkedIn posts:
   - Use your enrichment tool (e.g. `trigify profile posts --profile-url <linkedin_url> --page 0`)
   - Get last 3–5 posts. Extract: topics, themes, language used, pain points mentioned.
   - If this returns empty: note "No posts available" and continue.

### Part 4 — 30-day research (web search)

8. Run targeted web searches to find anything notable about this person or their company in the last 30 days:
   - Tool: `WebSearch`
   - Searches to run:
     - `"[Full Name]" podcast OR interview OR keynote 2026`
     - `"[Company Name]" funding OR acquisition OR launch OR news 2026`
     - `"[Full Name]" site:linkedin.com`
     - `"[Company Name]" [industry keyword] 2026`
   - Extract: podcast appearances, published articles, funding rounds, product launches, company news.
   - If nothing found in last 30 days: note "No recent news found" and skip this section in the brief.

### Part 5 — Build the research brief

9. Read `context/offers.md` and identify which 1–2 offers fit this person best based on their role, company size, industry, and pain signals.

10. Write the **Research Brief** (concise — short bullets, no paragraphs):
    - **Who they are:** Role at Company — 1–2 lines max
    - **Company:** What it does, size, industry — 1 line
    - **Right now:** What they're focused on (from posts/activity/news) — 1–2 bullets max, skip if no data
    - **Recent signal:** Anything notable from the last 30 days — 1 bullet, skip if nothing found
    - **Pain signal:** Visible problem or frustration based on profile + company context — 1 line
    - **Best offer fit:** Offer name + one-sentence reasoning
    - **Call type flag:** e.g., "Employee, not a founder — confirm budget authority early" or "Warm inbound — likely already sold"

### Part 6 — Build the personalized sales script

11. Run a silent **profile analysis** before writing. Think through:
    - Most relevant aspects of their background (industry, title, experience, seniority)
    - Specific signals from LinkedIn + research that can inform the script
    - **Conversation analysis (if present):** What resonated in DMs? What problem did they articulate? Why did they accept the call?
    - Likely pain points based on their role and industry
    - Which offer maps most naturally and why
    - Likely objections (price, timing, DIY)

12. Generate the **Personalized Sales Script** following the 12-step framework from `references/sales-script-template.md`:

    - **Step 1 (Preparation):** 3–5 specific prep items drawn from their profile and research.
    - **Step 2 (Micro Rapport):** 2 rapport questions drawn from their background or career path. Never reference LinkedIn directly — use the insight, not the source.
    - **Step 3 (Agenda & Alpha Frame):** Copy from template — no personalization needed.
    - **Step 4 (Primary Motive):** 2–3 pain-discovery questions tailored to their specific role and situation.
    - **Steps 5–6 (Discovery + Pain):** Adapt questions to their business type, team structure, acquisition/growth context.
    - **Steps 7–9 (Goal, Defeat, Conviction):** Copy from template — no personalization needed.
    - **Steps 10–11 (Pitch):** Name the offer to lead with. Write a 1-sentence positioning line using their own language and context.
    - **Step 12 (Pricing):** State full price, offer same-day decision bonus, stay silent. If they say "too expensive": *"Sorry that my price exceeds your value."* — then stay silent.

### Part 7 — Generate the pitch deck

13. Auto-pick the best-fit offer using a scoring rubric. Score every offer in `context/offers.md` against the lead on:
    - **Role fit** (0–3): how well the prospect's title matches the offer's ICP role
    - **Company fit** (0–3): company stage/size fit relative to offer's target
    - **Pain signal match** (0–3): explicit pain in their posts/profile/recent news that the offer solves
    - **Budget fit** (0–2): seniority + company stage suggest they can afford this offer
    - **Recent intent signal** (0–2): bookings, podcasts, posts hinting at the offer's space
    - Total possible = 13 per offer. Highest score wins.

    **Ambiguity rule:** if the top two offers are within 1 point of each other, pick the highest-scoring one and add a banner:
    > ⚠ Offer fit ambiguous between **[Top Offer]** and **[Second Offer]** (scores X vs Y). Glance before the call and override the deck if the second one feels closer.

14. Run `offer-build-pitch-deck` with these inputs:
    - Person: full name, role, company
    - Enriched profile summary (from Part 3)
    - Research brief (from Part 5)
    - Sales script (from Part 6)
    - Confirmed offer (name, pricing, deliverables from `context/offers.md`)
    - Deck requirements:
      - 8–15 pages max
      - Value and outcome driven — sell what they GET and HOW they achieve it with you, not features
      - Personalized with their name and company context throughout
      - Structure: Problem they have → Cost of not fixing it → The outcome they want → How we get there together → Offer details → Pricing → Next step
    - Save pitch deck to: `inbox/outputs/pdf/YYYY-MM-DD-operations-meeting-prep-[firstname-lastname].pdf`

    > **Note:** `offer-build-pitch-deck` is included in this starter pack under `skills/offer-build-pitch-deck/`. Install and configure it first.

15. **Pitch Deck files:** After the PDF is generated, note both outputs:
    - PDF path: `inbox/outputs/pdf/YYYY-MM-DD-operations-meeting-prep-[firstname-lastname].pdf`
    - HTML URL: `file:///[YOUR_PROJECT_PATH]/inbox/outputs/html/YYYY-MM-DD-operations-meeting-prep-[firstname-lastname].html`

### Part 8 — Save and push to Notion

16. Save the full output to:
    `inbox/outputs/md/YYYY-MM-DD-operations-meeting-prep-[firstname-lastname].md`

    Contents:
    - Research brief
    - Full personalized sales script
    - Reference to pitch deck PDF path

17. Push to the **Meeting Prep Report & Sales Script** database:
    - Tool: `mcp__claude_ai_Notion__notion-create-pages`
    - parent: `{"type": "data_source_id", "data_source_id": "YOUR_MEETING_PREP_NOTION_DB_ID"}`
    - Properties:
      - `Day & Date`: `YYYY-MM-DD — [First Last] call`
      - `date:Date:start`: today's date in YYYY-MM-DD format
      - `Research Report`: the concise research brief text
      - `Pitch Deck`: `file:///[YOUR_PROJECT_PATH]/inbox/outputs/html/YYYY-MM-DD-operations-meeting-prep-[firstname-lastname].html`
    - Page body content: the full personalized 12-step sales script

18. Print one-line summary: "Meeting prep ready for [Name]. Research brief + sales script + pitch deck saved to inbox and Notion."

---

## Output Format

```markdown
# Meeting Prep — [First Last] — YYYY-MM-DD

> ⚠️ [Call type flag — e.g., "Employee, not a founder — confirm budget authority early"]

---

## Research Brief

- **Who they are:** [Role at Company — 1–2 lines]
- **Company:** [What it does, size, industry]
- **Right now:** [What they're focused on — skip if no data]
- **Recent signal:** [Podcast/funding/news from last 30 days — skip if none]
- **Pain signal:** [Visible problem or gap]
- **Best offer fit:** [Offer name] — [1-sentence why]

---

## Personalized Sales Script

### Step 1: Preparation
...

### Step 12: Pricing
...

---

## Pitch Deck
PDF: `inbox/outputs/pdf/YYYY-MM-DD-operations-meeting-prep-[firstname-lastname].pdf`
HTML (interactive): [Open deck](file:///[YOUR_PROJECT_PATH]/inbox/outputs/html/YYYY-MM-DD-operations-meeting-prep-[firstname-lastname].html)
```

---

## Edge Cases

- **LinkedIn URL provided directly:** Skip Part 2 — go straight to enrichment.
- **Enrichment returns empty profile:** Use whatever partial data is available. Still generate the full script with role/company-informed questions. Note "Enrichment partial" at top.
- **No recent posts:** Skip "right now" bullet in brief.
- **No recent news found (WebSearch):** Skip "recent signal" bullet.
- **Offer fit ambiguous (top two within 1 point):** Pick the highest-scoring offer, generate the deck for it, AND add the ambiguity banner. Never pause.
- **Internal meeting (team call, known client check-in):** Output "Internal meeting — no prep needed." Skip all enrichment.
- **offer-build-pitch-deck skill not available:** Note the failure, save the research brief + script only.
- **Notion push fails:** Save to `inbox/outputs/` only. Tell user: "Notion push failed — output saved locally."
