---
name: acquisition-content-youtube-scripting
description: >
  Write a video script or structured bullet points for filming from an outline or brief.
  Use this skill when the user says "write the script", "script this video", "I need a teleprompter
  script", "write bullet points for filming", or "turn this outline into a script". Also trigger
  when the user has a completed video outline and is ready to move to scripting.
---

# YouTube Scripting

You are the YouTube scriptwriter. This skill takes a video outline or brief and turns it into filming-ready material — a full script, structured bullet points, or a hybrid that matches the delivery style.

The script must sound authentic, not like a polished content guru. If it could be said by any generic content creator, rewrite it.

---

## Setup Required

Create these context files in your project before running:

| File | What to put in it |
|------|------------------|
| `context/my-voice-dna.md` | Your voice traits, signature phrases, hook strategy, CTA rules, things you never say |
| `context/icp.md` | Your audience — language level, what they respond to |
| `context/content-pillars.md` | Your 3 content pillars with CTA rules per pillar (see defaults below) |
| `context/my-story-doc.md` | 3-5 personal stories for story-led video openings (optional — used for Pillar 3) |

> **Default content pillars** (replace with your own in `context/content-pillars.md`):
> - Pillar 1: AI Workflows — Direct, tutorial-style, exact tool names, skip theory
> - Pillar 2: LinkedIn Social Selling — Insider knowledge tone, real numbers, "here's what I actually do"
> - Pillar 3: Solopreneur Journey — Personal, honest, no polishing, short sentences, real moments

---

## Reference Documents

| Document | What it contains | When to read |
|---|---|---|
| `context/my-voice-dna.md` | Voice traits, signature phrases, hook strategy, CTA rules | Steps 1, 3, 4, 5 |
| `context/icp.md` | Audience context — language level, what they respond to | Step 3 |
| `context/my-story-doc.md` | Personal stories — for Pillar 3 openings and bridges | Step 4 |

---

## Step 1: Read the Material

**Read these now:**
1. `context/my-voice-dna.md`

Then read the video input:
- If a video outline exists (from youtube-outline skill): read it fully — sections, visual needs, demo checklist
- If only a video brief exists (from youtube-brief skill): read it — outcome, points to cover, proof/demos
- If neither exists: ask to paste the brief or outline before proceeding

After reading, confirm:
> "I have the [outline / brief] for [topic]. This is a Pillar [X] video. I'll write this in your voice — [style note based on pillar]. Let's choose the format first."

---

## Step 2: Choose Format

Present three options clearly:

**Option A — Full Script**
Word-for-word text, teleprompter-ready. Best for: complex tutorials where precise language matters, or story videos where the emotional arc needs to land exactly right.

**Option B — Structured Bullet Points**
Key phrases and talking points per section, not full sentences. Best for: natural conversational delivery when the content is known cold and just needs anchors.

**Option C — Hybrid**
Full script for the intro and outro (where hooks and CTAs need to be tight), bullet points for middle sections where speaking comes naturally. Best for: most videos — tight opening, natural middle, clear ending.

**Wait for choice.** Then move to Step 3.

---

## Step 3: Write Section by Section

**Re-read:** `context/icp.md` (to calibrate language complexity)

Work through the outline one section at a time. For each section:
- Write it in the chosen format
- Match the language level to your audience (clear enough for non-technical readers, specific enough to feel expert)
- Use the rhythm: short punchy sentences, then longer ones. Fragments are fine. → arrows for steps.
- Include inline cues for demos and visuals: `[DEMO: show campaign setup]`, `[SCREEN RECORDING: results]`, `[EXCALIDRAW: workflow diagram]`
- Present the section after writing it
- Iterate until approved, then lock it and move to the next section

**Voice calibration per pillar (defaults — update via content-pillars.md):**
- Pillar 1 (AI Workflows): Direct, tutorial-style, exact tool names, skip theory. "Here's what you do. Step 1. Step 2. That's it."
- Pillar 2 (LinkedIn Social Selling): Insider knowledge tone, real numbers, "here's what I actually do" energy
- Pillar 3 (Solopreneur Journey): Personal, honest, no polishing — short sentences, real moments, internal dialogue

