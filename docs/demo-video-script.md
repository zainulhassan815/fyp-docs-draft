# Hireflow — Project Demo Video Script (rough, ~9 min)

Target: 8–10 min (max 12). Full HD, 16:9 landscape, clean screen recording, external mic,
confident English. Structure follows *Guidelines for Project Demo Video.pdf*.

**Before recording:** pre-seed the app with a few documents, one job, some candidates, and a
live Gmail connection so nothing loads empty. Rehearse the demo once end-to-end so there is no
dead time while things load. Move the mouse slowly; pre-type or paste long search questions.

Speaking parts are split across the team — reassign freely.

---

## 0:00–0:30 — Introduction  *(Zain)*
> "Assalam-o-Alaikum. We are from the Department of Computer Science, Sharif College of
> Engineering & Technology, Lahore, affiliated with UET Lahore. Our final year project is
> **Hireflow — an AI-Powered HR Screening and Document Retrieval System using RAG**. The team is
> Amna Ikram, Zain Ul Hassan, and Ezza Ansar, supervised by Ms. Hirra Mustafa and co-supervised
> by Dr. Mazhar Iqbal."

`[SCREEN: title slide — project title, crest, names, supervisors]`

## 0:30–1:30 — Problem Statement  *(Amna)*
> "HR teams manage large volumes of unstructured documents — resumes, reports, scanned files —
> and spend most of their time manually reviewing resumes, on average around 23 hours to fill one
> position. Keyword search only matches exact words, so a search for 'machine learning engineer'
> misses a strong candidate who wrote 'ML researcher'. The information is scattered, review is
> inconsistent, and existing tools can't answer plain-language questions over a company's own
> documents with any proof of where the answer came from."

`[SCREEN: problem slide, or the standee's Introduction section]`

## 1:30–2:00 — Objectives  *(Amna)*
> "Hireflow set out to let HR staff ingest PDF, Word, and scanned documents with OCR; search them
> semantically; ask natural-language questions and get grounded, source-cited answers;
> automatically screen and rank candidates against a job; and pull candidates straight from Gmail."

`[SCREEN: objectives bullets]`

## 2:00–2:30 — Technologies Used  *(Ezza)*
> "The backend is a layered FastAPI application with Celery workers for async processing. We use
> PostgreSQL for metadata and full-text search, ChromaDB as the vector store, Redis, and MinIO for
> file storage. Embeddings come from sentence-transformers, OCR from Tesseract and PyMuPDF, and
> answer generation from Anthropic Claude. The frontend is a React 19 single-page app."

`[SCREEN: architecture or component diagram from the report]`

## 2:30–7:30 — Live Demonstration (5 min)  *(Zain drives; narrate every click)*

- **Login (~20s):** `[log in with HR credentials]`
  "Authentication uses JWT with secure sessions; every user only ever sees their own data."
- **Dashboard (~20s):** `[dashboard overview]`
  "The dashboard summarizes documents, jobs, and candidates at a glance."
- **Documents + preprocessing (~50s):** `[drag-and-drop a resume PDF]`
  "On upload the file returns immediately as *pending*, and a background worker extracts,
  classifies, chunks, embeds, and indexes it — the badge moves pending → processing → **ready** in
  real time." `[open in-app preview]`
- **Semantic Search (~40s):** `[open Search, type a query e.g. "AWS" or "machine learning"]`
  "Search is **semantic**, not keyword. It ranks documents by meaning, shows match strength and
  skill tags, and can be filtered by document type, skills, or years of experience." `[point to a
  "Strong match" result]`
- **Ask — RAG, the core feature (~1:05):** `[open Ask, type a question or click an example such as
  "Compare the top three backend candidates by years of experience"]`
  "This is **Retrieval-Augmented Generation**. The answer streams token by token, and every claim
  carries an inline **citation** — hover to see the source, click to jump to the exact document."
  `[click a citation]`
  Then `[ask an out-of-scope question]`:
  "Crucially, when a question isn't supported by the documents, it **refuses** instead of
  hallucinating."
- **Jobs (~30s):** `[create a job with required skills, experience, education]`
  "We define a role and its criteria."
- **Candidates — AI screening (~50s):** `[open the job → Match candidates]`
  "The system ranks candidates with a transparent, weighted score, and every score has an
  **explainable breakdown** — skills, experience, and semantic fit — so recruiters see *why*
  someone ranked where they did."
- **Gmail sync (~30s):** `[trigger Gmail sync]`
  "Candidates can be pulled automatically from Gmail — attachments are ingested through the same
  pipeline and de-duplicated, updating the database with new candidates."
- **Logs & Settings (~20s):** `[activity logs]` "Every action is recorded in an audit trail."
  `[settings]` "and users manage their profile and password here."

## 7:30–8:30 — Results  *(Ezza)*
> "On our development stack, hybrid search returns in about **72 milliseconds** median, RAG answers
> start streaming in under a second, and chunk embedding is under a millisecond on GPU. The
> prototype exposes 31 working API endpoints. On the non-functional side: strict per-user data
> isolation and encrypted personal fields for **security**, sub-second interactive latency for
> **performance**, a strictly layered architecture with swappable providers for **maintainability**,
> and stateless services plus a separate worker pool for **scalability**."

`[SCREEN: stat tiles / performance table + one or two result screenshots]`

## 8:30–9:00 — Closing  *(Zain)*
> "Hireflow delivers all four objectives in one self-hostable platform, with every answer traceable
> to its source. Thank you."

`[SCREEN: closing slide with GitHub QR]`

---

## Requirement coverage checklist (from the guidelines)
- User Login ✓ · Dashboard ✓ · Core Features (search, RAG, screening) ✓ · Reports/Audit (Logs) ✓
- Notifications (real-time status badges) ✓ · AI Predictions (RAG answers + candidate scoring) ✓
- Data Preprocessing (ingestion pipeline) ✓ · Outputs (cited answers, ranked candidates) ✓
- Database Updates (Gmail sync) ✓ · Admin (role-based access; mention admin bypass) ✓
- Mobile App — N/A (web SPA) · prefer live demo over screenshots throughout

## Recording tips
- One clean audio take per section; keep transitions smooth.
- Full HD, 16:9, no watermarks, stable recording.
- Explain both Functional and Non-Functional Requirements (NFRs woven into Results).

## Face bubble (webcam overlay)?
Optional. Recommended: a **small bubble on the Introduction and Results/Closing only**, and
**off (or pinned to bottom-left) during the 5-min live demo** so the UI stays unobstructed. Use it
only if webcam lighting and background are good; otherwise a clean voiceover looks more
professional. Hireflow's chat and citations sit center/right, so bottom-left is the safe corner if
you keep it on.
