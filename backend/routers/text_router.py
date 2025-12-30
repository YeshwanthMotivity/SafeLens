# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from utils.ner_detector import mask_sensitive_data
# from utils.prompt_optimizer import PromptOptimizer

# router = APIRouter()
# optimizer = PromptOptimizer(ml_model_path="distilbert-base-uncased")
# # Set your ML model path

# class TextInput(BaseModel):
#     text: str

# @router.post("/analyze")
# async def analyze_text(input_data: TextInput):
#     try:
#         # ---------------- Mask sensitive data ----------------
#         result = mask_sensitive_data(input_data.text)
#         masked_text = result["masked_text"]
#         detected_entities = result["detected_entities"]
#         triggered_keywords = result["triggered_keywords"]
#         private_contexts = result["private_contexts"]
#         sensitivity_score = result["sensitivity_score"]
#         sensitivity_level = result["sensitivity_level"]

#         # ---------------- Detect intents (ML + Rule hybrid) ----------------
#         detected_intents, intent_sources = optimizer.detect_intents(input_data.text)

#         # ---------------- Optimize prompt for multi-intent ----------------
#         optimized_prompt, combined_technique, intent_breakdown = optimizer.optimize_prompt_multi(
#             masked_text, detected_intents
#         )

#         # ---------------- Components breakdown ----------------
#         merged_components = {
#             "persona": [],
#             "audience": [],
#             "tone": [],
#             "context": masked_text,
#             "instruction": [],
#             "data": [],
#             "format": [],
#             "llm_guardrails": optimizer.guardrails
#         }

#         for intent in detected_intents:
#             template = optimizer.prompt_templates.get(intent, optimizer.prompt_templates["general"])
#             merged_components["persona"].append(template.get("persona"))
#             merged_components["audience"].append(template.get("audience"))
#             merged_components["tone"].append(template.get("tone"))
#             merged_components["instruction"].append(template.get("instruction"))
#             merged_components["data"].append(template.get("data"))
#             merged_components["format"].append(template.get("format"))

#         # ---------------- Format Detected Entities ----------------
#         formatted_entities = {label: list(set(values)) for label, values in detected_entities.items()}

#         # ---------------- Determine Masking Status ----------------
#         mask_status = (
#             "Sensitive personal data masked. Public entities preserved."
#             if any(detected_entities.values())
#             else "No sensitive data detected. Input remains unchanged."
#         )

#         # ---------------- Response ----------------
#         response = {
#             "original_text": input_data.text,
#             "masked_text": masked_text,
#             "detected_entities": formatted_entities,
#             "triggered_keywords": triggered_keywords,
#             "private_contexts": private_contexts,
#             "sensitivity_score": sensitivity_score,
#             "sensitivity_level": sensitivity_level,
#             "detected_intents": detected_intents,
#             "intent_sources": intent_sources,               # ML vs Rule source
#             "intent_breakdown": intent_breakdown,          # Technique applied per intent
#             "selected_prompt_technique": combined_technique,
#             "optimized_prompt": optimized_prompt,
#             "components_breakdown": merged_components,
#             "status": mask_status + " ✅"
#         }

#         return response

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")

# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from utils.ner_detector import mask_sensitive_data
# from utils.prompt_optimizer import PromptOptimizer
# import google.generativeai as genai  # ✅ Gemini integration

# # ---------------------- Configuration ----------------------
# router = APIRouter()

# # Disable ML in PromptOptimizer (rule-based intents only)
# optimizer = PromptOptimizer(ml_model_path=None)

# # 🔹 Configure Gemini API (Use your key)
# GEMINI_API_KEY = "AIzaSyDF8XWSK1lzwqPfZklEaqsPZGA9DMiYVes"
# genai.configure(api_key=GEMINI_API_KEY)

# class TextInput(BaseModel):
#     text: str


# @router.post("/analyze")
# async def analyze_text(input_data: TextInput):
#     try:
#         # ---------------- Step 1: Mask Sensitive Data ----------------
#         result = mask_sensitive_data(input_data.text)
#         masked_text = result["masked_text"]
#         detected_entities = result["detected_entities"]
#         triggered_keywords = result["triggered_keywords"]
#         private_contexts = result["private_contexts"]
#         sensitivity_score = result["sensitivity_score"]
#         sensitivity_level = result["sensitivity_level"]

#         # ---------------- Step 2: Detect Intents (RULE-BASED ONLY) ----------------
#         detected_intents, intent_sources = optimizer.detect_intents(input_data.text)

#         # ---------------- Step 3: Optimize Prompt ----------------
#         optimized_prompt, combined_technique, intent_breakdown = optimizer.optimize_prompt_multi(
#             masked_text, detected_intents
#         )

#         # ---------------- Step 4: Components Breakdown ----------------
#         merged_components = {
#             "persona": [],
#             "audience": [],
#             "tone": [],
#             "context": masked_text,
#             "instruction": [],
#             "data": [],
#             "format": [],
#             "llm_guardrails": optimizer.guardrails
#         }

#         for intent in detected_intents:
#             template = optimizer.prompt_templates.get(intent, optimizer.prompt_templates["general"])
#             merged_components["persona"].append(template.get("persona"))
#             merged_components["audience"].append(template.get("audience"))
#             merged_components["tone"].append(template.get("tone"))
#             merged_components["instruction"].append(template.get("instruction"))
#             merged_components["data"].append(template.get("data"))
#             merged_components["format"].append(template.get("format"))

#         # ---------------- Step 5: Send Optimized Prompt to Gemini ----------------
#         try:
#             model = genai.GenerativeModel("gemini-1.5-flash")  # ✅ You can change model variant here
#             gemini_response = model.generate_content(optimized_prompt)
#             llm_output = gemini_response.text
#         except Exception as gemini_error:
#             raise HTTPException(status_code=500, detail=f"Gemini API Error: {str(gemini_error)}")

#         # ---------------- Step 6: Format Detected Entities ----------------
#         formatted_entities = {label: list(set(values)) for label, values in detected_entities.items()}

#         # ---------------- Step 7: Determine Masking Status ----------------
#         mask_status = (
#             "Sensitive personal data masked. Public entities preserved."
#             if any(detected_entities.values())
#             else "No sensitive data detected. Input remains unchanged."
#         )

#         # ---------------- Step 8: Response ----------------
#         response = {
#             "original_text": input_data.text,
#             "masked_text": masked_text,
#             "detected_entities": formatted_entities,
#             "triggered_keywords": triggered_keywords,
#             "private_contexts": private_contexts,
#             "sensitivity_score": sensitivity_score,
#             "sensitivity_level": sensitivity_level,
#             "detected_intents": detected_intents,
#             "intent_sources": intent_sources,  # Will always show 'Rule'
#             "intent_breakdown": intent_breakdown,
#             "selected_prompt_technique": combined_technique,
#             "optimized_prompt": optimized_prompt,
#             "components_breakdown": merged_components,
#             "llm_response": llm_output,   # ✅ Gemini’s response
#             "status": mask_status + " ✅"
#         }

#         return response

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")

# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from utils.ner_detector import mask_sensitive_data
# from utils.prompt_optimizer import PromptOptimizer
# import google.generativeai as genai

# # ---------------------- Router Configuration ----------------------
# router = APIRouter()

# # Disable ML in PromptOptimizer (use rule-based intents only)
# optimizer = PromptOptimizer(ml_model_path=None)

# # Configure Gemini API
# GEMINI_API_KEY = "AIzaSyDF8XWSK1lzwqPfZklEaqsPZGA9DMiYVes"
# genai.configure(api_key=GEMINI_API_KEY)

# # ---------------------- Request Model ----------------------
# class TextInput(BaseModel):
#     text: str

# # ---------------------- Endpoint ----------------------
# @router.post("/analyze")
# async def analyze_text(input_data: TextInput):
#     try:
#         # ---------------- Step 1: Mask Sensitive Data ----------------
#         result = mask_sensitive_data(input_data.text)
#         masked_text = result.get("masked_text", "")
#         detected_entities = result.get("detected_entities", {})
#         triggered_keywords = result.get("triggered_keywords", [])
#         private_contexts = result.get("private_contexts", [])
#         sensitivity_score = result.get("sensitivity_score", 0)
#         sensitivity_level = result.get("sensitivity_level", "Low")

#         # ---------------- Step 2: Detect Intents (Rule-based) ----------------
#         detected_intents, intent_sources = optimizer.detect_intents(input_data.text)

#         # ---------------- Step 3: Optimize Prompt ----------------
#         optimized_prompt, combined_technique, intent_breakdown = optimizer.optimize_prompt_multi(
#             masked_text, detected_intents
#         )

#         # ---------------- Step 4: Components Breakdown ----------------
#         merged_components = {
#             "persona": [],
#             "audience": [],
#             "tone": [],
#             "context": masked_text,
#             "instruction": [],
#             "data": [],
#             "format": [],
#             "llm_guardrails": optimizer.guardrails
#         }

#         for intent in detected_intents:
#             template = optimizer.prompt_templates.get(intent, optimizer.prompt_templates["general"])
#             merged_components["persona"].append(template.get("persona"))
#             merged_components["audience"].append(template.get("audience"))
#             merged_components["tone"].append(template.get("tone"))
#             merged_components["instruction"].append(template.get("instruction"))
#             merged_components["data"].append(template.get("data"))
#             merged_components["format"].append(template.get("format"))

#         # ---------------- Step 5: Send Optimized Prompt to Gemini ----------------
#         llm_output = ""
#         try:
#             model = genai.GenerativeModel("gemini-2.5-flash")  # Change model if needed
#             gemini_response = model.generate_content(optimized_prompt)
#             llm_output = gemini_response.text
#         except Exception as gemini_error:
#             llm_output = f"Gemini API Error: {str(gemini_error)}"

#         # ---------------- Step 6: Format Detected Entities ----------------
#         formatted_entities = {label: list(set(values)) for label, values in detected_entities.items()}

#         # ---------------- Step 7: Determine Masking Status ----------------
#         mask_status = (
#             "Sensitive personal data masked. Public entities preserved."
#             if any(detected_entities.values())
#             else "No sensitive data detected. Input remains unchanged."
#         )

#         # ---------------- Step 8: Build Response ----------------
#         response = {
#             "original_text": input_data.text,
#             "masked_text": masked_text,
#             "detected_entities": formatted_entities,
#             "triggered_keywords": triggered_keywords,
#             "private_contexts": private_contexts,
#             "sensitivity_score": sensitivity_score,
#             "sensitivity_level": sensitivity_level,
#             "detected_intents": detected_intents,
#             "intent_sources": intent_sources,
#             "intent_breakdown": intent_breakdown,
#             "selected_prompt_technique": combined_technique,
#             "optimized_prompt": optimized_prompt,
#             "components_breakdown": merged_components,
#             "llm_response": llm_output,
#             "status": mask_status + " ✅"
#         }

#         return response

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")

# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from utils.ner_detector import mask_sensitive_data
# from utils.prompt_optimizer import PromptOptimizer
# import google.generativeai as genai

# # ---------------------- Router Configuration ----------------------
# router = APIRouter()
# optimizer = PromptOptimizer(ml_model_path=None)  # Rule-based intents only

# # Configure Gemini API
# GEMINI_API_KEY = "AIzaSyDF8XWSK1lzwqPfZklEaqsPZGA9DMiYVes"
# genai.configure(api_key=GEMINI_API_KEY)

# # ---------------------- Request Model ----------------------
# class TextInput(BaseModel):
#     text: str

