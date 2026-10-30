# PrismCheck AI

PrismCheck AI is a pre-publication brand-governance review workspace. It reviews a caption, artwork, PDF, or DOCX against a structured brand kit, explains every finding with a citation to the exact rule, fact, or palette entry it breaks, and keeps a human in the loop with a draft → review → approval workflow.

- Live demo: https://tech-coders.onrender.com/
- Source: https://github.com/venkatanarayana15/tech-coders
- Team: A2Z Creators — Tech Circuit 2026, Round 3

## Demo credentials

All three demo accounts use the password `demo123`. The same credentials are shown on the sign-in page.

| Role | Email | Permissions |
| --- | --- | --- |
| Creator | `ananya@northwind.example` | Own drafts only: create, resolve findings, submit for review |
| Creator | `rohan@northwind.example` | Own drafts only: create, resolve findings, submit for review |
| Reviewer | `kabir@northwind.example` | See all drafts; approve or request changes on submitted drafts |
| Admin | `meera@northwind.example` | Everything above, plus editing the brand kit |

## Features

- Role-based demo sign-in with signed cookie sessions and server-side permission checks.
- Creator dashboard with live counts, search, filters, and priority queues.
- Brand kit reference with 7 rules, 5 approved facts, 5 palette colours, and 10 language entries, each addressable by ID.
- Admin brand-kit editor with version bumps and a 10-entry history trail.
- New review from a caption, artwork (PNG/JPG/WebP), PDF, or DOCX.
- PII masking at ingest for emails, phone numbers, and Aadhaar-style IDs.
- Deterministic checks: claims against the fact bank (C-01), banned guarantees (T-14), urgency/absolutes (T-02), preferred vocabulary (T-03), CIELAB palette distance (V-05), WCAG contrast and alt text (A-03).
- Citation Lock: every displayed finding resolves to a real kit item; uncited findings are dropped and counted.
- One-click fixes grounded in approved facts, or “keep as is” with a required note.
- Draft lifecycle with submission guard, reviewer approve/request-changes, approved-draft lock, and revision timeline.
- Re-run review against the current kit.
- Insights: citation coverage, most-flagged rules, most-overridden rules, ambiguous-guideline signal, decision rate, and average review time.

## Technology

| Layer | Choice |
| --- | --- |
| Frontend | React 18, Vite 5, handcrafted CSS |
| Backend | FastAPI 0.141, Python 3.14+ |
| Data | SQLModel + SQLite (JSON columns for kit/finding metadata) |
| Images | Pillow 12, numpy 2.5, CIELAB ΔE and WCAG contrast |
| Documents | pypdf 6 for PDFs, zip/XML extraction for DOCX |
| Auth | `itsdangerous` signed HttpOnly cookies |
| Model | Deterministic local engine by default; optional Gemini/Ollama adapters |

## Architecture

```
Browser (React SPA served by FastAPI)
      │  JSON / multipart
      ▼
FastAPI routes
      │
      ├── auth / roles / approval state machine
      ├── review engine (deterministic checks)
      ├── Citation Lock (drops uncited findings)
      ├── SQLite via SQLModel
      └── local file storage for uploads
```

The frontend production build lives in `frontend/dist` and is served by the same FastAPI process, so the deployed app is a single origin. The review engine runs in-process and makes no external model call by default; if a Gemini key or Ollama model is configured, its suggestions must still pass Citation Lock.

## Run locally

Prerequisites: Python 3.11+ and Node 20+.

```bash
# 1. Backend
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

```bash
# 2. Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 in development, or http://127.0.0.1:8000 after `npm run build` (the production bundle is served by FastAPI).

Environment variables (all optional):

