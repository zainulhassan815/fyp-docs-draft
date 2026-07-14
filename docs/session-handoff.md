# FYP Session Handoff

Last updated: 2026-07-14. Active focus: **rebuilding all report diagrams in draw.io
standard UML/ER/DFD notation** (the prof rejected the previous versions).

## 1. Project at a glance
- Report: **Hireflow — AI Powered HR Screening and Document Retrieval System Using RAG** (BSCS, SCET).
- Source of truth: `src/SRS_Document.md` → built to `build/SRS_Document.docx`.
- Product code lives in the nested clone `hireflow/` and on GitHub: <https://github.com/zainulhassan815/hireflow>.
- Team/supervisors/deadlines are in agent memory (`fyp-team-and-title`, `fyp-deadlines-requirements`).

## 2. How the report builds
`./scripts/build.sh` runs, in order:
1. `pandoc src/SRS_Document.md -o build/SRS_Document.docx --reference-doc=templates/custom-reference.docx --lua-filter=scripts/docx-filter.lua --toc --toc-depth=3`
2. `scripts/merge_cover.py` — prepends `templates/cover.docx` (front matter) and swaps in the reference styles.xml
3. `scripts/autofit_tables.py` — tables to 100% width + graduated font (wide tables shrink)
4. `scripts/style_captions.py` — relabels "Table N.N:" paragraphs to the `Table Caption` style (for a List of Tables)
5. `scripts/justify_paragraphs.py` — justifies body prose only (skips headings/code/captions/tables; skips explicitly-aligned paras so the centred cover title is preserved)

**Python deps gotcha:** `python-docx`/`docxcompose` are NOT in system python (PEP 668). Use a venv:
```
SCR=/private/tmp/claude-502/-Users-zainulhassan-Downloads-Documents-FYP/<session>/scratchpad
python3 -m venv "$SCR/venv" && "$SCR/venv/bin/pip" install -q python-docx docxcompose
```
The scratchpad venv gets wiped between sessions — recreate it, then run the 4 python steps with `"$SCR/venv/bin/python" scripts/<name>.py`.

`templates/custom-reference.docx` is regenerated from the SCET template by `scripts/build-reference.sh` (SCET styles + pandoc styles + bordered Table style).

## 3. Report content status — COMPLETE
- **0 placeholders left.** Real 6.3 performance benchmarks are in (GPU RTX 5050 dev stack). Appendix B → GitHub repo. Appendix A → "user manual attached separately".
- Prose humanized; **no em/en dashes**. Body justified. Cover (`cover.docx`) fully built: title page, industrial approval certificate (embedded `src/images/approval-certificate.png`), declaration, plagiarism, dedication, acknowledgements, abstract.

## 4. Diagrams — the active task
**Tooling:** draw.io desktop is installed. Sources in `diagrams/*.drawio`, export with:
```
/Applications/draw.io.app/Contents/MacOS/draw.io -x -f png -s 3 --crop -b 20 -o OUT.png IN.drawio --no-sandbox
```
(`-s 2` while iterating, `-s 3` for the final saved PNG.) Render to scratchpad to review, then export to `src/images/` when approved.

**Style (locked):** black-and-white. White fill (`#ffffff`), black stroke (`#000000`/`#1A1A1A`), black font. Standard notation, minimal, no colour. Back up any image being replaced as `*_old.*`.

