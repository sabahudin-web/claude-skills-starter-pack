---
name: operations-autoresearch
description: >
  Autonomous optimization loop that continuously improves any file in the OS
  against measurable quality criteria. Two evaluation modes — deterministic
  (eval.py with proxy heuristics) or AI judge (LLM rubric scoring). Full
  four-way role separation. Use this skill when the user says "autoresearch
  [file or skill name]", "optimize this skill", "improve my voice DNA",
  "sharpen this command", "autoresearch CLAUDE.md", "make this better
  automatically", "run the optimization loop on", or "iterate on this until
  it's better". Works on: skills, CLAUDE.md, brain MOCs, context files,
  routine commands.
---

# operations-autoresearch

Autonomous goal-directed iteration loop that improves any OS file — skills, CLAUDE.md, brain notes, context files, or routine commands — against criteria you define. Inspired by Karpathy's autoresearch pattern.

## Automation Level
CHECKPOINT — always shows improved file to user before writing. Never overwrites without confirmation. Loop itself runs autonomously once started.

## Architecture: Four-Way Separation

Both eval modes maintain strict separation so no role can game the evaluation.

| Role | Who | Knows eval details? | Knows history? |
|------|-----|---------------------|---------------|
| **Optimizer** (you, main agent) | Makes changes, reads metric numbers, decides keep/discard | NO — never reads eval.py source or rubric scoring examples | YES — reads logs, plans changes |
| **Eval Agent** | `autoresearch-eval-agent` | YES — writes eval.py OR rubric.md | NO |
| **Test Runner** | `autoresearch-test-runner` | NO — fresh context every time | NO |
| **Judge** | `eval.py` (deterministic) OR `autoresearch-judge` agent (AI judge) | IS the eval / follows rubric | NO |

---

## Inputs
- The target file path (skill, CLAUDE.md, brain note, context file, command)
- User-confirmed quality criteria
- All reference files the target depends on

## Outputs
- `inbox/outputs/html/YYYY-MM-DD-operations-autoresearch-[target-name].html` — live dashboard
- `inbox/outputs/json/YYYY-MM-DD-operations-autoresearch-[target-name].jsonl` — iteration log
- The improved target file (shown to user before writing — CHECKPOINT)

---

## The Three Rules (Criteria Validation)

Every criterion MUST pass these before entering the loop. Bad criteria produce bad evals.

**Rule 1: State the exact condition, not the goal.**

| Bad | Good |
|-----|------|
| "Make the hook short" | "First line must be under 136 characters" |
| "Should be professional" | "Contains no exclamation marks and no ALL CAPS words (3+ letters)" |
| "Include relevant data" | "Contains at least one specific number or statistic" |

**Rule 2: One criterion, one variable.** If you'd use "and" to combine two checks, split them.

**Rule 3: Define the test (optional).** Describe what to count, what regex to match, or what structure to look for. Helps the eval agent write better checks.

If the user provides criteria that violate The Three Rules, rewrite them — show the before/after.

---

## Phase 0: Session Setup

When the user names a target file or says "autoresearch [something]":

1. Resolve the target file path:
   - Skill name → `.claude/skills/[skill-name]/SKILL.md`
   - "CLAUDE.md" → `CLAUDE.md`
   - "brain/acquisition" or "acquisition-moc" → `brain/acquisition-moc.md`
   - "context/my-voice-dna" → `context/my-voice-dna.md`
   - "[command name]" or "/content" → `.claude/commands/[command-name].md`

2. Read the target file.

3. Determine the output file type the target produces (for skills and commands — check the output section of the file):
   - Skills that produce markdown → `.md`
   - Skills that produce HTML → `.html`
   - Skills that produce JSON → `.json`
   - Skills that produce PDFs → `.pdf`
   - Skills that produce images → `.png`
   - Config/context/brain files → `.md` (the file itself is the output)