# # ---------------------- Prompt Templates ----------------------
# PROMPT_TEMPLATES = {
#     "Proposal": "Proposal (Role-based + Few-shot)\nYou are a [role]. Based on the following examples, create a proposal for [topic].\n\nExample 1: [Proposal example 1]\nExample 2: [Proposal example 2]\n\nNow, write a proposal for:\n{context}",
#     "Summarization": "Summarization (Zero-shot)\nSummarize the following text briefly:\n{context}",
#     "Task Generation": "Task Generation (Step-by-step + Few-shot)\nGenerate a step-by-step task plan based on these examples:\n\nExample 1:\nStep 1: ...\nStep 2: ...\nExample 2:\nStep 1: ...\nStep 2: ...\n\nNow create a task plan for:\n{context}",
#     "Educational": "Educational (Chain-of-Thought)\nExplain the concept step-by-step:\n\nLet's think through this carefully.\n{context}",
#     "Translation": "Translation (Zero-shot)\nTranslate the following text from English to [language]:\n{context}",
#     "Analysis": "Analysis (Chain-of-Thought)\nAnalyze the following situation carefully step by step:\n{context}\nLet's break it down.",
#     "QA": "QA (Zero-shot)\nQ: {context}\nA: Let's think step-by-step to find the answer.",
#     "Code": "Code (Zero-shot)\nWrite code to accomplish the following task:\n{context}",
#     "General": "General (General Instruction)\nPlease provide detailed information about:\n{context}"
# }

# # ---------------------- Endpoint ----------------------
# @router.post("/analyze")
# async def analyze_text(input_data: TextInput):
#     try:
#         # ---------------- Step 1: Mask Sensitive Data ----------------
#         result = mask_sensitive_data(input_data.text)
#         masked_text = result.get("masked_text", "")
#         detected_entities = result.get("detected_entities", {})
#         triggered_keywords = result.get("triggered_keywords", [])
#         private_contexts = result.get("private_contexts", [])
#         sensitivity_score = result.get("sensitivity_score", 0)
#         sensitivity_level = result.get("sensitivity_level", "Low")

#         # ---------------- Step 2: Detect Intents (Rule-based) ----------------
#         detected_intents, intent_sources = optimizer.detect_intents(input_data.text)

#         # ---------------- Step 3: Optimize Prompt ----------------
#         optimized_prompt, combined_technique, intent_breakdown = optimizer.optimize_prompt_multi(
#             masked_text, detected_intents
#         )

#         # ---------------- Step 3a: Apply Template with Context ----------------
#         selected_technique = combined_technique or "General"
#         selected_prompt_template = PROMPT_TEMPLATES.get(selected_technique, PROMPT_TEMPLATES["General"]).format(
#             context=masked_text
#         )

#         # ---------------- Step 4: Components Breakdown ----------------
#         merged_components = {
#             "persona": [],
#             "audience": [],
#             "tone": [],
#             "context": masked_text,
#             "instruction": [],
#             "data": [],
#             "format": [],
#             "llm_guardrails": optimizer.guardrails
#         }
#         for intent in detected_intents:
#             template = optimizer.prompt_templates.get(intent, optimizer.prompt_templates["general"])
#             merged_components["persona"].append(template.get("persona"))
#             merged_components["audience"].append(template.get("audience"))
#             merged_components["tone"].append(template.get("tone"))
#             merged_components["instruction"].append(template.get("instruction"))
#             merged_components["data"].append(template.get("data"))
#             merged_components["format"].append(template.get("format"))

#         # ---------------- Step 5: Send Prompt to Gemini ----------------
#         llm_output = ""
#         try:
#             model = genai.GenerativeModel("gemini-2.5-flash")
#             gemini_response = model.generate_content(selected_prompt_template)
#             llm_output = gemini_response.text
#         except Exception as gemini_error:
#             llm_output = f"Gemini API Error: {str(gemini_error)}"

#         # ---------------- Step 6: Format Detected Entities ----------------
#         formatted_entities = {label: list(set(values)) for label, values in detected_entities.items()}

#         # ---------------- Step 7: Determine Masking Status ----------------
#         mask_status = (
#             "Sensitive personal data masked. Public entities preserved."
#             if any(detected_entities.values())
#             else "No sensitive data detected. Input remains unchanged."
#         )

#         # ---------------- Step 8: Build Response ----------------
#         response = {
#             "original_text": input_data.text,
#             "masked_text": masked_text,
#             "detected_entities": formatted_entities,
#             "triggered_keywords": triggered_keywords,
#             "private_contexts": private_contexts,
#             "sensitivity_score": sensitivity_score,
#             "sensitivity_level": sensitivity_level,
#             "detected_intents": detected_intents,
#             "intent_sources": intent_sources,
#             "intent_breakdown": intent_breakdown,
#             "selected_prompt_technique": selected_technique,
#             "selected_prompt_template": selected_prompt_template,
#             "optimized_prompt": optimized_prompt,
#             "components_breakdown": merged_components,
#             "llm_response": llm_output,
#             "status": mask_status + " ✅"
#         }

#         return response

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")

# import os
# import re
# import logging
# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from utils.ner_detector import mask_sensitive_data
# from utils.prompt_optimizer import PromptOptimizer
# import google.generativeai as genai
# import ollama

# # ---------------------- Logger ----------------------
# logging.basicConfig(level=logging.INFO, format="🧩 [%(levelname)s] → %(message)s")

# # ---------------------- Router Configuration ----------------------
# router = APIRouter()
# optimizer = PromptOptimizer(ml_model_path=None)  # Rule-based intents only

# # ---------------------- API Keys ----------------------
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# OLLAMA_MODEL_NAME = os.getenv("OLLAMA_MODEL_NAME", "llama3:8b")
# if GEMINI_API_KEY:
#     genai.configure(api_key=GEMINI_API_KEY)
# else:
#     logging.warning("GEMINI_API_KEY not set. Gemini API calls may fail.")

# # ---------------------- Request Model ----------------------
# class TextInput(BaseModel):
#     text: str

# # ---------------------- Prompt Templates ----------------------
# PROMPT_TEMPLATES = {
#     "Proposal": "Proposal (Role-based + Few-shot)\nYou are a [role]. Based on the following examples, create a proposal for [topic].\n\nExample 1: [Proposal example 1]\nExample 2: [Proposal example 2]\n\nNow, write a proposal for:\n{context}",
#     "Summarization": "Summarization (Zero-shot)\nSummarize the following text briefly:\n{context}",
#     "Task Generation": "Task Generation (Step-by-step + Few-shot)\nGenerate a step-by-step task plan based on these examples:\n\nExample 1:\nStep 1: ...\nStep 2: ...\nExample 2:\nStep 1: ...\nStep 2: ...\n\nNow create a task plan for:\n{context}",
#     "Educational": "Educational (Chain-of-Thought)\nExplain the concept step-by-step:\n\nLet's think through this carefully.\n{context}",
#     "Translation": "Translation (Zero-shot)\nTranslate the following text from English to [language]:\n{context}",
#     "Analysis": "Analysis (Chain-of-Thought)\nAnalyze the following situation carefully step by step:\n{context}\nLet's break it down.",
#     "QA": "QA (Zero-shot)\nQ: {context}\nA: Let's think step-by-step to find the answer.",
#     "Code": "Code (Zero-shot)\nWrite code to accomplish the following task:\n{context}",
#     "General": "General (General Instruction)\nPlease provide detailed information about:\n{context}"
# }

# # ---------------------- Helper: Ollama Prompt Enhancer ----------------------
# def enhance_prompt_llm(masked_text: str, technique: str) -> str:
#     """
#     Use Ollama to dynamically enhance the prompt. Fallback to static template if it fails.
#     """
#     try:
#         task = f"""
# You are a Prompt Designer AI.
# Technique: {technique}
# Context: {masked_text}

# Output a neatly structured prompt ready for an LLM.
# """
#         response = ollama.chat(model=OLLAMA_MODEL_NAME, messages=[{"role": "user", "content": task}])
#         # Validate response format
#         if response and isinstance(response, list) and "content" in response[-1]:
#             return response[-1]["content"]
#         elif response and isinstance(response, list) and "message" in response[-1]:
#             return response[-1]["message"]
#         else:
#             logging.warning("Unexpected Ollama response format. Using fallback template.")
#             return PROMPT_TEMPLATES.get(technique, PROMPT_TEMPLATES["General"]).format(context=masked_text)
#     except Exception as e:
#         logging.error(f"Ollama prompt enhancement failed: {e}")
#         return PROMPT_TEMPLATES.get(technique, PROMPT_TEMPLATES["General"]).format(context=masked_text)

# # ---------------------- Endpoint ----------------------
# @router.post("/analyze")
# async def analyze_text(input_data: TextInput):
#     try:
#         # Step 1: Mask Sensitive Data
#         result = mask_sensitive_data(input_data.text)
#         masked_text = result.get("masked_text", "")
#         detected_entities = result.get("detected_entities", {})
#         triggered_keywords = result.get("triggered_keywords", {})
#         private_contexts = result.get("private_contexts", [])
#         sensitivity_score = result.get("sensitivity_score", 0)
#         sensitivity_level = result.get("sensitivity_level", "Low")

#         # Step 2: Detect Intents
#         detected_intents, intent_sources = optimizer.detect_intents(input_data.text)

#         # Step 3: Optimize Prompt
#         optimized_prompt, combined_technique, intent_breakdown = optimizer.optimize_prompt_multi(
#             masked_text, detected_intents
#         )

#         # Step 3a: Enhance Prompt via Ollama
#         selected_technique = combined_technique or "General"
#         selected_prompt_template = enhance_prompt_llm(masked_text, selected_technique)

#         # Step 4: Components Breakdown
#         merged_components = {
#             "persona": [],
#             "audience": [],
#             "tone": [],
#             "context": masked_text,
#             "instruction": [],
#             "data": [],
#             "format": [],
#             "llm_guardrails": optimizer.guardrails
#         }
#         for intent in detected_intents:
#             template = optimizer.prompt_templates.get(intent, optimizer.prompt_templates["general"])
#             merged_components["persona"].append(template.get("persona"))
#             merged_components["audience"].append(template.get("audience"))
#             merged_components["tone"].append(template.get("tone"))
#             merged_components["instruction"].append(template.get("instruction"))
#             merged_components["data"].append(template.get("data"))
#             merged_components["format"].append(template.get("format"))

#         # Step 5: Send Prompt to Gemini
#         llm_output = ""
#         try:
#             model = genai.GenerativeModel("gemini-2.5-flash")
#             gemini_response = model.generate_content(selected_prompt_template)
#             llm_output = gemini_response.text
#         except Exception as gemini_error:
#             llm_output = f"Gemini API Error: {str(gemini_error)}"
#             logging.error(llm_output)

#         # Step 6: Format Detected Entities
#         formatted_entities = {label: list(set(values)) for label, values in detected_entities.items()}

#         # Step 7: Determine Masking Status
#         mask_status = (
#             "Sensitive personal data masked. Public entities preserved."
#             if any(detected_entities.values())
#             else "No sensitive data detected. Input remains unchanged."
#         )

#         # Step 8: Build Response
#         response = {
#             "original_text": input_data.text,
#             "masked_text": masked_text,
#             "detected_entities": formatted_entities,
#             "triggered_keywords": triggered_keywords,
#             "private_contexts": private_contexts,
#             "sensitivity_score": sensitivity_score,
#             "sensitivity_level": sensitivity_level,
#             "detected_intents": detected_intents,
#             "intent_sources": intent_sources,
#             "intent_breakdown": intent_breakdown,
#             "selected_prompt_technique": selected_technique,
#             "selected_prompt_template": selected_prompt_template,
#             "optimized_prompt": optimized_prompt,
#             "components_breakdown": merged_components,
#             "llm_response": llm_output,
#             "status": mask_status + " ✅"
#         }

#         return response

#     except Exception as e:
#         logging.exception(f"Error processing text: {e}")
#         raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")


# import os
# import logging
# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from typing import List, Dict, Any, Optional
# from utils.ner_detector import mask_sensitive_data
# from utils.prompt_optimizer import PromptOptimizer
# import google.generativeai as genai
# import ollama
# import asyncio

# # ---------------------- Logger ----------------------
# logging.basicConfig(level=logging.INFO, format="🧩 [%(levelname)s] → %(message)s")

# # ---------------------- Router ----------------------
# router = APIRouter()
# optimizer = PromptOptimizer(ml_model_path=None)  # Rule-based intents only