### Done (draw.io, standard notation)
| Diagram | Source | Exported PNG | Report figure |
|---|---|---|---|
| Activity (swimlanes: HR User / Backend / Async Worker & AI; 3 decision diamonds: Valid credentials?, Confidence ≥ 0.4?, Relevant chunks found?) | `diagrams/activity.drawio` | `src/images/activity_diagram.png` | Fig 4.6 ✅ |
| Use Case (HR Personnel + Email Service actors, 11 use cases in "Hireflow System" boundary, «extend» Filter→Search, «include» Read Resumes→Sync Resumes; Receive Email removed) | `diagrams/use_case.drawio` | `src/images/use_case_diagram.png` | Fig 3.1 ✅ |
| Class (10 classes w/ attribute compartments, composition diamonds, multiplicities, Application as associative class) | `diagrams/class.drawio` | `src/images/class.png` | Fig 4.5 ✅ |
| ERD (11 tables from real SQLAlchemy models, PK/FK cols, crow's-foot edges; nullable SET-NULL rels use zero-to-one/zero-to-many markers; users central, applications as assoc. entity) | `diagrams/erd.drawio` | `src/images/erd.png` (old → `erd_old.png`) | Fig 4.9 ✅ |
| Sequence — **generalized SYSTEM sequence** (prof asked it to "cover system"): 7 lifelines (HR User, Web App, Backend API, Async Worker, Data Stores, LLM Provider, Gmail), 5 scenario frames (Authenticate, Upload & async index, RAG Q&A, Match candidates, Gmail sync); sync=filled arrow, return=dashed open, async/SSE=open arrow. RAG-only deep-dive version preserved at `diagrams/sequence_rag.drawio`. | `diagrams/sequence.drawio` | `src/images/sequence_diagram.png` (old → `sequence_diagram_old.png`) | Fig 4.8 ✅ |
| System Architecture — **high-level general** block diagram (user wanted the detailed layered view moved to the component diagram; keep 4.1 general): Client (Web Browser · React SPA) ↔ Hireflow Application Server (FastAPI + Celery) → Data Stores (PostgreSQL · ChromaDB · Redis · MinIO) + **External Services (LLM Provider Claude/Ollama · Gmail Email Service)**. 4 boxes only. | `diagrams/architecture.drawio` | `src/images/architecture_diagram.png` (old → `architecture_diagram_old.png`) | Fig 4.1 ✅ |
| Component — the detailed **layered view repurposed as a proper UML component diagram** (user: "this looks more like a component diagram, keep it as component"): `«component»` stereotype + component icons on React SPA, nginx, API/Service/Domain/Adapter layers, Celery Worker, PostgreSQL/ChromaDB/Redis/MinIO, LLM Provider, **Gmail (Email Service)**; dashed `«use»`/dependency arrows. Grouping rectangles = FastAPI Backend / Data & Infrastructure / External Systems. | `diagrams/component.drawio` | `src/images/component_diagram.png` (old → `component_diagram_old.png`) | Fig 4.7 ✅ |
| DFD Level 0 (context) — Gane-Sarson: 1 process (0 Hireflow System), 3 external entities (HR User/Admin, Gmail Service, LLM Provider), directional labeled flows. **SRS ref repointed `.jpeg`→`.png`.** | `diagrams/dfd_level_0.drawio` | `src/images/dfd_level_0.png` (old → `dfd_level_0_old.jpeg`) | Fig 4.2 ✅ |
| DFD Level 1 — 6 processes (Auth, Doc Ingestion, Hybrid Search & RAG, Job & Candidate Mgmt, Gmail Sync, Activity Logging), 8 data stores (D1 Users, D2 Documents, D3 Candidates, D4 Jobs, D5 Applications, D6 Vector Collection, D7 Activity Log, D8 Object Store), 3 external entities. | `diagrams/dfd_level_1.drawio` | `src/images/dfd_level_1.png` (old → `dfd_level_1_old.png`) | Fig 4.3 ✅ |
| DFD Level 2 — document-processing & retrieval subsystem: ingestion pipeline (2.1 extract → 2.2 persist → 2.3 classify → 2.4 chunk → 2.5 contextualise → 2.6 embed → 2.7 index) + query pipeline (3.1 parse → 3.2 vector → 3.3 lexical FTS → 3.4 metadata filter → 3.5 fuzzy fallback → 3.6 RRF fusion → 3.7 answer gen); stores D8/D2/D6; LLM external. | `diagrams/dfd_level_2.drawio` | `src/images/dfd_level_2.png` (old → `dfd_level_2_old.png`) | Fig 4.4 ✅ |

### Remaining
**All report diagrams are now rebuilt in draw.io standard notation.** Final steps: rebuild the docx (`./scripts/build.sh` via venv) and confirm 0 placeholders / valid output. Open items in §5 (Table 3.3 UC-08, page size A4 vs Letter, List of Figures/Tables) still pending user decisions.

### draw.io notation cheat-sheet (used so far)
- Initial node: `ellipse;fillColor=#000000;strokeColor=#000000`. Final: `shape=endState;fillColor=#000000`.
- Action: `rounded=1;arcSize=50`. Decision: `rhombus`. Control flow: `edgeStyle=orthogonalEdgeStyle;endArrow=open;endFill=0`.
- Swimlane: `swimlane;horizontal=1;startSize=34;fillColor=#ffffff` (activities placed as children of root `1`, positioned inside lane x-ranges; edges reference node ids).
- Actor: `shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top`. Use case: `ellipse`. Boundary: rectangle `fillColor=none;verticalAlign=top`. Association: `endArrow=none`. «extend»/«include»: `dashed=1;endArrow=open` with `«...»` label.
- Class: `swimlane;childLayout=stackLayout;startSize=26` (title) + `text;align=left` child for attributes. Composition: `startArrow=diamondThin;startFill=1`. Multiplicity: `edgeLabel` child cells with `mxGeometry x=±0.85 relative=1`.
- Constrain edge ends with `exitX/exitY/entryX/entryY` to avoid lines crossing shapes; add `<Array as="points">` waypoints for clean orthogonal routing.

## 5. Open items / decisions pending
- **Table 3.3** still lists **UC-08 Receive Email** (removed from the use-case diagram). Recommended: remove it from the table + renumber so text matches the diagram. NOT yet done (waiting on user OK).
- **Page size**: report is **US Letter** (from SCET template); the uni formatting preset says **A4**. Unresolved.
- **List of Figures / List of Tables**: caption styles are now distinct (`Image Caption`, `Table Caption`), so in Word: References → Insert Table of Figures → Options → From style. Not auto-inserted (offered a build-time field-injection option; declined so far).
- **Output filename**: user renamed the build to `build/Documentation.docx` (kept open in Word). The pipeline still writes `build/SRS_Document.docx`; copy/rename after building.
- Superseded: earlier `diagrams/*.d2` files and the user's 4 hand-styled PNGs (class/component/erd/sequence) are being replaced by the draw.io rebuilds.

## 6. Suggested next step
**All diagrams are rebuilt in draw.io** (Activity, Use Case, Class, ERD, Sequence, Architecture, Component, DFD 0/1/2). Next: run a final `./scripts/build.sh` (via scratchpad venv — see §2) to regenerate `build/SRS_Document.docx`, confirm 0 placeholders and a valid docx, then copy/rename to `build/Documentation.docx`. Resolve the §5 open items with the user (Table 3.3 UC-08 removal, A4 vs Letter, List of Figures/Tables insertion) when they're ready.