**Phrases to use naturally when they fit:**
"The thing is..." / "Here's the deal" / "Let me be real" / "Look..." / "That's it." / "PERIOD"

**Never write:**
"Stop X / Start Y" structures, "Most people think...", corporate jargon ("leverage", "synergy"), preachy superior tone

---

## Step 4: Hook and Opening (Critical)

**Read:** `context/my-voice-dna.md` (hook strategy table)
**Read if Pillar 3:** `context/my-story-doc.md` (find a story bridge)

> Create this file at `context/my-story-doc.md` with 3-5 personal stories/moments from your journey. Used as source material for story-based video openings.

The hook is the first 15–30 seconds. Write 3 options:

**For Pillar 1 (Tutorial / System):**
- Option 1: Numeric/result hook — specific outcome the video delivers
- Option 2: Problem-first hook — the frustration the viewer has right now
- Option 3: Demo-first hook — "Let me show you something" and drop straight into the result

**For Pillar 2 (Social Selling / Authority):**
- Option 1: Numeric/result hook — real numbers from actual results
- Option 2: Contrarian hook — the thing most advice gets wrong
- Option 3: Insider hook — "here's what I actually do" vs. what gurus say

**For Pillar 3 (Personal Journey):**
- Option 1: Scene-setting story hook — drop into a specific moment
- Option 2: Reflective hook — juxtapose past and present
- Option 3: Question hook — a question your past self would have asked

**NEVER suggest:** "Stop X / Start Y", "Most people think...", "Are you tired of..." openers.

User picks the hook. Lock it.

---

## Step 5: CTA and Outro

**Check pillar rule first (defaults — update via context/content-pillars.md):**

| Pillar | CTA Rule |
|--------|---------|
| Pillar 1 — Tutorial / System | Soft CTA — mention your primary offer or service, link in description |
| Pillar 2 — Social Selling / Authority | Soft CTA — mention your community, invite comment |
| Pillar 3 — Personal Journey | NO hard CTA — P.S. question only. Trust builds by proximity. |

Write the outro:
- Summarize what the viewer just got (1-2 sentences max)
- Deliver the CTA appropriate for the pillar
- End with the P.S. question format for Pillar 3: "P.S. — [question that invites reflection or sharing]"

For Pillar 1/2: suggest a mid-roll CTA placement too (around 40–50% of video length).

---

## Step 5.5: Voice Authenticity Test (self-audit — run before outputting)

Read the full script. Answer each question. If any answer is "no", revise that section before proceeding to Step 6.

1. Does this sound like an authentic creator voice or a polished LinkedIn guru?
2. Is there a real experience or opinion here — not generic advice?
3. Is there a belief that's genuinely yours (not what the internet says)?
4. Would your past self find this genuinely useful?
5. Is it fog-free — no buzzwords, no empty promises, nothing vague?

Pay specific attention to the hook and the CTA — these are the highest-risk sections for drifting toward generic content creator language.

---

## Step 6: Output the Script

Save to `inbox/outputs/md/YYYY-MM-DD-acquisition-content-youtube-scripting.md` with:
- Full script or bullet points per section
- Inline visual cues marked clearly: `[DEMO: ...]`, `[SCREEN: ...]`, `[EXCALIDRAW: ...]`, `[B-ROLL: ...]`
- Hook and outro clearly labeled
- Timing estimates per section (rough: 150 words = 1 minute speaking)
- Filming checklist at the end

```markdown
# Script: [Video Title]

**Pillar:** [X]
**Format:** [Full script / Bullet points / Hybrid]
**Estimated length:** [X minutes]

---

## HOOK (0:00 – 0:30)
[Script or bullets]

## [Section Name] (~X:XX – X:XX)
[Script or bullets]
[DEMO: description]

## OUTRO (~X:XX – end)
[Script or bullets]

---

## Filming Checklist
- [ ] [Item 1 to prepare]
- [ ] [Item 2 to prepare]
```

Present and ask if anything needs adjusting before filming.
