# Excalidraw Element Reference

Complete JSON specifications for all element types. This is the definitive guide for generating valid Excalidraw JSON data — adapted to Sabahudin's brand color system.

---

## CRITICAL RULES

### 1. One Visual = One Complete JSON File

Each visual must be a complete, self-contained Excalidraw file:

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "visual-coaching-skill",
  "elements": [ /* ALL elements */ ],
  "appState": {
    "viewBackgroundColor": "#FFFFFF",
    "gridSize": null
  },
  "files": {}
}
```

For clipboard paste format (if user prefers copy-paste):

```json
{
  "type": "excalidraw/clipboard",
  "elements": [ /* ALL elements for this section */ ],
  "files": {}
}
```

### 2. All Elements Share GroupIds

Every element in a logical group MUST have the same `groupIds` value.

```javascript
const groupId = `section${N}-group-${Math.random().toString(36).substr(2, 6)}`;
// Example: "section1-group-x7k2m"

// Apply to EVERY element in the group:
"groupIds": [groupId]
```

### 3. Frame Goes First (for slide-based visuals)

The slide frame (background rectangle) must be the FIRST element in the array.

### 4. Bound Elements Link Both Ways

When text is inside a shape:
- Container's `boundElements` lists the text: `[{ "id": "text-id", "type": "text" }]`
- Text's `containerId` points to container: `"containerId": "container-id"`

---

## Required Properties (ALL Elements)

Every element MUST include these properties:

```json
{
  "id": "unique-string-id",
  "type": "rectangle",
  "x": 100,
  "y": 100,
  "width": 200,
  "height": 80,
  "angle": 0,
  "strokeColor": "#463187",
  "backgroundColor": "#E0D6FF",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "seed": 1001,
  "version": 1,
  "versionNonce": 1,
  "isDeleted": false,
  "groupIds": ["section1-group-abc123"],
  "boundElements": null,
  "link": null,
  "locked": false
}
```

### Property Reference

| Property | Type | Description |
|----------|------|-------------|
| `id` | string | Unique identifier, use descriptive format: `s1-title`, `s1-box-email` |
| `type` | string | `rectangle`, `ellipse`, `diamond`, `text`, `arrow`, `line`, `freedraw` |
| `x`, `y` | number | Top-left corner position in canvas coordinates |
| `width`, `height` | number | Dimensions in pixels |
| `angle` | number | Rotation in radians (0 = no rotation) |
| `strokeColor` | string | Border/line color (hex) |
| `backgroundColor` | string | Fill color (hex) or `"transparent"` |
| `fillStyle` | string | `"solid"`, `"hachure"`, `"cross-hatch"`, `"dots"` |
| `strokeWidth` | number | Border thickness: 1 (thin), 2 (normal), 4 (bold) |
| `strokeStyle` | string | `"solid"`, `"dashed"`, `"dotted"` |
| `roughness` | number | Hand-drawn feel: 0 (clean), 1 (subtle), 2 (sketchy) |
| `opacity` | number | 0-100 (100 = fully opaque) |
| `seed` | number | Random seed for roughness (unique per element) |
| `version` | number | Always 1 for new elements |
| `versionNonce` | number | Always 1 for new elements |
| `isDeleted` | boolean | Always `false` |
| `groupIds` | array | Group membership: `["section1-group-xyz"]` |
| `boundElements` | array/null | Child elements bound to this container |
| `link` | string/null | URL link (usually `null`) |
| `locked` | boolean | Prevent editing (usually `false`) |

---

## Saba's Brand Color System

### Semantic Palette

| Role | Fill (bg) | Stroke | Use For |
|------|-----------|--------|---------|
| **Primary** | `#E0D6FF` | `#463187` | Main concepts, emphasis, key shapes |
| **Accent** | `#FFE8DC` | `#FF6719` | ONE emphasis point per section max |
| **Neutral** | `#FFFFFF` | `#C4B8F0` | Structural elements, backgrounds |
| **Canvas/Frame** | `#FFFFFF` | `#C4B8F0` | Slide frames |

### Text Colors

| Context | Color |
|---------|-------|
| All primary text | `#2C262E` |
| Secondary / muted text | `#8A7A8F` |
| On lavender background | `#463187` |

### Arrows and Connectors

| Purpose | strokeColor |
|---------|-------------|
| Primary flow/causation | `#463187` |
| Supporting connection | `#C4B8F0` |
| Emphasis arrow | `#FF6719` |

