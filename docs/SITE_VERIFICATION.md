# Site Functionality Verification — April 21, 2026

**Method**: Structural code verification (Chrome MCP not connected; Claude Preview sandbox-blocked). Static analysis of `index.html` + Firestore REST API + live_stats.json checks across local server and live deploy.

---

## ✅ Structural code checks (all features present)

| Feature | Selector / Function | Status |
|---|---|---|
| Search bar | `searchInput` | ✓ Present |
| Search highlight | `highlight` (function) | ✓ Present |
| Filter chips | `toggleFilter()` | ✓ Present |
| Stat menu hover/tap | `bindStatMenus` (IIFE) | ✓ Present |
| Source dropdown | `.sources-trigger` | ✓ Present |
| Internal banner | `isInternalSource()` | ✓ Present |
| Card click navigation | `scrollToContract()` | ✓ Present |
| Year sticky labels | `updateYearLabels()` | ✓ Present |
| Year fade animation | `syncYearLabelOffset()` | ✓ Present |
| **Bullets renderer** | `.event-bullets` + `Array.isArray(ev.bullets)` | ✓ **NEW (Phase 10b)** |
| Live flight stats | `Data/live_stats.json` polling | ✓ Present |
| Stat menu drawer-active | `.drawer-active` class | ✓ Present |
| ResizeObserver year sync | `ResizeObserver` | ✓ Present |
| Fallback STATS | `STATS_FALLBACK` constant | ✓ Present |
| Charles inline render | `charlesInlineEligible` (line 2090) | ✓ Present |

---

## 📱 Mobile / responsive breakpoints

| Breakpoint | Lines | Purpose |
|---|---|---|
| `@media (max-width: 1024px)` | 1402 | Tablet adjustments |
| `@media (max-width: 720px)` | 804, 1271, 1450 | Mobile (primary breakpoint per CLAUDE.md) |
| `@media (max-width: 767px)` | 1460 | Mobile fallback (close to 720px, may be redundant) |

All key responsive adjustments are wired. Per CLAUDE.md the primary mobile target is iPhone Safari at ~720px or smaller. **Recommend manual smoke test on iPhone** since I can't visually verify.

---

## ⚠️ Vercel deploy lag (known issue)

| File | Local | Live (skyways-timeline.vercel.app) | Δ |
|---|---|---|---|
| `live_stats.json` lifetimeFlights | 1565 | 1561 | -4 |
| `live_stats.json` flightTimeHours | 503.3 | 502.4 | -0.9 |
| `live_stats.json` kmFlown | 42,967.5 | 42,895.3 | -72.2 |
| `live_stats.json` updatedAt | 2026-04-20 14:25 UTC | 2026-04-16 16:15 UTC | -4 days |

**Diagnosis**: Vercel auto-deploy is stale since the April 18 security incident (per `memory/project_vercel_disconnect.md`). All recent commits (54b4d43, 25c9d98, 0c6ee2f, fee961c, 4029729) are on GitHub but not deployed.

**Impact**: Until Vercel is reconnected:
- ✗ Stat banner shows old flight counts
- ✗ Drawer copy bullets (Phase 10a) not visible
- ✗ Card detail bullets (Phase 10b) not visible
- ✓ Title rewrites + tag fixes ARE visible (those changes go through Firestore which serves live)
- ✓ Source URL fixes visible
- ✓ Tag em dash fixes visible

**Fix needed**: Reconnect GitHub→Vercel integration in Vercel dashboard.

---

## ✅ Firestore data layer (verified live)

```
Total docs: 60 (matches local JSON ✓)
Docs with bullets: 9 (matches Phase 10b plan ✓)
Sample with bullets: id=13 (4), id=19 (6), id=22 (5)
```

All Phase 1-10b data changes confirmed live in Firestore via REST API.

---

## 🧪 What I COULDN'T test (needs browser)

| Test | Why blocked |
|---|---|
| Visual layout on iPhone Safari | No mobile device automation; recommend manual |
| Touch interactions (tap-open, tap-close) | No touch simulator |
| Scroll bounce / stutter | Need browser scroll behavior |
| Stat menu hover transitions | Need cursor input |
| Year fade behavior | Need scroll context |
| Bullet rendering visual quality | Vercel stale; can't see live |
| Search highlight behavior | Visual + dynamic |

**Recommend**: 5-min Shae smoke test once Vercel reconnects:
1. Load on desktop Chrome — verify drawer bullets render in stat menus
2. Load on iPhone — scroll through entire timeline
3. Hover (or tap) on a contract card with bullets (e.g., "DIU/USN OTA") — verify bullets render
4. Search "Navy" — verify count + highlight
5. Tap a stat ("$46M+") — verify drawer opens cleanly
6. Tap a contract row in the drawer — verify scroll-to-card works

---

## Summary

- **Code-level**: All features wired correctly. Phase 10b renderer change is in place.
- **Data-level**: Firestore is the source of truth. All 60 docs match local JSON. 9 docs have bullets.
- **Live data lag**: Vercel disconnect blocks the index.html changes (drawer rewrites, card bullets, renderer change) from showing on the live site. Title/tag/source changes ARE live (they flow through Firestore).
- **Visual/touch testing**: Requires browser — recommend a 5-minute manual smoke test from Shae.