# # ---------------------- API Keys ----------------------
# GEMINI_API_KEY = os.getenv("AIzaSyDF8XWSK1lzwqPfZklEaqsPZGA9DMiYVes")
# OLLAMA_MODEL_NAME = os.getenv("OLLAMA_MODEL_NAME", "llama3:8b")
# if GEMINI_API_KEY:
#     genai.configure(api_key=GEMINI_API_KEY)
# else:
#     logging.warning("GEMINI_API_KEY not set. Gemini API calls may fail.")

# # ---------------------- Request & Response Models ----------------------
# class TextInput(BaseModel):
#     text: str

# class AnalyzeResponse(BaseModel):
#     original_text: str
#     masked_text: str
#     detected_entities: Dict[str, List[str]]
#     triggered_keywords: Dict[str, List[str]]
#     private_contexts: List[str]
#     sensitivity_score: float
#     sensitivity_level: str
#     detected_intents: List[str]
#     intent_sources: Dict[str, Any]
#     intent_breakdown: Dict[str, Any]
#     selected_prompt_technique: str
#     selected_prompt_template: str
#     optimized_prompt: str
#     components_breakdown: Dict[str, Any]
#     llm_response: str
#     status: str

# # ---------------------- Prompt Templates ----------------------
# PROMPT_TEMPLATES = {
#     "Proposal": "...",
#     "Summarization": "...",
#     "Task Generation": "...",
#     "Educational": "...",
#     "Translation": "...",
#     "Analysis": "...",
#     "QA": "...",
#     "Code": "...",
#     "General": "General (General Instruction)\nPlease provide detailed information about:\n{context}"
# }

# # ---------------------- Ollama Prompt Enhancer ----------------------
# async def enhance_prompt_llm(masked_text: str, technique: str) -> str:
#     try:
#         task = f"""
# You are a Prompt Designer AI.
# Technique: {technique}
# Context: {masked_text}

# Output a neatly structured prompt ready for an LLM.
# """
#         loop = asyncio.get_event_loop()
#         response = await loop.run_in_executor(None, lambda: ollama.chat(
#             model=OLLAMA_MODEL_NAME, messages=[{"role": "user", "content": task}]
#         ))
#         if response and isinstance(response, list):
#             return response[-1].get("content") or response[-1].get("message") \
#                    or PROMPT_TEMPLATES.get(technique, PROMPT_TEMPLATES["General"]).format(context=masked_text)
#         return PROMPT_TEMPLATES.get(technique, PROMPT_TEMPLATES["General"]).format(context=masked_text)
#     except Exception as e:
#         logging.error(f"Ollama enhancement failed: {e}")
#         return PROMPT_TEMPLATES.get(technique, PROMPT_TEMPLATES["General"]).format(context=masked_text)

# # ---------------------- Gemini LLM ----------------------
# async def call_gemini(prompt: str) -> str:
#     if not GEMINI_API_KEY:
#         return "Gemini API Key not set. Skipping LLM call."
#     try:
#         loop = asyncio.get_event_loop()
#         model = genai.GenerativeModel("gemini-2.5-flash")
#         response = await loop.run_in_executor(None, lambda: model.generate_content(prompt))
#         return getattr(response, "text", "No response from Gemini.")
#     except Exception as e:
#         logging.error(f"Gemini API call failed: {e}")
#         return f"Gemini API Error: {str(e)}"

# # ---------------------- Endpoint ----------------------
# @router.post("/analyze", response_model=AnalyzeResponse)
# async def analyze_text(input_data: TextInput):
#     try:
#         # Step 1: Mask Sensitive Data
#         result = mask_sensitive_data(input_data.text)
#         masked_text = result.get("masked_text", "")
#         detected_entities = {k: list(set(v)) for k, v in result.get("detected_entities", {}).items()}
#         triggered_keywords = result.get("triggered_keywords", {})
#         private_contexts = result.get("private_contexts", [])
#         sensitivity_score = result.get("sensitivity_score", 0)
#         sensitivity_level = result.get("sensitivity_level", "Low")

#         # Step 2: Detect Intents
#         detected_intents, intent_sources = optimizer.detect_intents(input_data.text)

#         # Step 3: Optimize Prompt
#         optimized_prompt, combined_technique, intent_breakdown = optimizer.optimize_prompt_multi(
#             masked_text, detected_intents
#         )
#         selected_technique = combined_technique or "General"
#         selected_prompt_template = await enhance_prompt_llm(masked_text, selected_technique)

#         # Step 4: Components Breakdown
#         merged_components = {k: [] for k in ["persona","audience","tone","instruction","data","format"]}
#         merged_components["context"] = masked_text
#         merged_components["llm_guardrails"] = getattr(optimizer, "guardrails", [])
#         for intent in detected_intents:
#             template = optimizer.prompt_templates.get(intent, optimizer.prompt_templates.get("general", {}))
#             for key in ["persona","audience","tone","instruction","data","format"]:
#                 merged_components[key].append(template.get(key, ""))

#         # Step 5: LLM Call
#         llm_output = await call_gemini(selected_prompt_template)

#         # Step 6: Masking Status
#         mask_status = "Sensitive personal data masked. Public entities preserved." \
#                       if any(detected_entities.values()) else "No sensitive data detected. Input remains unchanged."

#         # Step 7: Build Response
#         return AnalyzeResponse(
#             original_text=input_data.text,
#             masked_text=masked_text,
#             detected_entities=detected_entities,
#             triggered_keywords=triggered_keywords,
#             private_contexts=private_contexts,
#             sensitivity_score=sensitivity_score,
#             sensitivity_level=sensitivity_level,
#             detected_intents=detected_intents,
#             intent_sources=intent_sources,
#             intent_breakdown=intent_breakdown,
#             selected_prompt_technique=selected_technique,
#             selected_prompt_template=selected_prompt_template,
#             optimized_prompt=optimized_prompt,
#             components_breakdown=merged_components,
#             llm_response=llm_output,
#             status=mask_status + " ✅"
#         )

#     except Exception as e:
#         logging.exception(f"Error processing text: {e}")
#         raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")

# import os
# import logging
# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from typing import List, Dict, Any
# from utils.ner_detector import mask_sensitive_data
# from utils.prompt_optimizer import PromptOptimizer
# import google.generativeai as genai
# import ollama
# import asyncio

# # ---------------------- Logger ----------------------
# logging.basicConfig(level=logging.INFO, format="🧩 [%(levelname)s] → %(message)s")

# # ---------------------- Router ----------------------
# router = APIRouter()
# optimizer = PromptOptimizer(ml_model_path=None)  # Rule-based intents only

# # ---------------------- API Keys ----------------------
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# OLLAMA_MODEL_NAME = os.getenv("OLLAMA_MODEL_NAME", "llama3:8b")
# if GEMINI_API_KEY:
#     genai.configure(api_key=GEMINI_API_KEY)
# else:
#     logging.warning("GEMINI_API_KEY not set. Gemini API calls may fail.")

# # ---------------------- Request & Response Models ----------------------
# class TextInput(BaseModel):
#     text: str

# class AnalyzeResponse(BaseModel):
#     original_text: str
#     masked_text: str
#     detected_entities: Dict[str, List[str]]
#     triggered_keywords: Dict[str, List[str]]
#     private_contexts: List[str]
#     sensitivity_score: float
#     sensitivity_level: str
#     detected_intents: List[str]
#     intent_sources: Dict[str, Any]
#     intent_breakdown: Dict[str, Any]
#     selected_prompt_technique: str
#     selected_prompt_template: str
#     optimized_prompt: str
#     components_breakdown: Dict[str, Any]
#     llm_response: str
#     status: str

# # ---------------------- Prompt Templates ----------------------
# PROMPT_TEMPLATES = {
#     "Proposal": "...",
#     "Summarization": "...",
#     "Task Generation": "...",
#     "Educational": "...",
#     "Translation": "...",
#     "Analysis": "...",
#     "QA": "...",
#     "Code": "...",
#     "General": "General (General Instruction)\nPlease provide detailed information about:\n{context}"
# }

# # ---------------------- Ollama Prompt Enhancer ----------------------
# async def enhance_prompt_llm(masked_text: str, technique: str) -> str:
#     logging.info("Step 3a: Starting Ollama prompt enhancement")
#     try:
#         task = f"""
# You are a Prompt Designer AI.
# Technique: {technique}
# Context: {masked_text}

# Output a neatly structured prompt ready for an LLM.
# """
#         loop = asyncio.get_event_loop()
#         response = await loop.run_in_executor(None, lambda: ollama.chat(
#             model=OLLAMA_MODEL_NAME, messages=[{"role": "user", "content": task}]
#         ))
#         logging.info("Ollama response received")
#         if response and isinstance(response, list):
#             return response[-1].get("content") or response[-1].get("message") \
#                    or PROMPT_TEMPLATES.get(technique, PROMPT_TEMPLATES["General"]).format(context=masked_text)
#         return PROMPT_TEMPLATES.get(technique, PROMPT_TEMPLATES["General"]).format(context=masked_text)
#     except Exception as e:
#         logging.error(f"Ollama enhancement failed: {e}")
#         return PROMPT_TEMPLATES.get(technique, PROMPT_TEMPLATES["General"]).format(context=masked_text)

# # ---------------------- Gemini LLM ----------------------
# async def call_gemini(prompt: str) -> str:
#     logging.info("Step 5: Starting Gemini API call")
#     if not GEMINI_API_KEY:
#         logging.warning("GEMINI_API_KEY not set, skipping Gemini call")
#         return "Gemini API Key not set. Skipping LLM call."
#     try:
#         loop = asyncio.get_event_loop()
#         model = genai.GenerativeModel("gemini-2.5-flash")
#         response = await loop.run_in_executor(None, lambda: model.generate_content(prompt))
#         logging.info("Gemini response received")
#         return getattr(response, "text", "No response from Gemini.")
#     except Exception as e:
#         logging.error(f"Gemini API call failed: {e}")
#         return f"Gemini API Error: {str(e)}"

# # ---------------------- Endpoint ----------------------
# @router.post("/analyze", response_model=AnalyzeResponse)
# async def analyze_text(input_data: TextInput):
#     try:
#         logging.info("Step 1: Masking sensitive data")
#         result = mask_sensitive_data(input_data.text)
#         masked_text = result.get("masked_text", "")
#         detected_entities = {k: list(set(v)) for k, v in result.get("detected_entities", {}).items()}
#         triggered_keywords = result.get("triggered_keywords", {})
#         private_contexts = result.get("private_contexts", [])
#         sensitivity_score = result.get("sensitivity_score", 0)
#         sensitivity_level = result.get("sensitivity_level", "Low")
#         logging.info(f"Masked Text: {masked_text}")

#         logging.info("Step 2: Detecting intents")
#         detected_intents, intent_sources = optimizer.detect_intents(input_data.text)
#         logging.info(f"Detected Intents:     {detected_intents}")

#         logging.info("Step 3: Optimizing prompt")
#         optimized_prompt, combined_technique, intent_breakdown = optimizer.optimize_prompt_multi(
#             masked_text, detected_intents
#         )
#         selected_technique = combined_technique or "General"
#         logging.info(f"Selected Prompt Technique: {selected_technique}")

#         logging.info("Step 3a: Enhancing prompt via Ollama")
#         selected_prompt_template = await enhance_prompt_llm(masked_text, selected_technique)
#         logging.info(f"Selected Prompt Template: {selected_prompt_template[:100]}...")

#         logging.info("Step 4: Preparing components breakdown")
#         merged_components = {k: [] for k in ["persona","audience","tone","instruction","data","format"]}
#         merged_components["context"] = masked_text
#         merged_components["llm_guardrails"] = getattr(optimizer, "guardrails", [])
#         for intent in detected_intents:
#             template = optimizer.prompt_templates.get(intent, optimizer.prompt_templates.get("general", {}))
#             for key in ["persona","audience","tone","instruction","data","format"]:
#                 merged_components[key].append(template.get(key, ""))
#         logging.info("Components breakdown prepared")

#         logging.info("Step 5: Calling Gemini API")
#         llm_output = await call_gemini(selected_prompt_template)
#         logging.info(f"LLM Response: {llm_output[:100]}...")

#         logging.info("Step 6: Determining masking status")
#         mask_status = "Sensitive personal data masked. Public entities preserved." \
#                       if any(detected_entities.values()) else "No sensitive data detected. Input remains unchanged."