### Depth Layers

| Layer | strokeWidth | Fill | Use For |
|-------|-------------|------|---------|
| **Foreground** | 2-4 | `#E0D6FF` (lavender) | Primary focus |
| **Midground** | 1-2 | `#FFFFFF` (white) | Supporting elements |
| **Background/structure** | 1 | `#FFFFFF` (white) | Context, frames |

---

## Creative Element Usage

### Don't Just Build Boxes — Tell Visual Stories

| Element | Beyond Basic | Creative Applications |
|---------|--------------|----------------------|
| **Rectangle** | Not just "cards" | Platforms to stand on, building blocks stacking, windows/portals, road segments |
| **Ellipse** | Not just "bubbles" | Planets/orbits, spotlights, thought clouds, ripples, focal points |
| **Diamond** | Not just "decisions" | Gems/value, turning points, pivot moments, status indicators |
| **Arrow** | Not just "next step" | Growth trajectories, forces/pressure, cause->effect, transformation paths |
| **Line** | Not just "dividers" | Ground/horizon, connections, underlines for emphasis, paths walked |
| **Freedraw** | Not just "scribbles" | Handwritten emphasis, organic wrappers, circling things, energy/motion |

### Element Combinations for Metaphors

| Concept | Element Combination | How It Works |
|---------|---------------------|--------------|
| **Growth** | Rectangles stacking upward + upward arrow | Visualizes building/rising |
| **Transformation** | Diamond in center + radiating arrows | Shows change spreading outward |
| **Journey** | Curved line + small ellipses as waypoints | Path with milestones |
| **Core concept** | Large ellipse center + smaller ellipses + connecting lines | Hub and satellites |
| **Layers/Depth** | Nested rectangles (large->medium->small) | Onion/containment |
| **Tension** | Two shapes pulling opposite directions + stretched arrows | Visual conflict |
| **Funnel/Focus** | Wide shape narrowing to small shape + downward arrows | Convergence |
| **Cycle** | Ellipses in circle + curved arrows connecting them | Continuous loop |

---

## Element Types

### Rectangle

For: cards, containers, boxes, frames

```json
{
  "type": "rectangle",
  "id": "s1-card-1",
  "x": 100, "y": 100,
  "width": 200, "height": 80,
  "angle": 0,
  "strokeColor": "#463187",
  "backgroundColor": "#E0D6FF",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "roundness": { "type": 3 },
  "seed": 1001,
  "version": 1,
  "versionNonce": 1,
  "isDeleted": false,
  "groupIds": ["section1-group-abc"],
  "boundElements": null,
  "link": null,
  "locked": false
}
```

**Roundness options:**
- `{ "type": 3 }` — Rounded corners (use for cards, buttons, containers)
- `null` — Sharp corners (use for frames, technical diagrams)

---

### Ellipse

For: circles, ovals, organic blobs, hubs, nodes

```json
{
  "type": "ellipse",
  "id": "s1-hub-center",
  "x": 350, "y": 200,
  "width": 120, "height": 120,
  "angle": 0,
  "strokeColor": "#463187",
  "backgroundColor": "#E0D6FF",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "roundness": { "type": 2 },
  "seed": 1002,
  "version": 1,
  "versionNonce": 1,
  "isDeleted": false,
  "groupIds": ["section1-group-abc"],
  "boundElements": null,
  "link": null,
  "locked": false
}
```

**Note:** For perfect circle, use equal width and height.

---

### Diamond

For: decision points, emphasis, pivot moments, status indicators

```json
{
  "type": "diamond",
  "id": "s1-decision-1",
  "x": 200, "y": 150,
  "width": 100, "height": 100,
  "angle": 0,
  "strokeColor": "#FF6719",
  "backgroundColor": "#FFE8DC",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "roundness": { "type": 2 },
  "seed": 1003,
  "version": 1,
  "versionNonce": 1,
  "isDeleted": false,
  "groupIds": ["section1-group-abc"],
  "boundElements": null,
  "link": null,
  "locked": false
}
```

**Note:** Diamond with orange stroke = THE critical point. Use sparingly.

---

### Text (Standalone)

For: titles, labels, annotations, captions