| Variable | Default | Notes |
| --- | --- | --- |
| `PRISMCHECK_SECRET` | `dev-only-change-me` | Set a strong value in production |
| `PRISMCHECK_DB` | `backend/prismcheck.db` | SQLite file path |
| `PRISMCHECK_STORAGE` | `backend/storage` | Upload directory |
| `PRISMCHECK_MAX_UPLOAD_MB` | `8` | Upload limit |
| `PRISMCHECK_COOKIE_SECURE` | `false` | Set `true` behind HTTPS |
| `FRONTEND_DIST` | `../frontend/dist` | Built SPA directory |

## Tests and evaluation

```bash
python -m pytest backend/tests -q        # engine unit tests
python backend/evaluate.py               # synthetic-labelled review harness
```

The evaluation harness runs a deterministic set of 30 synthetic cases spanning clean copy, unsupported claims, banned guarantees, urgent tone, and preferred vocabulary, reporting precision, recall, F1, and false-positive rate. It is a repeatable measurement rig, not a real-world accuracy claim.

## Deployment

The repo includes a `render.yaml` blueprint for Render:

- Runtime: Python
- Build: `pip install -r backend/requirements.txt`
- Start: `uvicorn --app-dir backend app.main:app --host 0.0.0.0 --port $PORT`
- Health check: `/api/health`
- Env: `FRONTEND_DIST=frontend/dist`, `PRISMCHECK_COOKIE_SECURE=true`, `PRISMCHECK_SECRET` generated

SQLite is stored on the service's ephemeral filesystem unless a persistent disk is attached; attach a disk and point `PRISMCHECK_DB` and `PRISMCHECK_STORAGE` at it to preserve data across restarts.

## API summary

| Method | Path | Purpose |
| --- | --- | --- |
| POST | `/api/session` | Sign in with `{email, password}` or `{user_id}` |
| DELETE | `/api/session` | Sign out |
| GET | `/api/users` | Demo accounts (including demo password in demo mode) |
| GET | `/api/bootstrap` | Workspace bootstrap: user, stats, model, kit version |
| GET/PATCH | `/api/kit` | Read kit / admin-edited kit (versioned) |
| GET | `/api/drafts` | List drafts (creator-scoped) |
| GET | `/api/drafts/{id}` | Draft detail with findings and revisions |
| POST | `/api/drafts` | Create a draft (multipart) |
| POST | `/api/drafts/{id}/decisions` | Decide a finding (accept/keep) |
| POST | `/api/drafts/{id}/submit` | Submit for review (all findings resolved) |
| POST | `/api/drafts/{id}/approve` | Approve (reviewer/admin) |
| POST | `/api/drafts/{id}/request-changes` | Request changes (reviewer/admin) |
| POST | `/api/drafts/{id}/rerun` | Re-run review against current kit |
| GET | `/api/insights` | Aggregated review signals |

## Round 3 improvements

1. **Measured evaluation and false-positive reduction** — `backend/evaluate.py` plus overlap deduplication so a single clause cannot produce duplicate C-01 findings.
2. **Editable, versioned Brand Kit + Guideline Health** — admins can edit rules, facts, palette, banned/preferred language, and tolerance; every save bumps the version and appends a history snapshot.
3. **Failure recovery and reliability** — clear 4xx messages for bad uploads, empty documents, missing titles, duplicate actions, and locked drafts; engine unit tests; signed sessions that survive refresh.

## Known limitations

- Logo clear-space (L-01) is represented in the kit but is not yet enforced by a pixel-level check.
- Scanned/image-only PDFs are rejected with a clear error; OCR is not included.
- PII masking covers emails, phone numbers, and Aadhaar-style IDs; it is not a full compliance redaction engine.
- SQLite resets on deploy unless a persistent disk is attached.
- The evaluation harness is synthetic-labelled, not a real-world dataset.

## Roadmap

- Post-event: build the real 30-draft labelled set from pilot users and publish measured precision/recall.
- Next: OCR support, pixel-level logo clear-space checks, and exportable audit reports.
- Later: creative-suite integrations (Figma/Canva), video/audio review, publishing hand-off.
