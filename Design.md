# ReachlyEngine Design Document

## Overview

ReachlyEngine is an offline, LLM-powered outreach automation tool that converts LinkedIn profiles into structured personas and generates personalized messages across multiple channels. The system runs entirely locally using Ollama, eliminating dependency on cloud-based APIs.

### Core Value Proposition

- **Privacy-first**: All data processing happens locally
- **Offline-capable**: No external API dependencies after initial setup
- **Reusable knowledge**: Personas stored for long-term use
- **Multi-channel**: Generate messages for email, WhatsApp, LinkedIn DM, and Instagram DM

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         CLI Layer                            │
│  (Terminal UI, User Input, Output Rendering)                │
└─────────────────┬───────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────┐
│                    Application Layer                         │
│         (ReachlyApp - Orchestration & Workflow)             │
└──┬──────────┬──────────┬──────────┬──────────┬─────────────┘
   │          │          │          │          │
   │          │          │          │          │
┌──▼──────┐ ┌▼────────┐ ┌▼────────┐ ┌▼────────┐ ┌▼──────────┐
│ Scraping│ │Analysis │ │Generation│ │ Memory  │ │   Auth    │
│  Layer  │ │  Layer  │ │  Layer   │ │  Layer  │ │  Layer    │
└──┬──────┘ └┬────────┘ └┬─────────┘ └┬────────┘ └┬──────────┘
   │         │           │            │           │
   │         └───────────┴────────────┘           │
   │                     │                        │
   │                ┌────▼─────┐                  │
   │                │   LLM    │                  │
   │                │  (Ollama)│                  │
   │                └──────────┘                  │
   │                                              │
┌──▼──────────────────────────────────────────────▼───────────┐
│              External Integrations                           │
│  - LinkedIn (via authenticated session)                     │
│  - Ollama (local LLM server)                                │
└─────────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. Authentication Layer (`reachly_engine/auth/`)

**Purpose**: Manage LinkedIn session authentication

**Components**:
- `linkedin_auth.py`: Handles cookie extraction and validation
- `store.py`: Persists credentials to `~/.reachly/credentials.json`

**Design Decisions**:
- Uses session cookies (`li_at`) rather than OAuth to simplify setup
- One-time authentication per machine
- Credentials stored in user home directory for persistence across runs
- Browser-based authentication for better UX than manual cookie entry

**Flow**:
```
User starts app → Check for saved cookie → If missing:
  1. Open browser to LinkedIn
  2. User logs in manually
  3. User copies li_at cookie
  4. Validate cookie with test request
  5. Save to ~/.reachly/credentials.json
```

---

### 2. Scraping Layer (`reachly_engine/scraping/`)

**Purpose**: Extract clean text from LinkedIn profiles

**Components**:
- `linkedin.py`: LinkedIn-specific scraping logic
- `cleaner.py`: HTML cleanup and noise removal
- `web.py`: Generic web scraping (future extensibility)

**Key Design Decisions**:

1. **Preserve JSON in `<script>` tags**: LinkedIn embeds profile data in JavaScript objects. Standard HTML cleaning would remove this critical data.

2. **Multi-source text extraction**:
   - Visible DOM text
   - JSON payloads in script tags
   - Combined to maximize data capture

3. **Aggressive cleanup for LLM consumption**:
   - Remove UI noise ("Sign in", "Connect", etc.)
   - Normalize whitespace
   - Truncate to `MAX_PROFILE_CHARS` (12,000 chars)

**Text Processing Pipeline**:
```
Raw HTML → BeautifulSoup parsing → Extract visible text + scripts
         → Pattern-based noise removal → Whitespace normalization
         → Truncation → Save to data/profiles/
```

---

### 3. Analysis Layer (`reachly_engine/analysis/`)

**Purpose**: Convert raw profile text into structured personas

**Components**:
- `persona.py`: Main persona inference orchestrator
- `style.py`: Communication style analysis
- `summarizer.py`: Profile summarization

**Persona Structure**:
```python
@dataclass
class Persona:
    summary: str          # Concise factual summary
    style: str           # Communication style markers
    raw_analysis: str    # Full structured analysis
```

**Analysis Pipeline**:
```
Profile Text → LLM Analysis (PERSONA_ANALYSIS_PROMPT)
            → Style Inference (tone, emoji usage, formality)
            → Summary Generation (6 bullet points max)
            → Structured Persona object
```

**Design Rationale**:
- **Low temperature (0.2-0.3)**: Analysis should be factual, not creative
- **Structured prompts**: Force consistent output format
- **Separate style analysis**: Communication patterns need different temperature/focus
- **Reusable summaries**: Store once, generate many messages

