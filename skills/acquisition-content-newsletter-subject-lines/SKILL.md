---
name: acquisition-content-newsletter-subject-lines
description: >
  Generate 8-10 high-converting newsletter subject lines from a newsletter draft, using 100 battle-tested
  direct-response frameworks. Auto-reads today's newsletter when running inside a /content routine (Step 11a),
  picks 3-5 framework categories matching the edition intent, generates options, scores each, recommends
  the strongest pick with 2 A/B variants, and updates the Notion newsletter page Subject Line field.
  Use this skill when the user says "write subject lines", "I need email subjects", "generate subject lines",
  "subject line options", "A/B test subject lines", or "improve my email subject". Also trigger automatically
  as the final step of the /content routine after the newsletter draft is complete.
---

# Newsletter Subject Lines

Generate scored subject line options that get opens — not 5 random guesses. Every line is built from a real, named framework with a proven pattern.

**Automation level:** AUTONOMOUS (subject lines are low-risk; user picks the final one from the scored list)

---

## Setup Required

| Placeholder | What to replace it with |
|-------------|------------------------|
| `[YOUR_NEWSLETTER_DATABASE_NAME]` | The exact name of your Notion newsletter database (used to find and update the page in routine mode) |

> **Standalone mode** (calling this skill directly without a /content routine) requires **no Notion setup** — it skips the Notion update step entirely.

---

## Mode Detection (do this first)

Check whether today's newsletter exists:

```bash
ls inbox/outputs/md/$(date +%Y-%m-%d)-acquisition-content-newsletter-repurpose.md 2>/dev/null
```

- **Found** → **Routine Mode** (running as the final /content step)
- **Not found** → **Standalone Mode** (user called this skill directly)

Mode affects two things only:
| Mode | Newsletter source | Notion update |
|---|---|---|
| Routine | Auto-read from today's file | Update existing newsletter page |
| Standalone | Ask user for paste / file path | Skip Notion update |

Everything else in this skill works identically.

---

## Step 1: Read Context

Read these files before anything else:
- `context/my-voice-dna.md` — voice rules and strong opinions/beliefs that should colour the angle

These are non-negotiable for content skills.

---

## Step 2: Get the Newsletter Draft

