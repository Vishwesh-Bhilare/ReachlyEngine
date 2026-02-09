Got it 👍
Here’s **your same README**, with **only the required changes applied**:

* ✅ macOS → **Homebrew install**
* ✅ Windows → **CLI (winget) install**
* ❌ No extra fluff
* ❌ No restructuring
* ✅ Copy-paste safe

---

````md
# ReachlyEngine

ReachlyEngine is an offline, LLM-powered outreach engine that turns LinkedIn profiles into structured personas and generates personalized outreach messages across multiple channels.
It is designed to run fully locally using Ollama, without relying on cloud APIs.

## What it does

- Fetches LinkedIn profile text using your authenticated session
- Analyzes the profile to infer a structured persona
- Stores personas locally for reuse
- Generates tailored outreach messages for:
  - Email
  - WhatsApp or SMS
  - LinkedIn DM
  - Instagram DM
- Provides a clean terminal UI built with Rich

## Why ReachlyEngine

- Fully offline after setup
- No OpenAI or third-party API keys required
- Personas are reusable and searchable
- Simple CLI workflow
- Designed to be extensible and hackable

## Requirements

- Python 3.10 or higher
- Ollama installed and running
- A supported Ollama model pulled locally
- An active LinkedIn session (via cookies)

## Installation

```bash
git clone https://github.com/Vishwesh-Bhilare/ReachlyEngine.git
cd ReachlyEngine
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
````

## Ollama setup

ReachlyEngine uses Ollama to run large language models locally.

### Install Ollama

#### macOS (Homebrew)

```bash
brew install ollama
```

Start the Ollama service:

```bash
ollama serve
```

(Optional) Run Ollama in the background:

```bash
brew services start ollama
```

---

#### Linux

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Start the service:

```bash
ollama serve
```

---

#### Windows (CLI via winget)

Install Ollama using winget:

```powershell
winget install Ollama.Ollama
```

Start the Ollama service:

```powershell
ollama serve
```

If `ollama` is not recognized, restart your terminal or system.

---

### Download a model

Pull a supported model (example: Llama 3):

```bash
ollama pull llama3
```

Verify Ollama is working:

```bash
ollama list
```

Once Ollama is running and a model is pulled, ReachlyEngine is ready to use.

---

## Usage

Run the CLI:

```bash
bin/reachly
```

You will see the main menu:

```bash
1. Add LinkedIn profile (analyze and store persona)
2. Generate outreach messages from stored personas
3. View stored personas
4. Exit
```

### Add a LinkedIn profile

```bash
Paste a LinkedIn profile URL

The profile is fetched and analyzed

A persona is inferred and stored locally
```

You can optionally generate outreach messages immediately:

Select from previously stored personas →
Messages are generated for all supported channels →
Outputs are shown directly in the terminal

### View stored personas

Lists all stored personas with key fields
Useful for confirming stored data or selecting targets

### Data storage

* All data is stored locally
* Personas and messages are stored in a local SQLite database
* Raw profile text is stored under `data/profiles/`

#### To reset all stored personas for testing, delete the database file:

```bash
rm data/reachly.db
```

## Project structure

```bash
reachly_engine/
├── analysis/        # Persona inference
├── auth/            # LinkedIn auth and cookie handling
├── cli/             # Terminal UI
├── generation/      # Message generators
├── llm/             # Ollama client
├── memory/          # Local persistence layer
├── scraping/        # LinkedIn scraping logic
```

### Notes on LinkedIn usage

ReachlyEngine relies on your existing LinkedIn session cookies.
It does not bypass authentication or automate login beyond using your browser-authenticated session.

Use responsibly and at your own risk.

### Roadmap ideas

* Persona search and filtering
* Per-channel tone controls
* Persona editing
* CSV export
* Campaign batching

## License

MIT License

```

---

If you want, next I can:
- add **Windows + macOS troubleshooting**
- tighten language for **OSS credibility**
- add **badges + screenshots**
- prep a **v1.0 release README**

Just say 👌
```
