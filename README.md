# PromptForge 🔨




**AI-powered prompt optimizer for LLMs — stop guessing, start engineering.**

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green?style=flat-square&logo=fastapi)
![Claude API](https://img.shields.io/badge/Anthropic-Claude_API-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-purple?style=flat-square)
![Status](https://img.shields.io/badge/Status-Hackathon_Build-red?style=flat-square)




---

## What is PromptForge?

Most people interact with LLMs using vague, unstructured prompts — and get mediocre results.

**PromptForge** analyzes your rough prompt and rewrites it into a precise, optimized version tailored to the target model (GPT-4, Claude, Gemini, Mistral, etc.). Think of it as a **compiler for your prompts**.

```
Input:  "summarize this for me"
Output: "You are a senior technical writer. Summarize the following text in 3 bullet points,
         each under 20 words. Focus on key decisions, not background context. Audience: engineers."
```

---

## Features

| Feature | Description |
|---|---|
| Prompt Analyzer | Detects vagueness, missing context, and ambiguous goals |
| Multi-LLM Optimizer | Rewrites prompts tuned for GPT-4, Claude, Gemini, Mistral |
| Side-by-side Diff | Visual comparison of original vs optimized prompt |
| Tone Controls | Switch between technical, creative, and instructional styles |
| Prompt History | Save, tag, and reuse your best prompts |
| One-click Copy | Instantly copy the optimized prompt to clipboard |

---

## How It Works

```
User Input
    │
    ▼
┌─────────────────┐
│  Prompt Analyzer │  ← Detects: vagueness, missing role, missing format
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Optimizer Core  │  ← Claude API rewrites for target LLM + use case
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Output UI       │  ← Side-by-side diff + copy + save to history
└─────────────────┘
```

---

## Tech Stack

**Backend**
- Python 3.10+
- FastAPI — REST API server
- Anthropic Claude API — prompt rewriting engine

**Frontend**
- HTML / CSS / Vanilla JS (MVP)
- Diff highlighting for before/after comparison

**Infrastructure**
- Deployed on Render (free tier)
- Environment secrets via `.env`

---

## Project Structure

```
promptforge/
├── backend/
│   ├── app.py              # FastAPI entry point
│   ├── optimizer.py        # Claude API prompt rewriting logic
│   ├── analyzer.py         # Prompt weakness detection
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── main.js
├── .env.example            # API key template
├── .gitignore
└── README.md
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- An [Anthropic API key](https://console.anthropic.com/)

### Installation

```bash
# Clone the repo
git clone https://gitlab.com/your-username/promptforge.git
cd promptforge

# Install dependencies
pip install -r backend/requirements.txt

# Set up environment
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env

# Run the server
uvicorn backend.app:app --reload
```

Visit `http://localhost:8000` to open PromptForge.

---

## API Reference

### `POST /optimize`

Optimizes a prompt for a target LLM.

**Request body:**
```json
{
  "prompt": "explain quantum computing",
  "target_model": "claude",
  "style": "technical"
}
```

**Response:**
```json
{
  "original": "explain quantum computing",
  "optimized": "You are a physics professor...",
  "issues_found": ["no role defined", "no output format", "no audience specified"],
  "improvement_score": 84
}
```

---

## Roadmap

- [x] Project setup & architecture
- [ ] Prompt analyzer (weakness detection)
- [ ] Claude API optimizer integration
- [ ] Web UI with before/after diff
- [ ] Multi-model support (GPT-4, Gemini, Mistral)
- [ ] Prompt history + tagging
- [ ] Browser extension
- [ ] Public API for developers

---

## Built At

**Swecha Hackathon2 2026**
Swecha — Free Software Movement of India, Telangana

---

## License

MIT — free to use, modify, and distribute.