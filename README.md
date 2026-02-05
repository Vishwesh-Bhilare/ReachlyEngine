# ReachlyEngine

**ReachlyEngine** is an offline-first, CLI-based, LLM-powered cold outreach engine that generates hyper-personalized messages across multiple channels (Email, WhatsApp/SMS, LinkedIn DM, Instagram DM).

Unlike cloud-based outreach tools, ReachlyEngine:
- Runs **entirely locally**
- Uses **open-source LLMs via Ollama**
- Stores knowledge **on-device**
- Gives full control over tone, personalization, and experimentation

This is a **working product**, not a demo or template.

---

## Core Capabilities

- Offline LLM-powered message generation (Ollama)
- LinkedIn profile text extraction (raw HTML → clean text)
- Persona inference:
  - Role & seniority
  - Industry
  - Communication tone (formal / casual / mixed)
  - Language hints
- Multi-channel outreach generation:
  - Cold Email
  - WhatsApp / SMS
  - LinkedIn DM
  - Instagram DM
- CTA-focused, human-like messaging
- Local memory & reuse (SQLite):
  - Past profiles
  - Generated messages
  - Industry/role-based reuse
- Interactive CLI menu (no web UI required)

---

## Tech Stack

- **Language**: Python 3.10+
- **LLM Runtime**: Ollama
- **Model**: `mistral:7b-instruct-q4_K_M`
- **Database**: SQLite (local)
- **Scraping**: Requests + BeautifulSoup
- **CLI**: Rich (tables, layout, prompts)

---

## Requirements

### System
- Linux / macOS (Windows supported but not primary)
- Python 3.10+
- Ollama installed and running

### Ollama Setup
```bash
ollama pull mistral:7b-instruct-q4_K_M
ollama run mistral:7b-instruct-q4_K_M

