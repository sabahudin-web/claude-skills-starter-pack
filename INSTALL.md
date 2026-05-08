# Installation Guide

Step-by-step setup for every skill in the pack.

---

## Prerequisites

- [Claude Code](https://claude.ai/code) installed (CLI or desktop app)
- For MCP-dependent skills: relevant MCPs connected in your Claude settings

---

## Step 1 — Clone the repo

```bash
git clone https://github.com/[your-username]/claude-skills-starter-pack
cd claude-skills-starter-pack
```

---

## Step 2 — Copy skill(s) to your project

Each skill is a self-contained folder. Copy only the skills you want.

```bash
# Copy a single skill
cp -r skills/operations-prompt-master /path/to/your/project/.claude/skills/

# Copy multiple skills
cp -r skills/operations-skill-improve /path/to/your/project/.claude/skills/
cp -r skills/operations-autoresearch /path/to/your/project/.claude/skills/
```

Replace `/path/to/your/project/` with your actual Claude Code project root.

---

## Step 3 — Connect MCPs

Connect MCPs from your Claude Desktop settings or via `.mcp.json` in your project.

**No `.mcp.json` is included in this repo** — connect MCPs from your own settings to avoid overwriting existing connections.

| Skill | MCPs to connect |
|-------|----------------|
| operations-email-report | Gmail, Notion |
| operations-check-recent-calls | Notion, Fathom (or your call recording/transcription tool) |
| operations-meeting-prep | Notion, Playwright, Relay (for LinkedIn search) |
| offer-build-pitch-deck | Playwright |
| acquisition-content-newsletter-subject-lines | Notion (only for routine mode) |
| acquisition-repurpose-linkedin-lead-magnet | Notion (optional — for content dashboard) |
| delivery-visual-coaching | Excalidraw |

---

## Step 4 — Set your Notion database IDs

Skills that use Notion require you to replace placeholder IDs in the SKILL.md files.

**How to find your Notion database ID:**
1. Open the database in Notion
2. Click "Share" → "Copy link"
3. The UUID in the URL is your database ID
4. Format for the skill: `collection://[your-uuid-here]`

**Replace these placeholders:**

| Skill | Placeholder | Your database |
|-------|-------------|--------------|
| operations-email-report | `YOUR_CLIENT_DELIVERABLES_NOTION_DB_ID` | Your active clients database |
| operations-email-report | `YOUR_PEOPLE_CRM_NOTION_DB_ID` | Your CRM/prospects database |
| operations-check-recent-calls | `YOUR_TRANSCRIPTS_RECORDINGS_NOTION_DB_ID` | Your call recordings database |
| operations-check-recent-calls | `YOUR_CLIENT_DELIVERABLES_NOTION_DB_ID` | Your active clients database |
| operations-check-recent-calls | `YOUR_PEOPLE_CRM_NOTION_DB_ID` | Your CRM/prospects database |
| operations-check-recent-calls | `YOUR_DEALS_NOTION_DB_ID` | Your deals pipeline database |
| operations-meeting-prep | `YOUR_MEETING_PREP_NOTION_DB_ID` | Your meeting prep database |
| acquisition-content-newsletter-subject-lines | `[YOUR_NEWSLETTER_DATABASE_NAME]` | Your newsletter database name (exact string) |

---

## Step 5 — Install the voice-detect hook (for prompt-master users)

The `voice-detect.sh` hook fires on every message you send. It detects voice/dictation patterns and automatically triggers `operations-prompt-master` to clean up the input before Claude executes it.

```bash
# Copy the hook
cp hooks/voice-detect.sh /path/to/your/project/.claude/hooks/
chmod +x /path/to/your/project/.claude/hooks/voice-detect.sh
```

Then wire it in your project's `.claude/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/voice-detect.sh"
          }
        ]
      }
    ]
  }
}
```

**What this does:** When you dictate a message or write something informal/rambling, the hook injects a reminder for Claude to clean your prompt first before doing anything. No more half-executed tasks from voice input.

---

## Step 6 — Create context files (for content skills)

Some skills read context files to personalize their output. Create these in your project root:

### For acquisition-content-youtube-scripting:

```bash
mkdir -p context
touch context/my-voice-dna.md
touch context/content-pillars.md
touch context/my-story-doc.md  # optional — 3-5 personal stories for Pillar 3
```

**`context/my-voice-dna.md`** — Your voice rules:
- Phrases you use naturally
- Phrases you never write
- Hook patterns you prefer
- CTA rules per content type

**`context/content-pillars.md`** — Your 3 content pillars:
```markdown
# Content Pillars