---

### 4. Generation Layer (`reachly_engine/generation/`)

**Purpose**: Create channel-specific outreach messages

**Components**:
- `email.py`: Cold email generation
- `whatsapp.py`: WhatsApp/SMS messages
- `linkedin_dm.py`: LinkedIn direct messages
- `instagram_dm.py`: Instagram direct messages
- `cta.py`: Call-to-action generation (shared utility)

**Channel-Specific Characteristics**:

| Channel      | Tone          | Length      | Temperature | CTA Style          |
|--------------|---------------|-------------|-------------|--------------------|
| Email        | Professional  | 5-7 sent.   | 0.6         | Formal invite      |
| WhatsApp     | Friendly      | Very short  | 0.7         | Casual ask         |
| LinkedIn DM  | Professional  | Medium      | 0.55        | Soft, respectful   |
| Instagram DM | Casual        | Short       | 0.75        | Relaxed, authentic |

**Message Generation Pipeline**:
```
Persona block → Generate CTA → Inject into channel-specific prompt
             → LLM generation with tuned temperature
             → Post-process & return
```

**Design Decisions**:
- **CTA-first generation**: Ensures every message has a clear ask
- **Temperature tuning**: Balances creativity with professionalism
- **No emoji by default**: Only if persona analysis indicates heavy emoji usage
- **Anti-patterns built into prompts**: Explicitly avoid "corporate buzzwords" and "AI-sounding language"

---

### 5. Memory Layer (`reachly_engine/memory/`)

**Purpose**: Persistent storage for personas and messages

**Components**:
- `store.py`: CRUD operations
- `retrieval.py`: Similarity search (industry/role-based)
- `schema.sql`: SQLite database schema

**Schema Design**:

```sql
prospects (
    id, name, role, company, industry, seniority,
    summary, style, raw_profile, source, created_at
)

messages (
    id, prospect_id, channel, content, created_at,
    FOREIGN KEY (prospect_id) REFERENCES prospects(id)
)
```

**Design Rationale**:
- **SQLite**: Lightweight, zero-config, perfect for local-first architecture
- **Cascade deletes**: Messages deleted when prospect removed
- **Indexes on industry/role**: Fast similarity search without embeddings
- **Raw profile preservation**: Traceability and potential re-analysis

**Retrieval Strategy**:
```python
# Deterministic, fast, no embeddings required
find_similar_prospects(industry="fintech", role="engineer", limit=3)
```

---

### 6. LLM Layer (`reachly_engine/llm/`)

**Purpose**: Abstract Ollama API interactions

**Components**:
- `ollama_client.py`: HTTP client for Ollama API
- `prompts.py`: System and task prompts
- `tokenizer.py`: Token estimation and truncation

**Key Features**:
1. **Health checks**: Verify Ollama is running and model exists
2. **Token management**: Conservative truncation to avoid context overflow
3. **Timeout handling**: Default 120s for slower local models
4. **Streaming disabled**: Single-shot completions for simplicity

**Prompt Architecture**:

```python
SYSTEM_BASE = "You are a skilled human copywriter..."

SYSTEM_ANALYSIS = SYSTEM_BASE + "Your task is to analyze..."
SYSTEM_GENERATION = SYSTEM_BASE + "Your task is to write..."

# Task prompts are format strings:
PERSONA_ANALYSIS_PROMPT.format(profile_text=...)
EMAIL_PROMPT.format(persona=...)
```

**Design Decisions**:
- **Conservative char-per-token ratio (4:1)**: Safer than tiktoken for unknown models
- **Separate system prompts**: Clear role definition for analysis vs generation
- **No streaming**: Simpler error handling and processing
- **Model agnostic**: Works with any Ollama-compatible model

---

### 7. CLI Layer (`reachly_engine/cli/`)

**Purpose**: Terminal-based user interface

**Components**:
- `menu.py`: Menu navigation and workflow orchestration
- `prompts.py`: User input helpers
- `render.py`: Rich-based output formatting

**User Workflows**:

**Workflow 1: Add Profile**
```
User selects option 1 → Paste URL → Fetch profile → Analyze persona
                     → Save to DB → Optional: Generate messages
```

**Workflow 2: Generate Outreach**
```
User selects option 2 → View stored personas → Select by ID
                     → Generate all channels → Display results → Save to DB
```

**Workflow 3: View Personas**
```
User selects option 3 → Query DB → Render table → Return to menu
```