#         logging.info("Step 7: Building response")
#         return AnalyzeResponse(
#             original_text=input_data.text,
#             masked_text=masked_text,
#             detected_entities=detected_entities,
#             triggered_keywords=triggered_keywords,
#             private_contexts=private_contexts,
#             sensitivity_score=sensitivity_score,
#             sensitivity_level=sensitivity_level,
#             detected_intents=detected_intents,
#             intent_sources=intent_sources,
#             intent_breakdown=intent_breakdown,
#             selected_prompt_technique=selected_technique,
#             selected_prompt_template=selected_prompt_template,
#             optimized_prompt=optimized_prompt,
#             components_breakdown=merged_components,
#             llm_response=llm_output,
#             status=mask_status + " ✅"
#         )

#     except Exception as e:
#         logging.exception(f"Error processing text: {e}")
#         raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")

# import os
# import logging
# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from typing import List, Dict, Any
# from utils.ner_detector import mask_sensitive_data
# from utils.prompt_optimizer import PromptOptimizer
# import google.generativeai as genai
# import asyncio
# from groq import Groq  # ✅ Import Groq client

# # ---------------------- Logger ----------------------
# logging.basicConfig(level=logging.INFO, format="🧩 [%(levelname)s] → %(message)s")

# # ---------------------- Router ----------------------
# router = APIRouter()
# optimizer = PromptOptimizer(ml_model_path=None)

# # ---------------------- API Keys ----------------------
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# GROQ_API_KEY = "os.getenv("GROQ_API_KEY")"  # ✅ Use your Groq key directly
# if GEMINI_API_KEY:
#     genai.configure(api_key=GEMINI_API_KEY)
# else:
#     logging.warning("GEMINI_API_KEY not set. Gemini API calls may fail.")

# if not GROQ_API_KEY:
#     logging.warning("GROQ_API_KEY not set. Groq calls will fail.")

# groq_client = Groq(api_key=GROQ_API_KEY)

# # ---------------------- Request & Response Models ----------------------
# class TextInput(BaseModel):
#     text: str

# # class AnalyzeResponse(BaseModel):
# #     original_text: str
# #     masked_text: str
# #     detected_entities: Dict[str, List[str]]
# #     triggered_keywords: Dict[str, List[str]]
# #     private_contexts: List[str]
# #     sensitivity_score: float
# #     sensitivity_level: str
# #     detected_intents: List[str]
# #     intent_sources: Dict[str, Any]
# #     intent_breakdown: Dict[str, Any]
# #     selected_prompt_technique: str
# #     selected_prompt_template: str
# #     optimized_prompt: str
# #     components_breakdown: Dict[str, Any]
# #     llm_response: str
# #     status: str

# class AnalyzeResponse(BaseModel):
#     original_text: str
#     masked_text: str
#     detected_entities: Dict[str, List[str]]
#     triggered_keywords: Dict[str, List[str]]
#     private_contexts: List[str]
#     sensitivity_score: float
#     sensitivity_level: str
#     detected_intents: List[str]
#     intent_sources: Dict[str, Any]
#     intent_breakdown: Dict[str, Any]
#     selected_prompt_technique: str
#     prompt_template: str           # <- Groq-enhanced prompt
#     optimized_prompt: str          # <- Optimizer output
#     components_breakdown: Dict[str, Any]
#     llm_response: str
#     status: str


# # ---------------------- Prompt Templates ----------------------
# PROMPT_TEMPLATES = {
#     "Proposal": "...",
#     "Summarization": "...",
#     "Task Generation": "...",
#     "Educational": "...",
#     "Translation": "...",
#     "Analysis": "...",
#     "QA": "...",
#     "Code": "...",
#     "General": "General (General Instruction)\nPlease provide detailed information about:\n{context}"
# }

# # ---------------------- Groq Prompt Enhancer ----------------------
# async def enhance_prompt_llm(masked_text: str, technique: str) -> str:
#     logging.info("Step 3a: Starting Groq prompt enhancement")
#     try:
#         prompt = f"""
# You are a professional Prompt Engineer.
# Technique: {technique}
# Context: {masked_text}

# Generate a refined, well-structured prompt suitable for an LLM.
# """

#         loop = asyncio.get_event_loop()
#         response = await loop.run_in_executor(
#             None,
#             lambda: groq_client.chat.completions.create(
#                 model="groq/compound",  # ✅ Groq-supported model
#                 messages=[
#                     {"role": "system", "content": "You are an expert in prompt design."},
#                     {"role": "user", "content": prompt}
#                 ],
#                 temperature=0.7,
#                 max_tokens=500
#             )
#         )

#         enhanced = response.choices[0].message.content.strip()
#         logging.info("Groq enhancement successful")
#         return enhanced or PROMPT_TEMPLATES.get(technique, PROMPT_TEMPLATES["General"]).format(context=masked_text)
#     except Exception as e:
#         logging.error(f"Groq enhancement failed: {e}")
#         return PROMPT_TEMPLATES.get(technique, PROMPT_TEMPLATES["General"]).format(context=masked_text)

# # ---------------------- Gemini LLM ----------------------
# async def call_gemini(prompt: str) -> str:
#     logging.info("Step 5: Starting Gemini API call")
#     if not GEMINI_API_KEY:
#         logging.warning("GEMINI_API_KEY not set, skipping Gemini call")
#         return "Gemini API Key not set. Skipping LLM call."
#     try:
#         loop = asyncio.get_event_loop()
#         model = genai.GenerativeModel("gemini-2.5-flash")
#         response = await loop.run_in_executor(None, lambda: model.generate_content(prompt))
#         logging.info("Gemini response received")
#         return getattr(response, "text", "No response from Gemini.")
#     except Exception as e:
#         logging.error(f"Gemini API call failed: {e}")
#         return f"Gemini API Error: {str(e)}"

# # ---------------------- Endpoint ----------------------
# @router.post("/analyze", response_model=AnalyzeResponse)
# async def analyze_text(input_data: TextInput):
#     try:
#         logging.info("Step 1: Masking sensitive data")
#         result = mask_sensitive_data(input_data.text)
#         masked_text = result.get("masked_text", "")
#         detected_entities = {k: list(set(v)) for k, v in result.get("detected_entities", {}).items()}
#         triggered_keywords = result.get("triggered_keywords", {})
#         private_contexts = result.get("private_contexts", [])
#         sensitivity_score = result.get("sensitivity_score", 0)
#         sensitivity_level = result.get("sensitivity_level", "Low")
#         logging.info(f"Masked Text: {masked_text}")

#         logging.info("Step 2: Detecting intents")
#         detected_intents, intent_sources = optimizer.detect_intents(input_data.text)
#         logging.info(f"Detected Intents: {detected_intents}")

#         logging.info("Step 3: Optimizing prompt")
#         optimized_prompt, combined_technique, intent_breakdown = optimizer.optimize_prompt_multi(
#             masked_text, detected_intents
#         )
#         selected_technique = combined_technique or "General"
#         logging.info(f"Selected Prompt Technique: {selected_technique}")

#         logging.info("Step 3a: Enhancing prompt via Groq API")
#         selected_prompt_template = await enhance_prompt_llm(masked_text, selected_technique)
#         logging.info(f"Selected Prompt Template: {selected_prompt_template[:100]}...")

#         logging.info("Step 4: Preparing components breakdown")
#         merged_components = {k: [] for k in ["persona", "audience", "tone", "instruction", "data", "format"]}
#         merged_components["context"] = masked_text
#         merged_components["llm_guardrails"] = getattr(optimizer, "guardrails", [])
#         for intent in detected_intents:
#             template = optimizer.prompt_templates.get(intent, optimizer.prompt_templates.get("general", {}))
#             for key in ["persona", "audience", "tone", "instruction", "data", "format"]:
#                 merged_components[key].append(template.get(key, ""))
#         logging.info("Components breakdown prepared")

#         logging.info("Step 5: Calling Gemini API")
#         llm_output = await call_gemini(selected_prompt_template)
#         logging.info(f"LLM Response: {llm_output[:100]}...")

#         logging.info("Step 6: Determining masking status")
#         mask_status = "Sensitive personal data masked. Public entities preserved." \
#             if any(detected_entities.values()) else "No sensitive data detected. Input remains unchanged."

#         logging.info("Step 7: Building response")
#         # return AnalyzeResponse(
#         #     original_text=input_data.text,
#         #     masked_text=masked_text,
#         #     detected_entities=detected_entities,
#         #     triggered_keywords=triggered_keywords,
#         #     private_contexts=private_contexts,
#         #     sensitivity_score=sensitivity_score,
#         #     sensitivity_level=sensitivity_level,
#         #     detected_intents=detected_intents,
#         #     intent_sources=intent_sources,
#         #     intent_breakdown=intent_breakdown,
#         #     selected_prompt_technique=selected_technique,
#         #     selected_prompt_template=selected_prompt_template,
#         #     optimized_prompt=optimized_prompt,
#         #     components_breakdown=merged_components,
#         #     llm_response=llm_output,
#         #     status=mask_status + " ✅"
#         # )
#         # Return response
#         return AnalyzeResponse(
#             original_text=input_data.text,
#             masked_text=masked_text,
#             detected_entities=detected_entities,
#             triggered_keywords=triggered_keywords,
#             private_contexts=private_contexts,
#             sensitivity_score=sensitivity_score,
#             sensitivity_level=sensitivity_level,
#             detected_intents=detected_intents,
#             intent_sources=intent_sources,
#             intent_breakdown=intent_breakdown,
#             selected_prompt_technique=selected_technique,
#             prompt_template=selected_prompt_template,     # Groq output
#             optimized_prompt=optimized_prompt,         # Optimizer output
#             components_breakdown=merged_components,
#             llm_response=llm_output,
#             status=mask_status + " ✅"
#         )

#     except Exception as e:
#         logging.exception(f"Error processing text: {e}")
#         raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")

# import os
# import logging
# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from typing import List, Dict, Any
# from utils.ner_detector import mask_sensitive_data
# from utils.prompt_optimizer import PromptOptimizer
# import google.generativeai as genai
# import asyncio
# from groq import Groq

# logging.basicConfig(level=logging.INFO, format="🧩 [%(levelname)s] → %(message)s")

# router = APIRouter()
# optimizer = PromptOptimizer(ml_model_path=None)

# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# GROQ_API_KEY = os.getenv('GROQ')
# if GEMINI_API_KEY:
#     genai.configure(api_key=GEMINI_API_KEY)
# else:
#     logging.warning("GEMINI_API_KEY not set. Gemini API calls may fail.")

# groq_client = Groq(api_key=GROQ_API_KEY)

# class TextInput(BaseModel):
#     text: str

# class AnalyzeResponse(BaseModel):
#     original_text: str
#     masked_text: str
#     detected_entities: Dict[str, List[str]]
#     triggered_keywords: Dict[str, List[str]]
#     private_contexts: List[str]
#     sensitivity_score: float
#     sensitivity_level: str
#     detected_intents: List[str]
#     intent_sources: Dict[str, Any]
#     intent_breakdown: Dict[str, Any]
#     selected_prompt_technique: str
#     optimized_prompt: str          # Optimizer output
#     prompt_template: str           # Groq output
#     llm_response: str
#     status: str

# PROMPT_TEMPLATES = {
#     "General": "General Instruction:\nPlease provide detailed information about:\n{context}"
# }

# async def enhance_prompt_llm(masked_text: str, technique: str) -> str:
#     logging.info("Enhancing prompt via Groq")
#     try:
#         prompt = f"""
# You are a professional Prompt Engineer.
# Technique: {technique}
# Context: {masked_text}

# Generate a refined, well-structured prompt suitable for an LLM.
# """
#         loop = asyncio.get_event_loop()
#         response = await loop.run_in_executor(
#             None,
#             lambda: groq_client.chat.completions.create(
#                 model="groq/compound",
#                 messages=[
#                     {"role": "system", "content": "You are an expert in prompt design."},
#                     {"role": "user", "content": prompt}
#                 ],
#                 temperature=0.7,
#                 max_tokens=500
#             )
#         )
#         return response.choices[0].message.content.strip() or PROMPT_TEMPLATES.get(technique, PROMPT_TEMPLATES["General"]).format(context=masked_text)
#     except Exception as e:
#         logging.error(f"Groq enhancement failed: {e}")
#         return PROMPT_TEMPLATES.get(technique, PROMPT_TEMPLATES["General"]).format(context=masked_text)