```json
{
  "type": "text",
  "id": "s1-title",
  "x": 250, "y": 30,
  "width": 300, "height": 40,
  "angle": 0,
  "strokeColor": "#2C262E",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 1,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "text": "Visual Title Here",
  "fontSize": 32,
  "fontFamily": 2,
  "textAlign": "center",
  "verticalAlign": "top",
  "containerId": null,
  "originalText": "Visual Title Here",
  "lineHeight": 1.25,
  "seed": 1004,
  "version": 1,
  "versionNonce": 1,
  "isDeleted": false,
  "groupIds": ["section1-group-abc"],
  "boundElements": null,
  "link": null,
  "locked": false
}
```

**Font Sizes:**
| Context | fontSize | Estimated height |
|---------|----------|------------------|
| Main title | 28-36 | 35-45 |
| Section header | 20-24 | 25-30 |
| Body text | 14-18 | 18-22 |
| Small label | 12-14 | 15-18 |
| Annotation/caption | 10-12 | 12-15 |

**Font Families:**
- `1` — Virgil (handwritten — for casual/brainstorming visuals)
- `2` — Excalifont (recommended — clean default)
- `3` — Cascadia (monospace — for technical/code content)

**Text Alignment:**
- `textAlign`: `"left"`, `"center"`, `"right"`
- `verticalAlign`: `"top"`, `"middle"`, `"bottom"`

**Title text:** Use `strokeColor: "#463187"` (purple) for main titles
**Body text:** Use `strokeColor: "#2C262E"` (charcoal) for all other text
**Multi-line text:** Use `\n` for line breaks.

---

### Text (Bound to Container)

For: labels inside boxes, button text, card content

**The Container (with boundElements):**
```json
{
  "type": "rectangle",
  "id": "s1-box-email",
  "x": 100, "y": 100,
  "width": 160, "height": 60,
  "strokeColor": "#463187",
  "backgroundColor": "#E0D6FF",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "roundness": { "type": 3 },
  "seed": 1005,
  "version": 1,
  "versionNonce": 1,
  "isDeleted": false,
  "groupIds": ["section1-group-abc"],
  "boundElements": [
    { "id": "s1-label-email", "type": "text" }
  ],
  "link": null,
  "locked": false
}
```

**The Bound Text:**
```json
{
  "type": "text",
  "id": "s1-label-email",
  "x": 110, "y": 118,
  "width": 140, "height": 24,
  "strokeColor": "#2C262E",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 1,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "text": "Email",
  "fontSize": 16,
  "fontFamily": 2,
  "textAlign": "center",
  "verticalAlign": "middle",
  "containerId": "s1-box-email",
  "originalText": "Email",
  "lineHeight": 1.25,
  "seed": 1006,
  "version": 1,
  "versionNonce": 1,
  "isDeleted": false,
  "groupIds": ["section1-group-abc"],
  "boundElements": null,
  "link": null,
  "locked": false
}
```

**Bound Text Rules:**
- Text `x` = container `x` + 10 (padding)
- Text `y` = container `y` + (container `height` - text `height`) / 2 (centered)
- Text `width` = container `width` - 20 (padding)
- Container's `boundElements` MUST list the text
- Text's `containerId` MUST match container's `id`

---

### Arrow

For: connections, flows, causation, direction, process steps

```json
{
  "type": "arrow",
  "id": "s1-arrow-1",
  "x": 260, "y": 130,
  "width": 80, "height": 0,
  "angle": 0,
  "strokeColor": "#463187",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "roundness": { "type": 2 },
  "points": [[0, 0], [80, 0]],
  "startArrowhead": null,
  "endArrowhead": "arrow",
  "startBinding": null,
  "endBinding": null,
  "seed": 1007,
  "version": 1,
  "versionNonce": 1,
  "isDeleted": false,
  "groupIds": ["section1-group-abc"],
  "boundElements": null,
  "link": null,
  "locked": false
}
```

**Arrow Directions (via `points`):**

| Direction | Points Array |
|-----------|-------------|
| Right | `[[0, 0], [80, 0]]` |
| Left | `[[0, 0], [-80, 0]]` |
| Down | `[[0, 0], [0, 80]]` |
| Up | `[[0, 0], [0, -80]]` |
| Diagonal | `[[0, 0], [80, 60]]` |
| Curved | `[[0, 0], [40, -30], [80, 0]]` |

**Width/Height:** `width` = max X in points, `height` = max Y in points

**Arrowhead Types:** `null`, `"arrow"`, `"triangle"`, `"dot"`, `"bar"`

**Arrow color guide:**
- Primary flow: `#463187` (purple)
- Supporting connection: `#C4B8F0` (light purple)
- Emphasis/critical path: `#FF6719` (orange — use once)

