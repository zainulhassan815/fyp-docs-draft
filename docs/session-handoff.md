# FYP Session Handoff

Last updated: 2026-08-24. Active focus: **supervisor feedback fixes on the report**
(see §7).

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
- **Page size**: report is **US Letter** (from SCET template); the uni formatting preset says **A4**. Unresolved.
- **Output filename**: the pipeline writes `build/SRS_Document.docx`; `scripts/build.sh` does not rename it, so copy to `build/Documentation.docx` after building.

## 6. Build gotchas
- **pandoc** must be installed (`brew install pandoc`).
- `python-docx`/`docxcompose` are not in system python (PEP 668). Create a scratchpad venv and run the build with it on PATH:
  ```
  python3 -m venv "$SCR/venv" && "$SCR/venv/bin/pip" install -q python-docx docxcompose
  PATH="$SCR/venv/bin:$PATH" bash scripts/build.sh
  ```
  (Running `scripts/build.sh` through a copied script breaks it: it resolves paths from its own location.)

## 7. Supervisor feedback (2026-08-24) - all six addressed
| Feedback | Fix |
|---|---|
| Explain ingestion pipeline | §5.2 rewritten: seven-stage walkthrough + **Table 5.2** (stage / input / processing / output), plus version-stamping and failure-severity rationale. |
| Add existing systems in table | §2.2's R1-R7 bullet blocks replaced by **Table 2.1** (ref / system / problem / methodology / features / limitations / relevance). Closes the missing-Table-2.1 gap; Table 6.2/6.3 renumbered to 6.1/6.2 to close the same gap in Ch. 6. |
| Unnecessary highlights and bolds | 44 mid-sentence `**bold**` spans stripped from `src/SRS_Document.md` (run-in labels at paragraph/bullet start kept - they act as sub-headings). Grey fill removed from fenced code blocks; blue accent caption colour changed to black. |
| No page number | New `scripts/add_page_numbers.py` puts a centred `{ PAGE }` field in the footer of every section; wired into `scripts/build.sh`. |
| Abstract too long | Cut 229 -> 158 words in `templates/cover.docx`. |
| Heading size less than paragraph | The SCET template left Heading 3+ with no size, so they inherited Normal (12 pt). `scripts/build-reference.sh` now pins H1 16 / H2 14 / H3 13 / H4 12 pt, bold Times New Roman, above the 12 pt body. |

Style/caption fixes live in `scripts/build-reference.sh` (which regenerates `templates/custom-reference.docx`), so re-running it will not clobber them.

## 8. Use-case cleanup (2026-08-24)
`UC-08 Receive Email` was in Table 3.3 but not in the diagram, so it was removed and
the list renumbered. Renumbering exposed a second, pre-existing defect: the FR->UC
column in Table 3.1 had been written against an older use-case list and was offset
(FR04 "upload files" pointed at *Search Documents*, FR10 "filter documents" at
*Create Job*, FR07-09 "search" at *Export to Excel*).

FR04/FR05/FR06 had **no** valid target at all: the diagram had no upload use case,
even though upload is the system's primary entry action, and the traceability row
carrying the upload tests (TC-DOCS-001/004/005) was mislabelled as *Search
Documents*. On the user's decision, **`Upload Document` was added to
`diagrams/use_case.drawio`** as UC-03 (HR Personnel actor), the diagram re-exported
to `src/images/use_case_diagram.png`, and every downstream reference realigned.

Final state: **12 use cases**, table and diagram in exact agreement, all 20 FRs
mapped to a semantically correct use case, and every traceability-matrix row
matching Table 3.3. Verify with the cross-check in git history for this commit.

**draw.io was not installed on this machine** - `brew install --cask drawio`. Export:
```
/Applications/draw.io.app/Contents/MacOS/draw.io -x -f png -s 3 --crop -b 20 -o OUT.png IN.drawio --no-sandbox
```