# async def call_gemini(prompt: str) -> str:
#     logging.info("Calling Gemini API")
#     if not GEMINI_API_KEY:
#         return "Gemini API Key not set. Skipping LLM call."
#     try:
#         loop = asyncio.get_event_loop()
#         model = genai.GenerativeModel("gemini-2.5-flash")
#         response = await loop.run_in_executor(None, lambda: model.generate_content(prompt))
#         return getattr(response, "text", "No response from Gemini.")
#     except Exception as e:
#         logging.error(f"Gemini API call failed: {e}")
#         return f"Gemini API Error: {str(e)}"

# @router.post("/analyze", response_model=AnalyzeResponse)
# async def analyze_text(input_data: TextInput):
#     try:
#         # Step 1: Mask sensitive data
#         result = mask_sensitive_data(input_data.text)
#         masked_text = result.get("masked_text", "")
#         detected_entities = {k: list(set(v)) for k, v in result.get("detected_entities", {}).items()}
#         triggered_keywords = result.get("triggered_keywords", {})
#         private_contexts = result.get("private_contexts", [])
#         sensitivity_score = result.get("sensitivity_score", 0)
#         sensitivity_level = result.get("sensitivity_level", "Low")

#         # Step 2: Detect intents
#         detected_intents, intent_sources = optimizer.detect_intents(input_data.text)

#         # Step 3: Optimize prompt
#         optimized_prompt, combined_technique, intent_breakdown = optimizer.optimize_prompt_multi(masked_text, detected_intents)
#         selected_technique = combined_technique or "General"

#         # Step 4: Enhance via Groq
#         refined_prompt = await enhance_prompt_llm(optimized_prompt, selected_technique)

#         # Step 5: Call Gemini
#         llm_output = await call_gemini(refined_prompt)

#         # Step 6: Determine status
#         mask_status = "Sensitive personal data masked. Public entities preserved." if any(detected_entities.values()) else "No sensitive data detected. Input remains unchanged."

#         # Step 7: Return response
#         return AnalyzeResponse(
#             original_text=input_data.text,
#             masked_text=masked_text,
#             detected_entities=detected_entities,
#             triggered_keywords=triggered_keywords,
#             private_contexts=private_contexts,
#             sensitivity_score=sensitivity_score,
#             sensitivity_level=sensitivity_level,
#             detected_intents=detected_intents,
#             intent_sources=intent_sources,
#             intent_breakdown=intent_breakdown,
#             selected_prompt_technique=selected_technique,
#             optimized_prompt=optimized_prompt,
#             prompt_template=refined_prompt,
#             llm_response=llm_output,
#             status=mask_status + " ✅"
#         )

#     except Exception as e:
#         logging.exception(f"Error processing text: {e}")
#         raise HTTPException(status_code=500, detail=str(e))

# import os
# import logging
# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from typing import List, Dict, Any
# from utils.ner_detector import mask_sensitive_data
# from utils.prompt_optimizer import PromptOptimizer
# import google.generativeai as genai
# import asyncio
# from groq import Groq  # ✅ Import Groq client

# # ---------------------- Logger ----------------------
# logging.basicConfig(level=logging.INFO, format="🧩 [%(levelname)s] → %(message)s")

# # ---------------------- Router ----------------------
# router = APIRouter()
# optimizer = PromptOptimizer(ml_model_path=None)

# # ---------------------- API Keys ----------------------
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# GROQ_API_KEY = "os.getenv("GROQ_API_KEY")" 
# if GEMINI_API_KEY:
#     genai.configure(api_key=GEMINI_API_KEY)
# else:
#     logging.warning("GEMINI_API_KEY not set. Gemini API calls may fail.")

# if not GROQ_API_KEY:
#     logging.warning("GROQ_API_KEY not set. Groq calls will fail.")

# groq_client = Groq(api_key=GROQ_API_KEY)

# # ---------------------- Request & Response Models ----------------------
# class TextInput(BaseModel):
#     text: str

# class AnalyzeResponse(BaseModel):
#     original_text: str
#     masked_text: str
#     detected_entities: Dict[str, List[str]]
#     triggered_keywords: Dict[str, List[str]]
#     private_contexts: List[str]
#     sensitivity_score: float
#     sensitivity_level: str
#     detected_intents: List[str]
#     intent_sources: Dict[str, Any]
#     intent_breakdown: Dict[str, Any]
#     selected_prompt_technique: str
#     optimized_prompt: str          # Optimizer output
#     prompt_template: str           # Groq output
#     components_breakdown: Dict[str, Any]
#     llm_response: str
#     status: str

# # ---------------------- Prompt Templates ----------------------
# PROMPT_TEMPLATES = {
#     "General": "General Instruction:\nPlease provide detailed information about:\n{context}"
# }

# # ---------------------- Groq Prompt Enhancer ----------------------
# async def enhance_prompt_llm(masked_text: str, technique: str) -> str:
#     logging.info("Step 3a: Starting Groq prompt enhancement")
#     try:
#         prompt = f"""
# You are a professional Prompt Engineer.
# Technique: {technique}
# Context: {masked_text}

# Generate a refined, well-structured prompt suitable for an LLM.
# """
#         loop = asyncio.get_event_loop()
#         response = await loop.run_in_executor(
#             None,
#             lambda: groq_client.chat.completions.create(
#                 model="groq/compound",
#                 messages=[
#                     {"role": "system", "content": "You are an expert in prompt design."},
#                     {"role": "user", "content": prompt}
#                 ],
#                 temperature=0.7,
#                 max_tokens=500
#             )
#         )
#         enhanced = response.choices[0].message.content.strip()
#         logging.info("Groq enhancement successful")
#         return enhanced or PROMPT_TEMPLATES.get(technique, PROMPT_TEMPLATES["General"]).format(context=masked_text)
#     except Exception as e:
#         logging.error(f"Groq enhancement failed: {e}")
#         return PROMPT_TEMPLATES.get(technique, PROMPT_TEMPLATES["General"]).format(context=masked_text)

# # ---------------------- Gemini LLM ----------------------
# async def call_gemini(prompt: str) -> str:
#     logging.info("Step 5: Starting Gemini API call")
#     if not GEMINI_API_KEY:
#         logging.warning("GEMINI_API_KEY not set, skipping Gemini call")
#         return "Gemini API Key not set. Skipping LLM call."
#     try:
#         loop = asyncio.get_event_loop()
#         model = genai.GenerativeModel("gemini-2.5-flash")
#         response = await loop.run_in_executor(None, lambda: model.generate_content(prompt))
#         logging.info("Gemini response received")
#         return getattr(response, "text", "No response from Gemini.")
#     except Exception as e:
#         logging.error(f"Gemini API call failed: {e}")
#         return f"Gemini API Error: {str(e)}"

# # ---------------------- Endpoint ----------------------
# @router.post("/analyze", response_model=AnalyzeResponse)
# async def analyze_text(input_data: TextInput):
#     try:
#         logging.info("Step 1: Masking sensitive data")
#         result = mask_sensitive_data(input_data.text)
#         masked_text = result.get("masked_text", "")
#         detected_entities = {k: list(set(v)) for k, v in result.get("detected_entities", {}).items()}
#         triggered_keywords = result.get("triggered_keywords", {})
#         private_contexts = result.get("private_contexts", [])
#         sensitivity_score = result.get("sensitivity_score", 0)
#         sensitivity_level = result.get("sensitivity_level", "Low")
#         logging.info(f"Masked Text: {masked_text}")

#         logging.info("Step 2: Detecting intents")
#         detected_intents, intent_sources = optimizer.detect_intents(input_data.text)
#         logging.info(f"Detected Intents: {detected_intents}")

#         logging.info("Step 3: Optimizing prompt")
#         optimized_prompt, combined_technique, intent_breakdown = optimizer.optimize_prompt_multi(
#             masked_text, detected_intents
#         )
#         selected_technique = combined_technique or "General"
#         logging.info(f"Selected Prompt Technique: {selected_technique}")

#         logging.info("Step 3a: Enhancing prompt via Groq API")
#         selected_prompt_template = await enhance_prompt_llm(masked_text, selected_technique)
#         logging.info(f"Selected Prompt Template: {selected_prompt_template[:100]}...")

#         logging.info("Step 4: Preparing components breakdown")
#         merged_components = {k: [] for k in ["persona", "audience", "tone", "instruction", "data", "format"]}
#         merged_components["context"] = masked_text
#         merged_components["llm_guardrails"] = getattr(optimizer, "guardrails", [])
#         for intent in detected_intents:
#             template = optimizer.prompt_templates.get(intent, optimizer.prompt_templates.get("general", {}))
#             for key in ["persona", "audience", "tone", "instruction", "data", "format"]:
#                 merged_components[key].append(template.get(key, ""))
#         logging.info("Components breakdown prepared")

#         logging.info("Step 5: Calling Gemini API")
#         llm_output = await call_gemini(selected_prompt_template)
#         logging.info(f"LLM Response: {llm_output[:100]}...")

#         logging.info("Step 6: Determining masking status")
#         mask_status = "Sensitive personal data masked. Public entities preserved." \
#             if any(detected_entities.values()) else "No sensitive data detected. Input remains unchanged."

#         logging.info("Step 7: Building response")
#         return AnalyzeResponse(
#             original_text=input_data.text,
#             masked_text=masked_text,
#             detected_entities=detected_entities,
#             triggered_keywords=triggered_keywords,
#             private_contexts=private_contexts,
#             sensitivity_score=sensitivity_score,
#             sensitivity_level=sensitivity_level,
#             detected_intents=detected_intents,
#             intent_sources=intent_sources,
#             intent_breakdown=intent_breakdown,
#             selected_prompt_technique=selected_technique,
#             prompt_template=selected_prompt_template,
#             optimized_prompt=optimized_prompt,
#             components_breakdown=merged_components,
#             llm_response=llm_output,
#             status=mask_status + " ✅"
#         )

#     except Exception as e:
#         logging.exception(f"Error processing text: {e}")
#         raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")

# import os
# import logging
# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from typing import List, Dict, Any
# from utils.ner_detector import mask_sensitive_data
# from utils.prompt_optimizer import PromptOptimizer
# import google.generativeai as genai
# import asyncio
# from groq import Groq  # ✅ Import Groq client

# # ---------------------- Logger ----------------------
# logging.basicConfig(level=logging.INFO, format="🧩 [%(levelname)s] → %(message)s")

# # ---------------------- Router ----------------------
# router = APIRouter()
# optimizer = PromptOptimizer(ml_model_path=None)

# # ---------------------- API Keys ----------------------
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# GROQ_API_KEY = "os.getenv("GROQ_API_KEY")"

# if GEMINI_API_KEY:
#     genai.configure(api_key=GEMINI_API_KEY)
# else:
#     logging.warning("GEMINI_API_KEY not set. Gemini API calls may fail.")

# if not GROQ_API_KEY:
#     logging.warning("GROQ_API_KEY not set. Groq calls will fail.")

# groq_client = Groq(api_key=GROQ_API_KEY)

# # ---------------------- Request & Response Models ----------------------
# class TextInput(BaseModel):
#     text: str

# class AnalyzeResponse(BaseModel):
#     original_text: str
#     masked_text: str
#     detected_entities: Dict[str, List[str]]
#     triggered_keywords: Dict[str, List[str]]
#     private_contexts: List[str]
#     sensitivity_score: float
#     sensitivity_level: str
#     detected_intents: List[str]
#     intent_sources: Dict[str, Any]
#     intent_breakdown: Dict[str, Any]
#     selected_prompt_technique: str
#     optimized_prompt: str
#     prompt_template: str          # final prompt only
#     prompt_reasoning: str         # reasoning for frontend toggle
#     components_breakdown: Dict[str, Any]
#     llm_response: str
#     status: str

