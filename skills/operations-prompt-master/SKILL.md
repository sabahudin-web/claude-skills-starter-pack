---
name: operations-prompt-master
description: >
  Converts rough, informal, or ambiguous input into a single production-ready prompt — optimized
  for the specific target AI tool. Handles 30+ tool profiles (Claude Code, ChatGPT, Cursor, Midjourney,
  ElevenLabs, n8n, and more). Use this skill when the user says "clean up my prompt", "make a prompt
  from this", "I have rough notes", or gives a voice transcript. Also trigger automatically when
  input is informal, rambling, or mixed-task.
---

# operations-prompt-master

Takes rough input from the user, identifies the target AI tool, extracts actual intent, and outputs a single production-ready prompt — optimized for that specific tool, with zero wasted tokens.

**NEVER discuss prompting theory unless explicitly asked.**
**NEVER show framework names in your output.**
**Build prompts. One at a time. Ready to paste or run.**

---

### Hard Rules — NEVER violate

- NEVER output a prompt without first confirming the target tool — ask if ambiguous
- NEVER embed techniques that cause fabrication in single-prompt execution:
  - Mixture of Experts — model role-plays personas from one forward pass, no real routing
  - Tree of Thought — model generates linear text and simulates branching, no real parallelism
  - Graph of Thought — requires external graph engine, single-prompt = fabrication
  - Universal Self-Consistency — requires independent sampling, later paths contaminate earlier ones
  - Prompt chaining as a layered technique — pushes models into fabrication on longer chains
- NEVER add Chain of Thought to reasoning-native models (o3, o4-mini, DeepSeek-R1, Qwen3 thinking mode)
- NEVER ask more than 3 clarifying questions before producing a prompt
- NEVER pad output with explanations the user did not request

---

### Output Format — ALWAYS follow this

Your output is ALWAYS:
1. A single copyable prompt block ready to paste into the target tool
2. `🎯 Target: [tool name] · 💡 [one sentence — what was optimized and why]`
3. If the prompt needs setup steps before pasting/running, add a short plain-English note below (1-2 lines max — ONLY when genuinely needed)

For copywriting and content prompts, include fillable placeholders ONLY where relevant: `[TONE]`, `[AUDIENCE]`, `[BRAND VOICE]`, `[PRODUCT NAME]`.

Then ask: **"Would you like me to run this?"**

---

## EXECUTION PIPELINE

### Step 1 — Load context

Read `context/business-profile.md` + `context/current-priorities.md` if they exist in your project.

> **Note:** These files are optional. If they don't exist, skip this step — the skill runs fully without them. Context files improve targeting accuracy but aren't required.

Use whatever context is available to ground the prompt in the user's business reality — who they are, what they build, what matters now. This shapes role assignments, audience specs, and success criteria in the generated prompt.

---

### Step 2 — Detect the target tool

Identify which AI system will receive this prompt. Route to the correct profile below.

If the input mentions a specific tool, use that. If it's clearly a Claude Code task (skill build, rule, command, file edit), default to Claude Code. If genuinely ambiguous, ask ONE question: "Which tool is this for?"

---

### Step 3 — Extract 9 intent dimensions (silently)

| Dimension | What to extract | Critical? |
|-----------|----------------|-----------|
| **Task** | Specific action — convert vague verbs to precise operations | Always |
| **Target tool** | Which AI system receives this prompt | Always |
| **Output format** | Shape, length, structure, filetype | Always |
| **Constraints** | MUST / MUST NOT, scope boundaries | If complex |
| **Input** | What's being provided alongside the prompt | If applicable |
| **Context** | Prior decisions from this session, established stack/rules | If session has history |
| **Audience** | Who reads the output, their level | If user-facing |
| **Success criteria** | Binary pass/fail definition of done | If complex |
| **Examples** | Input/output pairs for pattern lock | If format-critical |

Missing critical dimensions → ask (max 3 questions total across steps 2–3).

---

### Step 4 — Run diagnostic checklist

Load `references/patterns.md`. Silently scan for all 35 credit-killing patterns.
Fix silently — flag only if the fix changes the user's intent.

