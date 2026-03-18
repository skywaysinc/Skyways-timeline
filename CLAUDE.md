# Project: Skyways Timeline

## Repository
- GitHub: `git@github.com:skyways-shaewilson/Skyways-timeline.git`
- Branch: `main`
- Single-file project: `index.html` (no build tools, no package.json)
- SSH auth configured (ed25519 key)

## User: Shae Wilson
- Director of Marketing at Skyways Air Transportation Inc.
- Tests primarily on mobile (iPhone/Safari) — always validate mobile behavior
- Prefers concise, compact UI — single-line elements over multi-line blocks
- Wants changes pushed to GitHub immediately after each edit (no batching)
- Iterative workflow: edit → push → test on device → report issues → fix
- Does not want local dev servers — just edit files and push
- Prefers direct action over planning discussions — just do it

## Technical Lessons (Mobile Safari / iOS)
- NEVER put `overflow-x: hidden` on `html` or `body` — it breaks `position: sticky`
- Use `overflow-x: clip` on individual content containers instead
- Touch devices need explicit `click`/`touchstart` handlers — CSS `:hover` doesn't work
- Source dropdown menus need: tap to open, tap-outside to close, scroll to dismiss
- `min-width` on absolutely positioned elements can cause horizontal scroll — constrain with `calc(100vw - Npx)` or `max-width`
- Always include `-webkit-sticky` for Safari sticky positioning support

## Filter System
- Legend items in `.legend-row` use `data-filter` attribute matching `data-category` on event cards
- JS `toggleFilter()` function reads `data-category` from `.event-card` elements
- When adding new categories: update legend HTML, add CSS dot/tag color, add `data-category` to cards, add defense-specific color variables
- Current categories: `contracts`, `product`, `milestone`, `defense`

## Spreadsheet Export
- Uses openpyxl for .xlsx generation
- Hyperlinks: one per cell limitation — use separate Source 1/2/3 columns
- Source label → URL mapping extracted from HTML source-link elements
- Color-coded rows matching timeline category colors

## Content Accuracy Notes
- Cross Park Drive move was May 2021 (not Nov 2021)
- Facility after Cross Park is "Center Ridge Drive" not "Cross Park expanded"
- Event details should be thorough enough that clicking source links isn't required
- All dates and facts must match published sources