4. Create the session directory: `inbox/outputs/autoresearch-sessions/YYYY-MM-DD-[target-name]/`
   Create subdirectory: `inbox/outputs/autoresearch-sessions/YYYY-MM-DD-[target-name]/outputs/`

5. Write session config to `autoresearch-session.md` in the session directory.

6. **Explain The Three Rules in chat.** Then propose 5-7 quality criteria specific to this file type.
   Examples by target type:
   - **Skill:** trigger phrases exist, numbered steps, correct output routing, edge cases section, context reads appropriate files
   - **CLAUDE.md:** every rule has a concrete example, no vague instructions, cross-references are accurate, all referenced paths exist
   - **Brain MOC:** covers key patterns from real outputs, links to sources, no stale references
   - **Context file:** every section under 200 words, no outdated info, actionable summary present
   - **Routine command:** every skill in the workflow table exists at the named path, all steps are numbered, output destination named

7. Use AskUserQuestion:
   - Question: "Do these quality criteria look right?"
   - Options: "These look good" / "Adjust some"

8. Use AskUserQuestion (separate step):
   - Question: "Which evaluation mode?"
   - Options: "Deterministic (checks things mechanically — structure, format, keywords)" / "AI Judge (LLM scores subjective quality — tone, authenticity, completeness)"

9. Use AskUserQuestion (separate step):
   - Question: "How many iterations? (5 recommended)"
   - Options: "5 (recommended)" / "10" / "20"

---

## Phase 1: Build the Eval System

10. Spawn `autoresearch-eval-agent` with:
    - Target file path + contents
    - Confirmed criteria list
    - Session directory path
    - Eval mode (deterministic or ai_judge)
    - Output file extension

    **Deterministic:** agent generates `eval.py` + `test_cases.json`
    **AI Judge:** agent generates `rubric.md` + `test_cases.json`

11. Read the generated file (eval.py or rubric.md) and show it to the user. Use AskUserQuestion:
    - Question: "Does this eval capture what you mean?"
    - Options: "Looks good" / "Adjust it"

    If adjust: spawn eval agent again with specific feedback.

12. Once confirmed — **eval artifacts are READ-ONLY for the rest of the session.** Never modify eval.py, rubric.md, or test_cases.json during the loop.

---

## Phase 2: Baseline (Iteration 0)

13. Spawn `autoresearch-test-runner` with:
    ```
    Execute the target file at [full path to target].
    Test cases are at [session directory]/test_cases.json.
    The working project is at [YOUR_PROJECT_PATH]. Replace with your actual absolute path before running.

    Reference files the target depends on (read these first):
    - [list ALL files the target references: context/, brain/, design-kit/, etc.]

    Use all available tools to produce real outputs.
    Save each output to [session directory]/outputs/output_00.[ext] through output_09.[ext].
    Follow the target exactly. One output per test case. No commentary.
    ```

    IMPORTANT: Scan the target file for any file paths, references/ mentions, context/ reads, or [[wikilinks]] — list all of them explicitly in the prompt.

14. Evaluate the baseline:
    - **Deterministic:** `python [session directory]/eval.py [session directory]/outputs/` — parse `METRIC pass_rate=X.XXXX`
    - **AI Judge:** Spawn `autoresearch-judge` with outputs/ + rubric.md — parse `quality_score` from `judge-scores.json`

15. Record baseline in `autoresearch-log.jsonl`. Create initial dashboard from `references/dashboard-template.html`.

---

## Phase 3: The Loop

Repeat for the chosen iteration count (stop early if metric plateaus for 10+ consecutive iterations or user says "stop"):

### Step 1 — Review
- Read current target file
- Read last 5 entries from `autoresearch-log.jsonl`
- Read failure details from last eval (which assertions fail most? which test cases are hardest?)
- Read `autoresearch-ideas.md` if it exists

### Step 2 — Ideate
- Pick ONE change to try. One hypothesis, one variable.
- Reason: target the weakest area from the last eval's assertion breakdown or rubric breakdown.
- Write the hypothesis in plain English before making the change.