Key patterns to catch:
- Vague task verb → replace with a precise operation
- Two tasks in one → split, deliver as Prompt 1 and Prompt 2
- No success criteria → derive binary pass/fail from stated goal
- No stop conditions for agents → add checkpoint and human review triggers
- Assumed prior knowledge → prepend memory block with all prior decisions
- No scope boundary → add explicit file/directory lock
- CoT added to reasoning models → REMOVE IT

---

### Step 5 — Select template

Auto-route to the correct framework. Never show the framework name in output.
Load `references/templates.md` only for the category you need.

| Task type | Template |
|-----------|----------|
| Simple one-shot | Template A — RTF |
| Business writing, reports | Template B — CO-STAR |
| Complex multi-step | Template C — RISEN |
| Creative / brand voice | Template D — CRISPE |
| Logic, debugging, analysis | Template E — Chain of Thought |
| Consistent structured output | Template F — Few-Shot |
| Code editing AI (Cursor/Copilot) | Template G — File-Scope |
| Claude Code / autonomous agents | Template H — ReAct + Stop Conditions ← most common |
| Image / video generation | Template I — Visual Descriptor |
| Editing existing image | Template J — Reference Image Editing |
| ComfyUI workflows | Template K — ComfyUI |
| Breaking down existing prompt | Template L — Prompt Decompiler |

---

### Step 6 — Apply safe techniques (only when genuinely needed)

**Role assignment** — for complex or specialized tasks:
- Weak: "You are a helpful assistant"
- Strong: "You are a senior backend engineer specializing in distributed systems who prioritizes correctness over cleverness"

**Few-shot examples** — when format is easier to show than describe. 2–5 examples. Apply when the user has re-prompted for the same formatting issue more than once.

**Grounding anchors** — for any factual or citation task:
"Use only information you are highly confident is accurate. If uncertain, write [uncertain]. Do not fabricate citations or statistics."

**Chain of Thought** — for logic, math, debugging on standard reasoning models ONLY (Claude, GPT-5.x, Gemini, Qwen2.5, Llama). NEVER on o3/o4-mini/R1/Qwen3-thinking.

**XML structural tags** — for Claude-based tools parsing multi-section prompts:
`<context>`, `<task>`, `<constraints>`, `<output_format>`

---

### Step 7 — Prepend Memory Block (when needed)

When the request references prior session decisions, prepend this block in the first 30% of the generated prompt:

```
## Context (carry forward)
- Stack and tool decisions established: [list]
- Architecture choices locked: [list]
- Constraints from prior turns: [list]
- What was tried and failed: [list]
```

---

### Step 8 — Token efficiency audit

Every word must be load-bearing. Strip:
- Padding phrases ("as an AI language model", "certainly", "I'd be happy to")
- Vague adjectives ("good", "nice", "professional" without measurable spec)
- Unrequested explanations
- Duplicate instructions

---

### Step 9 — Verification pass

Before delivering, confirm:
1. Target tool correctly identified and prompt formatted for its specific syntax?
2. Critical constraints in the first 30% of the generated prompt?
3. Strongest signal words used — MUST over should, NEVER over avoid?
4. All fabrication-prone techniques removed?
5. Token efficiency audit passed — every sentence load-bearing, scope bounded?
6. Stop conditions present for agentic tasks?
7. Would this prompt produce the right output on the first attempt?

---

### Step 10 — Output + pause

Deliver:
1. The clean prompt in a code block
2. `🎯 Target: [tool] · 💡 [what was optimized and why]`
3. Ask: **"Would you like me to run this?"**

Wait for confirmation before proceeding.

---

### Step 11 — On confirmation

Execute from the CLEAN prompt — not the original raw input.

---

### Step 12 — Save

Save to `inbox/outputs/md/YYYY-MM-DD-operations-prompt-master.md`:

```
# Prompt Master Output — YYYY-MM-DD

## Raw Input
[original input as-is]

## Clean Prompt
[the generated prompt]

## Optimization Note
🎯 Target: [tool] · 💡 [optimization note]
```

---

## TOOL ROUTING PROFILES

### Claude (claude.ai, Claude API, Claude 4.x)
- Be explicit and specific — Claude follows instructions literally, not by inference
- XML tags help for complex multi-section prompts: `<context>`, `<task>`, `<constraints>`, `<output_format>`
- Claude Opus 4.x over-engineers by default — add "Only make changes directly requested. Do not add features or refactor beyond what was asked."
- Provide context and reasoning WHY, not just WHAT — Claude generalizes better from explanations
- Always specify output format and length explicitly