**Design Decisions**:
- **Rich library**: Modern terminal UI with panels, tables, colors
- **Immediate feedback**: Show progress and results inline
- **Graceful interrupts**: KeyboardInterrupt returns to menu, not crash
- **Minimal input**: Single-digit menu selection, URL paste, ID entry

---

## Data Flow

### Complete End-to-End Flow

```
1. INGESTION
   LinkedIn URL → HTTP request with li_at cookie → HTML response
              → Extract text + JSON → Clean & save raw text

2. ANALYSIS
   Raw text → Truncate to context limit → LLM persona analysis
           → Style inference → Summary generation → Persona object

3. EXTRACTION (Best-effort)
   Persona.summary → Regex patterns → Extract name, role, company

4. PERSISTENCE
   Persona + raw_profile → Insert into SQLite → Return prospect_id

5. GENERATION (Optional or deferred)
   prospect_id → Retrieve from DB → Format persona block
              → Generate CTA → Generate email, WhatsApp, LinkedIn DM, Instagram DM
              → Save all messages to DB

6. DISPLAY
   Messages → Rich panels → Multi-column terminal output
```

---

## Configuration & Environment

### Configuration System (`config.py`)

**Environment Variables**:
```bash
REACHLY_DATA_DIR=/path/to/data      # Default: ./data
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral:7b-instruct-q4_K_M
OLLAMA_TIMEOUT=120
LOG_LEVEL=INFO
USER_AGENT=Mozilla/5.0...
```

**File System Layout**:
```
project_root/
├── data/
│   ├── profiles/           # Raw LinkedIn text
│   ├── summaries/          # (future)
│   ├── messages/           # (future)
│   └── memory.db           # SQLite database
├── reachly_engine/
│   └── ...
└── ~/.reachly/
    └── credentials.json    # LinkedIn cookie
```

---

## Error Handling Strategy

### Layered Error Handling

1. **Network Errors**:
   - LinkedIn fetch fails → Raise with clear message
   - Ollama unreachable → Health check catches early

2. **LLM Errors**:
   - Timeout → Increase `OLLAMA_TIMEOUT`
   - Invalid response → Log full payload, raise RuntimeError

3. **Parsing Errors**:
   - Name/role extraction fails → Store as `None`, continue
   - Best-effort approach: never fail on optional fields

4. **User Interrupts**:
   - KeyboardInterrupt → Return to menu with yellow warning
   - Graceful degradation over crashes

### Logging Strategy

```python
logger.info("Starting persona inference")
logger.error(f"Ollama connection error: {e}")
```

- **INFO**: Workflow milestones
- **ERROR**: Failures with context
- **Output**: Configurable via `LOG_LEVEL`

---

## Security & Privacy

### Privacy-First Design

1. **No cloud dependencies**: All processing happens locally
2. **User-controlled data**: Stored in user's filesystem
3. **Explicit authentication**: User provides cookie manually
4. **No telemetry**: Zero external reporting

### Security Considerations

1. **Cookie storage**: Plain text in `~/.reachly/credentials.json`
   - **Risk**: Filesystem access = LinkedIn access
   - **Mitigation**: Inform users, consider encryption in future

2. **SQL injection**: Prevented by parameterized queries
   ```python
   cursor.execute("SELECT * FROM prospects WHERE id = ?", (prospect_id,))
   ```

3. **Input validation**:
   - URLs: No validation (rely on LinkedIn 404)
   - IDs: `.isdigit()` check before DB query

---

## Performance Characteristics

### Bottlenecks

1. **LLM inference**: 5-30 seconds per generation (model-dependent)
2. **LinkedIn fetch**: 2-5 seconds per profile
3. **Database**: Negligible (<10ms for queries)

### Optimization Strategies

1. **Token truncation**: Cap context at 12,000 chars
2. **Batch message generation**: All 4 channels in ~30 seconds
3. **Reusable personas**: Analysis once, generate many times

### Scalability Limits

- **SQLite**: Handles thousands of prospects easily
- **Ollama**: Single-threaded, no concurrency needed
- **Memory**: ~2GB for Mistral 7B quantized model

---

## Design Trade-offs

### 1. Offline vs. Online LLMs

**Choice**: Ollama (offline)

**Trade-offs**:
- ✅ Privacy, no API costs, offline capability
- ❌ Slower inference, model quality dependent on hardware

### 2. Session Cookies vs. OAuth

**Choice**: Session cookies

**Trade-offs**:
- ✅ Simpler setup, no app registration
- ❌ Less secure, cookies expire

