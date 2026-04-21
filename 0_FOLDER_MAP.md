# 0 Folder Map — Agent Quick Reference

**Read this first.** This file maps every folder + file in this project so any agent can find what it needs without exploration. Updated April 21, 2026.

---

## 🚀 Most-used files (read these for context first)

| File | Why you read it |
|---|---|
| **CLAUDE.md** | Project conventions, tech stack, repo info, schema, lessons. ALWAYS read first. |
| **0_FOLDER_MAP.md** | This file — the index. |
| **index.html** | The entire frontend (HTML/CSS/JS in one file, ~3000 lines). All UI changes go here. |
| **Data/timeline_events_master.json** | Source-of-truth backup for the 60 timeline entries. Mirror of Firestore collection `skyways_history_and_story`. |
| **Data/live_stats.json** | Cron-generated Airtable snapshot (1565 flights / 503 hrs / 42968 km). Polled by the frontend every 60s. |
| **docs/STATS_AUDIT.md** | Last comprehensive audit of every numeric claim. Read before changing any stat. |

---

## 🗂 Project tree

```
Skyways Timeline/
├── 0_FOLDER_MAP.md           ← THIS FILE
├── CLAUDE.md                 ← project-wide rules + schema
├── index.html                ← frontend (single file)
├── aircraft_header.jpg       ← header background image (referenced from index.html)
├── nasa_bg.png               ← hero background (referenced from index.html)
├── hero_bg.png               ← legacy hero bg (kept for fallback)
│
├── Data/                     ← all data files
│   ├── timeline_events_master.json    ← 60 timeline entries (mirror of Firestore)
│   ├── live_stats.json                ← cron-generated Airtable snapshot
│   ├── media_mentions_master.json     ← Earned Media DB local backup
│   ├── skyways_fallback_images.json   ← thumbnail rotation pool
│   ├── url_verification_results.json  ← past URL-status audit results
│   ├── firestore.rules                ← deployed Firestore security rules
│   ├── Skyways Research Info/         ← research artifacts
│   └── Timeline Data/                 ← legacy timeline data
│
├── docs/                     ← all documentation
│   ├── PRD.md                ← product requirements doc
│   ├── FIRESTORE_SCHEMA.md   ← Firestore schema spec
│   ├── ACTION_PLAN_NEWSROOM_SYNC.md  ← newsroom action plan
│   ├── TIMELINE_REVIEW.md    ← Apr 21 cleanup review (TIER 1-6 findings)
│   ├── STATS_AUDIT.md        ← Apr 21 stats audit (PASS/FLAGGED/UNVERIFIED)
│   └── TIMELINE_MIGRATION_PLAN.md     ← legacy migration plan
│
├── scripts/                  ← active automation + sync scripts
│   ├── update_live_stats.py           ← cron: pull Airtable → Data/live_stats.json
│   ├── seed_firestore.py              ← initial seed (rarely re-run)
│   ├── sync_firestore_batch_abc.py    ← sync local JSON → Firestore (use for any data edit)
│   ├── cleanup_firestore_orphans.py   ← delete Firestore docs not in local JSON (after title renames)
│   ├── airtable_schema_sample.py      ← inspect Airtable field schema
│   ├── cleanup_batch_abc.py           ← Apr 21 Tier 1-4 cleanup script (reference template)
│   ├── cleanup_batch_d.py             ← Apr 21 dollar-in-title batch (reference template)
│   ├── cleanup_batch_e.py             ← Apr 21 Phase 10b bullets script (reference template)
│   └── oneoff/                        ← one-time analysis scripts (kept for reference)
│       ├── analyze_airtable.py
│       ├── count_tables.py
│       ├── list_tables.py
│       ├── max_flight.py
│       ├── sum_airtable.py
│       ├── sum_all_tables.py
│       ├── test_payload.py
│       └── test_sum.py
│
├── archive/                  ← deprecated files kept for reference
│   └── index_local_backup.html       ← old index.html backup (Apr 1)
│
├── Assets/                   ← (empty, reserved for future asset moves)
│
├── Founders Grotesk Family/  ← self-hosted font files (10 WOFF2)
├── Logos/                    ← brand logos + social banners + 3D models
├── .claude/                  ← Claude Code config
│   ├── launch.json           ← preview server config
│   └── serve.py              ← local preview server
├── .env.local                ← Airtable credentials (gitignored)
├── .gitignore
└── .git/
```

---

## 🔁 Common workflows

