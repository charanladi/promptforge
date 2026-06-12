import streamlit as st
from groq import Groq
import json
import re
import os

st.set_page_page_config(page_title="PromptForge", page_icon="🔨", layout="centered")

LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Kannada": "kn",
    "Bengali": "bn",
    "Marathi": "mr",
}

UI_TEXT = {
    "en": {
        "caption": "AI-powered prompt optimizer — stop guessing, start engineering.",
        "prompt_label": "Your prompt",
        "prompt_placeholder": "e.g. summarize this article for me",
        "model_label": "Optimize for Model",
        "style_label": "Style",
        "button": "⚡ Optimize Prompt",
        "score_label": "Improvement Score",
        "issues_label": "Issues detected:",
        "original_label": "Original",
        "optimized_label": "✦ Optimized",
        "warning": "Please enter a prompt first.",
        "error": "Service unavailable. Please try again later.",
        "spinner": "Optimizing your prompt...",
        "lang_instruction": "Respond entirely in English.",
    },
    "hi": {
        "caption": "AI-संचालित प्रॉम्प्ट ऑप्टिमाइज़र — अनुमान बंद करें, इंजीनियरिंग शुरू करें।",
        "prompt_label": "आपका प्रॉम्प्ट",
        "prompt_placeholder": "जैसे: इस लेख को संक्षेप में बताएं",
        "model_label": "मॉडल के लिए अनुकूलित करें",
        "style_label": "शैली",
        "button": "⚡ प्रॉम्प्ट अनुकूलित करें",
        "score_label": "सुधार स्कोर",
        "issues_label": "पाई गई समस्याएं:",
        "original_label": "मूल",
        "optimized_label": "✦ अनुकूलित",
        "warning": "कृपया पहले एक प्रॉम्प्ट दर्ज करें।",
        "error": "सेवा अनुपलब्ध है। कृपया बाद में पुनः प्रयास करें।",
        "spinner": "आपका प्रॉम्प्ट अनुकूलित किया जा रहा है...",
        "lang_instruction": "पूरी तरह हिंदी में जवाब दें।",
    },
    "te": {
        "caption": "AI-ఆధారిత ప్రాంప్ట్ ఆప్టిమైజర్ — అంచనాలు ఆపండి, ఇంజినీరింగ్ ప్రారంభించండి.",
        "prompt_label": "మీ ప్రాంప్ట్",
        "prompt_placeholder": "ఉదా: ఈ వ్యాసాన్ని సంక్షేపంగా చెప్పండి",
        "model_label": "మోడల్ కోసం ఆప్టిమైజ్ చేయండి",
        "style_label": "శైలి",
        "button": "⚡ ప్రాంప్ట్ ఆప్టిమైజ్ చేయండి",
        "score_label": "మెరుగుదల స్కోర్",
        "issues_label": "గుర్తించిన సమస్యలు:",
        "original_label": "అసలు",
        "optimized_label": "✦ ఆప్టిమైజ్ చేయబడింది",
        "warning": "దయచేసి ముందు ప్రాంప్ట్ నమోదు చేయండి.",
        "error": "సేవ అందుబాటులో లేదు. దయచేసి తర్వాత మళ్లీ ప్రయత్నించండి.",
        "spinner": "మీ ప్రాంప్ట్ ఆప్టిమైజ్ అవుతోంది...",
        "lang_instruction": "పూర్తిగా తెలుగులో సమాధానం ఇవ్వండి.",
    },
    "ta": {
        "caption": "AI-இயக்கும் prompt optimizer — யூகிப்பதை நிறுத்துங்கள், பொறியியல் தொடங்குங்கள்.",
        "prompt_label": "உங்கள் prompt",
        "prompt_placeholder": "எ.கா: இந்த கட்டுரையை சுருக்கமாக சொல்லுங்கள்",
        "model_label": "மாடலுக்காக மேம்படுத்து",
        "style_label": "பாணி",
        "button": "⚡ Prompt மேம்படுத்து",
        "score_label": "மேம்பாட்டு மதிப்பெண்",
        "issues_label": "கண்டறியப்பட்ட சிக்கல்கள்:",
        "original_label": "அசல்",
        "optimized_label": "✦ மேம்படுத்தப்பட்டது",
        "warning": "முதலில் ஒரு prompt உள்ளிடவும்.",
        "error": "சேவை கிடைக்கவில்லை. பின்னர் மீண்டும் முயற்சிக்கவும்.",
        "spinner": "உங்கள் prompt மேம்படுத்தப்படுகிறது...",
        "lang_instruction": "முழுவதும் தமிழில் பதில் அளிக்கவும்.",
    },
    "kn": {
        "caption": "AI-ಚಾಲಿತ ಪ್ರಾಂಪ್ಟ್ ಆಪ್ಟಿಮೈಜರ್ — ಊಹಿಸುವುದನ್ನು ನಿಲ್ಲಿಸಿ, ಎಂಜಿನಿಯರಿಂಗ್ ಪ್ರಾರಂಭಿಸಿ.",
        "prompt_label": "ನಿಮ್ಮ ಪ್ರಾಂಪ್ಟ್",
        "prompt_placeholder": "ಉದಾ: ಈ ಲೇಖನವನ್ನು ಸಂಕ್ಷಿಪ್ತವಾಗಿ ಹೇಳಿ",
        "model_label": "ಮಾಡೆಲ್‌ಗಾಗಿ ಆಪ್ಟಿಮೈಜ್ ಮಾಡಿ",
        "style_label": "ಶೈಲಿ",
        "button": "⚡ ಪ್ರಾಂಪ್ಟ್ ಆಪ್ಟಿಮೈಜ್ ಮಾಡಿ",
        "score_label": "ಸುಧಾರಣೆ ಸ್ಕೋರ್",
        "issues_label": "ಪತ್ತೆಯಾದ ಸಮಸ್ಯೆಗಳು:",
        "original_label": "ಮೂಲ",
        "optimized_label": "✦ ಆಪ್ಟಿಮೈಜ್ ಮಾಡಲಾಗಿದೆ",
        "warning": "ದಯವಿಟ್ಟು ಮೊದಲು ಪ್ರಾಂಪ್ಟ್ ನಮೂದಿಸಿ.",
        "error": "ಸೇವೆ ಲಭ್ಯವಿಲ್ಲ. ದಯವಿಟ್ಟು ನಂತರ ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
        "spinner": "ನಿಮ್ಮ ಪ್ರಾಂಪ್ಟ್ ಆಪ್ಟಿಮೈಜ್ ಆಗುತ್ತಿದೆ...",
        "lang_instruction": "ಸಂಪೂರ್ಣವಾಗಿ ಕನ್ನಡದಲ್ಲಿ ಉತ್ತರಿಸಿ.",
    },
    "bn": {
        "caption": "AI-চালিত প্রম্পট অপ্টিমাইজার — অনুমান বন্ধ করুন, ইঞ্জিনিয়ারিং শুরু করুন।",
        "prompt_label": "আপনার প্রম্পট",
        "prompt_placeholder": "যেমন: এই নিবন্ধটি সংক্ষেপে বলুন",
        "model_label": "মডেলের জন্য অপ্টিমাইজ করুন",
        "style_label": "শৈলী",
        "button": "⚡ প্রম্পট অপ্টিমাইজ করুন",
        "score_label": "উন্নতি স্কোর",
        "issues_label": "সনাক্ত করা সমস্যা:",
        "original_label": "মূল",
        "optimized_label": "✦ অপ্টিমাইজড",
        "warning": "অনুগ্রহ করে প্রথমে একটি প্রম্পট দিন।",
        "error": "সেবা অনুপলব্ধ। পরে আবার চেষ্টা করুন।",
        "spinner": "আপনার প্রম্পট অপ্টিমাইজ হচ্ছে...",
        "lang_instruction": "সম্পূর্ণ বাংলায় উত্তর দিন।",
    },
    "mr": {
        "caption": "AI-चालित प्रॉम्प्ट ऑप्टिमायझर — अंदाज थांबवा, अभियांत्रिकी सुरू करा.",
        "prompt_label": "तुमचा प्रॉम्प्ट",
        "prompt_placeholder": "उदा: हा लेख थोडक्यात सांगा",
        "model_label": "मॉडेलसाठी ऑप्टिमाइझ करा",
        "style_label": "शैली",
        "button": "⚡ प्रॉम्प्ट ऑप्टिमाइझ करा",
        "score_label": "सुधारणा स्कोर",
        "issues_label": "आढळलेल्या समस्या:",
        "original_label": "मूळ",
        "optimized_label": "✦ ऑप्टिमाइझ केलेले",
        "warning": "कृपया आधी प्रॉम्प्ट टाका.",
        "error": "सेवा उपलब्ध नाही. नंतर पुन्हा प्रयत्न करा.",
        "spinner": "तुमचा प्रॉम्प्ट ऑप्टिमाइझ होत आहे...",
        "lang_instruction": "संपूर्णपणे मराठीत उत्तर द्या.",
    },
}

