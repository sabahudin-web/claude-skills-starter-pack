---
name: offer-build-pitch-deck
description: >
  Build a branded HTML pitch deck from an Offer Doc — PDF + HTML output using your brand design system.
  Slides are driven by the offer content (not a fixed template count). Uses real brand assets (photos,
  logos, grain texture). Use this skill when the user says "build my pitch deck", "create slides",
  "presentation for my offer", "pitch deck", or wants a deck for sales calls, partnerships, or async
  outreach. Requires an Offer Doc to exist first.
---

# Offer Pitch Deck

Build a pitch deck from an Offer Doc. The deck sells through clarity, proof, and specificity — using your brand energy. Every slide pulls real content from the Offer Doc. No filler slides. No fixed slide count.

---

## Setup Required

Before running this skill, set up your brand assets:

```
design-kit/assets/my-photos/your-profile-photo.png      ← your headshot
design-kit/assets/logos/logo-on-dark.png                ← logo for dark backgrounds
design-kit/assets/logos/logo-on-brand.png               ← logo for brand-color backgrounds
design-kit/assets/logos/logo-on-light.png               ← logo for light backgrounds
design-kit/assets/textures/grain-texture.png            ← optional grain overlay (512x512, tileable)
design-kit/design-tokens.md                             ← your brand colors, fonts, CSS variables
```

> **Fonts:** The default configuration uses Alfa Slab One (headlines) + Schoolbell (body). These are Google Fonts — easy to swap. Update the font names in Step 4's CSS to match your brand fonts. Load via Google Fonts in the HTML `<head>`.

> **Colors:** The default palette (purple, black, orange, white, lavender, peach) is a tested brand combination. Replace the 6 hex values in Step 4 with your brand colors.

---

## Routine Mode vs Standalone Mode

**How to detect:** If this skill was invoked by a routine command, it is in **routine mode** (autonomous — no pause for confirmation). If the user called it directly, it is in **standalone mode** (interactive — one-question checkpoint for missing critical fields).

---

## Step 1 — Read the design system

Read these files before generating anything (if they exist in your project):

1. `design-kit/design-tokens.md` — CSS variables, fonts, colors, spacing, grain texture
2. `design-kit/brand-identity.md` — brand personality, anti-patterns, pre-flight checklist
3. `design-kit/component-patterns.md` — HTML components (cards, pills, buttons, footers, pricing tables)

If these files don't exist, use the brand defaults defined in Step 4 and update them to match your brand.

**Default typography:** Alfa Slab One (headlines) + Schoolbell (body text). Load via Google Fonts. Swap with your own fonts as needed.

**Default colors (replace with your brand palette):**
- `#463187` — deep purple (signature — titles, anchors, pills, structure)
- `#2C262E` — near-black (dark backgrounds, body text on light)
- `#FF6719` — orange (accent — ONE pop per slide)
- `#FFFFFF` — white (light backgrounds, text on dark)
- `#E0D6FF` — lavender (soft backgrounds, fills)
- `#FFE8DC` — peach (warm backgrounds, fills)

---

## Step 2 — Read the Offer Doc

Read the Offer Doc from `inbox/outputs/` (most recent offer-doc file or the one the user specifies).

Extract these sections — they become slide content:

| Variable | Source Section |
|----------|---------------|
| Offer Name | ## Offer Name |
| Target Audience | ## Ideal Client |
| Core Problems (all) | ## Core Problems |
| Dream Outcome | ## Dream Outcome |
| Signature Transformation | ## Signature Transformation |
| One Outcome | ## One Outcome |
| Unique Mechanism | ## Unique Mechanism |
| Proven Path (phases) | ## Proven Path |
| Objections + Counters | ## Objections and Counters |
| Value Stack | ## Value Stack |
| Bonus Stack | ## Bonus Stack |
| Guarantee | ## Guarantee |
| Investment / Price | ## Investment |
| Urgency / Scarcity | ## Urgency / Scarcity |
| Next Steps / CTA | ## Next Steps |
| Competitive Positioning | ## Competitive Positioning |

Also read:
- `context/business-profile.md` — for bio, positioning statement
- `context/proof-and-results.md` — for testimonial quotes and client outcomes

If critical fields are missing, ask ONE question before continuing.

---

## Step 3 — Design the slide outline

**Do NOT use a fixed template.** The number of slides depends on the offer content.

### Slide selection logic

| Slide type | When to include | Mode |
|------------|----------------|------|
| Cover | Always | Dark |
| Problem | Always (combine if <3 problems, split if 4+) | Light (peach or white) |
| Vision / Big Promise | Always — the "what if" moment | Purple |
| What It Is | Always — the product/system overview | Light (lavender) |
| How It Works | Always — the proven path / process | Dark |
| Unique Mechanism | Include if the mechanism is strong and differentiated | Purple |
| Competitive | Include if there's a clear competitor to contrast against | Light (white) |
| Proof / Traction | Include if real numbers or usage data exist | Dark |
| Testimonial | Include if real quotes exist — skip if none | Light |
| About | Include for solopreneur offers — skip for product-only | Light (lavender) |
| Value Stack | Include if the stack is detailed enough | Dark |
| Pricing | Always | Dark |
| Guarantee | Include if guarantee is strong | Purple |
| CTA | Always — the closing slide | Purple |

