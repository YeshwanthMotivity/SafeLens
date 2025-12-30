# from fastapi import APIRouter, UploadFile, File
# from fastapi.responses import StreamingResponse
# from utils.image_masker import mask_sensitive_areas
# import io

# router = APIRouter()

# @router.post("/image/analyze")
# async def analyze_image(file: UploadFile = File(...)):
#     try:
#         # Read uploaded file bytes
#         file_bytes = await file.read()

#         # Mask sensitive areas
#         masked_image_bytes, detected_regions = mask_sensitive_areas(file_bytes)

#         # Return masked image as response
#         return StreamingResponse(io.BytesIO(masked_image_bytes), media_type="image/jpeg")

#     except ValueError as e:
#         return {"detail": str(e)}


# # ---------------- Imports ----------------
# import logging
# from fastapi import APIRouter, File, UploadFile, HTTPException
# from utils.ocr_extractor import extract_text_from_image
# from utils.ner_detector import mask_sensitive_data
# from utils.prompt_optimizer import PromptOptimizer
# import asyncio

# # If you already have these utilities imported elsewhere, skip duplicates:
# from services.llm_enhancer import enhance_prompt_llm   # Your Groq function
# from services.gemini_client import call_gemini          # Your Gemini API function
# from models.responses import AnalyzeResponse            # Your response schema

# # ---------------- Router ----------------
# router = APIRouter()

# # Initialize the optimizer once
# optimizer = PromptOptimizer()

# # ---------------- Endpoint ----------------
# @router.post("/analyze_image", response_model=AnalyzeResponse)
# async def analyze_image(file: UploadFile = File(...)):
#     """
#     Full flow: Image → Text → Mask → Optimize → Refine → Generate
#     """
#     try:
#         logging.info("Step 1: Received image for processing")

#         # 🧾 Step 2: OCR extraction
#         image_bytes = await file.read()
#         extracted_text = extract_text_from_image(image_bytes)

#         # 🧩 Step 3: Mask sensitive info
#         masked_result = mask_sensitive_data(extracted_text)
#         masked_text = masked_result["masked_text"]

#         # 🎯 Step 4: Detect intent
#         intents, sources = optimizer.detect_intents(masked_text)

#         # 🧠 Step 5: Optimize prompt
#         optimized_prompt, technique, breakdown = optimizer.optimize_prompt_multi(masked_text, intents)

#         # 🪄 Step 6: Enhance prompt via Groq
#         enhanced_prompt = await enhance_prompt_llm(masked_text, technique, {
#             "persona": "Assistant",
#             "audience": "User",
#             "tone": "Neutral",
#             "instruction": "Respond appropriately based on extracted content",
#             "data": "",
#             "format": "Text",
#             "llm_guardrails": optimizer.guardrails
#         })

#         # 🤖 Step 7: Send refined prompt to Gemini for final result
#         final_output = await call_gemini(enhanced_prompt)

#         # 📦 Step 8: Return unified response
#         return AnalyzeResponse(
#             original_text=extracted_text,
#             masked_text=masked_text,
#             detected_entities=masked_result["detected_entities"],
#             triggered_keywords=masked_result["triggered_keywords"],
#             private_contexts=masked_result["private_contexts"],
#             sensitivity_score=masked_result["sensitivity_score"],
#             sensitivity_level=masked_result["sensitivity_level"],
#             detected_intents=intents,
#             intent_sources=sources,
#             intent_breakdown=breakdown,
#             selected_prompt_technique=technique,
#             optimized_prompt=optimized_prompt,
#             prompt_template=enhanced_prompt,
#             components_breakdown={
#                 "persona": "Assistant",
#                 "audience": "User",
#                 "tone": "Neutral",
#                 "context": masked_text
#             },
#             llm_response=final_output,
#             status="✅ Image processed successfully and LLM response generated."
#         )

#     except Exception as e:
#         logging.error(f"Image analysis failed: {e}")
#         raise HTTPException(status_code=500, detail=str(e)) 


# ---------------- Imports ----------------
import os
import logging
from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from utils.ocr_extractor import extract_text_from_image
from utils.ner_detector import mask_sensitive_data
from utils.prompt_optimizer import PromptOptimizer
import google.generativeai as genai
from groq import Groq
import asyncio

# ---------------- Config ----------------
logging.basicConfig(level=logging.INFO, format="🧩 [%(levelname)s] → %(message)s")
router = APIRouter()
optimizer = PromptOptimizer()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    logging.warning("⚠️ GEMINI_API_KEY not set. Gemini API calls may fail.")

groq_client = Groq(api_key=GROQ_API_KEY)

# ---------------- Response Model ----------------
class AnalyzeResponse(BaseModel):
    original_text: str
    masked_text: str
    detected_entities: Dict[str, List[str]]
    triggered_keywords: Dict[str, List[str]]
    private_contexts: List[str]
    sensitivity_score: float
    sensitivity_level: str
    detected_intents: List[str]
    intent_sources: Dict[str, Any]
    intent_breakdown: Dict[str, Any]
    selected_prompt_technique: str
    optimized_prompt: str
    prompt_template: str
    components_breakdown: Dict[str, Any]
    llm_response: str
    status: str


