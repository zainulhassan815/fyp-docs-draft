# RAG Architecture for HR Screening

## Overview

This document defines the Retrieval-Augmented Generation (RAG) architecture for the HR screening system. The goal is to enable natural language queries over resumes and job applications.

---

## Query Types

| Query Type | Example | Solution |
|------------|---------|----------|
| Exact lookup | "Ali's resume for SWE job" | PostgreSQL (metadata) |
| Semantic search | "Candidates with React experience" | ChromaDB (vectors) |
| Similarity | "Candidates like this resume" | ChromaDB (full doc embedding) |
| Hybrid | "Ali's skills matching job requirements" | PostgreSQL + ChromaDB |

---

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      User Query                          │
└─────────────────────┬───────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────┐
│                 Query Parser (LLM)                       │
│  Extracts: structured filters + semantic query           │
└─────────────────────┬───────────────────────────────────┘
                      ▼
         ┌────────────┴────────────┐
         ▼                         ▼
┌─────────────────┐      ┌─────────────────┐
│   PostgreSQL    │      │    ChromaDB     │
│  (Metadata)     │      │   (Vectors)     │
│                 │      │                 │
│ • candidate_name│      │ • resume chunks │
│ • job_id        │      │ • embeddings    │
│ • skills[]      │      │ • section type  │
│ • applied_date  │      │                 │
└────────┬────────┘      └────────┬────────┘
         │                        │
         └──────────┬─────────────┘
                    ▼
           ┌───────────────┐
           │ Combine/Rank  │
           └───────┬───────┘
                   ▼
              Response
```

---

## Data Model

### PostgreSQL (Structured Data)

```sql
-- Candidates
candidates (
    id UUID PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(20),
    skills TEXT[],              -- Extracted skills array
    years_experience INT,
    education_level VARCHAR(50),
    created_at TIMESTAMP
)

-- Jobs
jobs (
    id UUID PRIMARY KEY,
    title VARCHAR(200),
    description TEXT,
    requirements TEXT,
    status VARCHAR(20),
    created_at TIMESTAMP
)

-- Applications
applications (
    id UUID PRIMARY KEY,
    candidate_id UUID REFERENCES candidates,
    job_id UUID REFERENCES jobs,
    status VARCHAR(20),         -- pending, reviewed, shortlisted, rejected
    applied_at TIMESTAMP
)

-- Documents
documents (
    id UUID PRIMARY KEY,
    candidate_id UUID REFERENCES candidates,
    file_path VARCHAR(500),
    file_type VARCHAR(10),      -- pdf, docx
    original_filename VARCHAR(255),
    uploaded_at TIMESTAMP
)
```

### ChromaDB (Vector Storage)

**Collection: `resumes`**

```python
{
    "id": "{candidate_id}_{chunk_type}",
    "embedding": [0.1, 0.2, ...],  # 1536 dims (OpenAI) or 384 dims (local)
    "document": "chunk text content",
    "metadata": {
        "candidate_id": "uuid",
        "job_id": "uuid",
        "type": "full | section",
        "section": "experience | education | skills | projects | summary",
        "candidate_name": "Ali Khan"  # Denormalized for filtering
    }
}
```

---

## Chunking Strategy: Hybrid Approach

### Why Hybrid?

Resumes are short (1-3 pages) but dense. We store multiple representations:

1. **Full resume** → Overall similarity matching
2. **Section chunks** → Targeted skill/experience queries
3. **Structured metadata** → Exact filters

### Storage Structure

```
┌─────────────────────────────────────────────────┐
│              FULL RESUME EMBEDDING              │
│     (for overall similarity matching)           │
│     id: {candidate_id}_full                     │
└─────────────────────────────────────────────────┘
                      +
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  EXPERIENCE │ │   SKILLS    │ │  EDUCATION  │
│  [embed]    │ │  [embed]    │ │  [embed]    │
└─────────────┘ └─────────────┘ └─────────────┘
     id: {candidate_id}_experience    ...
                      +
