import re
import logging
from collections import Counter
from typing import List, Tuple, Dict

# ML Imports
import torch
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
import torch.nn.functional as F

logging.basicConfig(level=logging.INFO, format="🧩 [%(levelname)s] → %(message)s")

class PromptOptimizer:
    def __init__(self, ml_model_path: str = None, confidence_threshold: float = 0.6):
        # ---------------- Intent Detection Rules ----------------
        self.intent_rules = {
            "proposal": ["proposal", "plan", "strategy", "pitch"],
            "summarization": ["summarize", "shorten", "brief", "abstract"],
            "task_generation": ["write", "create", "compose", "generate", "draft", "make"],
            "educational": ["explain", "teach", "describe", "what is", "how does", "why"],
            "translation": ["translate", "conversion", "convert"],
            "analysis": ["analyze", "compare", "evaluate", "assess", "review"],
            "qa": ["what", "why", "who", "where", "how", "when"],
            "code": ["code", "script", "function", "program", "debug"],
        }

        # ---------------- Prompt Templates ----------------
        self.prompt_templates = {
            "general": {
                "persona": "Assistant",
                "audience": "User",
                "tone": "Neutral",
                "context": "{masked_text}",
                "instruction": "Respond appropriately",
                "data": "",
                "format": "Text"
            }
        }

        # ---------------- Technique Mapping ----------------
        self.technique_map = {
            "proposal": "Role-based + Few-shot",
            "summarization": "Zero-shot",
            "task_generation": "Step-by-step + Few-shot",
            "educational": "Chain-of-Thought",
            "translation": "Zero-shot",
            "analysis": "Chain-of-Thought",
            "qa": "Zero-shot",
            "code": "Zero-shot",
            "general": "General Instruction"
        }

        # ---------------- LLM Guardrails ----------------
        self.guardrails = [
            "Respect privacy and do not reveal personal information.",
            "Do not make assumptions beyond the provided context.",
            "Maintain the requested tone and persona.",
            "If uncertain, explicitly state 'I don't know'.",
            "Avoid including sensitive details (names, locations, emails) unless explicitly required.",
        ]

        # ---------------- ML Classifier ----------------
        self.conf_threshold = confidence_threshold
        self.use_ml = False
        if ml_model_path:
            self.tokenizer = DistilBertTokenizerFast.from_pretrained(ml_model_path)
            self.model = DistilBertForSequenceClassification.from_pretrained(ml_model_path)
            self.label_map = {i: label for i, label in enumerate(self.intent_rules.keys())}
            self.use_ml = True
            self.model.eval()
            logging.info("✅ ML classifier loaded successfully.")

    # ---------------- ML Prediction ----------------
    def predict_intent_ml(self, text: str) -> Tuple[List[str], Dict[str, float]]:
        if not self.use_ml:
            return [], {}

        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            logits = self.model(**inputs).logits
            probs = torch.sigmoid(logits).squeeze().tolist()

        if isinstance(probs, float):
            probs = [probs]

        predicted_intents = []
        confidence_scores = {}
        for idx, prob in enumerate(probs):
            label = self.label_map[idx]
            confidence_scores[label] = prob
            if prob >= self.conf_threshold:
                predicted_intents.append(label)

        return predicted_intents, confidence_scores

    # ---------------- Hybrid Intent Detection ----------------
    def detect_intents(self, text: str) -> Tuple[List[str], Dict[str, str]]:
        # Try ML first
        ml_intents, ml_conf = self.predict_intent_ml(text)
        intent_sources = {}

        if ml_intents:
            logging.info(f"✅ ML predicted intents: {ml_intents} with confidences {ml_conf}")
            for intent in ml_intents:
                intent_sources[intent] = "ML"
            return ml_intents, intent_sources

        # Fallback to rule-based
        text_lower = text.lower()
        intent_counter = Counter()
        for intent, keywords in self.intent_rules.items():
            for word in keywords:
                matches = re.findall(rf"\b{word}\b", text_lower)
                if matches:
                    intent_counter[intent] += len(matches)

        if not intent_counter:
            intent_counter["general"] = 1

        detected_intents = [intent for intent, _ in intent_counter.most_common()]
        for intent in detected_intents:
            intent_sources[intent] = "Rule"

        logging.info(f"✅ Rule-based intents: {detected_intents}")
        return detected_intents, intent_sources

    # ---------------- Optimize prompt for multi-intent with technique mapping ----------------
    def optimize_prompt_multi(self, masked_text: str, intents: List[str]) -> Tuple[str, str, Dict[str, str]]:
        combined_techniques = []
        combined_components = {
            "persona": set(),
            "instruction": [],
            "audience": set(),
            "tone": set(),
            "context": masked_text,
            "data": [],
            "format": [],
        }

        intent_breakdown = {}
        for intent in intents:
            template = self.prompt_templates.get(intent, self.prompt_templates["general"])
            technique = self.technique_map.get(intent, "General Instruction")
            combined_techniques.append(technique)
            intent_breakdown[intent] = technique

            combined_components["persona"].add(template["persona"])
            combined_components["instruction"].append(template["instruction"])
            combined_components["audience"].add(template["audience"])
            combined_components["tone"].add(template["tone"])
            combined_components["data"].append(template["data"])
            combined_components["format"].append(template["format"])

        # Build prompt text
        components_text = [
            f"Persona: {' / '.join(combined_components['persona'])}",
            f"Audience: {' / '.join(combined_components['audience'])}",
            f"Tone: {' / '.join(combined_components['tone'])}",
            f"Context: {combined_components['context'].strip()}",
            f"Instruction: {' | '.join(combined_components['instruction'])}",
            f"Data: {' | '.join(combined_components['data'])}",
            f"Format: {' | '.join(combined_components['format'])}",
            "LLM Guardrails: " + "; ".join(self.guardrails)
        ]

        optimized_prompt = "\n".join(components_text)
        combined_technique_str = " + ".join(combined_techniques)

        return optimized_prompt, combined_technique_str, intent_breakdown