### Edit timeline data (titles, details, sources, etc.)
1. Edit `Data/timeline_events_master.json`
2. Run `python3 scripts/sync_firestore_batch_abc.py`
3. Run `python3 scripts/cleanup_firestore_orphans.py` (catches title-rename orphans)
4. `git commit && git push origin main`
5. Verify via REST: `curl -s "https://firestore.googleapis.com/v1/projects/marketing---earned-media-db/databases/(default)/documents/skyways_history_and_story?key=AIzaSyCSsKbZzs2xRSbZC_Ask_-8uX59GiDSnmw&pageSize=100"`

### Edit UI (CSS, JS, structure)
1. Edit `index.html`
2. Local verify: `python3 -m http.server 8767` + `curl -s http://localhost:8767/index.html | grep "<unique-string>"`
3. `git commit && git push origin main`
4. Wait for Vercel deploy (currently disconnected — see `memory/project_vercel_disconnect.md`)

### Refresh live flight stats
- Cron `skyways-timeline-live-stats` runs every 15 min calling `scripts/update_live_stats.py`
- Manual: `python3 scripts/update_live_stats.py [--force]`

### Add a new timeline entry
- See `memory/process_timeline_data_sync.md` for full Pattern C steps
- Always pick a fresh ID > 113 (last used)
- Doc ID format: `[YYYY-MM] Title with / replaced by -`

---

## 🎯 Where to find domain knowledge

| Question | Where |
|---|---|
| "How does Shae prefer to work?" | `~/.claude/projects/.../memory/feedback_collaboration_patterns.md` |
| "What contracts has Skyways won?" | `~/.claude/projects/.../memory/reference_skyways_contract_archive.md` |
| "How do I sync data to Firestore?" | `~/.claude/projects/.../memory/process_timeline_data_sync.md` |
| "Vercel not deploying?" | `~/.claude/projects/.../memory/project_vercel_disconnect.md` |
| "What CSS quirks should I know?" | `~/.claude/projects/.../memory/reference_timeline_css_quirks.md` |
| "How are sources marked internal vs public?" | `~/.claude/projects/.../memory/feedback_internal_marking_style.md` |
| "Charles trumps public sources rule" | `~/.claude/projects/.../memory/feedback_charles_trumps_public.md` |
| "Auto-fact-check before any proposal" | `~/.claude/projects/.../memory/feedback_auto_fact_check.md` |
| Research methodology | `~/.claude/projects/.../memory/feedback_research_patterns.md` |

---

## ⚙️ Hard rules to follow (most critical)

1. **No em dashes** in copy (titles, tags, details). Use `|`, `,`, `:`, `-`, or `()`.
2. **Always push** every commit to GitHub immediately (`git commit && git push origin main` chained).
3. **Always fact-check** before proposing any factual change — verification status (✓/⚠️/✗) inline.
4. **Charles trumps public sources** when they conflict — but always flag the discrepancy.
5. **Test before declaring done** — UI changes must be browser-verified.
6. **Mirror JSON ↔ Firestore** on every data edit. Mismatch = bugs.
7. **Lowercase categories** in JSON (`contracts`, not `Contracts`) — case-sensitive CSS class matching.
8. **Don't delete and re-seed** the whole Firestore collection — use PATCH or DELETE+CREATE per doc.

---

## 📦 External integrations

| System | Purpose | Auth | Where |
|---|---|---|---|
| Firestore (`marketing---earned-media-db`) | Timeline data + Earned Media DB | Service account JSON in `~/Desktop/Claude/Marketing - Earned Media DB/secrets/` | All data flows |
| Airtable (`appoHrNhrbURTxmuh`) | Live flight telemetry | PAT in `.env.local` | `scripts/update_live_stats.py` |
| GitHub (`skywaysinc/Skyways-timeline`) | Source code | SSH key (ed25519) | All git ops |
| Vercel | Hosting (currently disconnected) | OAuth via web | Auto-deploy on push (broken Apr 18+) |
| Slack (`skywaysworkspace`) | Internal context | MCP-managed | `mcp__fd5805e7-*__slack_*` tools |
| Google Drive | Internal docs (TAA letter etc.) | MCP-managed | `mcp__4f8ba24f-*__*` tools |
| Sanity.io | Newsroom CMS | Separate project | See `memory/project_sanity_migration.md` |

---

## 🔍 Where new things land

When building NEW work, default to these locations:
- **New script**: `scripts/<descriptive-name>.py` (or `scripts/oneoff/` if single-use)
- **New doc / report**: `docs/<NAME>.md`
- **New data file**: `Data/<name>.json`
- **New asset**: `Assets/<category>/<name>` (or `Logos/` if brand)
- **New memory**: `~/.claude/projects/-Users-shaewilson-Desktop-Claude-Marketing---Earned-Media-DB/memory/<type>_<topic>.md` + update `MEMORY.md` index

---

*Auto-generated April 21, 2026 during the line-by-line cleanup pass. If you reorganize this folder, update this file in the same commit.*
