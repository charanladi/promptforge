import streamlit as st
import anthropic
import json
import re
import os

st.set_page_config(page_title="PromptForge", page_icon="🔨", layout="centered")

MODEL_TIPS = {
    "Claude": "Claude responds best to explicit role definitions, structured output formats, and clear constraints.",
    "GPT-4": "GPT-4 benefits from numbered instructions and explicit examples. Specify JSON output when needed.",
    "Gemini": "Gemini works well with direct, concise instructions. Include examples for complex tasks.",
    "Mistral": "Mistral is instruction-tuned; use clear imperative sentences. Avoid ambiguity.",
    "General": "Use clear role definitions, explicit output formats, and specify constraints like length, tone, and audience.",
}

STYLE_TIPS = {
    "General": "Balance clarity and flexibility. Define role, task, format, and constraints.",
    "Technical": "Use precise technical language. Specify output structure (JSON, markdown, code).",
    "Creative": "Allow creative latitude. Specify tone, style references, and desired emotional effect.",
    "Instructional": "Break into clear steps. Specify audience expertise level. Use numbered lists.",
}

SYSTEM_PROMPT = """You are PromptForge, an expert prompt engineer. Analyze the user's rough prompt and rewrite it into a highly optimized version.

Respond with ONLY a valid JSON object — no preamble, no markdown, no explanation outside the JSON.

JSON format:
{{
  "optimized": "<the rewritten, optimized prompt>",
  "issues_found": ["<issue 1>", "<issue 2>", ...],
  "improvement_score": <integer 0-100>
}}

Rules:
- Add a clear role/persona if missing
- Specify the exact output format
- Define the audience and tone
- Add constraints (length, style, what to avoid)
- Preserve the original intent

Model context: {model_tips}
Style context: {style_tips}
"""

def optimize_prompt(prompt, target_model, style, api_key):
    client = anthropic.Anthropic(api_key=api_key)
    system = SYSTEM_PROMPT.format(
        model_tips=MODEL_TIPS.get(target_model, MODEL_TIPS["General"]),
        style_tips=STYLE_TIPS.get(style, STYLE_TIPS["General"])
    )
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": f"Optimize this prompt:\n\n{prompt}"}]
    )
    raw = message.content[0].text.strip()
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"^```\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        result = {"optimized": raw, "issues_found": ["Could not parse response"], "improvement_score": 50}
    return {
        "original": prompt,
        "optimized": result.get("optimized", prompt),
        "issues_found": result.get("issues_found", []),
        "improvement_score": int(result.get("improvement_score", 50)),
    }

st.title("🔨 PromptForge")
st.caption("AI-powered prompt optimizer — stop guessing, start engineering.")
st.divider()

api_key = os.environ.get("ANTHROPIC_API_KEY", "")
if not api_key:
    api_key = st.text_input("🔑 Anthropic API Key", type="password", placeholder="sk-ant-...")
    st.caption("Your key is never stored. [Get one here](https://console.anthropic.com)")

prompt = st.text_area("Your prompt", placeholder="e.g. summarize this article for me", height=120)
col1, col2 = st.columns(2)
with col1:
    target_model = st.selectbox("Target Model", ["Claude", "GPT-4", "Gemini", "Mistral", "General"])
with col2:
    style = st.selectbox("Style", ["General", "Technical", "Creative", "Instructional"])

if st.button("⚡ Optimize Prompt", type="primary", use_container_width=True):
    if not prompt.strip():
        st.warning("Please enter a prompt first.")
    elif not api_key:
        st.error("Please enter your Anthropic API key.")
    else:
        with st.spinner("Optimizing your prompt..."):
            try:
                result = optimize_prompt(prompt, target_model, style, api_key)
                st.divider()
                score = result["improvement_score"]
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.metric("Score", f"{score}/100")
                with col2:
                    st.progress(score / 100)
                if result["issues_found"]:
                    st.write("**Issues detected:**")
                    for issue in result["issues_found"]:
                        st.markdown(f"⚠️ `{issue}`")
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Original**")
                    st.text_area("", result["original"], height=200, disabled=True, key="original")
                with col2:
                    st.write("**✦ Optimized**")
                    st.text_area("", result["optimized"], height=200, key="optimized")
            except Exception as e:
                st.error(f"Error: {str(e)}")

st.divider()
st.caption("Built at Swecha AI/ML Hackathon · [code.swecha.org/charanladi/promptforge](https://code.swecha.org/charanladi/promptforge)")
