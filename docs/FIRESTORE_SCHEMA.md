# Skyways Timeline — Firestore Schema

## Firebase Project
- **Project ID:** `marketing---earned-media-db` (shared with Earned Media DB — separate collection)
- **Collection:** `skyways_history_and_story`
- **Documents:** 54 events (as of April 2026)
- **Doc ID format:** `[YYYY-MM] Event Title` (two-digit months for sort order, `/` replaced with `-`)

---

## Document Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | Yes | Event headline. Use `\|` separators, no em dashes. |
| `date` | string | Yes | `YYYY-MM` format. Always equals `sort_date`. |
| `date_display` | string | Yes | `YYYY-MM` format. Always equals `sort_date`. |
| `year` | number | Yes | 4-digit year for grouping into year sections |
| `sort_date` | string | Yes | `YYYY-MM` format for chronological ordering |
| `category` | string | Yes | One of: `contracts`, `funding`, `product`, `milestone`, `defense` |
| `detail` | string | Yes | Full event description — fact-based, all acronyms spelled out |
| `tag` | string | Yes | Short label for the event tag chip (e.g., "Funding", "Internal") |
| `sources` | array | Yes | Array of `{label, url}` objects. URL is `null` for internal sources |
| `thumbnail` | string | No | URL to event image (source article image or Skyways fallback) |
| `thumbnail_status` | string | No | `fallback_hero`, `fallback_v2_ship`, `fallback_v3_hover`, etc. |

---

## Category Mapping

| Firestore `category` | Display Label | Dot Color |
|----------------------|---------------|-----------|
| `contracts` | Contracts | Blue (`--blue: #009AEB`) |
| `funding` | Funding | Green (`--green: #34A853`) |
| `product` | Product Development | Purple (`--purple: #6F52AE`) |
| `milestone` | Major Milestones | Teal (`--teal: #42C6C1`) |
| `defense` | Defense Milestones | Orange (`--orange: #FF9013`) |

---

## Source Object Shape

Public source:
```json
{
  "label": "FlyEye — Innovator Series",
  "url": "https://www.flyeye.io/skyways-autonomous-long-range-cargo-drones/"
}
```

Internal source (no public URL):
```json
{
  "label": "Skyways Internal — Charles Acknin",
  "url": null
}
```

No source available:
```json
{
  "label": "Skyways Internal — No Source",
  "url": null
}
```

---

## Example Document

**Doc ID:** `[2017-06] Y Combinator S17 Batch`

```json
{
  "title": "Y Combinator S17 Batch",
  "date": "2017-06",
  "date_display": "2017-06",
  "year": 2017,
  "sort_date": "2017-06",
  "category": "milestone",
  "detail": "Accepted into Y Combinator's Summer 2017 batch. Raised $120K pre-seed from Y Combinator and began building the initial aircraft prototypes in the Bay Area before relocating to Austin, TX.",
  "tag": "Milestone",
  "sources": [
    {"label": "Crunchbase", "url": "https://www.crunchbase.com/organization/skyways"},
    {"label": "FlyEye — Innovator Series", "url": "https://www.flyeye.io/skyways-autonomous-long-range-cargo-drones/"},
    {"label": "The Drone Girl — Inside Skyways (Nov 2025)", "url": "https://www.thedronegirl.com/2025/11/21/skyways/"}
  ],
  "thumbnail": "https://www.flyeye.io/wp-content/uploads/2025/10/Skyways-1028x685-1-e1760987568908-1000x600.webp",
  "thumbnail_status": null
}
```

---

## Firestore Security Rules

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /media_mentions/{document} {
      allow read: if true;
      allow write: if false;
    }
    match /skyways_history_and_story/{document} {
      allow read: if true;
      allow write: if false;
    }
    match /{document=**} {
      allow read, write: if false;
    }
  }
}
```

---

## Query Pattern (used in index.html)

The timeline uses the Firestore REST API (no SDK) with paginated fetches:
```
GET https://firestore.googleapis.com/v1/projects/marketing---earned-media-db/databases/(default)/documents/skyways_history_and_story?pageSize=100&key=API_KEY
```

Events are sorted client-side by `sort_date` after fetch.

---

## Thumbnail Fallback Images

7 Skyways website images rotated across cards without source thumbnails:

| Key | URL |
|-----|-----|
| hero | `https://www.skyways.com/_astro/hero.DmMP60zO_Z1mKK4i.webp` |
| v2_ship | `https://www.skyways.com/_astro/v2-aboard-ship.Dm1shnLv_ZVithb.webp` |
| v3_hover | `https://www.skyways.com/_astro/v3-hover.BZwWRBFB_t27Og.webp` |
| video_still | `https://www.skyways.com/_astro/video-still.KvHjdBXj_WuHxn.webp` |
| hype_still | `https://www.skyways.com/_astro/hype-still.zGCakefh_1kEicT.webp` |
| image1 | `https://www.skyways.com/_astro/image1.CXqs2Yt9_20n9Rg.webp` |
| image2 | `https://www.skyways.com/_astro/image2.CrwZsZIk_v3iRL.webp` |
| og | `https://www.skyways.com/og.png` |

Rule: No two consecutive cards should use the same thumbnail image.

---

## Content Rules
- Accuracy is #1 — every fact must be verifiable
- Charles Acknin corrections override published sources
- Details should be thorough enough that clicking source links isn't required
- No opinions, no editorializing — fact-based only
- All acronyms spelled out in full within each card's detail
- Titles use `|` separators, never em dashes