### Step 3 — Modify
- Copy target file to `[target-filename].backup` in the session directory
- Make EXACTLY ONE change to the target file

### Step 4 — Execute (via Test Runner)
- Scan the updated target file for reference files again (they may have changed)
- Spawn `autoresearch-test-runner` with the same prompt as Phase 2, updated with any new reference file paths

### Step 5 — Evaluate
- **Deterministic:** Run `python eval.py outputs/` — parse `METRIC pass_rate=X.XXXX`
- **AI Judge:** Spawn `autoresearch-judge` — parse `quality_score` from `judge-scores.json`

### Step 6 — Decide
| Condition | Action |
|-----------|--------|
| Metric improved | KEEP — change stays, update `.backup` to new version |
| Metric same or worse | DISCARD — restore from `.backup` |
| Eval crashed | CRASH — restore from `.backup`, note the error |

### Step 7 — Log + Dashboard
Append to `autoresearch-log.jsonl`:
```json
{"iteration": 1, "timestamp": "ISO", "hypothesis": "...", "metric_name": "pass_rate", "metric_value": 0.70, "baseline": 0.50, "best_so_far": 0.70, "delta": "+0.20", "eval_mode": "deterministic", "assertion_breakdown": {"assertion_1": 9, "assertion_2": 7}, "status": "keep"}
```
AI Judge format uses `"rubric_breakdown": {"criterion_1": 3.8, "criterion_2": 3.2}` instead.

Update dashboard HTML with current stats.

### Step 8 — Stuck Check
If 3+ consecutive discards on similar ideas → pivot radically. Try a completely different approach.

---

## Stopping

When the loop finishes (iteration count reached, plateau, or user says "stop"):

16. Write final summary to `autoresearch-worklog.md`:
    - Total iterations run
    - Best metric achieved vs baseline
    - Top 3 most impactful changes
    - Which criteria improved most
    - Untried ideas (from `autoresearch-ideas.md`)

17. Show the user the improved target file. Use AskUserQuestion:
    - Question: "Write the improved version to [target path]?"
    - Options: "Yes, write it" / "Skip" / "Edit first"

18. On confirmation: write the improved file to the original target path.

19. Save dashboard to `inbox/outputs/html/YYYY-MM-DD-operations-autoresearch-[target-name].html`
    Save log to `inbox/outputs/json/YYYY-MM-DD-operations-autoresearch-[target-name].jsonl`

---

## Separation Rules

1. **You are the optimizer. NEVER generate outputs, write eval code, or score quality yourself.**
2. **Eval artifacts (eval.py, rubric.md, test_cases.json) are READ-ONLY once confirmed.**
3. **Test runner NEVER sees the eval or rubric.** Fresh context every time.
4. **Judge NEVER sees iteration history.** Fresh context every time. (AI judge mode)
5. **You NEVER read eval.py source code or rubric scoring examples.** Only read the metric number.

---

## Edge Cases

| Situation | What to do |
|-----------|-----------|
| User says "autoresearch" without a target | Ask: "Which file do you want to optimize? (skill name, CLAUDE.md, context/[file], brain/[moc], or /command name)" |
| Target file doesn't exist | Stop and flag: "I can't find [path]. Check the name and try again." |
| Eval.py crashes with syntax error | Spawn eval agent again with the error message. Fix before starting the loop. |
| Skill produces binary output (PDF, image) | Deterministic eval checks file exists + non-empty only. Flag to user that content-level scoring isn't available. |
| All 20 iterations discard | Show user the final summary with a note: "The criteria may be too strict or the target may need manual redesign first." |
| User messages during loop | Pause, respond, then offer to resume: "Want me to continue from iteration X?" |
| Target is operations-autoresearch itself | Skip gracefully — don't recurse. |

---

## What Good Looks Like

The target file improves measurably across the iteration log. The dashboard shows a clear upward trend in the metric with the specific changes that drove each keep. The user sees a before/after and confirms. The session leaves a JSONL audit trail and dashboard in inbox/outputs/ for reference.
