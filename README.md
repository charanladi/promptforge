# PromptForge 🔨

> Craft better prompts, get better results — an AI-powered prompt optimizer for any LLM.

## Overview

PromptForge helps users transform rough, vague prompts into clear, optimized instructions tailored for different LLMs (GPT-4, Claude, Gemini, Mistral, etc.).

Whether you're a developer, researcher, or casual AI user — stop guessing and start engineering your prompts with precision.

## Features

- **Prompt Analyzer** — Identifies weaknesses in your prompt (vague instructions, missing context, ambiguous goals)
- **Multi-LLM Optimizer** — Rewrites your prompt optimized for a target model
- **Prompt Comparison** — Side-by-side view of original vs optimized prompt
- **Tone & Style Controls** — Adjust for technical, creative, or instructional use cases
- **Prompt History** — Save and revisit your best prompts

## Tech Stack

- **Frontend:** HTML / CSS / JavaScript (or React)
- **Backend:** Python (FastAPI)
- **AI:** Anthropic Claude API / OpenAI API
- **Deployment:** Render / Railway

## Getting Started

```bash
git clone https://gitlab.com/your-username/promptforge.git
cd promptforge
pip install -r requirements.txt
cp .env.example .env   # Add your API keys
python app.py
```

## Project Structure

```
promptforge/
├── backend/
│   ├── app.py
│   ├── optimizer.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── main.js
├── .env.example
└── README.md
```

## Roadmap

- [ ] Web UI (MVP)
- [ ] Multi-model support
- [ ] Prompt templates library
- [ ] Browser extension
- [ ] API endpoint for developers

## Team

Built at the Swecha AI/ML Hackathon 2025.

## License

MIT