## Pillar 1: [Your Primary Topic]
Voice: [how you write about this]
CTA rule: [soft/hard/no CTA]

## Pillar 2: [Your Secondary Topic]
Voice: [how you write about this]
CTA rule: [soft/hard/no CTA]

## Pillar 3: [Your Personal Journey]
Voice: [how you write about this]
CTA rule: [no hard CTA]
```

### For acquisition-repurpose-linkedin-lead-magnet:

1. Create `context/my-voice-dna.md` (same as above)
2. Fill in the template at `references/linkedin-content-universe.md` — replace every [BRACKET] with your own brand DNA

---

## Step 7 — Add brand assets (for offer-build-pitch-deck)

```bash
mkdir -p design-kit/assets/my-photos
mkdir -p design-kit/assets/logos
mkdir -p design-kit/assets/textures
```

Add these files:
```
design-kit/assets/my-photos/your-profile-photo.png
design-kit/assets/logos/logo-on-dark.png
design-kit/assets/logos/logo-on-brand.png
design-kit/assets/logos/logo-on-light.png
design-kit/assets/textures/grain-texture.png   ← optional
```

Then create `design-kit/design-tokens.md` with your brand colors and fonts. See the skill's SKILL.md for the expected format.

---

## Step 8 — Configure brand for visual coaching

For `delivery-visual-coaching`, create a brand config:

```bash
mkdir -p .excalidraw
```

Create `.excalidraw/brand.md`:
```markdown
primary: "#YOUR_PRIMARY_COLOR"
primary_bg: "#YOUR_PRIMARY_LIGHT"
accent: "#YOUR_ACCENT_COLOR"
accent_bg: "#YOUR_ACCENT_LIGHT"
text: "#YOUR_TEXT_COLOR"
canvas: "#FFFFFF"
stroke_light: "#YOUR_LIGHT_STROKE"
```

If this file doesn't exist, the skill uses the default purple/orange palette — which works fine as a starting point.

---

## Testing your install

After installing, verify each skill works by typing these prompts in Claude Code:

| Skill | Test prompt |
|-------|------------|
| operations-prompt-master | "make a prompt from this: I want to write a blog post about AI trends" |
| operations-skill-improve | Run any skill → say "I don't like this, never do that again" |
| operations-autoresearch | "autoresearch operations-prompt-master" |
| operations-email-report | "email report" |
| operations-check-recent-calls | "check recent calls" |
| operations-meeting-prep | "prep for my meeting with [Name], LinkedIn: [URL]" |
| offer-build-pitch-deck | "build my pitch deck" (requires Offer Doc in inbox/outputs/) |
| acquisition-content-youtube-scripting | "script this video" (requires outline or brief) |
| acquisition-content-newsletter-subject-lines | "write subject lines" (paste a newsletter draft) |
| acquisition-repurpose-linkedin-lead-magnet | "write a lead magnet post about [your resource]" |
| delivery-visual-coaching | "make a mindmap about [topic]" |
| brand-guidelines | "apply Anthropic brand to this presentation" |

---

## Troubleshooting

**"Skill not triggering"** — Make sure the skill folder is in `.claude/skills/` (not a subfolder of subfolder). Claude Code looks for SKILL.md directly inside the skill folder.

**"MCP tool not found"** — The MCP needs to be connected in your Claude settings. Check Settings → Integrations in Claude Desktop.

**"Notion ID not found"** — Make sure you replaced the placeholder (e.g. `YOUR_CLIENT_DELIVERABLES_NOTION_DB_ID`) with your actual UUID. The format is `collection://[uuid]`.

**"Voice detect hook not firing"** — Check that `voice-detect.sh` is executable (`chmod +x`) and that the hook is wired in `.claude/settings.json` under `UserPromptSubmit`.

---

## Questions?

Open an issue on the repo or connect on LinkedIn → [Sabahudin Murtic](https://www.linkedin.com/in/sabahudinmurtic/)
