import anthropic
import json
import os
import re

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

MODEL_TIPS = {
    "claude": "Claude responds best to explicit role definitions, structured output formats, and clear constraints. It handles nuance and long context well.",
    "gpt4": "GPT-4 benefits from numbered instructions, system/user message separation, and explicit examples. Specify JSON output when needed.",
    "gemini": "Gemini works well with direct, concise instructions. Include examples for complex tasks. Specify format expectations clearly.",
    "mistral": "Mistral is instruction-tuned; use clear imperative sentences. Avoid ambiguity. Works best with short, focused prompts.",
    "general": "Use clear role definitions, explicit output formats, and specify constraints like length, tone, and audience.",
}

STYLE_TIPS = {
    "technical": "Use precise technical language. Specify output structure (JSON, markdown, code). Include error handling expectations.",
    "creative": "Allow creative latitude. Specify tone, style references, and desired emotional effect. Avoid over-constraining.",
    "instructional": "Break into clear steps. Specify audience expertise level. Use numbered lists for sequential tasks.",
    "general": "Balance clarity and flexibility. Define role, task, format, and constraints.",
}

SYSTEM_PROMPT = """You are PromptForge, an expert prompt engineer. Your job is to analyze a user's rough prompt and rewrite it into a highly optimized version.

You MUST respond with ONLY a valid JSON object — no preamble, no markdown, no explanation outside the JSON.

The JSON must have exactly these fields:
{{
  "optimized": "<the rewritten, optimized prompt>",
  "issues_found": ["<issue 1>", "<issue 2>", ...],
  "improvement_score": <integer 0-100>
}}

Rules for optimization:
- Add a clear role/persona if missing ("You are a...")
- Specify the exact output format (bullet points, JSON, paragraph, etc.)
- Define the audience and tone
- Add constraints (length, style, what to avoid)
- Make the task unambiguous
- Preserve the original intent — never change what the user is asking for

Model context: {model_tips}
Style context: {style_tips}
"""

async def optimize_prompt(prompt: str, target_model: str, style: str) -> dict:
    model_tips = MODEL_TIPS.get(target_model, MODEL_TIPS["general"])
    style_tips = STYLE_TIPS.get(style, STYLE_TIPS["general"])

    system = SYSTEM_PROMPT.format(model_tips=model_tips, style_tips=style_tips)

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system=system,
        messages=[
            {
                "role": "user",
                "content": f"Optimize this prompt:\n\n{prompt}"
            }
        ]
    )

    raw = message.content[0].text.strip()

    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"^```\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        result = {
            "optimized": raw,
            "issues_found": ["Could not parse structured response"],
            "improvement_score": 50
        }

    return {
        "original": prompt,
        "optimized": result.get("optimized", prompt),
        "issues_found": result.get("issues_found", []),
        "improvement_score": int(result.get("improvement_score", 50)),
    }