**Typical range: 8-14 slides.** Never pad to hit a number. Every slide must move the deal forward.

**Mode alternation:** Dark → Light → Purple → Light → Dark → Purple → Light → Dark → Purple. The rhythm creates visual energy. Never put two same-mode slides next to each other.

---

## Step 4 — Build the HTML deck

### Brand assets to embed

Use actual file paths from your `design-kit/`. For HTML files, convert images to base64 data URIs so the deck is self-contained:

| Asset | Default Path | Usage |
|-------|-------------|-------|
| Profile photo | `design-kit/assets/my-photos/your-profile-photo.png` | About slide — circular clip with 4px brand-color border |
| Logo (dark bg) | `design-kit/assets/logos/logo-on-dark.png` | Cover slide top-right, dark slide footers |
| Logo (brand bg) | `design-kit/assets/logos/logo-on-brand.png` | Brand-color slide footers |
| Logo (light bg) | `design-kit/assets/logos/logo-on-light.png` | Light slide footers |
| Grain texture | `design-kit/assets/textures/grain-texture.png` | Tiled overlay on every slide (optional) |

**How to embed images as base64:**
```python
import base64
with open('path/to/image.png', 'rb') as f:
    b64 = base64.b64encode(f.read()).decode()
data_uri = f'data:image/png;base64,{b64}'
```

Use a Python script to read all assets, convert to base64, and inject into the HTML template. This makes the deck fully self-contained (no broken image links).

### HTML architecture

Each slide is a `<section>` element:
```html
<section class="slide mode-dark grain" style="...">
  <div class="content" style="position: relative; z-index: 2;">
    <!-- slide content -->
  </div>
</section>
```

- Slides: 1280x720px (16:9)
- All font sizes use `clamp()` for responsive scaling
- Spring animations on entrance (`cubic-bezier(0.34, 1.56, 0.64, 1)`)
- Hard shadows (`4px 4px 0px [brand-color]`) on cards and interactive elements
- Brand-color pills as section labels
- Accent color used once per slide max — for the most important element only

### Copy rules

- Headlines: short, punchy, headline font. Max 8 words.
- Body: body font everywhere. Conversational, not corporate.
- Pull exact copy from the Offer Doc — rewrite for slide brevity but keep the substance
- Testimonial quotes must be exact — never paraphrase
- Numbers are always in headline font, colored in accent

### Logo placement

- Cover slide: top-right corner, height 36px, opacity 0.9
- CTA slide: centered above contact info, height 48px
- Other slides: no logo (keeps it clean)

---

## Step 5 — Generate with Python script

1. Write a Python script that:
   - Reads all brand assets and converts to base64
   - Builds the complete HTML string with all slides
   - Saves to `inbox/outputs/html/YYYY-MM-DD-pitch-deck-[offer-name].html`

2. Execute the script with Bash

3. Open in Playwright browser, take a full-page screenshot for preview

4. Export PDF via Playwright browser_pdf_save

5. Save PDF to `inbox/outputs/pdf/YYYY-MM-DD-pitch-deck-[offer-name].pdf`

6. Delete the build script after successful generation

---

## Step 6 — Pre-flight checklist

Before presenting to the user, verify:

- [ ] Every headline uses your headline font, every body uses your body font? (no other fonts)
- [ ] Only your brand colors used? (no grays, blues, or invented colors)
- [ ] Grain texture visible on every slide background (if using)?
- [ ] Accent color appears max once per slide?
- [ ] Real profile photo on About slide (not placeholder)?
- [ ] Your logo on cover and CTA slides?
- [ ] Mode alternation creates rhythm? (no two same-mode slides adjacent)
- [ ] Every slide has real content from the Offer Doc? (no lorem ipsum, no "insert here")
- [ ] Would someone recognize this as your brand without reading the text?
- [ ] Does it feel bold and textured, not corporate and clean?

---

## Step 7 — Output

Report to user:
- HTML path: `inbox/outputs/html/YYYY-MM-DD-pitch-deck-[offer-name].html`
- PDF path: `inbox/outputs/pdf/YYYY-MM-DD-pitch-deck-[offer-name].pdf`
- Slide count + what each slide covers
- Screenshot preview

---

## assets/ folder

See `assets/README.md` for instructions on what brand files to add here.

---

## Edge Cases

- **No testimonials:** Skip testimonial slide, strengthen proof/traction slide instead
- **No case studies:** Skip competitive slide, expand unique mechanism
- **Solopreneur offer:** Include About slide with photo + bio
- **Multiple pricing tiers:** Expand pricing into its own slide with 3-column layout
- **User wants fewer slides:** Minimum viable = Cover + Problem + Vision + How It Works + Pricing + CTA (6 slides)
- **No proof data:** Be honest in the proof slide ("Built and tested on the builder's own business for X days") — never fabricate numbers
- **Offer Doc missing sections:** Ask user for the missing info rather than inventing content
- **Brand assets not found:** Warn the user and offer to generate a placeholder deck — note which files are missing
