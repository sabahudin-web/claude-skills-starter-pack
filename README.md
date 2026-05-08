# claude-skills-starter-pack

**12 battle-tested Claude Code skills for running a business on AI.**

Every skill in this repo has been used in real daily operations — not demos, not prototypes. Clone the repo, copy the skills you want, and you're up and running in minutes.

---

## What's inside

### 🔧 Foundation

| Skill | What it does | Setup |
|-------|-------------|-------|
| [operations-prompt-master](skills/operations-prompt-master/) | Converts messy voice notes or rough input into a production-ready prompt for any AI tool. Handles 30+ tool profiles — Claude Code, ChatGPT, Cursor, Midjourney, n8n, ElevenLabs, and more. | Zero setup |
| [operations-skill-improve](skills/operations-skill-improve/) | Takes a correction from a session and writes it permanently into the relevant skill's SKILL.md. Your AI gets smarter every time you correct it. | Zero setup |

### ⚙️ Operations

| Skill | What it does | Setup |
|-------|-------------|-------|
| [operations-autoresearch](skills/operations-autoresearch/) | Autonomous optimization loop. Give it a skill or file and quality criteria — it iterates, measures, and improves automatically. Deterministic or AI judge mode. | Zero setup |
| [operations-email-report](skills/operations-email-report/) | Scans 24h of Gmail, buckets by content type (INBOUND/CLIENT/REVENUE/ADMIN/FYI), priority-scores by rubric, surfaces dropped threads, outputs action items. Decision aid, not inbox copy. | Gmail MCP + Notion MCP |
| [operations-check-recent-calls](skills/operations-check-recent-calls/) | Scans last 3 days of call transcripts, auto-extracts high-confidence commitments into Notion Client Deliverables. Runs every morning before you open your laptop. | Notion MCP + Fathom MCP |
| [operations-meeting-prep](skills/operations-meeting-prep/) | Deep enrichment + personalized 12-step sales script + PDF pitch deck per discovery call. Auto-runs for every call booked today. | Notion + LinkedIn enrichment + Playwright MCPs |

### 💼 Sales

| Skill | What it does | Setup |
|-------|-------------|-------|
| [offer-build-pitch-deck](skills/offer-build-pitch-deck/) | Builds a branded HTML+PDF pitch deck from your Offer Doc. Slide count is content-driven, not fixed. Self-contained — no broken image links. | Playwright MCP + Python 3 + brand assets |

### 📝 Content

| Skill | What it does | Setup |
|-------|-------------|-------|
| [acquisition-content-youtube-scripting](skills/acquisition-content-youtube-scripting/) | Writes full video scripts, structured bullet points, or hybrid formats from a video outline. Built-in Voice Authenticity Test catches generic guru language before it ships. | Context files (voice-dna.md, content-pillars.md) |
| [acquisition-content-newsletter-subject-lines](skills/acquisition-content-newsletter-subject-lines/) | Generates 8-10 scored subject lines using 100 direct-response frameworks. Standalone mode needs zero setup — just paste your newsletter draft. | Notion MCP (routine mode only) |
| [acquisition-repurpose-linkedin-lead-magnet](skills/acquisition-repurpose-linkedin-lead-magnet/) | Writes LinkedIn lead magnet posts using the Giveaway structure: result first, proof, breakdown, use cases, self-aware CTA. Never desperate. | Context files (voice-dna.md) |

### 🎨 Delivery

| Skill | What it does | Setup |
|-------|-------------|-------|
| [delivery-visual-coaching](skills/delivery-visual-coaching/) | Co-designs Excalidraw coaching visuals — mindmaps, roadmaps, blueprints, process flows. Guided by a visual design philosophy that teaches you to illustrate, not decorate. | Excalidraw MCP |

### 🖌️ Design

| Skill | What it does | Setup |
|-------|-------------|-------|
| [brand-guidelines](skills/brand-guidelines/) | Applies Anthropic's official brand colors and typography (Poppins + Lora, dark/light/accent palette) to any artifact — presentations, documents, visuals. | Python + python-pptx |

---

## Setup tiers