MODEL_TIPS = {
    "Gemini": "Gemini works well with direct, concise instructions.",
    "GPT-4": "GPT-4 benefits from numbered instructions and explicit examples.",
    "Claude": "Claude responds best to explicit role definitions.",
    "Mistral": "Mistral is instruction-tuned; use clear imperative sentences.",
    "General": "Use clear role definitions, explicit output formats, and specify constraints.",
}

STYLE_TIPS = {
    "General": "Balance clarity and flexibility.",
    "Technical": "Use precise technical language.",
    "Creative": "Allow creative latitude.",
    "Instructional": "Break into clear steps.",
}

SYSTEM_PROMPT = """You are PromptForge, an expert prompt engineer. Analyze the user's rough prompt and rewrite it into a highly optimized version.

{lang_instruction}

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
- All text in response must be in the selected language

Model context: {model_tips}
Style context: {style_tips}
"""

def optimize_prompt(prompt, target_model, style, api_key, lang_code):
    client = Groq(api_key=api_key)
    t = UI_TEXT.get(lang_code, UI_TEXT["en"])
    system = SYSTEM_PROMPT.format(
        lang_instruction=t["lang_instruction"],
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

api_key = st.secrets.get("GROQ_API_KEY", "") or os.environ.get("GROQ_API_KEY", "")

# Language selector top right
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🔨 PromptForge")
with col2:
    selected_lang = st.selectbox("🌐", list(LANGUAGES.keys()), label_visibility="collapsed")

lang_code = LANGUAGES[selected_lang]
t = UI_TEXT.get(lang_code, UI_TEXT["en"])

st.caption(t["caption"])
st.divider()

prompt = st.text_area(t["prompt_label"], placeholder=t["prompt_placeholder"], height=120)
col1, col2 = st.columns(2)
with col1:
    target_model = st.selectbox(t["model_label"], ["Gemini", "GPT-4", "Claude", "Mistral", "General"])
with col2:
    style = st.selectbox(t["style_label"], ["General", "Technical", "Creative", "Instructional"])

if st.button(t["button"], type="primary", use_container_width=True):
    if not prompt.strip():
        st.warning(t["warning"])
    elif not api_key:
        st.error(t["error"])
    else:
        with st.spinner(t["spinner"]):
            try:
                result = optimize_prompt(prompt, target_model, style, api_key, lang_code)
                st.divider()
                score = result["improvement_score"]
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.metric(t["score_label"], f"{score}/100")
                with col2:
                    st.progress(score / 100)
                if result["issues_found"]:
                    st.write(f"**{t['issues_label']}**")
                    for issue in result["issues_found"]:
                        st.markdown(f"⚠️ `{issue}`")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**{t['original_label']}**")
                    st.text_area("", result["original"], height=200, disabled=True, key="original")
                with col2:
                    st.write(f"**{t['optimized_label']}**")
                    st.text_area("", result["optimized"], height=200, key="optimized")
            except Exception as e:
                st.error(f"Error: {str(e)}")

st.divider()
st.caption("Built at Swecha AI/ML Hackathon · [code.swecha.org/charanladi/promptforge](https://code.swecha.org/charanladi/promptforge)")