# # ---------------------- Prompt Templates ----------------------
# PROMPT_TEMPLATES = {
#     "General": "General Instruction:\nPlease provide detailed information about:\n{context}"
# }

# # ---------------------- Groq Prompt Enhancer ----------------------
# async def enhance_prompt_llm(masked_text: str, technique: str) -> Dict[str, str]:
#     """
#     Returns a dict with 'final_prompt' (sent to LLM) and 'reasoning' (toggle display).
#     """
#     logging.info("Step 3a: Starting Groq prompt enhancement")
#     try:
#         prompt = f"""
# You are a professional Prompt Engineer.
# Technique: {technique}
# Context: {masked_text}

# Generate a refined, well-structured prompt suitable for an LLM.
# Include a reasoning section describing your design choices.
# """
#         loop = asyncio.get_event_loop()
#         response = await loop.run_in_executor(
#             None,
#             lambda: groq_client.chat.completions.create(
#                 model="groq/compound",
#                 messages=[
#                     {"role": "system", "content": "You are an expert in prompt design."},
#                     {"role": "user", "content": prompt}
#                 ],
#                 temperature=0.7,
#                 max_tokens=500
#             )
#         )
#         enhanced_text = response.choices[0].message.content.strip()
#         logging.info("Groq enhancement successful")

#         # Split final prompt and reasoning
#         if "**Refined, well‑structured prompt**" in enhanced_text:
#             parts = enhanced_text.split("**Refined, well‑structured prompt**")
#             reasoning = parts[0].strip() if parts[0] else "No reasoning provided."
#             final_prompt = parts[1].strip() if len(parts) > 1 else enhanced_text
#         else:
#             final_prompt = enhanced_text
#             reasoning = "No reasoning section detected."

#         return {"final_prompt": final_prompt, "reasoning": reasoning}
#     except Exception as e:
#         logging.error(f"Groq enhancement failed: {e}")
#         fallback_prompt = PROMPT_TEMPLATES.get(technique, PROMPT_TEMPLATES["General"]).format(context=masked_text)
#         return {"final_prompt": fallback_prompt, "reasoning": "Fallback used due to error."}

# # ---------------------- Gemini LLM ----------------------
# async def call_gemini(prompt: str) -> str:
#     logging.info("Step 5: Starting Gemini API call")
#     if not GEMINI_API_KEY:
#         logging.warning("GEMINI_API_KEY not set, skipping Gemini call")
#         return "Gemini API Key not set. Skipping LLM call."
#     try:
#         loop = asyncio.get_event_loop()
#         model = genai.GenerativeModel("gemini-2.5-flash")
#         response = await loop.run_in_executor(None, lambda: model.generate_content(prompt))
#         logging.info("Gemini response received")
#         return getattr(response, "text", "No response from Gemini.")
#     except Exception as e:
#         logging.error(f"Gemini API call failed: {e}")
#         return f"Gemini API Error: {str(e)}"

# # ---------------------- Endpoint ----------------------
# @router.post("/analyze", response_model=AnalyzeResponse)
# async def analyze_text(input_data: TextInput):
#     try:
#         logging.info("Step 1: Masking sensitive data")
#         result = mask_sensitive_data(input_data.text)
#         masked_text = result.get("masked_text", "")
#         detected_entities = {k: list(set(v)) for k, v in result.get("detected_entities", {}).items()}
#         triggered_keywords = result.get("triggered_keywords", {})
#         private_contexts = result.get("private_contexts", [])
#         sensitivity_score = result.get("sensitivity_score", 0)
#         sensitivity_level = result.get("sensitivity_level", "Low")
#         logging.info(f"Masked Text: {masked_text}")

#         logging.info("Step 2: Detecting intents")
#         detected_intents, intent_sources = optimizer.detect_intents(input_data.text)
#         logging.info(f"Detected Intents: {detected_intents}")

#         logging.info("Step 3: Optimizing prompt")
#         optimized_prompt, combined_technique, intent_breakdown = optimizer.optimize_prompt_multi(
#             masked_text, detected_intents
#         )
#         selected_technique = combined_technique or "General"
#         logging.info(f"Selected Prompt Technique: {selected_technique}")

#         logging.info("Step 3a: Enhancing prompt via Groq API")
#         groq_result = await enhance_prompt_llm(masked_text, selected_technique)
#         refined_prompt = groq_result["final_prompt"]
#         prompt_reasoning = groq_result["reasoning"]
#         logging.info(f"Refined Prompt: {refined_prompt[:100]}...")
#         logging.info(f"Prompt Reasoning (truncated): {prompt_reasoning[:100]}...")

#         logging.info("Step 4: Preparing components breakdown")
#         merged_components = {k: [] for k in ["persona", "audience", "tone", "instruction", "data", "format"]}
#         merged_components["context"] = masked_text
#         merged_components["llm_guardrails"] = getattr(optimizer, "guardrails", [])
#         for intent in detected_intents:
#             template = optimizer.prompt_templates.get(intent, optimizer.prompt_templates.get("general", {}))
#             for key in ["persona", "audience", "tone", "instruction", "data", "format"]:
#                 merged_components[key].append(template.get(key, ""))
#         logging.info("Components breakdown prepared")

#         logging.info("Step 5: Calling Gemini API")
#         llm_output = await call_gemini(refined_prompt)
#         logging.info(f"LLM Response: {llm_output[:100]}...")

#         logging.info("Step 6: Determining masking status")
#         mask_status = "Sensitive personal data masked. Public entities preserved." \
#             if any(detected_entities.values()) else "No sensitive data detected. Input remains unchanged."

#         logging.info("Step 7: Building response")
#         return AnalyzeResponse(
#             original_text=input_data.text,
#             masked_text=masked_text,
#             detected_entities=detected_entities,
#             triggered_keywords=triggered_keywords,
#             private_contexts=private_contexts,
#             sensitivity_score=sensitivity_score,
#             sensitivity_level=sensitivity_level,
#             detected_intents=detected_intents,
#             intent_sources=intent_sources,
#             intent_breakdown=intent_breakdown,
#             selected_prompt_technique=selected_technique,
#             optimized_prompt=optimized_prompt,
#             prompt_template=refined_prompt,      # final prompt only
#             prompt_reasoning=prompt_reasoning,   # reasoning for frontend toggle
#             components_breakdown=merged_components,
#             llm_response=llm_output,
#             status=mask_status + " ✅"
#         )

#     except Exception as e:
#         logging.exception(f"Error processing text: {e}")
#         raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")

# import os
# import logging
# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from typing import List, Dict, Any
# from utils.ner_detector import mask_sensitive_data
# from utils.prompt_optimizer import PromptOptimizer
# import google.generativeai as genai
# import asyncio
# from groq import Groq  # ✅ Groq client

# # ---------------------- Logger ----------------------
# logging.basicConfig(level=logging.INFO, format="🧩 [%(levelname)s] → %(message)s")

# # ---------------------- Router ----------------------
# router = APIRouter()
# optimizer = PromptOptimizer(ml_model_path=None)

# # ---------------------- API Keys ----------------------
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# GROQ_API_KEY = "os.getenv("GROQ_API_KEY")"

# if GEMINI_API_KEY:
#     genai.configure(api_key=GEMINI_API_KEY)
# else:
#     logging.warning("GEMINI_API_KEY not set. Gemini API calls may fail.")

# if not GROQ_API_KEY:
#     logging.warning("GROQ_API_KEY not set. Groq calls will fail.")

# groq_client = Groq(api_key=GROQ_API_KEY)

# # ---------------------- Request & Response Models ----------------------
# class TextInput(BaseModel):
#     text: str

# class AnalyzeResponse(BaseModel):
#     original_text: str
#     masked_text: str
#     detected_entities: Dict[str, List[str]]
#     triggered_keywords: Dict[str, List[str]]
#     private_contexts: List[str]
#     sensitivity_score: float
#     sensitivity_level: str
#     detected_intents: List[str]
#     intent_sources: Dict[str, Any]
#     intent_breakdown: Dict[str, Any]
#     selected_prompt_technique: str
#     optimized_prompt: str
#     prompt_template: str          # final prompt only
#     prompt_reasoning: str         # reasoning for frontend toggle
#     components_breakdown: Dict[str, Any]
#     llm_response: str
#     status: str

# # ---------------------- Prompt Templates ----------------------
# PROMPT_TEMPLATES = {
#     "General": "General Instruction:\nPlease provide detailed information about:\n{context}"
# }

# # ---------------------- Groq Prompt Enhancer ----------------------
# async def enhance_prompt_llm(masked_text: str, technique: str) -> Dict[str, str]:
#     """
#     Returns a dict with:
#       - 'final_prompt' (sent to Gemini)
#       - 'reasoning' (toggle display)
#     """
#     logging.info("Step 3a: Starting Groq prompt enhancement")
#     try:
#         prompt = f"""
# You are a professional Prompt Engineer.
# Technique: {technique}
# Context: {masked_text}

# Generate a refined, well-structured prompt suitable for an LLM.
# Include a reasoning section describing your design choices.
# """
#         loop = asyncio.get_event_loop()
#         response = await loop.run_in_executor(
#             None,
#             lambda: groq_client.chat.completions.create(
#                 model="groq/compound",
#                 messages=[
#                     {"role": "system", "content": "You are an expert in prompt design."},
#                     {"role": "user", "content": prompt}
#                 ],
#                 temperature=0.7,
#                 max_tokens=700
#             )
#         )
#         full_content = response.choices[0].message.content.strip()

#         # Split into final prompt and reasoning
#         if "**Refined Prompt**" in full_content and "### Reasoning" in full_content:
#             final_prompt = full_content.split("### Reasoning")[0].replace("**Refined Prompt**", "").strip()
#             reasoning = full_content.split("### Reasoning")[1].strip()
#         else:
#             final_prompt = full_content
#             reasoning = "No reasoning section detected."

#         logging.info("Groq enhancement successful")
#         return {"final_prompt": final_prompt, "reasoning": reasoning}

#     except Exception as e:
#         logging.error(f"Groq enhancement failed: {e}")
#         fallback_prompt = PROMPT_TEMPLATES.get(technique, PROMPT_TEMPLATES["General"]).format(context=masked_text)
#         return {"final_prompt": fallback_prompt, "reasoning": "Fallback used due to error."}

# # ---------------------- Gemini LLM ----------------------
# async def call_gemini(prompt: str) -> str:
#     logging.info("Step 5: Starting Gemini API call")
#     if not GEMINI_API_KEY:
#         logging.warning("GEMINI_API_KEY not set, skipping Gemini call")
#         return "Gemini API Key not set. Skipping LLM call."
#     try:
#         loop = asyncio.get_event_loop()
#         model = genai.GenerativeModel("gemini-2.5-flash")
#         response = await loop.run_in_executor(None, lambda: model.generate_content(prompt))
#         logging.info("Gemini response received")
#         return getattr(response, "text", "No response from Gemini.")
#     except Exception as e:
#         logging.error(f"Gemini API call failed: {e}")
#         return f"Gemini API Error: {str(e)}"

# # ---------------------- Endpoint ----------------------
# @router.post("/analyze", response_model=AnalyzeResponse)
# async def analyze_text(input_data: TextInput):
#     try:
#         logging.info("Step 1: Masking sensitive data")
#         result = mask_sensitive_data(input_data.text)
#         masked_text = result.get("masked_text", "")
#         detected_entities = {k: list(set(v)) for k, v in result.get("detected_entities", {}).items()}
#         triggered_keywords = result.get("triggered_keywords", {})
#         private_contexts = result.get("private_contexts", [])
#         sensitivity_score = result.get("sensitivity_score", 0)
#         sensitivity_level = result.get("sensitivity_level", "Low")
#         logging.info(f"Masked Text: {masked_text}")

#         logging.info("Step 2: Detecting intents")
#         detected_intents, intent_sources = optimizer.detect_intents(input_data.text)
#         logging.info(f"Detected Intents: {detected_intents}")

