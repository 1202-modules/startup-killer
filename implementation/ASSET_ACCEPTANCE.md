# ASSET_ACCEPTANCE.md — критерии генерации и принятия ассетов

## Production gates
1. `proof`: first render **CoffeeBot** and **PetMind** using exact fixed prompts and style anchor. Create browser mock screenshots at desktop 1440×900 and mobile 360×800. Present 2-image contact sheet to project owner. No generation of other 8 before proof approval.
2. `batch`: generate remaining eight using same lighting/style reference and the fixed per-startup prompts. At most 2 regeneration attempts per asset for clearly failed output; thereafter escalate, do not improvise style.
3. `format`: from each master produce `hero-desktop.webp` 1280×800, `hero-mobile.webp` 600×750 (central 4:5), and `thumb.webp` 320×320. Correct orientation, no upscaling beyond the actual source without approval. Optimize outside production server.
4. `integrate`: source names are exact `asset_key`s, public paths exactly as in manifest; UI uses `<picture>` by viewport, fallback static graphic only for transient load failure. No placeholder permitted in release.
5. `verify`: all 30 files exist, can be decoded, have expected dimensions, size caps respected, no wrong or duplicate pictures, image fingerprints recorded in build report; cross-check all 10 `asset_key`s against `data/startups.json`.

## Quality checklist — each rendered master must pass all
- Photorealistic high-end commercial 3D CGI, not stylized/flat cartoon.
- Physically sensible product and intended business recognisable; no switching industry.
- Consistent graphite/coal-blue dark studio language across all ten; lime restrained, amber subtle. The approved CoffeeBot render is style-only reference where supported.
- 16:10 landscape with subject completely inside central 45%, **mobile 4:5 center crop** preserves all important product details.
- No readable text/digits/watermarks/trademarks, no recognisable individuals, no anatomy mistakes, no visually impossible hardware. Brand logo and title must be HTML.
- Clean foreground-background separation; text overlay only outside image or with contrast-tested scrim.
- Image should not look misleadingly like an official ad for any real company.

## Performance/quality trade-off
Absolute per-image caps: desktop <=350 KiB, mobile <=200 KiB, thumb <=50 KiB; if meaningful product detail becomes unreadable at cap, record actual quality/size trade-off and ask owner before altering caps. **Do not ship a 3–5 MB PNG/AVIF master to browsers.** Preload only current startup hero; the other 9 and their event art are never initial downloads. Never run imagemagick or frontend build on the 2-GB production host unless a measured exception is approved.

## Runtime fallback vs unfinished work
Development placeholders are allowed for UI integration while proof approval is pending and must be visibly tagged DEV_ONLY. The released app must use the approved render; unavailable generator => asset task blocked, not permission to use internet stock. Avoid breaking a saved session if image fails to load: use a lightweight monochrome placeholder at runtime, report image error and keep game operational.

## Release report template
Record: generator/tool used; approval reference for proof pair; versioned master paths; for each slug: image dimensions, compressed sizes, SHA-256, crop screenshot reviewed, pass/fail flags; all 30 paths; total initial viewport bytes measured and reduced-motion acceptance. Do not invent a report if tool or assets not available.
