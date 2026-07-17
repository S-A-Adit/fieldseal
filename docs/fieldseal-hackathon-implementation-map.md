# FieldSeal hackathon implementation map

This map compares the six-screen wireframe and 20-item delivery checklist with the fork at the start of `fieldseal-hackathon-demo`.

## Frozen three-minute scenario

The demo uses one clearly synthetic US residential case: a hardwired 48 A Level 2 EV charger on a dedicated 60 A, 240 V branch circuit at a fictional Bradenton, Florida residence. The fixture includes load calculation, permit/inspection placeholder, installation plan, electrical tests, commissioning, photographs, owner handover, FieldSeal commitment, and recorded Midnight preprod transaction metadata. All names, work, measurements, permit data, and locations are explicitly synthetic.

## Six-screen product map

| Wireframe screen | Existing implementation | Status | Hackathon action |
|---|---|---|---|
| 01 Manager overview | `static/index.html` overview, metrics, assignment queues; rendering in `static/app.js` | Working core | Rebrand and seed one US synthetic scenario |
| 02 Five-step assignment | `static/index.html` assignment workspace with steps 1–5 and previous/next navigation | Working core | Replace Norway-specific labels and validate the judge path |
| 03 Evidence capture | `POST /api/assignments/<id>/evidence`, private files, hashes, commitments, evidence timeline | Working core | Verify multi-worker synthetic evidence in browser |
| 04 Review gate | Planning and completion submission/review endpoints plus reviewer UI | Working core | Make approve/return state obvious in the demonstration |
| 05 Archive and sharing | Encrypted document packages, archive filters, recipient grants and revocation | Working core | Rebrand and simplify the seeded handover state |
| 06 Recipient verification | `/en/demo-report`, `/api/public/midnight-demo`, verify button and controlled handover | Working and visually verified | FieldSeal identity pass completed first; preserve safe API boundary |

## Delivery checklist baseline

### Product and demo

- **US synthetic scenario:** Partial. The public report is English but still contains Norwegian company and electrical/EKOM assumptions.
- **Five-step journey and roles:** Implemented in the application and documented in the wireframe.
- **Three-minute walkthrough:** Not yet scripted or timed.
- **Screenshots/video:** Not yet produced.
- **Submission copy/credits:** README now includes upstream credit; final submission copy remains.

### FieldSeal application

- **Create and assign work order:** Implemented and covered by `workflow_smoke.py`.
- **Timestamped multi-worker evidence:** Backend and timeline implemented; demo click-through still needed.
- **Professionally responsible person:** Team endpoint and UI implemented.
- **Approve and issue encrypted report:** Implemented and covered by the smoke workflow.
- **Open protected report as recipient:** Implemented; public synthetic recipient view is available.

### Midnight proof

- **Canonical salted commitment:** Implemented by `document_commitment()` and tested.
- **Submit/confirm preprod receipt:** Queue, worker API, and Compact pilot exist. Local smoke uses a synthetic worker result; a fresh live preprod transaction is a separate verification gate.
- **Verify unchanged report:** Implemented and tested.
- **Changed-report failure:** Implemented and tested by manifest tampering in `workflow_smoke.py`.
- **Revocation without content publication:** Implemented and tested through register/revoke worker operations.

### Quality and safety

- **Complete smoke test:** Passing on the working branch.
- **Desktop/mobile layout:** Desktop public report and wireframe verified in a real browser; dedicated mobile click-through remains.
- **Repository hygiene:** `.gitignore` excludes runtime data, secrets, private state, generated contract artifacts, caches, and virtual environments.
- **Public API safety:** Smoke coverage asserts the synthetic public endpoint and controlled fields; continue reviewing after any payload change.
- **Preprod fallback:** `visual_preview.py` provides a clearly labeled local synthetic confirmed-preprod fixture, not a claim of a new transaction.

## Completed implementation batches

### Batch 1 — public proof path

1. Added the corrected FieldSeal wireframe as a tracked planning artifact.
2. Rebranded the public verification report and all its locale copy to FieldSeal.
3. Exported both the new and previous locale globals and kept the reader fallback, allowing mixed cached asset versions during the transition.
4. Updated the README with the US-market demo path, privacy boundary, upstream credit, and preprod compatibility warning.
5. Extended smoke assertions for the new branded public assets and reran the full workflow.

### Batch 2 — primary application identity

1. Rebranded the SPA header, page title, login page, join page, archive privacy copy, and evidence privacy copy.
2. Updated PWA manifest metadata to FieldSeal.
3. Rebranded the synthetic archive/share/recipient presentation without changing its storage identifiers.
4. Bumped application and translation asset versions, synchronized the service-worker precache, and advanced the cache generation to prevent stale cached branding.
5. Added smoke coverage for the SPA, PWA manifest, login identity, translated privacy copy, and new asset versions.
6. Kept `ESENSE_*`, schemas, database paths, browser storage keys, service names, and deployment paths unchanged for compatibility.

## Midnight audit guardrails

- Repository smoke tests prove the local queue/result lifecycle with synthetic transaction metadata; they are not evidence of a fresh live preprod transaction.
- The CLI `verify` command reads public contract state; do not describe it as generating a private validity proof.
- Do not run `test:preprod` casually. It deploys and mutates live preprod state, and the current test must be hardened to require an explicit issuer secret before use.
- Keep the proof server loopback-only and keep wallet seed, issuer secret, and private-state password outside the Flask environment.
- Treat Python canonical JSON as a protocol boundary. Add golden vectors before implementing commitment generation in another language.
- Generated contract bindings, wallet caches, private state, deployment secrets, and live runtime records remain excluded from version control.

## Explicit compatibility boundary

Do not globally rename `ESENSE_*`, schema strings, database paths, worker service names, or deployment paths during the first hackathon batch. Public identity can move to FieldSeal while these identifiers remain compatible and are migrated later with aliases and focused deployment tests.