#         logging.info("Step 3: Optimizing prompt")
#         optimized_prompt, combined_technique, intent_breakdown = optimizer.optimize_prompt_multi(
#             masked_text, detected_intents
#         )
#         selected_technique = combined_technique or "General"
#         logging.info(f"Selected Prompt Technique: {selected_technique}")

#         logging.info("Step 3a: Enhancing prompt via Groq API")
#         groq_result = await enhance_prompt_llm(masked_text, selected_technique)
#         refined_prompt = groq_result["final_prompt"]
#         prompt_reasoning = groq_result["reasoning"]
#         logging.info(f"Refined Prompt: {refined_prompt[:100]}...")
#         logging.info(f"Prompt Reasoning (truncated): {prompt_reasoning[:100]}...")

#         logging.info("Step 4: Preparing components breakdown")
#         merged_components = {k: [] for k in ["persona", "audience", "tone", "instruction", "data", "format"]}
#         merged_components["context"] = masked_text
#         merged_components["llm_guardrails"] = getattr(optimizer, "guardrails", [])
#         for intent in detected_intents:
#             template = optimizer.prompt_templates.get(intent, optimizer.prompt_templates.get("general", {}))
#             for key in ["persona", "audience", "tone", "instruction", "data", "format"]:
#                 merged_components[key].append(template.get(key, ""))

#         logging.info("Step 5: Calling Gemini API")
#         llm_output = await call_gemini(refined_prompt)
#         logging.info(f"LLM Response: {llm_output[:100]}...")

#         logging.info("Step 6: Determining masking status")
#         mask_status = "Sensitive personal data masked. Public entities preserved." \
#             if any(detected_entities.values()) else "No sensitive data detected. Input remains unchanged."

#         logging.info("Step 7: Building response")
#         return AnalyzeResponse(
#             original_text=input_data.text,
#             masked_text=masked_text,
#             detected_entities=detected_entities,
#             triggered_keywords=triggered_keywords,
#             private_contexts=private_contexts,
#             sensitivity_score=sensitivity_score,
#             sensitivity_level=sensitivity_level,
#             detected_intents=detected_intents,
#             intent_sources=intent_sources,
#             intent_breakdown=intent_breakdown,
#             selected_prompt_technique=selected_technique,
#             optimized_prompt=optimized_prompt,
#             prompt_template=refined_prompt,      # final prompt only
#             prompt_reasoning=prompt_reasoning,   # reasoning for frontend toggle
#             components_breakdown=merged_components,
#             llm_response=llm_output,
#             status=mask_status + " ✅"
#         )

#     except Exception as e:
#         logging.exception(f"Error processing text: {e}")
#         raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")

# import os
# import logging
# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from typing import List, Dict, Any
# from utils.ner_detector import mask_sensitive_data
# from utils.prompt_optimizer import PromptOptimizer
# import google.generativeai as genai
# import asyncio
# from groq import Groq  # ✅ Groq client

# # ---------------------- Logger ----------------------
# logging.basicConfig(level=logging.INFO, format="🧩 [%(levelname)s] → %(message)s")

# # ---------------------- Router ----------------------
# router = APIRouter()
# optimizer = PromptOptimizer(ml_model_path=None)

# # ---------------------- API Keys ----------------------
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# GROQ_API_KEY = "os.getenv("GROQ_API_KEY")"

# if GEMINI_API_KEY:
#     genai.configure(api_key=GEMINI_API_KEY)
# else:
#     logging.warning("GEMINI_API_KEY not set. Gemini API calls may fail.")

# if not GROQ_API_KEY:
#     logging.warning("GROQ_API_KEY not set. Groq calls will fail.")

# groq_client = Groq(api_key=GROQ_API_KEY)

# # ---------------------- Request & Response Models ----------------------
# class TextInput(BaseModel):
#     text: str

# class AnalyzeResponse(BaseModel):
#     original_text: str
#     masked_text: str
#     detected_entities: Dict[str, List[str]]
#     triggered_keywords: Dict[str, List[str]]
#     private_contexts: List[str]
#     sensitivity_score: float
#     sensitivity_level: str
#     detected_intents: List[str]
#     intent_sources: Dict[str, Any]
#     intent_breakdown: Dict[str, Any]
#     selected_prompt_technique: str
#     optimized_prompt: str
#     prompt_template: str          # final prompt only
#     prompt_reasoning: str         # empty string now
#     components_breakdown: Dict[str, Any]
#     llm_response: str
#     status: str

# # ---------------------- Prompt Templates ----------------------
# PROMPT_TEMPLATES = {
#     "General": "General Instruction:\nPlease provide detailed information about:\n{context}"
# }

# # ---------------------- Groq Prompt Enhancer ----------------------
# async def enhance_prompt_llm(masked_text: str, technique: str) -> Dict[str, str]:
#     """
#     Uses Groq to refine the prompt ONLY — not generate the final answer.
#     Returns:
#       - 'final_prompt': The optimized prompt ready for Gemini
#       - 'reasoning': (kept empty)
#     """
#     logging.info("Step 3a: Starting Groq prompt enhancement")
#     try:
#         # Explicit instruction that Groq should only refine, not generate output
#         prompt = f"""
# You are a Prompt Optimization System (POS).
# Your only role is to refine and structure the user's input into a professional, well-formed instruction
# that can be sent to another LLM (such as Gemini) for final generation.

# DO NOT generate or simulate the final answer yourself.

# Technique(s) to apply: {technique}

# Input (masked user request):
# {masked_text}

# Your task:
# 1. Apply the specified prompting technique(s) — Role-based, Few-shot, Step-by-step, or others as mentioned.
# 2. Produce a single, final refined prompt ready for Gemini or another LLM to execute.
# 3. End your response with the refined prompt text only — do not include analysis, reasoning, examples, or the actual proposal.
# 4. Make sure the refined prompt includes:
#    - Clear role setup
#    - Structured step-by-step task instructions
#    - Any placeholders (e.g., [MASKED_COMPANY]) preserved
#    - A clear “Now generate...” instruction at the end for Gemini to act upon
# """

#         loop = asyncio.get_event_loop()
#         response = await loop.run_in_executor(
#             None,
#             lambda: groq_client.chat.completions.create(
#                 model="groq/compound",
#                 messages=[
#                     {"role": "system", "content": "You are a world-class Prompt Engineer that refines prompts for downstream LLMs. You NEVER generate the final answer."},
#                     {"role": "user", "content": prompt}
#                 ],
#                 temperature=0.3,
#                 max_tokens=700
#             )
#         )

#         final_prompt = response.choices[0].message.content.strip()
#         logging.info("Groq enhancement successful")
#         return {"final_prompt": final_prompt, "reasoning": ""}

#     except Exception as e:
#         logging.error(f"Groq enhancement failed: {e}")
#         fallback_prompt = PROMPT_TEMPLATES.get(technique, PROMPT_TEMPLATES["General"]).format(context=masked_text)
#         return {"final_prompt": fallback_prompt, "reasoning": ""}

# # ---------------------- Gemini LLM ----------------------
# async def call_gemini(prompt: str) -> str:
#     logging.info("Step 5: Starting Gemini API call")
#     if not GEMINI_API_KEY:
#         logging.warning("GEMINI_API_KEY not set, skipping Gemini call")
#         return "Gemini API Key not set. Skipping LLM call."
#     try:
#         loop = asyncio.get_event_loop()
#         model = genai.GenerativeModel("gemini-2.5-flash")
#         response = await loop.run_in_executor(None, lambda: model.generate_content(prompt))
#         logging.info("Gemini response received")
#         return getattr(response, "text", "No response from Gemini.")
#     except Exception as e:
#         logging.error(f"Gemini API call failed: {e}")
#         return f"Gemini API Error: {str(e)}"

# # ---------------------- Endpoint ----------------------
# @router.post("/analyze", response_model=AnalyzeResponse)
# async def analyze_text(input_data: TextInput):
#     try:
#         logging.info("Step 1: Masking sensitive data")
#         result = mask_sensitive_data(input_data.text)
#         masked_text = result.get("masked_text", "")
#         detected_entities = {k: list(set(v)) for k, v in result.get("detected_entities", {}).items()}
#         triggered_keywords = result.get("triggered_keywords", {})
#         private_contexts = result.get("private_contexts", [])
#         sensitivity_score = result.get("sensitivity_score", 0)
#         sensitivity_level = result.get("sensitivity_level", "Low")
#         logging.info(f"Masked Text: {masked_text}")

#         logging.info("Step 2: Detecting intents")
#         detected_intents, intent_sources = optimizer.detect_intents(input_data.text)
#         logging.info(f"Detected Intents: {detected_intents}")

#         logging.info("Step 3: Optimizing prompt")
#         optimized_prompt, combined_technique, intent_breakdown = optimizer.optimize_prompt_multi(
#             masked_text, detected_intents
#         )
#         selected_technique = combined_technique or "General"
#         logging.info(f"Selected Prompt Technique: {selected_technique}")

#         logging.info("Step 3a: Enhancing prompt via Groq API")
#         groq_result = await enhance_prompt_llm(masked_text, selected_technique)
#         refined_prompt = groq_result["final_prompt"]
#         prompt_reasoning = groq_result["reasoning"]
#         logging.info(f"Refined Prompt: {refined_prompt[:100]}...")

#         logging.info("Step 4: Preparing components breakdown")
#         merged_components = {k: [] for k in ["persona", "audience", "tone", "instruction", "data", "format"]}
#         merged_components["context"] = masked_text
#         merged_components["llm_guardrails"] = getattr(optimizer, "guardrails", [])
#         for intent in detected_intents:
#             template = optimizer.prompt_templates.get(intent, optimizer.prompt_templates.get("general", {}))
#             for key in ["persona", "audience", "tone", "instruction", "data", "format"]:
#                 merged_components[key].append(template.get(key, ""))

#         logging.info("Step 5: Calling Gemini API")
#         llm_output = await call_gemini(refined_prompt)
#         logging.info(f"LLM Response: {llm_output[:100]}...")

#         logging.info("Step 6: Determining masking status")
#         mask_status = "Sensitive personal data masked. Public entities preserved." \
#             if any(detected_entities.values()) else "No sensitive data detected. Input remains unchanged."

#         logging.info("Step 7: Building response")
#         return AnalyzeResponse(
#             original_text=input_data.text,
#             masked_text=masked_text,
#             detected_entities=detected_entities,
#             triggered_keywords=triggered_keywords,
#             private_contexts=private_contexts,
#             sensitivity_score=sensitivity_score,
#             sensitivity_level=sensitivity_level,
#             detected_intents=detected_intents,
#             intent_sources=intent_sources,
#             intent_breakdown=intent_breakdown,
#             selected_prompt_technique=selected_technique,
#             optimized_prompt=optimized_prompt,
#             prompt_template=refined_prompt,      # final prompt only
#             prompt_reasoning=prompt_reasoning,   # now empty string
#             components_breakdown=merged_components,
#             llm_response=llm_output,
#             status=mask_status + " ✅"
#         )

#     except Exception as e:
#         logging.exception(f"Error processing text: {e}")
#         raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")

# import os
# import logging
# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from typing import List, Dict, Any
# from utils.ner_detector import mask_sensitive_data
# from utils.prompt_optimizer import PromptOptimizer
# import google.generativeai as genai
# import asyncio
# from groq import Groq  # ✅ Groq client

# # ---------------------- Logger ----------------------
# logging.basicConfig(level=logging.INFO, format="🧩 [%(levelname)s] → %(message)s")

# # ---------------------- Router ----------------------
# router = APIRouter()
# optimizer = PromptOptimizer(ml_model_path=None)

# # ---------------------- API Keys ----------------------
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# GROQ_API_KEY = "os.getenv("GROQ_API_KEY")"

# if GEMINI_API_KEY:
#     genai.configure(api_key=GEMINI_API_KEY)
# else:
#     logging.warning("GEMINI_API_KEY not set. Gemini API calls may fail.")

# if not GROQ_API_KEY:
#     logging.warning("GROQ_API_KEY not set. Groq calls will fail.")

# groq_client = Groq(api_key=GROQ_API_KEY)

# # ---------------------- Request & Response Models ----------------------
# class TextInput(BaseModel):
#     text: str

