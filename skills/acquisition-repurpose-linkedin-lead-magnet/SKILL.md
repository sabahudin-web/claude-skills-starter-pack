---
name: acquisition-repurpose-linkedin-lead-magnet
description: >
  Write a LinkedIn lead magnet post that gives away a real system, template, or resource using
  your generous-but-not-desperate style. Use this skill when the user says "write a lead
  magnet post", "I want to give away a resource", "free templates post", "LinkedIn giveaway post",
  or "promote my resource on LinkedIn". Also trigger when the /content routine reaches the lead magnet step.
---

# LinkedIn Lead Magnet Post

Write a LinkedIn post that gives away a real resource — system, template, checklist, or framework — using your signature move: result first, self-aware CTA, never desperate.

**Engagement range:** 0.6x - 0.8x reactions (lower than stories, but drives real conversion)
**Dial settings:** Emotion 4-6 / Humor 4-6 / Technical 3-6

---

## Setup Required

Create these context files in your project before running:

| File | What to put in it |
|------|------------------|
| `context/my-voice-dna.md` | Your voice rules — phrases you use, phrases you never use, tone guidelines |
| `context/content-pillars.md` | Your content pillars for post categorization |

---

## Step 1: Read Reference Files

Read before writing:
- `context/my-voice-dna.md` — voice rules
- `references/linkedin-content-universe.md` (skill-local) — lead magnet DNA and the Lead Magnet Giveaway structure

> **First time setup:** The `references/linkedin-content-universe.md` file in this repo is a template. Fill in the [BRACKET] sections with your own brand DNA — your personal characters, story arc, origin, community, and any engagement data you have. The more you fill in, the better the posts will match your authentic voice.

---

## Step 2: Get the Resource

If not already in context, ask:
> "What are you giving away? Describe it in one sentence — what it is, what problem it solves, and what result it produces."

Also ask:
> "Is the link ready, or should I write it with a 'comment to get it' CTA?"

---

## Step 3: Find the Personal Context

The lead magnet post must have personal context — why YOU built this, what problem it solved for YOU specifically. Without this it becomes generic giveaway content.

Ask if not clear from source:
> "What's the quick backstory? Did you build this because you had a specific problem, hit a specific result with it, or saw others struggling without it?"

One sentence is enough. Never write the post without a personal hook.

---

## Step 4: Write the Post

Apply the Lead Magnet Giveaway structure:

1. **HOOK** — Specific result + what you're giving away. Lead with the outcome, not the resource name.
   - Good: "I hit 1M impressions using these 40 templates."
   - Bad: "I created some templates I want to share."

2. **PROOF** — What this helped you (or clients) achieve. One specific number or outcome.

3. **BREAKDOWN** — What's inside. Bulleted, specific. Each bullet = one concrete thing.

4. **USE CASES** — Who it's for and how to apply it. 2-3 specific scenarios.

5. **CTA** — Two options:

   **Option A (direct link available):**
   Break the pattern with self-awareness:
   > "Comment Templ... I'm kidding, the link is below."
   Then drop the link.

   **Option B (no link yet):**
   > "DM me '[keyword]' and I'll send it over."
   Keep it simple, no hoop-jumping.

6. **P.S.** — Related question or self-aware joke. Not another CTA.

---

## Step 5: Voice Check

**Non-negotiable rules:**
- No em dashes (—)
- No "This will change your life" or any overpromise
- No vague descriptions ("amazing resources", "incredible templates")
- No dark energy ("you're leaving money on the table")
- Generous but not desperate — you're sharing, not begging
- Self-aware CTA breaks the "comment X for Y" LinkedIn trope
- Short sentences throughout
- P.S. at the end, always

**Forbidden words:** game-changer, unlock, leverage, optimize, transform, next level, revolutionary, paradigm

**Voice Authenticity Test (self-audit — answer before saving):**

Run these yourself. If any answer is "no", revise before proceeding.

1. Does this sound like you or a polished LinkedIn guru?
2. Is there a real experience or opinion here — not generic advice?
3. Is there a belief that's genuinely yours (not what the internet says)?
4. Would your past self find this genuinely useful?
5. Is it fog-free — no buzzwords, no empty promises, nothing vague?

---

## Step 6: Save Output

Save to `inbox/outputs/md/YYYY-MM-DD-acquisition-repurpose-linkedin-lead-magnet.md`

Include at the top:
```
Post type: Lead Magnet
Resource: [what's being given away]
Pillar: [which content pillar]
CTA type: Direct link / DM request
Dial: Emotion [X] / Humor [X] / Technical [X]
```

---

## Step 7: Push to LinkedIn Content Dashboard (optional)

If you have a Notion LinkedIn content database:

1. Call `mcp__claude_ai_Notion__notion-search` with query "[YOUR_LINKEDIN_CONTENT_DATABASE]" to find the database ID.
2. Call `mcp__claude_ai_Notion__notion-create-pages` to create the record:
   - **Post title:** First line (hook) of the post — keep under 100 characters
   - **Notes:** Topic context — 1-sentence description of the post topic
   - **Post status:** "Draft"
   - **Content pillar:** Match the closest pillar from `context/content-pillars.md`
   - **Draft:** Full text of the LinkedIn post
   - **Post format:** "Lead Magnet"
3. Confirm: "Pushed to LinkedIn Content Dashboard."

Skip this step if you don't use Notion for content tracking.

---

## Edge Cases

| Situation | Action |
|-----------|--------|
| No personal context for the resource | Ask for the backstory before writing — do not invent one |
| Resource is generic (not your own) | Frame it as "I curated this because..." — still needs personal context |
| No result/proof available yet | Use the problem it solves instead: "I built this because I kept running into [problem]" |
| User wants carousel format for the breakdown | Output the caption here, then note that a carousel skill can handle the slides separately |