---

### Line

For: dividers, underlines, connectors without direction

```json
{
  "type": "line",
  "id": "s1-divider",
  "x": 50, "y": 250,
  "width": 700, "height": 0,
  "angle": 0,
  "strokeColor": "#C4B8F0",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 1,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "roundness": { "type": 2 },
  "points": [[0, 0], [700, 0]],
  "seed": 1008,
  "version": 1,
  "versionNonce": 1,
  "isDeleted": false,
  "groupIds": ["section1-group-abc"],
  "boundElements": null,
  "link": null,
  "locked": false
}
```

---

### Freedraw

For: organic shapes, hand-drawn paths, emphasis marks, custom curves

```json
{
  "type": "freedraw",
  "id": "s1-sketch-1",
  "x": 100, "y": 200,
  "width": 150, "height": 80,
  "angle": 0,
  "strokeColor": "#FF6719",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "points": [
    [0, 40], [20, 20], [40, 50], [60, 10], [80, 45],
    [100, 15], [120, 40], [150, 30]
  ],
  "pressures": [0.5, 0.6, 0.7, 0.8, 0.7, 0.6, 0.5, 0.4],
  "seed": 1009,
  "version": 1,
  "versionNonce": 1,
  "isDeleted": false,
  "groupIds": ["section1-group-abc"],
  "boundElements": null,
  "link": null,
  "locked": false
}
```

---

### Frame (Slide Background)

For slide-based visuals, every slide starts with a frame rectangle — always FIRST in the elements array:

```json
{
  "type": "rectangle",
  "id": "s1-frame",
  "x": 0, "y": 0,
  "width": 800, "height": 500,
  "angle": 0,
  "strokeColor": "#C4B8F0",
  "backgroundColor": "#FFFFFF",
  "fillStyle": "solid",
  "strokeWidth": 1,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "roundness": { "type": 3 },
  "seed": 1000,
  "version": 1,
  "versionNonce": 1,
  "isDeleted": false,
  "groupIds": ["section1-group-abc"],
  "boundElements": null,
  "link": null,
  "locked": false
}
```

**Frame positioning by slide number:**
- Slide 1: x=0, y=0
- Slide 2: x=900, y=0
- Slide 3: x=0, y=600
- Slide 4: x=900, y=600

All elements within a slide are offset by the same x/y as the frame.

For single visuals (mindmaps, roadmaps), no frame is needed — elements float on the canvas.

---

## Sizing Standards

### Canvas Dimensions

- **Single slide:** 800 x 500 px
- **Gap between slides:** 100 px
- **Single visual (small):** ~1200 x 800 px
- **Single visual (medium):** ~1600 x 1000 px
- **Single visual (large):** ~2000 x 1400 px

### Element Dimensions

| Element Type | Width | Height |
|--------------|-------|--------|
| Slide frame | 800 | 500 |
| Large card | 200-280 | 80-160 |
| Medium card | 120-180 | 50-80 |
| Small card/badge | 60-100 | 30-50 |
| Hub circle | 100-140 | 100-140 |
| Icon placeholder | 40-60 | 40-60 |
| Mindmap center node | 160-220 | 80-120 |
| Mindmap branch node | 120-160 | 50-70 |
| Roadmap milestone | 140-180 | 60-80 |

### Spacing

| Context | Pixels |
|---------|--------|
| Between cards | 20-30 |
| Inside card padding | 10-15 |
| Title from top | 20-30 |
| Content zone start | 80 |
| Footer zone start | 430 |
| Mindmap branch gap | 40-60 |
| Roadmap phase gap | 80-120 |

---

## ID and Seed Conventions

### ID Format

```
s{sectionNum}-{elementType}-{descriptor}
```

Examples:
- `s1-frame` — Section 1 frame
- `s1-title` — Section 1 title text
- `s1-hub-center` — Section 1 center hub
- `s1-branch-setup` — Section 1, branch for "setup"
- `s1-label-setup` — Label inside setup branch
- `s1-arrow-1` — First arrow in section 1
- `s2-milestone-launch` — Section 2 milestone for "launch"

### Seed Ranges

| Section | Seed Range |
|---------|------------|
| Section 1 | 1000-1099 |
| Section 2 | 2000-2099 |
| Section 3 | 3000-3099 |
| Section 4 | 4000-4099 |

**Rule:** Increment by 1 within each section. No two elements share a seed.