# class AnalyzeResponse(BaseModel):
#     original_text: str
#     masked_text: str
#     detected_entities: Dict[str, List[str]]
#     triggered_keywords: Dict[str, List[str]]
#     private_contexts: List[str]
#     sensitivity_score: float
#     sensitivity_level: str
#     detected_intents: List[str]
#     intent_sources: Dict[str, Any]
#     intent_breakdown: Dict[str, Any]
#     selected_prompt_technique: str
#     optimized_prompt: str
#     prompt_template: str          # final prompt only (reasoning removed)
#     components_breakdown: Dict[str, Any]
#     llm_response: str
#     status: str

# # ---------------------- Prompt Templates ----------------------
# PROMPT_TEMPLATES = {
#     "General": "General Instruction:\nPlease provide detailed information about:\n{context}"
# }

# # ---------------------- Groq Prompt Enhancer ----------------------
# async def enhance_prompt_llm(masked_text: str, technique: str) -> str:
#     """
#     Uses Groq to refine the prompt ONLY — not generate the final answer.
#     Returns only the refined prompt string.
#     """
#     logging.info("Step 3a: Starting Groq prompt enhancement")
#     try:
#         prompt = f"""
# You are a Prompt Optimization System (POS).
# Your only role is to refine and structure the user's input into a professional, well-formed instruction
# that can be sent to another LLM (such as Gemini) for final generation.

# DO NOT generate or simulate the final answer yourself.

# Technique(s) to apply: {technique}

# Input (masked user request):
# {masked_text}

# Your task:
# 1. Apply the specified prompting technique(s).
# 2. Produce a single, final refined prompt ready for Gemini or another LLM to execute.
# 3. End your response with only the refined prompt text.
# """

#         loop = asyncio.get_event_loop()
#         response = await loop.run_in_executor(
#             None,
#             lambda: groq_client.chat.completions.create(
#                 model="groq/compound",
#                 messages=[
#                     {"role": "system", "content": "You are a world-class Prompt Engineer that refines prompts for downstream LLMs. You NEVER generate the final answer."},
#                     {"role": "user", "content": prompt}
#                 ],
#                 temperature=0.3,
#                 max_tokens=700
#             )
#         )

#         final_prompt = response.choices[0].message.content.strip()
#         logging.info("Groq enhancement successful")
#         return final_prompt

#     except Exception as e:
#         logging.error(f"Groq enhancement failed: {e}")
#         fallback_prompt = PROMPT_TEMPLATES.get(technique, PROMPT_TEMPLATES["General"]).format(context=masked_text)
#         return fallback_prompt

# # ---------------------- Gemini LLM ----------------------
# async def call_gemini(prompt: str) -> str:
#     logging.info("Step 5: Starting Gemini API call")
#     if not GEMINI_API_KEY:
#         logging.warning("GEMINI_API_KEY not set, skipping Gemini call")
#         return "Gemini API Key not set. Skipping LLM call."
#     try:
#         loop = asyncio.get_event_loop()
#         model = genai.GenerativeModel("gemini-2.5-flash")
#         response = await loop.run_in_executor(None, lambda: model.generate_content(prompt))
#         logging.info("Gemini response received")
#         return getattr(response, "text", "No response from Gemini.")
#     except Exception as e:
#         logging.error(f"Gemini API call failed: {e}")
#         return f"Gemini API Error: {str(e)}"

# # ---------------------- Endpoint ----------------------
# @router.post("/analyze", response_model=AnalyzeResponse)
# async def analyze_text(input_data: TextInput):
#     try:
#         logging.info("Step 1: Masking sensitive data")
#         result = mask_sensitive_data(input_data.text)
#         masked_text = result.get("masked_text", "")
#         detected_entities = {k: list(set(v)) for k, v in result.get("detected_entities", {}).items()}
#         triggered_keywords = result.get("triggered_keywords", {})
#         private_contexts = result.get("private_contexts", [])
#         sensitivity_score = result.get("sensitivity_score", 0)
#         sensitivity_level = result.get("sensitivity_level", "Low")

#         logging.info("Step 2: Detecting intents")
#         detected_intents, intent_sources = optimizer.detect_intents(input_data.text)
#         optimized_prompt, combined_technique, intent_breakdown = optimizer.optimize_prompt_multi(
#             masked_text, detected_intents
#         )
#         selected_technique = combined_technique or "General"

#         logging.info("Step 3a: Enhancing prompt via Groq API")
#         refined_prompt = await enhance_prompt_llm(masked_text, selected_technique)

#         logging.info("Step 4: Preparing components breakdown")
#         merged_components = {k: [] for k in ["persona", "audience", "tone", "instruction", "data", "format"]}
#         merged_components["context"] = masked_text
#         merged_components["llm_guardrails"] = getattr(optimizer, "guardrails", [])

#         for intent in detected_intents:
#             template = optimizer.prompt_templates.get(intent, optimizer.prompt_templates.get("general", {}))
#             for key in ["persona", "audience", "tone", "instruction", "data", "format"]:
#                 merged_components[key].append(template.get(key, ""))

#         logging.info("Step 5: Calling Gemini API")
#         llm_output = await call_gemini(refined_prompt)

#         mask_status = (
#             "Sensitive personal data masked. Public entities preserved."
#             if any(detected_entities.values())
#             else "No sensitive data detected. Input remains unchanged."
#         )

#         return AnalyzeResponse(
#             original_text=input_data.text,
#             masked_text=masked_text,
#             detected_entities=detected_entities,
#             triggered_keywords=triggered_keywords,
#             private_contexts=private_contexts,
#             sensitivity_score=sensitivity_score,
#             sensitivity_level=sensitivity_level,
#             detected_intents=detected_intents,
#             intent_sources=intent_sources,
#             intent_breakdown=intent_breakdown,
#             selected_prompt_technique=selected_technique,
#             optimized_prompt=optimized_prompt,
#             prompt_template=refined_prompt,
#             components_breakdown=merged_components,
#             llm_response=llm_output,
#             status=mask_status + " ✅",
#         )

#     except Exception as e:
#         logging.exception(f"Error processing text: {e}")
#         raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")

import os
import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from utils.ner_detector import mask_sensitive_data
from utils.prompt_optimizer import PromptOptimizer
import google.generativeai as genai
import asyncio
from groq import Groq  # ✅ Groq client

# ---------------------- Logger ----------------------
logging.basicConfig(level=logging.INFO, format="🧩 [%(levelname)s] → %(message)s")

# ---------------------- Router ----------------------
router = APIRouter()
optimizer = PromptOptimizer(ml_model_path=None)

# ---------------------- API Keys ----------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    logging.warning("GEMINI_API_KEY not set. Gemini API calls may fail.")

if not GROQ_API_KEY:
    logging.warning("GROQ_API_KEY not set. Groq calls will fail.")

groq_client = Groq(api_key=GROQ_API_KEY)

# ---------------------- Request & Response Models ----------------------
class TextInput(BaseModel):
    text: str

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
    prompt_template: str          # final refined prompt (Groq output)
    components_breakdown: Dict[str, Any]
    llm_response: str
    status: str

# ---------------------- Prompt Templates ----------------------
PROMPT_TEMPLATES = {
    "General": "General Instruction:\nPlease provide detailed information about:\n{context}"
}

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

# ---------------------- Gemini LLM ----------------------
async def call_gemini(prompt: str) -> str:
    logging.info("Step 5: Starting Gemini API call")
    if not GEMINI_API_KEY:
        logging.warning("GEMINI_API_KEY not set, skipping Gemini call")
        return "Gemini API Key not set. Skipping LLM call."
    try:
        loop = asyncio.get_event_loop()
        model = genai.GenerativeModel("gemini-2.5-flash")
        # Use generate_content with a prompt string (Gemini client may vary - adapt if needed)
        response = await loop.run_in_executor(None, lambda: model.generate_content(prompt))
        logging.info("Gemini response received")
        return getattr(response, "text", "No response from Gemini.")
    except Exception as e:
        logging.error(f"Gemini API call failed: {e}")
        return f"Gemini API Error: {str(e)}"

# ---------------------- Endpoint ----------------------
@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_text(input_data: TextInput):
    try:
        logging.info("Step 1: Masking sensitive data")
        result = mask_sensitive_data(input_data.text)
        masked_text = result.get("masked_text", "")
        detected_entities = {k: list(set(v)) for k, v in result.get("detected_entities", {}).items()}
        triggered_keywords = result.get("triggered_keywords", {})
        private_contexts = result.get("private_contexts", [])
        sensitivity_score = result.get("sensitivity_score", 0)
        sensitivity_level = result.get("sensitivity_level", "Low")
        logging.info(f"Masked Text: {masked_text}")

        logging.info("Step 2: Detecting intents")
        detected_intents, intent_sources = optimizer.detect_intents(input_data.text)
        logging.info(f"Detected Intents: {detected_intents}")

        logging.info("Step 3: Optimizing prompt (local optimizer)")
        optimized_prompt, combined_technique, intent_breakdown = optimizer.optimize_prompt_multi(
            masked_text, detected_intents
        )
        selected_technique = combined_technique or "General"
        logging.info(f"Selected Prompt Technique: {selected_technique}")

        logging.info("Step 3a: Build components breakdown for Groq")
        # Build structured components using optimizer templates (fall back to sensible defaults)
        merged_components = {k: "" for k in ["persona", "audience", "tone", "instruction", "data", "format"]}
        merged_components["context"] = masked_text
        merged_components["llm_guardrails"] = getattr(optimizer, "guardrails", [
            "Respect privacy and do not reveal personal information.",
            "Do not make assumptions beyond the provided context.",
            "Maintain the requested tone and persona.",
            "If uncertain, explicitly state 'I don't know'.",
            "Avoid including sensitive details (names, locations, emails) unless explicitly required."
        ])

        # Populate merged components by aggregating templates discovered for each detected intent
        for intent in detected_intents:
            template = optimizer.prompt_templates.get(intent, optimizer.prompt_templates.get("general", {}))
            for key in ["persona", "audience", "tone", "instruction", "data", "format"]:
                value = template.get(key, "")
                if value:
                    # concat unique pieces to give Groq richer context
                    existing = merged_components.get(key, "")
                    if existing and value not in existing:
                        merged_components[key] = existing + " | " + value
                    elif not existing:
                        merged_components[key] = value

        # If still empty, add safe defaults
        if not merged_components["persona"]:
            merged_components["persona"] = "Professional business consultant with expertise in startup strategy and investor pitching."
        if not merged_components["audience"]:
            merged_components["audience"] = "Early-stage investors and VC partners."
        if not merged_components["tone"]:
            merged_components["tone"] = "Concise, persuasive, and investor-focused."
        if not merged_components["format"]:
            merged_components["format"] = "Markdown with clear headings and bullet lists."

        logging.info("Step 3b: Enhancing prompt via Groq API")
        refined_prompt = await enhance_prompt_llm(masked_text, selected_technique, merged_components)
        logging.info(f"Refined Prompt (Groq) preview: {refined_prompt[:200]}...")

        logging.info("Step 4: Calling Gemini API with refined prompt")
        llm_output = await call_gemini(refined_prompt)
        logging.info(f"LLM Response received (truncated): {llm_output[:200]}...")

        logging.info("Step 5: Determining masking status")
        mask_status = "Sensitive personal data masked. Public entities preserved." \
            if any(detected_entities.values()) else "No sensitive data detected. Input remains unchanged."

        logging.info("Step 6: Building response")
        return AnalyzeResponse(
            original_text=input_data.text,
            masked_text=masked_text,
            detected_entities=detected_entities,
            triggered_keywords=triggered_keywords,
            private_contexts=private_contexts,
            sensitivity_score=sensitivity_score,
            sensitivity_level=sensitivity_level,
            detected_intents=detected_intents,
            intent_sources=intent_sources,
            intent_breakdown=intent_breakdown,
            selected_prompt_technique=selected_technique,
            optimized_prompt=optimized_prompt,
            prompt_template=refined_prompt,
            components_breakdown=merged_components,
            llm_response=llm_output,
            status=mask_status + " ✅"
        )

    except Exception as e:
        logging.exception(f"Error processing text: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")

