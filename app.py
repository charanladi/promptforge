import streamlit as st
from groq import Groq
import json
import re
import os

st.set_page_config(page_title="PromptForge", page_icon="🔨", layout="centered")

MODEL_TIPS = {
    "Gemini": "Gemini works well with direct, concise instructions. Include examples for complex tasks.",
    "GPT-4": "GPT-4 benefits from numbered instructions and explicit examples.",
    "Claude": "Claude responds best to explicit role definitions and structured output formats.",
    "Mistral": "Mistral is instruction-tuned; use clear imperative sentences.",
    "General": "Use clear role definitions, explicit output formats, and specify constraints.",
}

STYLE_TIPS = {
    "General": "Balance clarity and flexibility. Define role, task, format, and constraints.",
    "Technical": "Use precise technical language. Specify output structure.",
    "Creative": "Allow creative latitude. Specify tone and desired emotional effect.",
    "Instructional": "Break into clear steps. Specify audience expertise level.",
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
    client = Groq(api_key=api_key)
    system = SYSTEM_PROMPT.format(
        model_tips=MODEL_TIPS.get(target_model, MODEL_TIPS["General"]),
        style_tips=STYLE_TIPS.get(style, STYLE_TIPS["General"])
    )
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": f"Optimize this prompt:\n\n{prompt}"}
        ],
        max_tokens=1024
    )
    raw = response.choices[0].message.content.strip()
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

api_key = st.text_input("🔑 Groq API Key", type="password", placeholder="gsk_...")
st.caption("Free API key at [console.groq.com](https://console.groq.com)")

prompt = st.text_area("Your prompt", placeholder="e.g. summarize this article for me", height=120)
col1, col2 = st.columns(2)
with col1:
    target_model = st.selectbox("Optimize for Model", ["Gemini", "GPT-4", "Claude", "Mistral", "General"])
with col2:
    style = st.selectbox("Style", ["General", "Technical", "Creative", "Instructional"])

if st.button("⚡ Optimize Prompt", type="primary", use_container_width=True):
    if not prompt.strip():
        st.warning("Please enter a prompt first.")
    elif not api_key:
        st.error("Please enter your Groq API key.")
    else:
        with st.spinner("Optimizing your prompt..."):
            try:
                result = optimize_prompt(prompt, target_model, style, api_key)
                st.divider()
                score = result["improvement_score"]
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.metric("Improvement Score", f"{score}/100")
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