# ---------------------- Groq Prompt Enhancer ----------------------
async def enhance_prompt_llm(masked_text: str, technique: str, components: Dict[str, Any]) -> str:
    """
    Uses Groq to refine the prompt ONLY — not generate the final answer.
    Inputs:
      - masked_text: user's masked input text (with placeholders)
      - technique: selected technique string (e.g., "Role-based + Few-shot + Step-by-step")
      - components: dict with keys persona, audience, tone, instruction, data, format, llm_guardrails
    Returns:
      - single refined prompt string ready to send to Gemini
    """
    logging.info("Step 3a: Starting Groq prompt enhancement (advanced prompt engineer mode)")
    try:
        # Safely extract components with defaults
        persona = components.get("persona", "Assistant")
        audience = components.get("audience", "User")
        tone = components.get("tone", "Neutral")
        instruction = components.get("instruction", "")
        data = components.get("data", "")
        fmt = components.get("format", "Text")
        guardrails = components.get("llm_guardrails", [])

        # Build guardrails text
        guardrails_text = "\n".join([f"- {g}" for g in guardrails]) if guardrails else "- Respect privacy and do not reveal personal information."

        # Groq system/user prompt: explicit, deterministic, and strict.
        groq_system = (
            "You are an Advanced Prompt Engineer (APE). Your only job is to produce a single, "
            "high-quality refined prompt for a downstream LLM (Gemini). You MUST NOT generate the final answer. "
            "Be precise, concise, and deterministic. Preserve placeholders like [MASKED_COMPANY] and [MASKED_STREET_ADDRESS]. "
            "Do not include internal reasoning, analysis, or meta commentary — return only the refined prompt text."
        )

        groq_user = f"""
Technique: {technique}

USER INPUT (masked):
{masked_text}

COMPONENTS:
Persona: {persona}
Audience: {audience}
Tone: {tone}
Instruction: {instruction}
Data: {data}
Format: {fmt}

LLM GUARDRAILS:
{guardrails_text}

TASK (strict):
1) Combine the above into a single, production-ready prompt for Gemini. The prompt must:
   - Start with a role line, e.g., "You are a {persona}..."
   - Include a one-sentence context that preserves the masked_text placeholders.
   - Provide clear, numbered step-by-step instructions for the downstream LLM to generate the requested output.
   - Explicitly state any constraints (e.g., "Do not include addresses" or "Do not invent facts") using the guardrails.
   - Set output format expectations (e.g., headings, bullet points, tables) as per 'Format'.
   - Keep the prompt under 600 words, but rich enough to elicit a precise investor-ready response.
2) Output only the final refined prompt text — nothing else.
"""

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: groq_client.chat.completions.create(
                model="groq/compound",
                messages=[
                    {"role": "system", "content": groq_system},
                    {"role": "user", "content": groq_user}
                ],
                temperature=0.25,   # deterministic
                max_tokens=800
            )
        )

        final_prompt = response.choices[0].message.content.strip()
        logging.info("Groq enhancement successful (refined prompt produced)")
        return final_prompt

    except Exception as e:
        logging.error(f"Groq enhancement failed: {e}")
        # fallback to a simple constructed prompt if Groq fails
        fallback_prompt = PROMPT_TEMPLATES.get(technique, PROMPT_TEMPLATES["General"]).format(context=masked_text)
        return fallback_prompt


# ---------------- Gemini Client ----------------
async def call_gemini(prompt: str) -> str:
    try:
        if not GEMINI_API_KEY:
            return "Gemini API Key not set."
        model = genai.GenerativeModel("gemini-2.5-flash")
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, lambda: model.generate_content(prompt))
        return getattr(response, "text", "No response from Gemini.")
    except Exception as e:
        logging.error(f"Gemini call failed: {e}")
        return f"Gemini API error: {e}"

# ---------------- Endpoint ----------------
@router.post("/analyze_image", response_model=AnalyzeResponse)
async def analyze_image(file: UploadFile = File(...)):
    try:
        logging.info("📸 Step 1: Reading uploaded image")
        image_bytes = await file.read()

        logging.info("🧾 Step 2: Extracting text using OCR")
        extracted_text = extract_text_from_image(image_bytes)

        logging.info("🛡️ Step 3: Masking sensitive information")
        masked_result = mask_sensitive_data(extracted_text)
        masked_text = masked_result["masked_text"]

        logging.info("🧠 Step 4: Detecting intents")
        intents, sources = optimizer.detect_intents(masked_text)

        logging.info("🎯 Step 5: Optimizing prompt")
        optimized_prompt, technique, breakdown = optimizer.optimize_prompt_multi(masked_text, intents)

        logging.info("✨ Step 6: Enhancing prompt via Groq")
        enhanced_prompt = await enhance_prompt_llm(masked_text, technique, {
            "persona": "Assistant",
            "audience": "User",
            "tone": "Neutral",
            "instruction": "Respond appropriately based on extracted content",
            "data": "",
            "format": "Text",
            "llm_guardrails": optimizer.guardrails
        })

        logging.info("🤖 Step 7: Calling Gemini API")
        final_output = await call_gemini(enhanced_prompt)

        logging.info("✅ Step 8: Returning unified response")
        return AnalyzeResponse(
            original_text=extracted_text,
            masked_text=masked_text,
            detected_entities=masked_result["detected_entities"],
            triggered_keywords=masked_result["triggered_keywords"],
            private_contexts=masked_result["private_contexts"],
            sensitivity_score=masked_result["sensitivity_score"],
            sensitivity_level=masked_result["sensitivity_level"],
            detected_intents=intents,
            intent_sources=sources,
            intent_breakdown=breakdown,
            selected_prompt_technique=technique,
            optimized_prompt=optimized_prompt,
            prompt_template=enhanced_prompt,
            components_breakdown={
                "persona": "Assistant",
                "audience": "User",
                "tone": "Neutral",
                "context": masked_text
            },
            llm_response=final_output,
            status="✅ Image processed successfully and LLM response generated."
        )

    except Exception as e:
        logging.error(f"❌ Image analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