### ChatGPT / GPT-5.x / OpenAI GPT models
- Start with the smallest prompt that achieves the goal — add structure only when needed
- Be explicit about the output contract: format, length, what "done" looks like
- Constrain verbosity when needed: "Respond in under 150 words. No preamble. No caveats."
- GPT-5.x is strong at long-context synthesis and tone adherence — leverage these

### o3 / o4-mini / OpenAI reasoning models
- SHORT clean instructions ONLY — these models reason across thousands of internal tokens
- NEVER add CoT, "think step by step", or reasoning scaffolding — it actively degrades output
- Prefer zero-shot first
- State what you want and what done looks like. Nothing more.
- Keep system prompts under 200 words

### Gemini 2.x / Gemini 3 Pro
- Strong at long-context and multimodal — leverage its large context window for document-heavy prompts
- Prone to hallucinated citations — always add "Cite only sources you are certain of. If uncertain, say [uncertain]."
- For grounded tasks add "Base your response only on the provided context. Do not extrapolate."

### Claude Code
- Agentic — runs tools, edits files, executes commands autonomously
- Starting state + target state + allowed actions + forbidden actions + stop conditions + checkpoints
- Stop conditions are MANDATORY — runaway loops are the biggest credit killer
- Claude Opus 4.x over-engineers — add "Only make changes directly requested. Do not add extra files, abstractions, or features."
- Always scope to specific files and directories — never give a global instruction without a path anchor
- Human review triggers required: "Stop and ask before deleting any file, adding any dependency, or affecting the database schema"
- For complex tasks: split into sequential prompts

### Cursor / Windsurf
- File path + function name + current behavior + desired change + do-not-touch list + language and version
- Never give a global instruction without a file anchor
- "Done when:" is required — defines when the agent stops editing

### GitHub Copilot
- Write the exact function signature, docstring, or comment immediately before invoking
- Describe input types, return type, edge cases, and what the function must NOT do

### Bolt / v0 / Lovable / Figma Make / Google Stitch
- Full-stack generators default to bloated boilerplate — scope it down explicitly
- Always specify: stack, version, what NOT to scaffold, clear component boundaries
- Add "Do not add authentication, dark mode, or features not explicitly listed" to prevent feature bloat

### Midjourney
- Comma-separated descriptors, not prose. Subject first, then style, mood, lighting.
- Parameters at end: `--ar 16:9 --v 6 --style raw`

### DALL-E 3
- Prose description works. Add "do not include text in the image unless specified."

### Stable Diffusion
- `(word:weight)` syntax. CFG 7-12. Negative prompt is MANDATORY. Steps 20-30 for drafts.

### ElevenLabs
- Specify emotion, pacing, emphasis markers, and speech rate directly
- Prose descriptions do not translate — specify parameters directly

### Zapier / Make / n8n
- Trigger app + trigger event → action app + action + field mapping. Step by step.
- For multi-step workflows: number each step and specify what data passes between steps

---

## EDGE CASES

| Situation | Action |
|-----------|--------|
| Tool genuinely unclear | Ask "Which tool is this for?" — counts toward 3-question limit |
| Input contains 2 unrelated tasks | Split into Prompt 1 + Prompt 2, present both, ask which to run first |
| Input is already a clean prompt | Run diagnostic only — output fixed version or "This prompt is already tight — no changes needed" |
| User declines to run | Save clean prompt to inbox, confirm: "Saved to inbox/outputs/md/YYYY-MM-DD-operations-prompt-master.md" |
| Critical info missing after 3 questions | Build the best possible prompt from available info, mark assumptions clearly |
| Session transcript as input | Extract the core task from the transcript, ignore filler and repetition |

---

## WHAT GOOD LOOKS LIKE

The user pastes or runs the generated prompt in their target tool. It works on the first try. Zero re-prompts needed. Every word in the prompt is load-bearing — nothing vague, nothing missing, nothing over-scoped.

For Claude Code specifically: the generated prompt includes a clear objective, starting state, target state, scope lock on which files to touch, stop conditions, and checkpoint output after each major step. Claude Code never has to guess what "done" looks like.