### 3. SQLite vs. Vector DB

**Choice**: SQLite with keyword search

**Trade-offs**:
- ✅ Zero dependencies, fast, simple
- ❌ Less sophisticated similarity search

### 4. Rich CLI vs. Web UI

**Choice**: Terminal CLI

**Trade-offs**:
- ✅ Developer-friendly, scriptable, fast
- ❌ Less accessible to non-technical users

---

## Extensibility Points

### 1. New Channels

Add new message generator:
```python
# reachly_engine/generation/telegram.py
def generate_telegram(persona: str, llm: OllamaClient) -> str:
    # Implement channel-specific logic
```

Update `app.py`:
```python
messages["Telegram"] = generate_telegram(persona_block, self.llm)
```

### 2. New Data Sources

Implement scraper interface:
```python
# reachly_engine/scraping/twitter.py
def fetch_twitter_profile_text(username: str) -> str:
    # Implement Twitter-specific scraping
```

### 3. Advanced Retrieval

Replace keyword search with embeddings:
```python
# reachly_engine/memory/embeddings.py
def find_similar_by_embedding(query: str, top_k: int) -> List[Dict]:
    # Use sentence-transformers or similar
```

### 4. Campaign Management

Add batch processing:
```python
# reachly_engine/campaigns/batch.py
def process_csv(csv_path: Path) -> List[Persona]:
    # Bulk ingestion and generation
```

---

## Testing Strategy

### Current Test Coverage

1. **Unit Tests** (`tests/`):
   - `test_persona.py`: Persona inference
   - `test_generation.py`: Message generation
   - `test_scraping.py`: HTML cleaning

2. **Integration Tests** (manual):
   - Full workflow: URL → Persona → Messages
   - Database persistence
   - Ollama connectivity

### Testing Challenges

1. **LLM non-determinism**: Assertions on exact content difficult
2. **LinkedIn dependency**: Cannot test live scraping in CI
3. **Ollama requirement**: Tests require local Ollama server

### Recommended Test Strategy

```python
# Mock LLM for deterministic tests
@pytest.fixture
def mock_llm():
    llm = Mock(spec=OllamaClient)
    llm.generate.return_value = "Mock response"
    return llm

# Integration test with real Ollama (requires local setup)
@pytest.mark.integration
def test_end_to_end():
    if not OllamaClient().health_check():
        pytest.skip("Ollama not running")
    # ... test full workflow
```

---

## Future Improvements

### Short-term Roadmap

1. **Persona editing**: Allow manual refinement of extracted fields
2. **CSV export**: Export personas and messages
3. **Campaign batching**: Process multiple profiles in one session
4. **Search/filter**: Query personas by role, industry, etc.

### Long-term Vision

1. **Multi-step conversations**: Track outreach threads
2. **A/B testing**: Generate multiple message variants
3. **Embeddings-based retrieval**: Semantic persona search
4. **Web UI**: Optional GUI for non-CLI users
5. **Response tracking**: Integration with email/LinkedIn APIs

---

## Appendix: Prompt Engineering

### Persona Analysis Prompt

```
PROFILE TEXT:
{profile_text}

Analyze the person above and return:

1. Name (if available)
2. Current role
3. Company
4. Industry
5. Seniority level
6. Interests or focus areas
7. Communication style (formal / casual / mixed)
8. Writing traits (short sentences, emojis, slang, etc.)

Respond in clean bullet points.
```

**Design Rationale**:
- Numbered list forces structured output
- Bullet points easier to parse than prose
- "if available" handles incomplete profiles
- Explicit style markers guide tone matching

### Email Generation Prompt

```
PERSONA:
{persona}

Write a cold email:
- Short subject line
- 5–7 sentences max
- Personalized
- Clear CTA for a short call

CTA:
{cta}
```

**Design Rationale**:
- Constraints prevent generic templates
- Pre-generated CTA ensures consistency
- "5-7 sentences" prevents wall-of-text emails
- "Personalized" triggers relevant details from persona

---

## Conclusion

ReachlyEngine demonstrates a privacy-first, locally-run approach to outreach automation. The architecture prioritizes:

1. **Simplicity**: Minimal dependencies, clear separation of concerns
2. **Privacy**: Local-only processing, user-controlled data
3. **Extensibility**: Easy to add channels, sources, features
4. **Developer experience**: Clean CLI, comprehensive logging

The design accommodates both immediate use cases (single-profile analysis) and future scaling (batch processing, advanced retrieval), while maintaining the core principle of offline-first operation.