┌─────────────────────────────────────────────────┐
│           EXTRACTED METADATA (PostgreSQL)       │
│  name, email, skills[], years_exp, education    │
└─────────────────────────────────────────────────┘
```

### Query Routing

| Query | Storage Used |
|-------|--------------|
| "Ali's resume" | PostgreSQL (name filter) |
| "Candidates like this resume" | ChromaDB (full embedding) |
| "React experience" | ChromaDB (experience section) |
| "CS degree holders" | PostgreSQL (education_level) |
| "5+ years Python" | PostgreSQL (years_exp, skills) |

---

## Resume Parser

### Responsibilities

1. Extract text from PDF/DOCX
2. Detect and split sections
3. Extract structured metadata
4. Prepare chunks for embedding

### Section Detection: Hybrid Approach

**Step 1: Try regex patterns (fast path)**

```python
SECTION_PATTERNS = {
    "summary": r"(?i)(summary|objective|profile|about\s*me)",
    "experience": r"(?i)(work\s*experience|professional\s*experience|employment|work\s*history)",
    "education": r"(?i)(education|academic|qualifications|degrees?)",
    "skills": r"(?i)(skills|technical\s*skills|competencies|technologies)",
    "projects": r"(?i)(projects|portfolio|personal\s*projects)",
    "certifications": r"(?i)(certifications?|licenses?|credentials)"
}
```

**Step 2: LLM fallback (if regex unclear)**

```python
prompt = """
Extract sections from this resume. Return JSON with these keys:
- summary
- experience
- education
- skills
- projects
- certifications

If a section doesn't exist, use null.

Resume:
{resume_text}
"""
```

### Metadata Extraction (LLM)

```python
prompt = """
Extract candidate information from this resume. Return JSON:
{
    "name": "Full Name",
    "email": "email@example.com",
    "phone": "+1234567890",
    "skills": ["Python", "React", ...],
    "years_experience": 5,
    "education_level": "Bachelor's | Master's | PhD | Other",
    "current_title": "Software Engineer",
    "location": "City, Country"
}

Resume:
{resume_text}
"""
```

---

## Indexing Pipeline

```python
async def index_resume(
    file_path: str,
    candidate_id: str,
    job_id: str
) -> None:
    # 1. Parse resume
    parsed = await resume_parser.parse(file_path)

    # 2. Store metadata in PostgreSQL
    await db.update_candidate_metadata(
        candidate_id=candidate_id,
        metadata=parsed.metadata
    )

    # 3. Store full resume embedding
    await chroma.add(
        ids=[f"{candidate_id}_full"],
        documents=[parsed.full_text],
        metadatas=[{
            "candidate_id": candidate_id,
            "job_id": job_id,
            "type": "full",
            "candidate_name": parsed.metadata.name
        }]
    )

    # 4. Store section embeddings
    for section_name, section_text in parsed.sections.items():
        if section_text and len(section_text.strip()) > 50:
            await chroma.add(
                ids=[f"{candidate_id}_{section_name}"],
                documents=[section_text],
                metadatas=[{
                    "candidate_id": candidate_id,
                    "job_id": job_id,
                    "type": "section",
                    "section": section_name,
                    "candidate_name": parsed.metadata.name
                }]
            )
```

---

## Search Pipeline

### Query Parser

```python
class QueryIntent:
    type: Literal["exact_lookup", "semantic_search", "similarity", "hybrid"]
    filters: dict          # {name: "Ali", job_id: "..."}
    semantic_query: str    # For vector search
    target_section: str    # experience, skills, etc.

async def parse_query(query: str) -> QueryIntent:
    prompt = """
    Parse this HR search query. Return JSON:
    {
        "type": "exact_lookup | semantic_search | similarity | hybrid",
        "filters": {"name": "...", "job_title": "..."},
        "semantic_query": "...",
        "target_section": "experience | skills | education | null"
    }

    Query: {query}
    """
    return await llm.parse(prompt)
```

### Search Executor

```python
async def search(query: str, job_id: str = None) -> list[SearchResult]:
    intent = await parse_query(query)

    results = []

    # Exact lookup from PostgreSQL
    if intent.filters:
        db_results = await db.search_candidates(
            name=intent.filters.get("name"),
            job_id=job_id or intent.filters.get("job_id"),
            skills=intent.filters.get("skills")
        )
        results.extend(db_results)

    # Semantic search from ChromaDB
    if intent.semantic_query:
        where_filter = {"job_id": job_id} if job_id else {}

        if intent.target_section:
            where_filter["section"] = intent.target_section
        else:
            where_filter["type"] = "full"

        vector_results = await chroma.query(
            query_texts=[intent.semantic_query],
            where=where_filter,
            n_results=10
        )
        results.extend(vector_results)

    # Deduplicate and rank
    return dedupe_and_rank(results)
```

---

## Query Examples

### Example 1: Exact Lookup
**Query**: "Ali's resume for Software Engineering job"

```python
intent = {
    "type": "exact_lookup",
    "filters": {"name": "Ali", "job_title": "Software Engineering"},
    "semantic_query": None
}

# Executes:
SELECT * FROM candidates c
JOIN applications a ON c.id = a.candidate_id
JOIN jobs j ON a.job_id = j.id
WHERE c.name ILIKE '%ali%'
AND j.title ILIKE '%software engineer%'
```

### Example 2: Skill Search
**Query**: "Candidates with distributed systems experience"

```python
intent = {
    "type": "semantic_search",
    "filters": {},
    "semantic_query": "distributed systems experience",
    "target_section": "experience"
}

