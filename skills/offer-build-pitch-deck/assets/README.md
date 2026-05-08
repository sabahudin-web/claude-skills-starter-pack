# Pitch Deck Assets

This folder holds brand assets used by the `offer-build-pitch-deck` skill to generate self-contained HTML/PDF pitch decks.

## What to add here

The skill reads assets from your `design-kit/` folder in the project root, **not from this folder directly**. This folder is here as a reference.

Set up your brand assets at these paths in your project:

```
design-kit/assets/my-photos/your-profile-photo.png
design-kit/assets/logos/logo-on-dark.png
design-kit/assets/logos/logo-on-brand.png
design-kit/assets/logos/logo-on-light.png
design-kit/assets/textures/grain-texture.png    ← optional, adds a paper texture feel
```

## What each file does

| File | Used on |
|------|---------|
| `your-profile-photo.png` | The "About" slide — shown in a circular clip |
| `logo-on-dark.png` | Cover slide and dark-mode slide footers |
| `logo-on-brand.png` | Brand-color slide footers |
| `logo-on-light.png` | Light-mode slide footers |
| `grain-texture.png` | Tiled overlay on all slide backgrounds — gives the deck a premium, textured feel |

## Tips

- Profile photo: square crop works best for circular clips. Minimum 400x400px.
- Logos: PNG with transparent background. The skill switches between dark/brand/light variants automatically based on slide mode.
- Grain texture: should be a tileable 512x512 RGBA PNG with transparency — so it overlays on any background color. If you don't have one, remove the grain overlay from the CSS in Step 4.