**Routine Mode:**
- Read `inbox/outputs/md/YYYY-MM-DD-acquisition-content-newsletter-repurpose.md` (today's date)
- The Notion page ID was logged by the upstream skill — capture it from the session context for Step 8

**Standalone Mode:**
- Ask: *"Paste the newsletter draft, or give me the file path."*
- If the user gives a path, read it
- No Notion page exists — skip the Notion update at Step 8

Extract from the draft:
- Core topic (1 phrase)
- Lead story / hook moment (1 sentence)
- Key result, number, or specific claim (if any)
- One-line lesson the edition lands on

---

## Step 3: Identify Edition Intent

Pick ONE primary intent for the edition:

| Intent | When it applies |
|---|---|
| **Educational** | Teaching a system, framework, or how-to |
| **Story-based** | Personal moment, struggle arc, lesson from experience |
| **Authority** | Establishing credibility, sharing internal data, calling out bad practice |
| **Roundup** | Multiple items curated with commentary |
| **Launch** | New offer, cohort, deadline, or product announcement |

Then map intent → framework categories using this table:

| Edition Intent | Best Categories (load these from `references/frameworks.md`) |
|---|---|
| Educational | Curiosity, Quick Win, Contrarian |
| Story-based | Story, Pain Point, Curiosity |
| Authority | Authority, Results, Contrarian |
| Roundup | Curiosity, Value, Quick Win, Trend |
| Launch | Action, Empowerment, Urgency |

---

## Step 4: Load Frameworks

Read ONLY the matched category sections from `references/frameworks.md`. Do not load the whole file — that wastes context.

Each framework in the file has:
- **Pattern** — the template to instantiate
- **When to use** — situational fit
- **Example** — voice anchor

Use the Pattern as the structure. Use the Example as the voice/style reference. Never invent a new framework — pick one of the 100 by name.

---

## Step 5: Generate 8-10 Subject Lines

For each subject line:
1. Pick a framework that genuinely fits the newsletter content (not just one that sounds clever)
2. Instantiate the Pattern using real specifics from the draft (numbers, names, the actual lesson)
3. Write a complementary Preview Text (40-90 chars) — extends the subject, doesn't repeat it

**Distribution rule:** Spread across at least 3 different frameworks. Don't generate 8 variants of "Confession" — variety lets the strongest framework stand out.

---

## Step 6: Score Each Line

Score every subject line silently on 4 criteria (1-4 each, max 16):

| Criterion | What it means |
|---|---|
| **Curiosity pull (1-4)** | Does it open a loop? Does the reader need to click to close it? |
| **Specificity (1-4)** | Real number, real name, real moment > vague claims |
| **Voice fit (1-4)** | Sounds authentic (lowercase, direct, no fluff) > sounds like every other newsletter |
| **Length efficiency (1-4)** | Under 50 chars = 4. 50-65 = 3. 65-80 = 2. Over 80 = 1. |

---

## Step 7: Build the Output

```
# Newsletter Subject Lines — YYYY-MM-DD

**Source:** YYYY-MM-DD-acquisition-content-newsletter-repurpose.md  (or "user-pasted draft")
**Edition intent:** [intent]
**Framework categories used:** [list]

---

## ⭐ Recommended Pick

**Subject:** "[winning line]"
**Framework:** [name] ([category])
**Preview:** "[preview text]"
**Score:** [N]/16 (curiosity [X], specificity [X], voice [X], length [X])
**Why this one:** [1 sentence — what makes it the strongest match for this edition]

### A/B Variants of Pick
| Variant | Subject | Preview | Different angle |
|---|---|---|---|
| A | "[variant 1]" | "[preview]" | [what makes A different from pick] |
| B | "[variant 2]" | "[preview]" | [what makes B different from pick] |

---

## All Options

| # | Subject | Framework | Preview | Score |
|---|---|---|---|---|
| 1 | [line] | [name] | [preview] | [N]/16 |
| ... | | | | |

(Sorted highest score first)

---

## Style Audit

- Lowercase: [N]/[total]
- Under 50 chars: [N]/[total]
- No banned words (unlock, transform, game-changer, revolutionary, breakthrough, level up, paradigm, mindset shift, leverage, optimize, crush it, life-changing, next level, skyrocket, utilize, implement, facilitate, synergy, don't miss, discover): [N]/[total]
- No em dashes (—): [N]/[total]
- Specific (number / name / moment present): [N]/[total]

If any audit row is below 80%, regenerate the failing lines before saving.
```

---

## Step 8: Update Notion (Routine Mode Only)

Skip this step entirely in Standalone Mode.

In Routine Mode:
1. The newsletter page in `[YOUR_NEWSLETTER_DATABASE_NAME]` was created by the upstream newsletter skill with a placeholder Subject Line
2. Update that page using `mcp__claude_ai_Notion__notion-update-page`
3. Patch the **Subject Line** field with the recommended pick (the winner from Step 7, not the variants)
4. Confirm: *"Notion newsletter page Subject Line updated to: '[pick]'"*

If the Notion page ID is not in session context, search Notion for the most recent page in `[YOUR_NEWSLETTER_DATABASE_NAME]` matching today's date; if no match, skip update.

---

## Step 9: Save Output

Save to `inbox/outputs/md/YYYY-MM-DD-acquisition-content-newsletter-subject-lines.md`

Then tell the user:
> "Subject lines ready. Recommended: '[pick]'. Two A/B variants saved if you want to test."

---

## Edge Cases

| Situation | Action |
|---|---|
| Newsletter draft not found in routine mode | Fall back to Standalone Mode behaviour — ask user to paste |
| Newsletter is shorter than 200 words | Generate 5-6 options instead of 8-10; less material = less variation worth producing |
| No clear edition intent (mixed signals) | Default to "Story-based" if a personal moment is present, else "Educational" |
| All generated lines fail style audit (banned words, length) | Regenerate the failing batch — never save lines that failed audit |
| Notion MCP unavailable | Log "Notion update skipped — MCP unavailable", save locally, surface to user |
| User pastes draft that's not a newsletter (random text) | Ask: "This doesn't look like a newsletter draft. Want me to proceed anyway, or paste the right file?" |

---

## What good looks like

A scored, voice-tuned shortlist where the recommended pick is obviously the strongest, the A/B variants give a real testing option, and every line in the table could plausibly be sent. No "filler" options. No banned words. Every line backed by a real framework name from `references/frameworks.md`.
