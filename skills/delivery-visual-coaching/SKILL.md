---
name: delivery-visual-coaching
description: Creates visual learning materials for coaching sessions -- mindmaps, roadmaps, blueprints, process flows, and presentations in Excalidraw. Use this skill when the user says "create a visual for coaching", "make a mindmap", "build a roadmap for [client]", "I need a diagram", or "create a coaching visual". Also trigger when the user says "Excalidraw", "visual explainer", "process flow for a client", or "presentation for a coaching session".
---

# Delivery Visual Coaching

Purpose: Create visual learning materials for coaching sessions — mindmaps, roadmaps, blueprints, process flows, and presentations using Excalidraw with brand-consistent styling.

## When to Use

- Coaching session needs a visual to explain a concept, system, or plan
- Client needs a roadmap, blueprint, or mindmap as a deliverable
- Creating async learning materials that must stand alone without narration
- Preparing pre-session visuals to frame a coaching call

## Reference Files

Before generating any visual, read these if they exist in your project:
1. `design-kit/guides/excalidraw/design-principles.md` — Visual design philosophy and brand color system
2. `design-kit/guides/excalidraw/element-reference.md` — Excalidraw JSON specs, element types, sizing standards
3. `design-kit/design-tokens.md` — Brand colors, fonts, and CSS variables

If these files don't exist, use the brand defaults in Phase 2 below.

## Steps

### Phase 1: Understand Intent

1. Ask what type of coaching visual is needed:
   - **Mindmap** — Branch out from a central topic, explore connections and subtopics
   - **Roadmap / Blueprint** — Step-by-step path from A to B, phases and milestones
   - **Process / Workflow diagram** — How something works, decision trees, pipelines
   - **Concept explainer** — Break down one concept visually so the learner understands it
   - **Presentation / Slide deck** — Multi-slide visual walkthrough for a session or workshop

2. Ask the coaching context:
   - 1:1 coaching session (live call walkthrough)
   - Community / group session (must be self-explanatory)
   - Async learning material (must stand alone without narration)
   - Pre-session prep (frames the discussion before a call)

3. Ask the learning goal:
   - Understanding a system (how parts connect)
   - A clear plan to follow (what to do first, second, third)
   - A mental model (new way of thinking about a concept)
   - Confidence to take action (path is clear and doable)

4. Summarize: "Got it — a [type] for [context] so the learner walks away with [goal]."

### Phase 2: Brand Confirmation

5. Check for saved config at `.excalidraw/brand.md` in working directory
6. If found, ask whether to use saved config or start fresh
7. If not found, apply brand defaults silently (replace these with your brand colors):

```
primary:       "#463187"  (deep purple)    — titles, anchors, main shapes
primary_bg:    "#E0D6FF"  (soft lavender)  — fills for primary shapes
accent:        "#FF6719"  (orange)         — one emphasis point only
accent_bg:     "#FFE8DC"  (light peach)    — fills for accent shapes
text:          "#2C262E"  (charcoal)       — all text
canvas:        "#FFFFFF"  (white)          — background
stroke_light:  "#C4B8F0"  (muted lavender) — structural elements
```

> **Setup tip:** Create `.excalidraw/brand.md` in your project root with your own hex values. The skill reads it on every run. Example format:
> ```
> primary: "#YOUR_PRIMARY_COLOR"
> accent: "#YOUR_ACCENT_COLOR"
> text: "#YOUR_TEXT_COLOR"
> ```

8. Save brand config to `.excalidraw/brand.md` if it doesn't exist

### Phase 3: Content & Narrative Discovery

9. Ask if user has content ready (notes, outline, bullet points) or if we build together
10. If content provided: read, extract core concept, key learning points, dependencies, action items — confirm back
11. If no content: run guided interview:
    - "What's the core concept? If the learner remembers ONE thing, what should it be?"
    - "What are the 3-5 key building blocks?"
    - "Any common misconceptions or aha moments to surface visually?"
    - "What should the learner DO after understanding this?"

12. Propose visual structure:
    - **Center-out (Mindmap)** — Core in middle, branches radiating out
    - **Left-to-right (Journey / Roadmap)** — Start here, end there
    - **Top-to-bottom (Hierarchy / Funnel)** — Big picture top, details below
    - **Cycle (Loop / Flywheel)** — Steps that repeat
    - **Before/After (Transformation)** — Old way vs. new way side by side

13. Propose the visual outline (nodes, sections, slides) — wait for confirmation

### Phase 4: Visual-by-Visual Co-Design

14. For each section/slide, describe the visual concept BEFORE generating JSON:
    - What the user will see
    - Shapes used and why
    - Mood and color treatment

15. Ask for approval: Go ahead / Different layout / Simpler / More detailed

16. Once approved, generate:
    - Read element-reference.md for JSON specs (if available)
    - Read design-principles.md for design philosophy (if available)
    - Think illustration first — find the spatial metaphor (expand, branch, cycle, flow)
    - Apply brand colors (75% white/light, 20% primary structure, 5% accent)
    - Generate valid Excalidraw JSON with proper groupIds, boundElements, seeds

17. Save to `.excalidraw/{topic}-{type}.excalidraw` file
18. Ask: "How does the visual look?" — iterate until approved
19. Repeat steps 14-18 for every section/slide

### Phase 5: Final Assembly & Delivery

20. Merge all sections into one `.excalidraw` file if multi-section
21. Ask: "Want to adjust anything before we finalize?"
22. Save final file and confirm:
    - "Saved to `.excalidraw/{filename}` — open at excalidraw.com via File > Open"

### Phase 6: Learn & Save

23. Update `.excalidraw/brand.md` with any learned preferences
24. Append session to brand.md history:
    ```
    ### YYYY-MM-DD — [Visual Title]
    - Type: [mindmap/roadmap/blueprint/process/presentation]
    - Context: [1:1/community/async/prep]
    - Elements: [N]
    - Style notes: [any preferences noted]
    ```

## Inputs

- Topic or concept to visualize (from user or from project context)
- Coaching context (1:1, community, async, pre-session)
- Content notes or outline (optional — can build together)
- Brand config at `.excalidraw/brand.md` (optional — uses defaults if missing)

## Outputs

- `.excalidraw` file saved to `.excalidraw/` folder in working directory
- Updated `.excalidraw/brand.md` with session history and learned preferences

## Visual Type Quick Reference

| Type | Best For | Key Visual Pattern |
|------|----------|--------------------|
| Mindmap | Exploring a topic, showing connections | Center hub + radiating branches |
| Roadmap | Step-by-step plans, timelines | Left-to-right path with milestones |
| Blueprint | System architecture, "how it all fits" | Nested containers with connections |
| Process flow | Workflows, decision trees, pipelines | Sequential shapes with arrows |
| Concept explainer | Single idea deep dive | Large focal shape + annotations |
| Presentation | Multi-slide coaching session | Grid of slides, one concept per slide |

## Key Design Rules

- **Illustrate, don't decorate** — shapes carry meaning before text is added
- **One focal point** per visual section — largest, highest-contrast element
- **Cards and grids are a last resort** — use hub-and-spoke, paths, cycles, metaphors
- **Accent color used once max** per section — the ONE critical insight
- **3-second glance test** — can someone understand the point at a glance?
- **Text is labels, not content** — 2-5 words per element, never sentences

## Edge Cases

- If user asks for a type not listed, map it to the closest visual type and confirm
- If content is too complex for one visual, propose splitting into multiple linked visuals
- If brand config conflicts with readability, prioritize readability and note the override
- If no Excalidraw experience, explain: "This creates a file you open at excalidraw.com — a free whiteboard tool"
