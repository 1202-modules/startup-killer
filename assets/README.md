# assets/ — source prompts and dev-only master staging

The archive deliberately contains **no generated binary images yet**. Antigravity is authorized to generate them with its own image-generation tool during implementation, using the locked prompts in `assets/prompts/` and the `produce-game-assets` skill. This is production of static media ahead of the event, **not** image generation during play. The ten runtime hero images are derived from ten generated masters; UI event scenes are browser-generated SVG/CSS using those static heroes.

Do not upload uncompressed masters to the production site. After asset proof approval, local dev master outputs may be staged under `assets/source/` (excluded from deployed static assets), and compressed variants must be written to exact manifest paths under `apps/web/public/assets/startups/`.