# Executes:
chroma.query(
    query_texts=["distributed systems experience"],
    where={"section": "experience"},
    n_results=10
)
```

### Example 3: Similarity Search
**Query**: "Find candidates similar to resume #123"

```python
# Get reference resume embedding
reference = chroma.get(id="candidate_123_full")

# Find similar
chroma.query(
    query_embeddings=[reference.embedding],
    where={"type": "full"},
    n_results=10
)
```

### Example 4: Hybrid
**Query**: "Python developers with 5+ years experience"

```python
# Step 1: Filter by years in PostgreSQL
candidates = db.query(
    "SELECT id FROM candidates WHERE years_experience >= 5"
)

# Step 2: Semantic search within filtered set
chroma.query(
    query_texts=["Python developer"],
    where={
        "candidate_id": {"$in": [c.id for c in candidates]},
        "section": "skills"
    }
)
```

---

## Embedding Model Selection

### Options Evaluated

#### Cloud/API Models

| Model | Dimensions | Cost | MTEB Score | Notes |
|-------|------------|------|------------|-------|
| **OpenAI text-embedding-3-small** | 1536 | $0.02/1M tokens | ~62% | Best cost/performance |
| OpenAI text-embedding-3-large | 3072 | $0.13/1M tokens | ~64.6% | Overkill for resumes |
| Voyage AI | 1024 | $0.02/1M tokens | High | Good for documents |
| Cohere embed-v3 | 1024 | $0.10/1M tokens | High | Multilingual focus |

#### Local/Self-Hosted Models

| Model | Dimensions | Size | Speed | Accuracy | Notes |
|-------|------------|------|-------|----------|-------|
| all-MiniLM-L6-v2 | 384 | 23M | Fastest | ~78-80% | Resource-constrained |
| E5-base-v2 | 768 | 110M | Fast | ~83% | Balanced |
| **BGE-base-en-v1.5** | 768 | 110M | Moderate | ~84.7% | Best local option |
| BGE-M3 | 1024 | 560M | Slower | SOTA | Multilingual, long docs |

### Recommendation

**Primary: OpenAI `text-embedding-3-small`**

| Factor | Assessment |
|--------|------------|
| Quality | Superior semantic matching |
| Cost | ~$0.01 per 1000 resumes |
| Simplicity | No GPU, no model management |
| Dimension flexibility | Can reduce 1536 → 512 if needed |

**Fallback: `BGE-base-en-v1.5`**
- Free, self-hosted
- ~85% accuracy
- Good for offline/privacy requirements

### Cost Estimate

```
Average resume: ~500 tokens
1,000 resumes = 500K tokens = $0.01
100,000 resumes = 50M tokens = $1.00
```

### Implementation

```python
# backend/app/services/embedding.py
from enum import StrEnum
from openai import AsyncOpenAI


class EmbeddingProvider(StrEnum):
    OPENAI = "openai"
    LOCAL = "local"


class EmbeddingService:
    def __init__(self, provider: EmbeddingProvider = EmbeddingProvider.OPENAI):
        self.provider = provider

        if provider == EmbeddingProvider.OPENAI:
            self.client = AsyncOpenAI()
            self.model = "text-embedding-3-small"
            self.dimensions = 1536
        else:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer("BAAI/bge-base-en-v1.5")
            self.dimensions = 768

    async def embed(self, text: str) -> list[float]:
        if self.provider == EmbeddingProvider.OPENAI:
            response = await self.client.embeddings.create(
                model=self.model,
                input=text
            )
            return response.data[0].embedding

        # Local model (sync, but fast)
        return self.model.encode(text).tolist()

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        if self.provider == EmbeddingProvider.OPENAI:
            response = await self.client.embeddings.create(
                model=self.model,
                input=texts
            )
            return [item.embedding for item in response.data]

        return self.model.encode(texts).tolist()
```

---

## Decisions Made

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Chunking strategy | Hybrid (full + sections) | Flexibility for different query types |
| Section detection | LLM with regex fallback | Accuracy for varied formats |
| Metadata storage | PostgreSQL | Exact filters, ACID compliance |
| Vector storage | ChromaDB | Simple, good for prototype |
| Query routing | LLM-based intent parsing | Natural language flexibility |
| **Embedding model** | OpenAI text-embedding-3-small | Best quality/cost ratio |
| **Fallback embedding** | BGE-base-en-v1.5 | Free, self-hosted option |

---

## Research Completed

- [x] Chunking strategy for resumes
- [x] Embedding model selection
- [ ] Similarity threshold tuning
- [ ] Reranking strategies

---

## References

- [ChromaDB Documentation](https://docs.trychroma.com/)
- [LangChain RAG Guide](https://python.langchain.com/docs/tutorials/rag/)
- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)
- [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)
- [BGE Models](https://huggingface.co/BAAI/bge-base-en-v1.5)
- [Embedding Model Comparison](https://modal.com/blog/embedding-models-article)