**Zero setup — clone and use immediately:**
- operations-prompt-master *(also add the voice-detect hook for best experience)*
- operations-skill-improve
- operations-autoresearch
- acquisition-content-newsletter-subject-lines *(standalone mode)*

**Low setup — 1 context file or 1 MCP:**
- delivery-visual-coaching → Excalidraw MCP
- brand-guidelines → python-pptx installed

**Medium setup — 2-3 MCPs + context files:**
- operations-email-report → Gmail + Notion MCPs + reference files
- acquisition-content-youtube-scripting → create context/my-voice-dna.md + context/content-pillars.md
- acquisition-repurpose-linkedin-lead-magnet → create context/my-voice-dna.md + fill in references/linkedin-content-universe.md
- offer-build-pitch-deck → Playwright + Python + brand assets

**High setup — multiple MCPs + Notion IDs:**
- operations-check-recent-calls → Notion MCP (4 database IDs) + Fathom MCP
- operations-meeting-prep → Notion + LinkedIn enrichment + Playwright MCPs

---

## MCP Requirements

| Skill | MCPs Required | Notes |
|-------|--------------|-------|
| operations-prompt-master | None | Add voice-detect hook (optional but recommended) |
| operations-skill-improve | None | — |
| operations-autoresearch | None | Python 3 required for deterministic eval mode |
| operations-email-report | Gmail, Notion | 2 Notion DB IDs to configure |
| operations-check-recent-calls | Notion, Fathom | 4 Notion DB IDs to configure |
| operations-meeting-prep | Notion, Playwright, Relay or LinkedIn enrichment tool | 1 Notion DB ID + absolute path |
| offer-build-pitch-deck | Playwright | Python 3 required; brand assets to add |
| acquisition-content-youtube-scripting | None | 2-3 context files to create |
| acquisition-content-newsletter-subject-lines | Notion (routine mode only) | Standalone mode: zero setup |
| acquisition-repurpose-linkedin-lead-magnet | Notion (optional) | For content dashboard push |
| delivery-visual-coaching | Excalidraw | Brand config optional |
| brand-guidelines | None (MCP) | python-pptx required |

Connect MCPs via your Claude Desktop or Claude Code settings. No `.mcp.json` is included — connect from your own settings.

---

## Quick install

```bash
git clone https://github.com/[your-username]/claude-skills-starter-pack
cd claude-skills-starter-pack

# Copy a skill to your Claude Code project
cp -r skills/operations-prompt-master /path/to/your/project/.claude/skills/

# For prompt-master: also install the voice-detect hook
cp hooks/voice-detect.sh /path/to/your/project/.claude/hooks/
chmod +x /path/to/your/project/.claude/hooks/voice-detect.sh
```

**→ Full setup guide: [INSTALL.md](INSTALL.md)**

---

## How to use each skill

Once installed, trigger a skill in Claude Code by describing what you want in natural language:

| Say this... | Runs this skill |
|-------------|----------------|
| "clean up my prompt", "make a prompt from this" | operations-prompt-master |
| "I don't like this, never do that again" | operations-skill-improve |
| "autoresearch [skill name]", "optimize this" | operations-autoresearch |
| "email report", "check my inbox" | operations-email-report |
| "check recent calls", "any tasks from yesterday's call" | operations-check-recent-calls |
| "prep for my meeting with [Name]" | operations-meeting-prep |
| "build my pitch deck", "create slides for my offer" | offer-build-pitch-deck |
| "script this video", "write bullet points for filming" | acquisition-content-youtube-scripting |
| "write subject lines", "I need email subjects" | acquisition-content-newsletter-subject-lines |
| "write a lead magnet post", "LinkedIn giveaway post" | acquisition-repurpose-linkedin-lead-magnet |
| "create a visual for coaching", "make a mindmap" | delivery-visual-coaching |
| "apply Anthropic brand", "brand guidelines" | brand-guidelines |

---

## Built by

**Sabahudin Murtic** — AI consultant who builds Claude Code operating systems for solopreneurs and SMB owners.

Every skill in this pack runs daily in a real business. Battle-tested before it ships.

→ [Connect on LinkedIn](https://www.linkedin.com/in/sabahudinmurtic/)
