# # import re
# # import spacy

# # # Load transformer-based spaCy model
# # try:
# #     nlp = spacy.load("en_core_web_trf")
# # except OSError:
# #     raise OSError("Please install 'en_core_web_trf' via: python -m spacy download en_core_web_trf")

# # # Regex-based extra patterns for fallback detection
# # EXTRA_PATTERNS = {
# #     "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}",
# #     "phone": r"\b\d{10}\b",
# #     "street_address": r"\d+\s[\w\s]+(?:Street|St|Road|Rd|Avenue|Ave|Lane|Ln|Boulevard|Blvd|Drive|Dr|Square|Sq)\b",
# # }

# # PERSON_KEYWORDS = ["my name is", "i am", "this is"]
# # ADDRESS_KEYWORDS = ["my address", "residence", "home", "living at", "this is my address"]

# # COMMON_WORDS = set([
# #     "i", "you", "he", "she", "it", "we", "they",
# #     "my", "your", "his", "her", "our", "their",
# #     "and", "the", "for", "in", "on", "at", "with",
# #     "to", "from", "by", "a", "an", "of", "that",
# # ])

# # def mask_sensitive_data(text: str):
# #     detected = {}
# #     triggered_keywords = {}
# #     masked_text = text
# #     lower_text = text.lower()
# #     entities_to_mask = []

# #     # 1️⃣ Detect personal names using keywords
# #     for phrase in PERSON_KEYWORDS:
# #         if phrase in lower_text:
# #             pattern = re.escape(phrase) + r"\s+([A-Z][a-z]+(?:\s[A-Z]\.)?\s[A-Z][a-z]+)?"
# #             match = re.search(pattern, text)
# #             if match:
# #                 name = match.group(1)
# #                 if name:
# #                     detected.setdefault("name", []).append(name)
# #                     triggered_keywords.setdefault("name", []).append(phrase)
# #                     entities_to_mask.append((name, "[MASKED_NAME]"))

# #     # 2️⃣ Detect personal addresses using keywords
# #     for phrase in ADDRESS_KEYWORDS:
# #         if phrase in lower_text:
# #             start_idx = lower_text.index(phrase)
# #             snippet = masked_text[start_idx:start_idx+150]
# #             doc = nlp(snippet)
# #             for ent in doc.ents:
# #                 if ent.label_ in ["GPE", "LOC", "FAC", "ADDRESS"]:
# #                     if ent.text not in detected.get("address", []):
# #                         detected.setdefault("address", []).append(ent.text)
# #                         triggered_keywords.setdefault("address", []).append(phrase)
# #                         entities_to_mask.append((ent.text, "[MASKED_ADDRESS]"))

# #     # 3️⃣ spaCy NER on entire text (only mask real sensitive entities)
# #     doc = nlp(masked_text)
# #     for ent in doc.ents:
# #         entity_text = ent.text.strip()
# #         if not entity_text or entity_text.lower() in COMMON_WORDS:
# #             continue
# #         if ent.label_ == "PERSON":
# #             if entity_text not in detected.get("name", []):
# #                 detected.setdefault("name", []).append(entity_text)
# #                 entities_to_mask.append((entity_text, "[MASKED_NAME]"))
# #         elif ent.label_ in ["GPE", "LOC", "FAC"]:
# #             if entity_text not in detected.get("address", []):
# #                 detected.setdefault("address", []).append(entity_text)
# #                 entities_to_mask.append((entity_text, "[MASKED_ADDRESS]"))

# #     # 4️⃣ Regex-based fallback (emails, phones, addresses)
# #     for label, pattern in EXTRA_PATTERNS.items():
# #         matches = re.findall(pattern, masked_text)
# #         if matches:
# #             detected.setdefault(label, [])
# #             triggered_keywords.setdefault(label, [])
# #             for match in set(matches):
# #                 if match not in detected[label]:
# #                     detected[label].append(match)
# #                     triggered_keywords[label].append("regex")
# #                     entities_to_mask.append((match, f"[MASKED_{label.upper()}]"))

# #     # 5️⃣ Apply masking with overlap check
# #     entities_to_mask = sorted(entities_to_mask, key=lambda x: len(x[0]), reverse=True)
# #     masked_positions = set()
# #     for original, mask in entities_to_mask:
# #         for match in re.finditer(re.escape(original), masked_text):
# #             start, end = match.span()
# #             if all(pos not in masked_positions for pos in range(start, end)):
# #                 masked_text = masked_text[:start] + mask + masked_text[end:]
# #                 masked_positions.update(range(start, end))

# #     # Deduplicate
# #     detected = {k: sorted(set(v)) for k, v in detected.items()}
# #     triggered_keywords = {k: sorted(set(v)) for k, v in triggered_keywords.items()}

# #     return masked_text, detected, triggered_keywords

# # import re
# # import spacy

# # # Load transformer-based spaCy model
# # try:
# #     nlp = spacy.load("en_core_web_trf")
# # except OSError:
# #     raise OSError("Please install 'en_core_web_trf' via: python -m spacy download en_core_web_trf")

# # # Regex-based extra patterns for fallback detection
# # EXTRA_PATTERNS = {
# #     "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}",
# #     "phone": r"\b\d{10}\b",
# #     "street_address": r"\d+\s[\w\s]+(?:Street|St|Road|Rd|Avenue|Ave|Lane|Ln|Boulevard|Blvd|Drive|Dr|Square|Sq)\b",
# # }

# # # Public cities / countries (not considered sensitive)
# # PUBLIC_LOCATIONS = {
# #     "new york", "los angeles", "london", "paris", "india", "usa", "canada",
# #     "tokyo", "japan", "germany", "australia", "italy", "france", "china",
# #     "dubai", "brazil", "singapore", "new delhi", "chicago", "mumbai"
# # }

# # PERSON_KEYWORDS = ["my name is", "i am", "this is"]
# # ADDRESS_KEYWORDS = ["my address", "residence", "home", "living at", "this is my address"]

# # COMMON_WORDS = set([
# #     "i", "you", "he", "she", "it", "we", "they",
# #     "my", "your", "his", "her", "our", "their",
# #     "and", "the", "for", "in", "on", "at", "with",
# #     "to", "from", "by", "a", "an", "of", "that",
# # ])


# # def mask_sensitive_data(text: str):
# #     detected = {}
# #     triggered_keywords = {}
# #     masked_text = text
# #     lower_text = text.lower()
# #     entities_to_mask = []

# #     # 1️⃣ Detect personal names using keywords
# #     for phrase in PERSON_KEYWORDS:
# #         if phrase in lower_text:
# #             pattern = re.escape(phrase) + r"\s+([A-Z][a-z]+(?:\s[A-Z]\.)?\s[A-Z][a-z]+)?"
# #             match = re.search(pattern, text)
# #             if match:
# #                 name = match.group(1)
# #                 if name:
# #                     detected.setdefault("name", []).append(name)
# #                     triggered_keywords.setdefault("name", []).append(phrase)
# #                     entities_to_mask.append((name, "[MASKED_NAME]"))

# #     # 2️⃣ Detect personal addresses using keywords
# #     for phrase in ADDRESS_KEYWORDS:
# #         if phrase in lower_text:
# #             start_idx = lower_text.index(phrase)
# #             snippet = masked_text[start_idx:start_idx+150]
# #             doc = nlp(snippet)
# #             for ent in doc.ents:
# #                 if ent.label_ in ["GPE", "LOC", "FAC", "ADDRESS"]:
# #                     if ent.text not in detected.get("address", []):
# #                         detected.setdefault("address", []).append(ent.text)
# #                         triggered_keywords.setdefault("address", []).append(phrase)
# #                         entities_to_mask.append((ent.text, "[MASKED_ADDRESS]"))

# #     # 3️⃣ spaCy NER on entire text with location filtering
# #     doc = nlp(masked_text)
# #     for ent in doc.ents:
# #         entity_text = ent.text.strip()
# #         if not entity_text or entity_text.lower() in COMMON_WORDS:
# #             continue

# #         # PERSON → Mask
# #         if ent.label_ == "PERSON":
# #             if entity_text not in detected.get("name", []):
# #                 detected.setdefault("name", []).append(entity_text)
# #                 entities_to_mask.append((entity_text, "[MASKED_NAME]"))

# #         # ORG → Mask
# #         elif ent.label_ == "ORG":
# #             if entity_text not in detected.get("company", []):
# #                 detected.setdefault("company", []).append(entity_text)
# #                 entities_to_mask.append((entity_text, "[MASKED_COMPANY]"))

# #         # GPE / LOC / FAC → Mask only if private context
# #         elif ent.label_ in ["GPE", "LOC", "FAC"]:
# #             entity_lower = entity_text.lower()

# #             # Skip masking if public city/country name
# #             if entity_lower in PUBLIC_LOCATIONS:
# #                 continue

# #             # Mask only if context shows user linkage (e.g., "my", "home", "living in")
# #             if any(kw in lower_text for kw in ADDRESS_KEYWORDS):
# #                 detected.setdefault("address", []).append(entity_text)
# #                 entities_to_mask.append((entity_text, "[MASKED_ADDRESS]"))
# #             elif re.search(r"\d", entity_lower):  # address-like structure
# #                 detected.setdefault("address", []).append(entity_text)
# #                 entities_to_mask.append((entity_text, "[MASKED_ADDRESS]"))

# #     # 4️⃣ Regex-based fallback (emails, phones, etc.)
# #     for label, pattern in EXTRA_PATTERNS.items():
# #         matches = re.findall(pattern, masked_text)
# #         if matches:
# #             detected.setdefault(label, [])
# #             triggered_keywords.setdefault(label, [])
# #             for match in set(matches):
# #                 if match not in detected[label]:
# #                     detected[label].append(match)
# #                     triggered_keywords[label].append("regex")
# #                     entities_to_mask.append((match, f"[MASKED_{label.upper()}]"))

# #     # 5️⃣ Apply masking with overlap check
# #     entities_to_mask = sorted(entities_to_mask, key=lambda x: len(x[0]), reverse=True)
# #     masked_positions = set()
# #     for original, mask in entities_to_mask:
# #         for match in re.finditer(re.escape(original), masked_text):
# #             start, end = match.span()
# #             if all(pos not in masked_positions for pos in range(start, end)):
# #                 masked_text = masked_text[:start] + mask + masked_text[end:]
# #                 masked_positions.update(range(start, end))

# #     # Deduplicate results
# #     detected = {k: sorted(set(v)) for k, v in detected.items()}
# #     triggered_keywords = {k: sorted(set(v)) for k, v in triggered_keywords.items()}

# #     return masked_text, detected, triggered_keywords

# import re
# import spacy

# # Load transformer-based spaCy model
# try:
#     nlp = spacy.load("en_core_web_trf")
# except OSError:
#     raise OSError("Please install 'en_core_web_trf' via: python -m spacy download en_core_web_trf")

# # Regex-based extra patterns for fallback detection
# EXTRA_PATTERNS = {
#     "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}",
#     "phone": r"\b\d{10}\b",
#     "street_address": r"\d+\s[\w\s]+(?:Street|St|Road|Rd|Avenue|Ave|Lane|Ln|Boulevard|Blvd|Drive|Dr|Square|Sq)\b",
# }

# # Context keywords for phone validation
# PHONE_CONTEXT_KEYWORDS = ["call", "mobile", "phone", "contact", "reach", "number"]

# # Public cities / countries (not considered sensitive)
# PUBLIC_LOCATIONS = {
#     "new york", "los angeles", "london", "paris", "india", "usa", "canada",
#     "tokyo", "japan", "germany", "australia", "italy", "france", "china",
#     "dubai", "brazil", "singapore", "new delhi", "chicago", "mumbai"
# }

# PERSON_KEYWORDS = ["my name is", "i am", "this is"]
# ADDRESS_KEYWORDS = ["my address", "residence", "home", "living at", "this is my address"]

# COMMON_WORDS = set([
#     "i", "you", "he", "she", "it", "we", "they",
#     "my", "your", "his", "her", "our", "their",
#     "and", "the", "for", "in", "on", "at", "with",
#     "to", "from", "by", "a", "an", "of", "that",
# ])


# # ✅ Helper: Check if numeric string is within phone context
# def is_phone_number_context(text, match_span):
#     context_window = 20  # chars before/after number
#     start, end = match_span
#     left_context = text[max(0, start - context_window):start].lower()
#     right_context = text[end:end + context_window].lower()
#     return any(keyword in left_context or keyword in right_context for keyword in PHONE_CONTEXT_KEYWORDS)


# def mask_sensitive_data(text: str):
#     detected = {}
#     triggered_keywords = {}
#     masked_text = text
#     lower_text = text.lower()
#     entities_to_mask = []

#     # 1️⃣ Detect personal names using keywords
#     for phrase in PERSON_KEYWORDS:
#         if phrase in lower_text:
#             pattern = re.escape(phrase) + r"\s+([A-Z][a-z]+(?:\s[A-Z]\.)?\s[A-Z][a-z]+)?"
#             match = re.search(pattern, text)
#             if match:
#                 name = match.group(1)
#                 if name:
#                     detected.setdefault("name", []).append(name)
#                     triggered_keywords.setdefault("name", []).append(phrase)
#                     entities_to_mask.append((name, "[MASKED_NAME]"))

#     # 2️⃣ Detect personal addresses using keywords
#     for phrase in ADDRESS_KEYWORDS:
#         if phrase in lower_text:
#             start_idx = lower_text.index(phrase)
#             snippet = masked_text[start_idx:start_idx + 150]
#             doc = nlp(snippet)
#             for ent in doc.ents:
#                 if ent.label_ in ["GPE", "LOC", "FAC", "ADDRESS"]:
#                     if ent.text not in detected.get("address", []):
#                         detected.setdefault("address", []).append(ent.text)
#                         triggered_keywords.setdefault("address", []).append(phrase)
#                         entities_to_mask.append((ent.text, "[MASKED_ADDRESS]"))

#     # 3️⃣ spaCy NER on entire text with location filtering
#     doc = nlp(masked_text)
#     for ent in doc.ents:
#         entity_text = ent.text.strip()
#         if not entity_text or entity_text.lower() in COMMON_WORDS:
#             continue

#         if ent.label_ == "PERSON":
#             detected.setdefault("name", []).append(entity_text)
#             entities_to_mask.append((entity_text, "[MASKED_NAME]"))

#         elif ent.label_ == "ORG":
#             detected.setdefault("company", []).append(entity_text)
#             entities_to_mask.append((entity_text, "[MASKED_COMPANY]"))

#         elif ent.label_ in ["GPE", "LOC", "FAC"]:
#             entity_lower = entity_text.lower()
#             if entity_lower not in PUBLIC_LOCATIONS:
#                 if any(kw in lower_text for kw in ADDRESS_KEYWORDS):
#                     detected.setdefault("address", []).append(entity_text)
#                     entities_to_mask.append((entity_text, "[MASKED_ADDRESS]"))
#                 elif re.search(r"\d", entity_lower):
#                     detected.setdefault("address", []).append(entity_text)
#                     entities_to_mask.append((entity_text, "[MASKED_ADDRESS]"))

#     # 4️⃣ Regex-based fallback (emails, phones, etc.)
#     for label, pattern in EXTRA_PATTERNS.items():
#         matches = list(re.finditer(pattern, masked_text))
#         if matches:
#             detected.setdefault(label, [])
#             triggered_keywords.setdefault(label, [])
#             for match in matches:
#                 value = match.group(0)

#                 # Context-aware filtering for phone numbers
#                 if label == "phone":
#                     if not is_phone_number_context(masked_text, match.span()):
#                         continue
#                     try:
#                         if int(value) > 9999999999 or int(value) < 1000000000:
#                             continue
#                     except ValueError:
#                         continue

#                 if value not in detected[label]:
#                     detected[label].append(value)
#                     triggered_keywords[label].append("regex")
#                     entities_to_mask.append((value, f"[MASKED_{label.upper()}]"))

#     # 5️⃣ Apply masking with overlap check
#     entities_to_mask = sorted(entities_to_mask, key=lambda x: len(x[0]), reverse=True)
#     masked_positions = set()
#     for original, mask in entities_to_mask:
#         for match in re.finditer(re.escape(original), masked_text):
#             start, end = match.span()
#             if all(pos not in masked_positions for pos in range(start, end)):
#                 masked_text = masked_text[:start] + mask + masked_text[end:]
#                 masked_positions.update(range(start, end))

#     # Deduplicate results
#     detected = {k: sorted(set(v)) for k, v in detected.items()}
#     triggered_keywords = {k: sorted(set(v)) for k, v in triggered_keywords.items()}

#     return masked_text, detected, triggered_keywords

# import re
# import spacy

# # Load transformer-based spaCy model
# try:
#     nlp = spacy.load("en_core_web_trf")
# except OSError:
#     raise OSError("Please install 'en_core_web_trf' via: python -m spacy download en_core_web_trf")

# EXTRA_PATTERNS = {
#     "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}",
#     "phone": r"\b\d{10}\b",
#     "street_address": r"\d+\s[\w\s]+(?:Street|St|Road|Rd|Avenue|Ave|Lane|Ln|Boulevard|Blvd|Drive|Dr|Square|Sq)\b",
# }

# PHONE_CONTEXT_KEYWORDS = ["call", "mobile", "phone", "contact", "reach", "number"]

# PUBLIC_LOCATIONS = {
#     "new york", "los angeles", "london", "paris", "india", "usa", "canada",
#     "tokyo", "japan", "germany", "australia", "italy", "france", "china",
#     "dubai", "brazil", "singapore", "new delhi", "chicago", "mumbai"
# }

# COMMON_WORDS = set([
#     "i", "you", "he", "she", "it", "we", "they",
#     "my", "your", "his", "her", "our", "their",
#     "and", "the", "for", "in", "on", "at", "with",
#     "to", "from", "by", "a", "an", "of", "that",
# ])

# # Relation keywords for regex detection
# RELATION_PATTERNS = {
#     "relation_pattern": r"\b(?:my|our)?\s*(?:child|son|daughter|kid|friend|brother|sister|wife|husband|mother|father)\s+([A-Z][a-z]+)\b",
#     "inlaw_pattern": r"\b(?:my|our)?\s*(?:in-?law|mother-?in-?law|father-?in-?law|brother-?in-?law|sister-?in-?law|spouse(?:'s)?(?: parent|relative)?|cousin)\s+([A-Z][a-z]+)\b",
# }

# def is_phone_number_context(text, match_span):
#     context_window = 20
#     start, end = match_span
#     left_context = text[max(0, start - context_window):start].lower()
#     right_context = text[end:end + context_window].lower()
#     return any(keyword in left_context or keyword in right_context for keyword in PHONE_CONTEXT_KEYWORDS)

# def mask_sensitive_data(text: str):
#     detected = {}
#     triggered_keywords = {}
#     masked_text = text
#     lower_text = text.lower()
#     entities_to_mask = []
#     sensitivity_score = 0
#     private_contexts = []

#     # 1️⃣ Relation-based names (including in-laws, cousins, spouses)
#     for keyword, pattern_str in RELATION_PATTERNS.items():
#         pattern = re.compile(pattern_str, flags=re.IGNORECASE)
#         for match in pattern.finditer(text):
#             possible_name = match.group(1).strip()
#             if possible_name.lower() not in COMMON_WORDS and len(possible_name) > 1:
#                 detected.setdefault("name", []).append(possible_name)
#                 triggered_keywords.setdefault("name", []).append(keyword)
#                 entities_to_mask.append((possible_name, "[MASKED_NAME]"))
#                 sensitivity_score += 0.3

#     # 2️⃣ spaCy NER for PERSON, ORG, GPE, LOC, FAC
#     doc = nlp(masked_text)
#     for ent in doc.ents:
#         entity_text = ent.text.strip()
#         if not entity_text or entity_text.lower() in COMMON_WORDS:
#             continue

#         if ent.label_ == "PERSON":
#             detected.setdefault("name", []).append(entity_text)
#             entities_to_mask.append((entity_text, "[MASKED_NAME]"))
#             sensitivity_score += 0.3
#         elif ent.label_ == "ORG":
#             detected.setdefault("company", []).append(entity_text)
#             entities_to_mask.append((entity_text, "[MASKED_COMPANY]"))
#         elif ent.label_ in ["GPE", "LOC", "FAC"]:
#             if entity_text.lower() not in PUBLIC_LOCATIONS:
#                 detected.setdefault("address", []).append(entity_text)
#                 entities_to_mask.append((entity_text, "[MASKED_ADDRESS]"))

#     # 3️⃣ Regex fallback (emails, phones, addresses)
#     for label, pattern in EXTRA_PATTERNS.items():
#         for match in re.finditer(pattern, masked_text):
#             value = match.group(0)
#             if label == "phone" and not is_phone_number_context(masked_text, match.span()):
#                 continue
#             detected.setdefault(label, []).append(value)
#             triggered_keywords.setdefault(label, []).append("regex")
#             entities_to_mask.append((value, f"[MASKED_{label.upper()}]"))
#             sensitivity_score += 0.4 if label in ["email", "phone", "street_address"] else 0

#     # 4️⃣ Contextual sensitivity detection
#     SENSITIVE_CONTEXT_PATTERNS = {
#         "emotional": ["apology", "sorry", "remorse", "regret", "disagreement", "fight", "argue"],
#         "relationship": ["friend", "family", "child", "spouse", "colleague"],
#         "financial": ["money", "loan", "debt", "salary", "land", "property", "inheritance"]
#     }
#     for category, words in SENSITIVE_CONTEXT_PATTERNS.items():
#         for w in words:
#             if re.search(rf"\b{re.escape(w)}\b", lower_text):
#                 private_contexts.append(category)
#                 triggered_keywords.setdefault("context", []).append(category)
#                 sensitivity_score += 0.2

#     # 5️⃣ Apply masking
#     entities_to_mask = sorted(entities_to_mask, key=lambda x: len(x[0]), reverse=True)
#     masked_positions = set()
#     for original, mask in entities_to_mask:
#         for match in re.finditer(re.escape(original), masked_text):
#             start, end = match.span()
#             if all(pos not in masked_positions for pos in range(start, end)):
#                 masked_text = masked_text[:start] + mask + masked_text[end:]
#                 masked_positions.update(range(start, end))

#     # 6️⃣ Sensitivity classification
#     sensitivity_level = "Low"
#     if sensitivity_score >= 0.6:
#         sensitivity_level = "High"
#     elif sensitivity_score >= 0.3:
#         sensitivity_level = "Medium"

#     # Deduplicate
#     detected = {k: sorted(set(v)) for k, v in detected.items()}
#     triggered_keywords = {k: sorted(set(v)) for k, v in triggered_keywords.items()}

#     return {
#         "masked_text": masked_text,
#         "detected_entities": detected,
#         "triggered_keywords": triggered_keywords,
#         "private_contexts": sorted(set(private_contexts)),
#         "sensitivity_score": round(min(sensitivity_score, 1.0), 2),
#         "sensitivity_level": sensitivity_level
#     }

# import re
# import spacy
# import requests
# from functools import lru_cache

# # 🔹 Load transformer-based spaCy model
# try:
#     nlp = spacy.load("en_core_web_trf")
# except OSError:
#     raise OSError("Please install 'en_core_web_trf' via: python -m spacy download en_core_web_trf")

# EXTRA_PATTERNS = {
#     "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}",
#     "phone": r"\b\d{10}\b",
#     "street_address": r"\d+\s[\w\s]+(?:Street|St|Road|Rd|Avenue|Ave|Lane|Ln|Boulevard|Blvd|Drive|Dr|Square|Sq)\b",
# }

# PHONE_CONTEXT_KEYWORDS = ["call", "mobile", "phone", "contact", "reach", "number"]

# PUBLIC_LOCATIONS = {
#     "new york", "los angeles", "london", "paris", "india", "usa", "canada",
#     "tokyo", "japan", "germany", "australia", "italy", "france", "china",
#     "dubai", "brazil", "singapore", "new delhi", "chicago", "mumbai", "hyderabad"
# }

# COMMON_WORDS = {
#     "i", "you", "he", "she", "it", "we", "they", "my", "your", "his", "her",
#     "our", "their", "and", "the", "for", "in", "on", "at", "with", "to",
#     "from", "by", "a", "an", "of", "that"
# }

# RELATION_PATTERNS = {
#     "relation_pattern": r"\b(?:my|our)?\s*(?:child|son|daughter|kid|friend|brother|sister|wife|husband|mother|father)\s+([A-Z][a-z]+)\b",
#     "inlaw_pattern": r"\b(?:my|our)?\s*(?:in-?law|mother-?in-?law|father-?in-?law|brother-?in-?law|sister-?in-?law|spouse(?:'s)?(?: parent|relative)?|cousin)\s+([A-Z][a-z]+)\b",
# }


# # 🔹 Wikipedia-based public figure check (cached)
# @lru_cache(maxsize=500)
# def is_public_figure(name: str) -> bool:
#     try:
#         response = requests.get(
#             "https://en.wikipedia.org/api/rest_v1/page/summary/" + name.replace(" ", "_"),
#             timeout=3
#         )
#         if response.status_code == 200:
#             data = response.json()
#             if "description" in data and data.get("type") != "disambiguation":
#                 desc = data["description"].lower()
#                 if any(word in desc for word in [
#                     "actor", "singer", "politician", "cricketer", "footballer",
#                     "entrepreneur", "scientist", "leader", "player"
#                 ]):
#                     return True
#         return False
#     except Exception:
#         return False


# # 🔹 Context check for phone numbers
# def is_phone_number_context(text, match_span):
#     context_window = 20
#     start, end = match_span
#     left_context = text[max(0, start - context_window):start].lower()
#     right_context = text[end:end + context_window].lower()
#     return any(keyword in left_context or keyword in right_context for keyword in PHONE_CONTEXT_KEYWORDS)


# # 🔹 Detect if user is asking a public info query
# def is_public_query_context(text):
#     return bool(re.search(r"\b(tell me about|who is|what is|give details about)\b", text.lower()))


# # 🔹 Check if location appears in an address context
# def is_address_context(text: str, match_span) -> bool:
#     ADDRESS_CONTEXT_KEYWORDS = [
#         "address", "plot", "house", "door no", "street", "lane", "road",
#         "colony", "h.no", "flat", "building", "resides", "lives in", "home", "my address"
#     ]
#     context_window = 40
#     start, end = match_span
#     left_context = text[max(0, start - context_window):start].lower()
#     right_context = text[end:end + context_window].lower()
#     return any(keyword in left_context or keyword in right_context for keyword in ADDRESS_CONTEXT_KEYWORDS)


# # 🔹 Main masking function
# def mask_sensitive_data(text: str):
#     detected = {}
#     triggered_keywords = {}
#     masked_text = text
#     lower_text = text.lower()
#     entities_to_mask = []
#     sensitivity_score = 0
#     private_contexts = []

#     # 1️⃣ Relation-based names
#     for keyword, pattern_str in RELATION_PATTERNS.items():
#         for match in re.finditer(pattern_str, text, re.IGNORECASE):
#             possible_name = match.group(1).strip()
#             if possible_name.lower() not in COMMON_WORDS:
#                 detected.setdefault("name", []).append(possible_name)
#                 triggered_keywords.setdefault("name", []).append(keyword)
#                 entities_to_mask.append((possible_name, "[MASKED_NAME]"))
#                 sensitivity_score += 0.3

#     # 2️⃣ spaCy NER
#     doc = nlp(masked_text)
#     public_query = is_public_query_context(text)

#     for ent in doc.ents:
#         entity_text = ent.text.strip()
#         if not entity_text or entity_text.lower() in COMMON_WORDS:
#             continue

#         if ent.label_ == "PERSON":
#             if is_public_figure(entity_text) or public_query:
#                 continue
#             detected.setdefault("name", []).append(entity_text)
#             entities_to_mask.append((entity_text, "[MASKED_NAME]"))
#             sensitivity_score += 0.3

#         elif ent.label_ == "ORG":
#             detected.setdefault("company", []).append(entity_text)
#             entities_to_mask.append((entity_text, "[MASKED_COMPANY]"))

#         elif ent.label_ in ["GPE", "LOC", "FAC"]:
#             entity_text_lower = entity_text.lower()
#             match_span = (ent.start_char, ent.end_char)

#             # 🔸 Mask only if used in address context
#             if entity_text_lower in PUBLIC_LOCATIONS:
#                 if is_address_context(text, match_span):
#                     detected.setdefault("address", []).append(entity_text)
#                     entities_to_mask.append((entity_text, "[MASKED_ADDRESS]"))
#                     sensitivity_score += 0.3
#             else:
#                 detected.setdefault("address", []).append(entity_text)
#                 entities_to_mask.append((entity_text, "[MASKED_ADDRESS]"))
#                 sensitivity_score += 0.3

#     # 3️⃣ Regex fallback (emails, phones, addresses)
#     for label, pattern in EXTRA_PATTERNS.items():
#         for match in re.finditer(pattern, masked_text):
#             value = match.group(0)
#             if label == "phone" and not is_phone_number_context(masked_text, match.span()):
#                 continue
#             detected.setdefault(label, []).append(value)
#             triggered_keywords.setdefault(label, []).append("regex")
#             entities_to_mask.append((value, f"[MASKED_{label.upper()}]"))
#             if label in ["email", "phone", "street_address"]:
#                 sensitivity_score += 0.4

#     # 4️⃣ Contextual patterns
#     SENSITIVE_CONTEXT_PATTERNS = {
#         "emotional": ["apology", "sorry", "regret", "fight", "argue"],
#         "relationship": ["friend", "family", "spouse", "colleague"],
#         "financial": ["money", "loan", "salary", "property"]
#     }
#     for category, words in SENSITIVE_CONTEXT_PATTERNS.items():
#         if any(re.search(rf"\b{re.escape(w)}\b", lower_text) for w in words):
#             private_contexts.append(category)
#             triggered_keywords.setdefault("context", []).append(category)
#             sensitivity_score += 0.2

#     # 5️⃣ Apply masking
#     entities_to_mask = sorted(entities_to_mask, key=lambda x: len(x[0]), reverse=True)
#     for original, mask in entities_to_mask:
#         masked_text = re.sub(re.escape(original), mask, masked_text)

#     # 6️⃣ Sensitivity level
#     if sensitivity_score >= 0.6:
#         sensitivity_level = "High"
#     elif sensitivity_score >= 0.3:
#         sensitivity_level = "Medium"
#     else:
#         sensitivity_level = "Low"

#     detected = {k: sorted(set(v)) for k, v in detected.items()}
#     triggered_keywords = {k: sorted(set(v)) for k, v in triggered_keywords.items()}

#     return {
#         "masked_text": masked_text,
#         "detected_entities": detected,
#         "triggered_keywords": triggered_keywords,
#         "private_contexts": sorted(set(private_contexts)),
#         "sensitivity_score": round(min(sensitivity_score, 1.0), 2),
#         "sensitivity_level": sensitivity_level
#     }

# import re
# import spacy
# import requests
# from functools import lru_cache

# # 🔹 Load transformer-based spaCy model
# try:
#     nlp = spacy.load("en_core_web_trf")
# except OSError:
#     raise OSError("Please install 'en_core_web_trf' via: python -m spacy download en_core_web_trf")

# EXTRA_PATTERNS = {
#     "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}",
#     "phone": r"\b\d{10}\b",
#     "street_address": r"\d+\s[\w\s]+(?:Street|St|Road|Rd|Avenue|Ave|Lane|Ln|Boulevard|Blvd|Drive|Dr|Square|Sq)\b",
# }

# PHONE_CONTEXT_KEYWORDS = ["call", "mobile", "phone", "contact", "reach", "number"]

# PUBLIC_LOCATIONS = {
#     "new york", "los angeles", "london", "paris", "india", "usa", "canada",
#     "tokyo", "japan", "germany", "australia", "italy", "france", "china",
#     "dubai", "brazil", "singapore", "new delhi", "chicago", "mumbai", "hyderabad"
# }

# COMMON_WORDS = {
#     "i", "you", "he", "she", "it", "we", "they", "my", "your", "his", "her",
#     "our", "their", "and", "the", "for", "in", "on", "at", "with", "to",
#     "from", "by", "a", "an", "of", "that"
# }

# RELATION_PATTERNS = {
#     "relation_pattern": r"\b(?:my|our)?\s*(?:child|son|daughter|kid|friend|brother|sister|wife|husband|mother|father)\s+([A-Z][a-z]+)\b",
#     "inlaw_pattern": r"\b(?:my|our)?\s*(?:in-?law|mother-?in-?law|father-?in-?law|brother-?in-?law|sister-?in-?law|spouse(?:'s)?(?: parent|relative)?|cousin)\s+([A-Z][a-z]+)\b",
# }

# # 🔹 Wikipedia-based public figure check (cached + fuzzy handling)
# @lru_cache(maxsize=500)
# def is_public_figure(name: str) -> bool:
#     try:
#         candidates = [name]
#         # Handle initials and full-name variations
#         if name.lower().startswith("ms "):
#             candidates.append(name.replace("ms", "Mahendra Singh", 1))
#         if len(name.split()) == 1:
#             candidates.append("ms " + name)
#             candidates.append("mahendra singh " + name)

#         for candidate in candidates:
#             response = requests.get(
#                 "https://en.wikipedia.org/api/rest_v1/page/summary/" + candidate.replace(" ", "_"),
#                 timeout=3
#             )
#             if response.status_code == 200:
#                 data = response.json()
#                 if "description" in data and data.get("type") != "disambiguation":
#                     desc = data["description"].lower()
#                     if any(word in desc for word in [
#                         "actor", "singer", "politician", "cricketer", "footballer",
#                         "entrepreneur", "scientist", "leader", "player"
#                     ]):
#                         return True
#         return False
#     except Exception:
#         return False

# # 🔹 Context check for phone numbers
# def is_phone_number_context(text, match_span):
#     context_window = 20
#     start, end = match_span
#     left_context = text[max(0, start - context_window):start].lower()
#     right_context = text[end:end + context_window].lower()
#     return any(keyword in left_context or keyword in right_context for keyword in PHONE_CONTEXT_KEYWORDS)

# # 🔹 Detect if user is asking a public info query
# def is_public_query_context(text):
#     return bool(re.search(
#         r"\b(tell me about|who is|what is|give details about|know about|information about)\b",
#         text.lower()
#     ))

# # 🔹 Check if location appears in an address context
# def is_address_context(text: str, match_span) -> bool:
#     ADDRESS_CONTEXT_KEYWORDS = [
#         "address", "plot", "house", "door no", "street", "lane", "road",
#         "colony", "h.no", "flat", "building", "resides", "lives in", "home", "my address"
#     ]
#     context_window = 40
#     start, end = match_span
#     left_context = text[max(0, start - context_window):start].lower()
#     right_context = text[end:end + context_window].lower()
#     return any(keyword in left_context or keyword in right_context for keyword in ADDRESS_CONTEXT_KEYWORDS)

# # 🔹 Main masking function with public figure checks & debug
# def mask_sensitive_data(text: str):
#     detected = {}
#     triggered_keywords = {}
#     masked_text = text
#     lower_text = text.lower()
#     entities_to_mask = []
#     sensitivity_score = 0
#     private_contexts = []

#     # 1️⃣ Relation-based names (check public figures)
#     for keyword, pattern_str in RELATION_PATTERNS.items():
#         for match in re.finditer(pattern_str, text, re.IGNORECASE):
#             possible_name = match.group(1).strip()
#             if possible_name.lower() in COMMON_WORDS:
#                 continue

#             # 🔹 Public figure check
#             try:
#                 if is_public_figure(possible_name):
#                     print(f"✅ Relation name is public figure, skipping mask: {possible_name}")
#                     continue
#             except Exception as e:
#                 print(f"⚠️ Error checking public figure for {possible_name}: {e}")

#             detected.setdefault("name", []).append(possible_name)
#             triggered_keywords.setdefault("name", []).append(keyword)
#             entities_to_mask.append((possible_name, "[MASKED_NAME]"))
#             sensitivity_score += 0.3

#     # 2️⃣ spaCy NER
#     doc = nlp(masked_text)
#     for ent in doc.ents:
#         entity_text = ent.text.strip()
#         if not entity_text or entity_text.lower() in COMMON_WORDS:
#             continue

#         if ent.label_ == "PERSON":
#             # Include common prefixes in full name check
#             full_name = entity_text
#             start_idx = ent.start
#             if start_idx > 0:
#                 prev_token = doc[start_idx - 1].text.lower()
#                 if prev_token in {"ms", "mr", "mrs", "dr"}:
#                     full_name = prev_token + " " + entity_text

#             # 🔹 Public figure check
#             try:
#                 if is_public_figure(full_name):
#                     print(f"✅ NER name is public figure, skipping mask: {full_name}")
#                     continue
#             except Exception as e:
#                 print(f"⚠️ Error checking public figure for {full_name}: {e}")

#             detected.setdefault("name", []).append(entity_text)
#             entities_to_mask.append((entity_text, "[MASKED_NAME]"))
#             sensitivity_score += 0.3

#         elif ent.label_ == "ORG":
#             detected.setdefault("company", []).append(entity_text)
#             entities_to_mask.append((entity_text, "[MASKED_COMPANY]"))

#         elif ent.label_ in ["GPE", "LOC", "FAC"]:
#             entity_text_lower = entity_text.lower()
#             match_span = (ent.start_char, ent.end_char)
#             if entity_text_lower in PUBLIC_LOCATIONS:
#                 if is_address_context(text, match_span):
#                     detected.setdefault("address", []).append(entity_text)
#                     entities_to_mask.append((entity_text, "[MASKED_ADDRESS]"))
#                     sensitivity_score += 0.3
#             else:
#                 detected.setdefault("address", []).append(entity_text)
#                 entities_to_mask.append((entity_text, "[MASKED_ADDRESS]"))
#                 sensitivity_score += 0.3

#     # 3️⃣ Regex fallback (emails, phones, addresses)
#     for label, pattern in EXTRA_PATTERNS.items():
#         for match in re.finditer(pattern, masked_text):
#             value = match.group(0)
#             if label == "phone" and not is_phone_number_context(masked_text, match.span()):
#                 continue
#             detected.setdefault(label, []).append(value)
#             triggered_keywords.setdefault(label, []).append("regex")
#             entities_to_mask.append((value, f"[MASKED_{label.upper()}]"))
#             if label in ["email", "phone", "street_address"]:
#                 sensitivity_score += 0.4

#     # 4️⃣ Contextual patterns
#     SENSITIVE_CONTEXT_PATTERNS = {
#         "emotional": ["apology", "sorry", "regret", "fight", "argue"],
#         "relationship": ["friend", "family", "spouse", "colleague"],
#         "financial": ["money", "loan", "salary", "property"]
#     }
#     for category, words in SENSITIVE_CONTEXT_PATTERNS.items():
#         if any(re.search(rf"\b{re.escape(w)}\b", lower_text) for w in words):
#             private_contexts.append(category)
#             triggered_keywords.setdefault("context", []).append(category)
#             sensitivity_score += 0.2

#     # 5️⃣ Apply masking
#     entities_to_mask = sorted(entities_to_mask, key=lambda x: len(x[0]), reverse=True)
#     for original, mask in entities_to_mask:
#         masked_text = re.sub(re.escape(original), mask, masked_text)

#     # 6️⃣ Sensitivity level
#     if sensitivity_score >= 0.6:
#         sensitivity_level = "High"
#     elif sensitivity_score >= 0.3:
#         sensitivity_level = "Medium"
#     else:
#         sensitivity_level = "Low"

#     detected = {k: sorted(set(v)) for k, v in detected.items()}
#     triggered_keywords = {k: sorted(set(v)) for k, v in triggered_keywords.items()}

#     return {
#         "masked_text": masked_text,
#         "detected_entities": detected,
#         "triggered_keywords": triggered_keywords,
#         "private_contexts": sorted(set(private_contexts)),
#         "sensitivity_score": round(min(sensitivity_score, 1.0), 2),
#         "sensitivity_level": sensitivity_level
#     }

# import re
# import spacy
# import requests
# from functools import lru_cache
# from rapidfuzz import fuzz

# # 🔹 Load transformer-based spaCy model
# try:
#     nlp = spacy.load("en_core_web_trf")
# except OSError:
#     raise OSError("Please install 'en_core_web_trf' via: python -m spacy download en_core_web_trf")

# EXTRA_PATTERNS = {
#     "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}",
#     "phone": r"\b\d{10}\b",
#     "street_address": r"\d+\s[\w\s]+(?:Street|St|Road|Rd|Avenue|Ave|Lane|Ln|Boulevard|Blvd|Drive|Dr|Square|Sq)\b",
# }

# PHONE_CONTEXT_KEYWORDS = ["call", "mobile", "phone", "contact", "reach", "number"]

# PUBLIC_LOCATIONS = {
#     "new york", "los angeles", "london", "paris", "india", "usa", "canada",
#     "tokyo", "japan", "germany", "australia", "italy", "france", "china",
#     "dubai", "brazil", "singapore", "new delhi", "chicago", "mumbai", "hyderabad"
# }

# COMMON_WORDS = {
#     "i", "you", "he", "she", "it", "we", "they", "my", "your", "his", "her",
#     "our", "their", "and", "the", "for", "in", "on", "at", "with", "to",
#     "from", "by", "a", "an", "of", "that"
# }

# RELATION_PATTERNS = {
#     "relation_pattern": r"\b(?:my|our)?\s*(?:child|son|daughter|kid|friend|brother|sister|wife|husband|mother|father)\s+([A-Z][a-z]+)\b",
#     "inlaw_pattern": r"\b(?:my|our)?\s*(?:in-?law|mother-?in-?law|father-?in-?law|brother-?in-?law|sister-?in-?law|spouse(?:'s)?(?: parent|relative)?|cousin)\s+([A-Z][a-z]+)\b",
# }

# # 🔹 Public figure whitelist
# PUBLIC_FIGURE_WHITELIST = {
#     "MS Dhoni", "Sachin Tendulkar", "Lionel Messi", "Cristiano Ronaldo",
#     "Elon Musk", "Narendra Modi", "Oprah Winfrey"
# }

# # 🔹 Wikipedia-based public figure check with fuzzy handling
# @lru_cache(maxsize=1000)
# def is_public_figure(name: str) -> bool:
#     if name in PUBLIC_FIGURE_WHITELIST:
#         print(f"✅ {name} found in whitelist, skipping mask")
#         return True

#     candidates = [name.strip(), name.title(), name.upper()]
#     if len(name.split()) == 1:
#         candidates.append("MS " + name)
#         candidates.append("Mahendra Singh " + name)

#     for candidate in candidates:
#         wiki_title = candidate.replace(" ", "_")
#         url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{wiki_title}"
#         try:
#             print(f"🔍 Checking Wikipedia: {url}")
#             response = requests.get(url, timeout=3)
#             if response.status_code == 200:
#                 data = response.json()
#                 if data.get("type") == "disambiguation":
#                     continue
#                 desc = data.get("description", "").lower()
#                 if any(word in desc for word in [
#                     "actor", "singer", "politician", "cricketer", "footballer",
#                     "entrepreneur", "scientist", "leader", "player"
#                 ]):
#                     print(f"✅ {candidate} detected as public figure ({desc})")
#                     return True
#                 page_title = data.get("title", "")
#                 if fuzz.ratio(page_title.lower(), candidate.lower()) > 85:
#                     print(f"✅ Fuzzy match: {candidate} ≈ {page_title}")
#                     return True
#         except Exception as e:
#             print(f"⚠️ Error checking Wikipedia for {candidate}: {e}")
#             continue
#     return False

# # 🔹 Context checks
# def is_phone_number_context(text, match_span):
#     context_window = 20
#     start, end = match_span
#     left_context = text[max(0, start - context_window):start].lower()
#     right_context = text[end:end + context_window].lower()
#     return any(keyword in left_context or keyword in right_context for keyword in PHONE_CONTEXT_KEYWORDS)

# def is_public_query_context(text):
#     return bool(re.search(
#         r"\b(tell me about|who is|what is|give details about|know about|information about)\b",
#         text.lower()
#     ))

# def is_address_context(text: str, match_span) -> bool:
#     ADDRESS_CONTEXT_KEYWORDS = [
#         "address", "plot", "house", "door no", "street", "lane", "road",
#         "colony", "h.no", "flat", "building", "resides", "lives in", "home", "my address"
#     ]
#     context_window = 40
#     start, end = match_span
#     left_context = text[max(0, start - context_window):start].lower()
#     right_context = text[end:end + context_window].lower()
#     return any(keyword in left_context or keyword in right_context for keyword in ADDRESS_CONTEXT_KEYWORDS)

# # 🔹 Main masking function with public figure checks
# def mask_sensitive_data(text: str):
#     detected = {}
#     triggered_keywords = {}
#     masked_text = text
#     lower_text = text.lower()
#     entities_to_mask = []
#     sensitivity_score = 0
#     private_contexts = []

#     # 1️⃣ Relation-based names
#     for keyword, pattern_str in RELATION_PATTERNS.items():
#         for match in re.finditer(pattern_str, text, re.IGNORECASE):
#             possible_name = match.group(1).strip()
#             if possible_name.lower() in COMMON_WORDS:
#                 continue
#             if is_public_figure(possible_name):
#                 continue
#             detected.setdefault("name", []).append(possible_name)
#             triggered_keywords.setdefault("name", []).append(keyword)
#             entities_to_mask.append((possible_name, "[MASKED_NAME]"))
#             sensitivity_score += 0.3

#     # 2️⃣ spaCy NER
#     doc = nlp(masked_text)
#     for ent in doc.ents:
#         entity_text = ent.text.strip()
#         if not entity_text or entity_text.lower() in COMMON_WORDS:
#             continue
#         if ent.label_ == "PERSON":
#             full_name = entity_text
#             start_idx = ent.start
#             if start_idx > 0:
#                 prev_token = doc[start_idx - 1].text.lower()
#                 if prev_token in {"ms", "mr", "mrs", "dr"}:
#                     full_name = prev_token + " " + entity_text
#             if is_public_figure(full_name):
#                 continue
#             detected.setdefault("name", []).append(entity_text)
#             entities_to_mask.append((entity_text, "[MASKED_NAME]"))
#             sensitivity_score += 0.3
#         elif ent.label_ == "ORG":
#             detected.setdefault("company", []).append(entity_text)
#             entities_to_mask.append((entity_text, "[MASKED_COMPANY]"))
#         elif ent.label_ in ["GPE", "LOC", "FAC"]:
#             entity_text_lower = entity_text.lower()
#             match_span = (ent.start_char, ent.end_char)
#             if entity_text_lower in PUBLIC_LOCATIONS and is_address_context(text, match_span):
#                 detected.setdefault("address", []).append(entity_text)
#                 entities_to_mask.append((entity_text, "[MASKED_ADDRESS]"))
#                 sensitivity_score += 0.3
#             else:
#                 detected.setdefault("address", []).append(entity_text)
#                 entities_to_mask.append((entity_text, "[MASKED_ADDRESS]"))
#                 sensitivity_score += 0.3

#     # 3️⃣ Regex fallback
#     for label, pattern in EXTRA_PATTERNS.items():
#         for match in re.finditer(pattern, masked_text):
#             value = match.group(0)
#             if label == "phone" and not is_phone_number_context(masked_text, match.span()):
#                 continue
#             detected.setdefault(label, []).append(value)
#             triggered_keywords.setdefault(label, []).append("regex")
#             entities_to_mask.append((value, f"[MASKED_{label.upper()}]"))
#             if label in ["email", "phone", "street_address"]:
#                 sensitivity_score += 0.4

#     # 4️⃣ Contextual patterns
#     SENSITIVE_CONTEXT_PATTERNS = {
#         "emotional": ["apology", "sorry", "regret", "fight", "argue"],
#         "relationship": ["friend", "family", "spouse", "colleague"],
#         "financial": ["money", "loan", "salary", "property"]
#     }
#     for category, words in SENSITIVE_CONTEXT_PATTERNS.items():
#         if any(re.search(rf"\b{re.escape(w)}\b", lower_text) for w in words):
#             private_contexts.append(category)
#             triggered_keywords.setdefault("context", []).append(category)
#             sensitivity_score += 0.2

#     # 5️⃣ Apply masking
#     entities_to_mask = sorted(entities_to_mask, key=lambda x: len(x[0]), reverse=True)
#     for original, mask in entities_to_mask:
#         masked_text = re.sub(re.escape(original), mask, masked_text)

#     # 6️⃣ Sensitivity level
#     if sensitivity_score >= 0.6:
#         sensitivity_level = "High"
#     elif sensitivity_score >= 0.3:
#         sensitivity_level = "Medium"
#     else:
#         sensitivity_level = "Low"

#     detected = {k: sorted(set(v)) for k, v in detected.items()}
#     triggered_keywords = {k: sorted(set(v)) for k, v in triggered_keywords.items()}

#     return {
#         "masked_text": masked_text,
#         "detected_entities": detected,
#         "triggered_keywords": triggered_keywords,
#         "private_contexts": sorted(set(private_contexts)),
#         "sensitivity_score": round(min(sensitivity_score, 1.0), 2),
#         "sensitivity_level": sensitivity_level
#     }

# import re
# import spacy
# import requests
# from functools import lru_cache
# from rapidfuzz import fuzz

# # 🔹 Load spaCy transformer model
# try:
#     nlp = spacy.load("en_core_web_trf")
# except OSError:
#     raise OSError("Please install 'en_core_web_trf': python -m spacy download en_core_web_trf")

# EXTRA_PATTERNS = {
#     "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}",
#     "phone": r"\b\d{10}\b",
#     "street_address": r"\d+\s[\w\s]+(?:Street|St|Road|Rd|Avenue|Ave|Lane|Ln|Boulevard|Blvd|Drive|Dr|Square|Sq)\b",
# }

# PHONE_CONTEXT_KEYWORDS = ["call", "mobile", "phone", "contact", "reach", "number"]

# PUBLIC_LOCATIONS = {
#     "new york", "los angeles", "london", "paris", "india", "usa", "canada",
#     "tokyo", "japan", "germany", "australia", "italy", "france", "china",
#     "dubai", "brazil", "singapore", "new delhi", "chicago", "mumbai", "hyderabad"
# }

# COMMON_WORDS = {
#     "i", "you", "he", "she", "it", "we", "they", "my", "your", "his", "her",
#     "our", "their", "and", "the", "for", "in", "on", "at", "with", "to",
#     "from", "by", "a", "an", "of", "that"
# }

# RELATION_PATTERNS = {
#     "relation_pattern": r"\b(?:my|our)?\s*(?:child|son|daughter|kid|friend|brother|sister|wife|husband|mother|father)\s+([A-Z][a-z]+)\b",
#     "inlaw_pattern": r"\b(?:my|our)?\s*(?:in-?law|mother-?in-?law|father-?in-?law|brother-?in-?law|sister-?in-?law|spouse(?:'s)?(?: parent|relative)?|cousin)\s+([A-Z][a-z]+)\b",
# }

# PUBLIC_FIGURE_WHITELIST = {
#     "MS Dhoni", "Sachin Tendulkar", "Lionel Messi", "Cristiano Ronaldo",
#     "Elon Musk", "Narendra Modi", "Oprah Winfrey", "Virat Kohli", "Mike Tyson"
# }

# @lru_cache(maxsize=1000)
# def is_public_figure(name: str) -> bool:
#     name_clean = name.strip().lower()
#     for pf in PUBLIC_FIGURE_WHITELIST:
#         if name_clean == pf.lower():
#             return True
#     candidates = [name.strip(), name.title(), name.upper()]
#     if len(name.split()) == 1:
#         candidates.append("MS " + name)
#         candidates.append("Mahendra Singh " + name)
#     for candidate in candidates:
#         wiki_title = candidate.replace(" ", "_")
#         url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{wiki_title}"
#         try:
#             response = requests.get(url, timeout=3)
#             if response.status_code != 200:
#                 continue
#             data = response.json()
#             if data.get("type") == "disambiguation":
#                 continue
#             desc = data.get("description", "").lower()
#             if any(word in desc for word in [
#                 "actor", "singer", "politician", "cricketer", "footballer",
#                 "entrepreneur", "scientist", "leader", "player", "boxer"
#             ]):
#                 return True
#             page_title = data.get("title", "")
#             if fuzz.ratio(page_title.lower(), candidate.lower()) > 85:
#                 return True
#         except Exception:
#             continue
#     return False

# # 🔹 Context checks
# def is_phone_number_context(text, match_span):
#     context_window = 20
#     start, end = match_span
#     left_context = text[max(0, start - context_window):start].lower()
#     right_context = text[end:end + context_window].lower()
#     return any(keyword in left_context or keyword in right_context for keyword in PHONE_CONTEXT_KEYWORDS)

# def is_address_context(text: str, match_span) -> bool:
#     ADDRESS_CONTEXT_KEYWORDS = [
#         "address", "plot", "house", "door no", "street", "lane", "road",
#         "colony", "h.no", "flat", "building", "resides", "lives in", "home", "my address"
#     ]
#     context_window = 40
#     start, end = match_span
#     left_context = text[max(0, start - context_window):start].lower()
#     right_context = text[end:end + context_window].lower()
#     return any(keyword in left_context or keyword in right_context for keyword in ADDRESS_CONTEXT_KEYWORDS)

# # 🔹 Intent detection for public info requests
# def detect_intent(text: str):
#     info_keywords = ["know about", "tell me about", "information about", "who is", "what is", "details about"]
#     text_lower = text.lower()
#     if any(k in text_lower for k in info_keywords):
#         return "general"
#     return "personal"

# def should_mask_person(name: str, intent: str) -> bool:
#     """
#     Determine if a PERSON entity should be masked.
#     - If intent is 'general' (informational query) and it's a public figure, do NOT mask
#     - Otherwise, mask it
#     """
#     if intent == "general" and is_public_figure(name):
#         return False
#     return True

# def mask_sensitive_data(text: str):
#     detected = {}
#     triggered_keywords = {}
#     masked_text = text
#     lower_text = text.lower()
#     entities_to_mask = []
#     sensitivity_score = 0
#     private_contexts = []

#     # Determine intent
#     intent = detect_intent(text)

#     # 1️⃣ Relation-based names
#     for keyword, pattern_str in RELATION_PATTERNS.items():
#         for match in re.finditer(pattern_str, text, re.IGNORECASE):
#             possible_name = match.group(1).strip()
#             if possible_name.lower() in COMMON_WORDS:
#                 continue
#             if not should_mask_person(possible_name, intent):
#                 continue
#             detected.setdefault("name", []).append(possible_name)
#             triggered_keywords.setdefault("name", []).append(keyword)
#             entities_to_mask.append((possible_name, "[MASKED_NAME]"))
#             sensitivity_score += 0.3

#     # 2️⃣ spaCy NER
#     doc = nlp(text)
#     for ent in doc.ents:
#         entity_text = ent.text.strip()
#         if not entity_text or entity_text.lower() in COMMON_WORDS:
#             continue

#         if ent.label_ == "PERSON":
#             full_name = entity_text
#             start_idx = ent.start
#             if start_idx > 0:
#                 prev_token = doc[start_idx - 1].text.lower()
#                 if prev_token in {"ms", "mr", "mrs", "dr"}:
#                     full_name = prev_token + " " + entity_text

#             if should_mask_person(full_name, intent):
#                 detected.setdefault("name", []).append(entity_text)
#                 entities_to_mask.append((entity_text, "[MASKED_NAME]"))
#                 sensitivity_score += 0.3

#         elif ent.label_ == "ORG":
#             detected.setdefault("company", []).append(entity_text)
#             entities_to_mask.append((entity_text, "[MASKED_COMPANY]"))

#         elif ent.label_ in ["GPE", "LOC", "FAC"]:
#             entity_text_lower = entity_text.lower()
#             match_span = (ent.start_char, ent.end_char)
#             if entity_text_lower in PUBLIC_LOCATIONS and is_address_context(text, match_span):
#                 detected.setdefault("address", []).append(entity_text)
#                 entities_to_mask.append((entity_text, "[MASKED_ADDRESS]"))
#                 sensitivity_score += 0.3
#             else:
#                 detected.setdefault("address", []).append(entity_text)
#                 entities_to_mask.append((entity_text, "[MASKED_ADDRESS]"))
#                 sensitivity_score += 0.3

#     # 3️⃣ Regex fallback
#     for label, pattern in EXTRA_PATTERNS.items():
#         for match in re.finditer(pattern, masked_text):
#             value = match.group(0)
#             if label == "phone" and not is_phone_number_context(masked_text, match.span()):
#                 continue
#             detected.setdefault(label, []).append(value)
#             triggered_keywords.setdefault(label, []).append("regex")
#             entities_to_mask.append((value, f"[MASKED_{label.upper()}]"))
#             if label in ["email", "phone", "street_address"]:
#                 sensitivity_score += 0.4

#     # 4️⃣ Contextual patterns
#     SENSITIVE_CONTEXT_PATTERNS = {
#         "emotional": ["apology", "sorry", "regret", "fight", "argue"],
#         "relationship": ["friend", "family", "spouse", "colleague"],
#         "financial": ["money", "loan", "salary", "property"]
#     }
#     for category, words in SENSITIVE_CONTEXT_PATTERNS.items():
#         if any(re.search(rf"\b{re.escape(w)}\b", lower_text) for w in words):
#             private_contexts.append(category)
#             triggered_keywords.setdefault("context", []).append(category)
#             sensitivity_score += 0.2

#     # 5️⃣ Apply masking
#     entities_to_mask = sorted(entities_to_mask, key=lambda x: len(x[0]), reverse=True)
#     for original, mask in entities_to_mask:
#         masked_text = re.sub(re.escape(original), mask, masked_text)

#     # 6️⃣ Sensitivity level
#     if sensitivity_score >= 0.6:
#         sensitivity_level = "High"
#     elif sensitivity_score >= 0.3:
#         sensitivity_level = "Medium"
#     else:
#         sensitivity_level = "Low"

#     detected = {k: sorted(set(v)) for k, v in detected.items()}
#     triggered_keywords = {k: sorted(set(v)) for k, v in triggered_keywords.items()}

#     return {
#         "original_text": text,
#         "masked_text": masked_text,
#         "detected_entities": detected,
#         "triggered_keywords": triggered_keywords,
#         "private_contexts": sorted(set(private_contexts)),
#         "sensitivity_score": round(min(sensitivity_score, 1.0), 2),
#         "sensitivity_level": sensitivity_level,
#         "detected_intents": [intent],
#         "status": "Sensitive personal data masked. Public figures preserved for informational queries. ✅"
#     }

# import re
# import spacy
# import requests
# from functools import lru_cache
# from rapidfuzz import fuzz

# # 🔹 Load spaCy transformer model
# try:
#     nlp = spacy.load("en_core_web_trf")
# except OSError:
#     raise OSError("Please install 'en_core_web_trf': python -m spacy download en_core_web_trf")

# # -------------------------- Regex & Keyword Patterns --------------------------
# EXTRA_PATTERNS = {
#     "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}",
#     "phone": r"\b\d{10}\b",
#     "street_address": r"\d+\s[\w\s]+(?:Street|St|Road|Rd|Avenue|Ave|Lane|Ln|Boulevard|Blvd|Drive|Dr|Square|Sq)\b",
# }

# PHONE_CONTEXT_KEYWORDS = ["call", "mobile", "phone", "contact", "reach", "number"]

# PUBLIC_LOCATIONS = {
#     "new york", "los angeles", "london", "paris", "india", "usa", "canada",
#     "tokyo", "japan", "germany", "australia", "italy", "france", "china",
#     "dubai", "brazil", "singapore", "new delhi", "chicago", "mumbai", "hyderabad"
# }

# COMMON_WORDS = {
#     "i", "you", "he", "she", "it", "we", "they", "my", "your", "his", "her",
#     "our", "their", "and", "the", "for", "in", "on", "at", "with", "to",
#     "from", "by", "a", "an", "of", "that"
# }

# RELATION_PATTERNS = {
#     "relation_pattern": r"\b(?:my|our)?\s*(?:child|son|daughter|kid|friend|brother|sister|wife|husband|mother|father)\s+([A-Z][a-z]+)\b",
#     "inlaw_pattern": r"\b(?:my|our)?\s*(?:in-?law|mother-?in-?law|father-?in-?law|brother-?in-?law|sister-?in-?law|spouse(?:'s)?(?: parent|relative)?|cousin)\s+([A-Z][a-z]+)\b",
# }

# PUBLIC_FIGURE_WHITELIST = {
#     "MS Dhoni", "Sachin Tendulkar", "Lionel Messi", "Cristiano Ronaldo",
#     "Elon Musk", "Narendra Modi", "Oprah Winfrey", "Virat Kohli", "Mike Tyson"
# }

# # -------------------------- Fame Detection --------------------------
# @lru_cache(maxsize=1000)
# def is_public_figure(name: str) -> bool:
#     """
#     Determine whether a name belongs to a public figure using TextRazor as primary
#     and Wikipedia as fallback.
#     """
#     TEXTRAZOR_API_KEY = "37c1da92568a2afc9831fc080250a1e1e645d060c5b2b555b9026aa9"
#     name_clean = name.strip().lower()

#     # Whitelist check
#     for pf in PUBLIC_FIGURE_WHITELIST:
#         if name_clean == pf.lower():
#             return True

#     # TextRazor check
#     try:
#         textrazor_endpoint = "https://api.textrazor.com/"
#         headers = {"x-textrazor-key": TEXTRAZOR_API_KEY}
#         data = {"extractors": "entities", "text": name}

#         response = requests.post(textrazor_endpoint, headers=headers, data=data, timeout=5)
        
#         print(f"\n🔹 [DEBUG] TextRazor API called for: {name}")
#         print(f"🔹 [DEBUG] Status Code: {response.status_code}")
#         try:
#             print(f" 🔹 [DEBUG] Response JSON: {response.json()}\n")
#         except Exception as e:
#             print("⚠️ [DEBUG] Could not parse JSON response: {e}\n")
            
#         if response.status_code == 200:
#             result = response.json()
#             entities = result.get("response", {}).get("entities", [])
#             for entity in entities:
#                 types = entity.get("type", [])
#                 wiki_link = entity.get("wikiLink")
#                 if "Person" in types and wiki_link:
#                     print(f"✅ [DEBUG] Found public figure via TextRazor: {entity.get('entityId', name)}")
#                     return True
#         else:
#             print(f"⚠️ [DEBUG] Non-200 response from TextRazor: {response.text[:300]}")
#     except Exception:
#         print(f"⚠️ [DEBUG] TextRazor check failed for {name}: {e}\n")

#     # Wikipedia fallback
#     candidates = [name.strip(), name.title(), name.upper()]
#     if len(name.split()) == 1:
#         candidates.extend(["MS " + name, "Mahendra Singh " + name])

#     for candidate in candidates:
#         wiki_title = candidate.replace(" ", "_")
#         url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{wiki_title}"
#         try:
#             response = requests.get(url, timeout=3)
#             if response.status_code != 200:
#                 continue
#             data = response.json()
#             if data.get("type") == "disambiguation":
#                 continue
#             desc = data.get("description", "").lower()
#             if any(word in desc for word in [
#                 "actor", "singer", "politician", "cricketer", "footballer",
#                 "entrepreneur", "scientist", "leader", "player", "boxer"
#             ]):
#                 return True
#             page_title = data.get("title", "")
#             if fuzz.ratio(page_title.lower(), candidate.lower()) > 85:
#                 return True
#         except Exception:
#             continue

#     return False

# # -------------------------- Context & Intent --------------------------
# def is_phone_number_context(text, match_span):
#     context_window = 20
#     start, end = match_span
#     left_context = text[max(0, start - context_window):start].lower()
#     right_context = text[end:end + context_window].lower()
#     return any(keyword in left_context or keyword in right_context for keyword in PHONE_CONTEXT_KEYWORDS)

# def is_address_context(text: str, match_span) -> bool:
#     ADDRESS_CONTEXT_KEYWORDS = [
#         "address", "plot", "house", "door no", "street", "lane", "road",
#         "colony", "h.no", "flat", "building", "resides", "lives in", "home", "my address"
#     ]
#     context_window = 40
#     start, end = match_span
#     left_context = text[max(0, start - context_window):start].lower()
#     right_context = text[end:end + context_window].lower()
#     return any(keyword in left_context or keyword in right_context for keyword in ADDRESS_CONTEXT_KEYWORDS)

# def detect_intent(text: str):
#     info_keywords = ["know about", "tell me about", "information about", "who is", "what is", "details about"]
#     text_lower = text.lower()
#     if any(k in text_lower for k in info_keywords):
#         return "general"
#     return "personal"

# # Cached decision for repeated names
# @lru_cache(maxsize=2000)
# def should_mask_person(name: str, intent: str) -> bool:
#     """
#     Determine if a PERSON entity should be masked.
#     Uses caching for faster repeated evaluations.
#     """
#     if intent == "general" and is_public_figure(name):
#         return False
#     return True

# # -------------------------- Main Masking Logic --------------------------
# def mask_sensitive_data(text: str):
#     detected = {}
#     triggered_keywords = {}
#     masked_text = text
#     lower_text = text.lower()
#     entities_to_mask = []
#     sensitivity_score = 0
#     private_contexts = []

#     intent = detect_intent(text)

#     # Relation-based names
#     for keyword, pattern_str in RELATION_PATTERNS.items():
#         for match in re.finditer(pattern_str, text, re.IGNORECASE):
#             possible_name = match.group(1).strip()
#             if possible_name.lower() in COMMON_WORDS:
#                 continue
#             if not should_mask_person(possible_name, intent):
#                 continue
#             detected.setdefault("name", []).append(possible_name)
#             triggered_keywords.setdefault("name", []).append(keyword)
#             entities_to_mask.append((possible_name, "[MASKED_NAME]"))
#             sensitivity_score += 0.3

#     # spaCy NER
#     doc = nlp(text)
#     for ent in doc.ents:
#         entity_text = ent.text.strip()
#         if not entity_text or entity_text.lower() in COMMON_WORDS:
#             continue

#         if ent.label_ == "PERSON":
#             full_name = entity_text
#             start_idx = ent.start
#             if start_idx > 0:
#                 prev_token = doc[start_idx - 1].text.lower()
#                 if prev_token in {"ms", "mr", "mrs", "dr"}:
#                     full_name = prev_token + " " + entity_text

#             if should_mask_person(full_name, intent):
#                 detected.setdefault("name", []).append(entity_text)
#                 entities_to_mask.append((entity_text, "[MASKED_NAME]"))
#                 sensitivity_score += 0.3

#         elif ent.label_ == "ORG":
#             detected.setdefault("company", []).append(entity_text)
#             entities_to_mask.append((entity_text, "[MASKED_COMPANY]"))

#         elif ent.label_ in ["GPE", "LOC", "FAC"]:
#             entity_text_lower = entity_text.lower()
#             match_span = (ent.start_char, ent.end_char)
#             if entity_text_lower in PUBLIC_LOCATIONS and is_address_context(text, match_span):
#                 detected.setdefault("address", []).append(entity_text)
#                 entities_to_mask.append((entity_text, "[MASKED_ADDRESS]"))
#                 sensitivity_score += 0.3
#             else:
#                 detected.setdefault("address", []).append(entity_text)
#                 entities_to_mask.append((entity_text, "[MASKED_ADDRESS]"))
#                 sensitivity_score += 0.3

#     # Regex fallback
#     for label, pattern in EXTRA_PATTERNS.items():
#         for match in re.finditer(pattern, masked_text):
#             value = match.group(0)
#             if label == "phone" and not is_phone_number_context(masked_text, match.span()):
#                 continue
#             detected.setdefault(label, []).append(value)
#             triggered_keywords.setdefault(label, []).append("regex")
#             entities_to_mask.append((value, f"[MASKED_{label.upper()}]"))
#             if label in ["email", "phone", "street_address"]:
#                 sensitivity_score += 0.4

#     # Contextual patterns
#     SENSITIVE_CONTEXT_PATTERNS = {
#         "emotional": ["apology", "sorry", "regret", "fight", "argue"],
#         "relationship": ["friend", "family", "spouse", "colleague"],
#         "financial": ["money", "loan", "salary", "property"]
#     }
#     for category, words in SENSITIVE_CONTEXT_PATTERNS.items():
#         if any(re.search(rf"\b{re.escape(w)}\b", lower_text) for w in words):
#             private_contexts.append(category)
#             triggered_keywords.setdefault("context", []).append(category)
#             sensitivity_score += 0.2

#     # Apply masking
#     entities_to_mask = sorted(entities_to_mask, key=lambda x: len(x[0]), reverse=True)
#     for original, mask in entities_to_mask:
#         masked_text = re.sub(re.escape(original), mask, masked_text)

#     # Sensitivity level
#     if sensitivity_score >= 0.6:
#         sensitivity_level = "High"
#     elif sensitivity_score >= 0.3:
#         sensitivity_level = "Medium"
#     else:
#         sensitivity_level = "Low"

#     detected = {k: sorted(set(v)) for k, v in detected.items()}
#     triggered_keywords = {k: sorted(set(v)) for k, v in triggered_keywords.items()}

#     return {
#         "original_text": text,
#         "masked_text": masked_text,
#         "detected_entities": detected,
#         "triggered_keywords": triggered_keywords,
#         "private_contexts": sorted(set(private_contexts)),
#         "sensitivity_score": round(min(sensitivity_score, 1.0), 2),
#         "sensitivity_level": sensitivity_level,
#         "detected_intents": [intent],
#         "status": "Sensitive personal data masked. Public figures preserved for informational queries. ✅"
#     }

# import re
# import spacy
# import requests
# from functools import lru_cache
# from rapidfuzz import fuzz

# # -------------------------- Load spaCy --------------------------
# try:
#     nlp = spacy.load("en_core_web_trf")
# except OSError:
#     raise OSError("Please install 'en_core_web_trf': python -m spacy download en_core_web_trf")

# # -------------------------- Patterns --------------------------
# EXTRA_PATTERNS = {
#     "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}",
#     "phone": r"\b\d{10}\b",
#     "street_address": r"\d+\s[\w\s]+(?:Street|St|Road|Rd|Avenue|Ave|Lane|Ln|Boulevard|Blvd|Drive|Dr|Square|Sq)\b",
# }

# PHONE_CONTEXT_KEYWORDS = ["call", "mobile", "phone", "contact", "reach", "number"]

# PUBLIC_LOCATIONS = {
#     "new york", "los angeles", "london", "paris", "india", "usa", "canada",
#     "tokyo", "japan", "germany", "australia", "italy", "france", "china",
#     "dubai", "brazil", "singapore", "new delhi", "chicago", "mumbai", "hyderabad"
# }

# COMMON_WORDS = {
#     "i", "you", "he", "she", "it", "we", "they", "my", "your", "his", "her",
#     "our", "their", "and", "the", "for", "in", "on", "at", "with", "to",
#     "from", "by", "a", "an", "of", "that"
# }

# RELATION_PATTERNS = {
#     "relation_pattern": r"\b(?:my|our)?\s*(?:child|son|daughter|kid|friend|brother|sister|wife|husband|mother|father)\s+([A-Z][a-z]+)\b",
#     "inlaw_pattern": r"\b(?:my|our)?\s*(?:in-?law|mother-?in-?law|father-?in-?law|brother-?in-?law|sister-?in-?law|spouse(?:'s)?(?: parent|relative)?|cousin)\s+([A-Z][a-z]+)\b",
# }

# PUBLIC_FIGURE_WHITELIST = {
#     "MS Dhoni", "Sachin Tendulkar", "Lionel Messi", "Cristiano Ronaldo",
#     "Elon Musk", "Narendra Modi", "Oprah Winfrey", "Virat Kohli", "Mike Tyson"
# }

# TEXTRAZOR_API_KEY = "37c1da92568a2afc9831fc080250a1e1e645d060c5b2b555b9026aa9"

# # -------------------------- Fame Detection --------------------------
# @lru_cache(maxsize=1000)
# def is_public_figure(name: str) -> bool:
#     """
#     Determine if a name is a public figure.
#     Uses TextRazor as primary, Wikipedia as fallback.
#     """
#     name_clean = name.strip().lower()

#     # Whitelist check
#     for pf in PUBLIC_FIGURE_WHITELIST:
#         if name_clean == pf.lower():
#             return True

#     # -------------------- TextRazor check (Primary) --------------------
#     try:
#         textrazor_endpoint = "https://api.textrazor.com/"
#         headers = {"x-textrazor-key": TEXTRAZOR_API_KEY}
#         data = {"extractors": "entities", "text": name}

#         response = requests.post(textrazor_endpoint, headers=headers, data=data, timeout=5)
#         if response.status_code == 200:
#             result = response.json()
#             entities = result.get("response", {}).get("entities", [])
#             for entity in entities:
#                 types = entity.get("type", [])
#                 wiki_link = entity.get("wikiLink")
#                 if "Person" in types and wiki_link:
#                     return True
#         else:
#             print(f"⚠️ TextRazor returned non-200: {response.status_code}")
#     except Exception as e:
#         print(f"⚠️ TextRazor check failed: {e}")

#     # -------------------- Wikipedia fallback --------------------
#     candidates = [name.strip(), name.title(), name.upper()]
#     if len(name.split()) == 1:
#         candidates.extend(["MS " + name, "Mahendra Singh " + name])

#     for candidate in candidates:
#         url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{candidate.replace(' ', '_')}"
#         try:
#             response = requests.get(url, timeout=3)
#             if response.status_code != 200:
#                 continue
#             data = response.json()
#             if data.get("type") == "disambiguation":
#                 continue
#             desc = data.get("description", "").lower()
#             if any(word in desc for word in ["actor", "singer", "politician", "cricketer",
#                                              "footballer", "entrepreneur", "scientist",
#                                              "leader", "player", "boxer"]):
#                 return True
#             if fuzz.ratio(data.get("title", "").lower(), candidate.lower()) > 85:
#                 return True
#         except Exception:
#             continue

#     return False

# # -------------------------- Context & Intent --------------------------
# def is_phone_number_context(text, match_span):
#     context_window = 20
#     start, end = match_span
#     left_context = text[max(0, start - context_window):start].lower()
#     right_context = text[end:end + context_window].lower()
#     return any(k in left_context or k in right_context for k in PHONE_CONTEXT_KEYWORDS)

# def is_address_context(text: str, match_span) -> bool:
#     keywords = ["address", "plot", "house", "door no", "street", "lane", "road",
#                 "colony", "h.no", "flat", "building", "resides", "lives in", "home", "my address"]
#     context_window = 40
#     start, end = match_span
#     left_context = text[max(0, start - context_window):start].lower()
#     right_context = text[end:end + context_window].lower()
#     return any(k in left_context or k in right_context for k in keywords)

# def detect_intent(text: str):
#     info_keywords = ["know about", "tell me about", "information about", "who is", "what is", "details about"]
#     return "general" if any(k in text.lower() for k in info_keywords) else "personal"

# @lru_cache(maxsize=2000)
# def should_mask_person(name: str, intent: str) -> bool:
#     if intent == "general" and is_public_figure(name):
#         return False
#     return True

# # -------------------------- Main Masking --------------------------
# def mask_sensitive_data(text: str):
#     detected = {}
#     triggered_keywords = {}
#     masked_text = text
#     lower_text = text.lower()
#     entities_to_mask = []
#     sensitivity_score = 0
#     private_contexts = []

#     intent = detect_intent(text)

#     # Relation-based names
#     for keyword, pattern in RELATION_PATTERNS.items():
#         for match in re.finditer(pattern, text, re.IGNORECASE):
#             name = match.group(1).strip()
#             if name.lower() in COMMON_WORDS or not should_mask_person(name, intent):
#                 continue
#             detected.setdefault("name", []).append(name)
#             triggered_keywords.setdefault("name", []).append(keyword)
#             entities_to_mask.append((name, "[MASKED_NAME]"))
#             sensitivity_score += 0.3

#     # spaCy NER
#     doc = nlp(text)
#     for ent in doc.ents:
#         entity_text = ent.text.strip()
#         if not entity_text or entity_text.lower() in COMMON_WORDS:
#             continue
#         if ent.label_ == "PERSON" and should_mask_person(entity_text, intent):
#             detected.setdefault("name", []).append(entity_text)
#             entities_to_mask.append((entity_text, "[MASKED_NAME]"))
#             sensitivity_score += 0.3
#         elif ent.label_ == "ORG":
#             detected.setdefault("company", []).append(entity_text)
#             entities_to_mask.append((entity_text, "[MASKED_COMPANY]"))
#         elif ent.label_ in ["GPE", "LOC", "FAC"]:
#             detected.setdefault("address", []).append(entity_text)
#             entities_to_mask.append((entity_text, "[MASKED_ADDRESS]"))
#             sensitivity_score += 0.3

#     # Regex patterns
#     for label, pattern in EXTRA_PATTERNS.items():
#         for match in re.finditer(pattern, masked_text):
#             value = match.group(0)
#             if label == "phone" and not is_phone_number_context(masked_text, match.span()):
#                 continue
#             detected.setdefault(label, []).append(value)
#             triggered_keywords.setdefault(label, []).append("regex")
#             entities_to_mask.append((value, f"[MASKED_{label.upper()}]"))
#             if label in ["email", "phone", "street_address"]:
#                 sensitivity_score += 0.4

#     # Sensitive contexts
#     CONTEXT_PATTERNS = {
#         "emotional": ["apology", "sorry", "regret", "fight", "argue"],
#         "relationship": ["friend", "family", "spouse", "colleague"],
#         "financial": ["money", "loan", "salary", "property"]
#     }
#     for category, words in CONTEXT_PATTERNS.items():
#         if any(re.search(rf"\b{re.escape(w)}\b", lower_text) for w in words):
#             private_contexts.append(category)
#             triggered_keywords.setdefault("context", []).append(category)
#             sensitivity_score += 0.2

#     # Non-overlapping masking
#     entities_to_mask = sorted(entities_to_mask, key=lambda x: len(x[0]), reverse=True)
#     for original, mask in entities_to_mask:
#         masked_text = re.sub(re.escape(original), mask, masked_text)

#     # Sensitivity level
#     if sensitivity_score >= 0.6:
#         sensitivity_level = "High"
#     elif sensitivity_score >= 0.3:
#         sensitivity_level = "Medium"
#     else:
#         sensitivity_level = "Low"

#     return {
#         "original_text": text,
#         "masked_text": masked_text,
#         "detected_entities": {k: sorted(set(v)) for k, v in detected.items()},
#         "triggered_keywords": {k: sorted(set(v)) for k, v in triggered_keywords.items()},
#         "private_contexts": sorted(set(private_contexts)),
#         "sensitivity_score": round(min(sensitivity_score, 1.0), 2),
#         "sensitivity_level": sensitivity_level,
#         "detected_intents": [intent],
#         "status": "Sensitive personal data masked. Public figures preserved for informational queries. ✅"
#     }


# import re
# import spacy
# import requests
# from functools import lru_cache
# from rapidfuzz import fuzz

# # -------------------------- Load spaCy --------------------------
# try:
#     nlp = spacy.load("en_core_web_trf")
# except OSError:
#     raise OSError("Please install 'en_core_web_trf': python -m spacy download en_core_web_trf")

# # -------------------------- Patterns --------------------------
# EXTRA_PATTERNS = {
#     "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}",
#     "phone": r"\b\d{10}\b",
#     "street_address": r"\d+\s[\w\s]+(?:Street|St|Road|Rd|Avenue|Ave|Lane|Ln|Boulevard|Blvd|Drive|Dr|Square|Sq)\b",
# }

# # 💰 Financial & ID patterns
# FINANCIAL_PATTERNS = {
#     "aadhaar": r"(?<!\d)(?:\d{4}[-\s]?\d{4}[-\s]?\d{4})(?!\d)",
#     "credit_card": r"(?<!\d)(?:\d[\d\s-]{11,17}\d)(?!\d)",  # 13–19 digits (handles spaces/hyphens)
#     "account": r"(?<!\d)(?:\d{9,18})(?!\d)",                 # 9–18 digits (bank account)
#     "card_last4": r"(?:ending|ends with|last|last 4|last four)\s*(?:digits\s*)?[:\-\s]*([0-9]{4})",
# }

# PHONE_CONTEXT_KEYWORDS = ["call", "mobile", "phone", "contact", "reach", "number"]

# PUBLIC_LOCATIONS = {
#     "new york", "los angeles", "london", "paris", "india", "usa", "canada",
#     "tokyo", "japan", "germany", "australia", "italy", "france", "china",
#     "dubai", "brazil", "singapore", "new delhi", "chicago", "mumbai", "hyderabad"
# }

# COMMON_WORDS = {
#     "i", "you", "he", "she", "it", "we", "they", "my", "your", "his", "her",
#     "our", "their", "and", "the", "for", "in", "on", "at", "with", "to",
#     "from", "by", "a", "an", "of", "that"
# }

# RELATION_PATTERNS = {
#     "relation_pattern": r"\b(?:my|our)?\s*(?:child|son|daughter|kid|friend|brother|sister|wife|husband|mother|father)\s+([A-Z][a-z]+)\b",
#     "inlaw_pattern": r"\b(?:my|our)?\s*(?:in-?law|mother-?in-?law|father-?in-?law|brother-?in-?law|sister-?in-?law|spouse(?:'s)?(?: parent|relative)?|cousin)\s+([A-Z][a-z]+)\b",
# }

# PUBLIC_FIGURE_WHITELIST = {
#     "MS Dhoni", "Sachin Tendulkar", "Lionel Messi", "Cristiano Ronaldo",
#     "Elon Musk", "Narendra Modi", "Oprah Winfrey", "Virat Kohli", "Mike Tyson"
# }

# TEXTRAZOR_API_KEY = "37c1da92568a2afc9831fc080250a1e1e645d060c5b2b555b9026aa9"

# # -------------------------- Fame Detection --------------------------
# @lru_cache(maxsize=1000)
# def is_public_figure(name: str) -> bool:
#     name_clean = name.strip().lower()
#     for pf in PUBLIC_FIGURE_WHITELIST:
#         if name_clean == pf.lower():
#             return True

#     try:
#         textrazor_endpoint = "https://api.textrazor.com/"
#         headers = {"x-textrazor-key": TEXTRAZOR_API_KEY}
#         data = {"extractors": "entities", "text": name}
#         response = requests.post(textrazor_endpoint, headers=headers, data=data, timeout=5)
#         if response.status_code == 200:
#             result = response.json()
#             entities = result.get("response", {}).get("entities", [])
#             for entity in entities:
#                 types = entity.get("type", [])
#                 wiki_link = entity.get("wikiLink")
#                 if "Person" in types and wiki_link:
#                     return True
#     except Exception:
#         pass

#     candidates = [name.strip(), name.title(), name.upper()]
#     if len(name.split()) == 1:
#         candidates.extend(["MS " + name, "Mahendra Singh " + name])
#     for candidate in candidates:
#         url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{candidate.replace(' ', '_')}"
#         try:
#             response = requests.get(url, timeout=3)
#             if response.status_code != 200:
#                 continue
#             data = response.json()
#             if data.get("type") == "disambiguation":
#                 continue
#             desc = data.get("description", "").lower()
#             if any(w in desc for w in ["actor", "singer", "politician", "cricketer",
#                                        "footballer", "entrepreneur", "scientist",
#                                        "leader", "player", "boxer"]):
#                 return True
#             if fuzz.ratio(data.get("title", "").lower(), candidate.lower()) > 85:
#                 return True
#         except Exception:
#             continue
#     return False

# # -------------------------- Helpers --------------------------
# def is_phone_number_context(text, match_span):
#     context_window = 20
#     start, end = match_span
#     left = text[max(0, start - context_window):start].lower()
#     right = text[end:end + context_window].lower()
#     return any(k in left or k in right for k in PHONE_CONTEXT_KEYWORDS)

# def detect_intent(text: str):
#     info_keywords = ["know about", "tell me about", "information about", "who is", "what is", "details about"]
#     return "general" if any(k in text.lower() for k in info_keywords) else "personal"

# @lru_cache(maxsize=2000)
# def should_mask_person(name: str, intent: str) -> bool:
#     if intent == "general" and is_public_figure(name):
#         return False
#     return True

# # -------------------------- Main Masking --------------------------
# def mask_sensitive_data(text: str):
#     detected = {}
#     triggered_keywords = {}
#     masked_text = text
#     lower_text = text.lower()
#     entities_to_mask = []
#     sensitivity_score = 0
#     private_contexts = []

#     intent = detect_intent(text)

#     # ---------- FINANCIAL ID MASKING ----------
#     for label, pattern in FINANCIAL_PATTERNS.items():
#         for match in re.finditer(pattern, masked_text, flags=re.IGNORECASE):
#             value = match.group(0)
#             detected.setdefault(label, []).append(value)
#             triggered_keywords.setdefault(label, []).append("regex")
#             if label == "aadhaar":
#                 entities_to_mask.append((value, "[MASKED_AADHAAR]"))
#             elif label == "credit_card":
#                 entities_to_mask.append((value, "[MASKED_CARD]"))
#             elif label == "account":
#                 entities_to_mask.append((value, "[MASKED_ACCOUNT]"))
#             elif label == "card_last4":
#                 # Handle "ending 9921" → only mask last-4 digits
#                 end_digits = match.group(1)
#                 entities_to_mask.append((end_digits, "[MASKED_CARD_LAST4]"))
#             sensitivity_score += 0.5

#     # ---------- Relation-based names ----------
#     for keyword, pattern in RELATION_PATTERNS.items():
#         for match in re.finditer(pattern, text, re.IGNORECASE):
#             name = match.group(1).strip()
#             if name.lower() in COMMON_WORDS or not should_mask_person(name, intent):
#                 continue
#             detected.setdefault("name", []).append(name)
#             triggered_keywords.setdefault("name", []).append(keyword)
#             entities_to_mask.append((name, "[MASKED_NAME]"))
#             sensitivity_score += 0.3

#     # ---------- spaCy NER ----------
#     doc = nlp(text)
#     for ent in doc.ents:
#         entity_text = ent.text.strip()
#         if not entity_text or entity_text.lower() in COMMON_WORDS:
#             continue
#         if ent.label_ == "PERSON" and should_mask_person(entity_text, intent):
#             detected.setdefault("name", []).append(entity_text)
#             entities_to_mask.append((entity_text, "[MASKED_NAME]"))
#             sensitivity_score += 0.3
#         elif ent.label_ == "ORG":
#             detected.setdefault("company", []).append(entity_text)
#             entities_to_mask.append((entity_text, "[MASKED_COMPANY]"))
#         elif ent.label_ in ["GPE", "LOC", "FAC"]:
#             detected.setdefault("address", []).append(entity_text)
#             entities_to_mask.append((entity_text, "[MASKED_ADDRESS]"))
#             sensitivity_score += 0.3

#     # ---------- Regex patterns (phone/email/address) ----------
#     for label, pattern in EXTRA_PATTERNS.items():
#         for match in re.finditer(pattern, masked_text):
#             value = match.group(0)
#             if label == "phone" and not is_phone_number_context(masked_text, match.span()):
#                 continue
#             detected.setdefault(label, []).append(value)
#             triggered_keywords.setdefault(label, []).append("regex")
#             entities_to_mask.append((value, f"[MASKED_{label.upper()}]"))
#             if label in ["email", "phone", "street_address"]:
#                 sensitivity_score += 0.4

#     # ---------- Sensitive contexts ----------
#     CONTEXT_PATTERNS = {
#         "emotional": ["apology", "sorry", "regret", "fight", "argue"],
#         "relationship": ["friend", "family", "spouse", "colleague"],
#         "financial": ["money", "loan", "salary", "property"]
#     }
#     for category, words in CONTEXT_PATTERNS.items():
#         if any(re.search(rf"\b{re.escape(w)}\b", lower_text) for w in words):
#             private_contexts.append(category)
#             triggered_keywords.setdefault("context", []).append(category)
#             sensitivity_score += 0.2

#     # ---------- Non-overlapping masking ----------
#     entities_to_mask = sorted(entities_to_mask, key=lambda x: len(x[0]), reverse=True)
#     for original, mask in entities_to_mask:
#         masked_text = re.sub(re.escape(original), mask, masked_text)

#     # ---------- Sensitivity level ----------
#     if sensitivity_score >= 0.6:
#         sensitivity_level = "High"
#     elif sensitivity_score >= 0.3:
#         sensitivity_level = "Medium"
#     else:
#         sensitivity_level = "Low"

#     return {
#         "original_text": text,
#         "masked_text": masked_text,
#         "detected_entities": {k: sorted(set(v)) for k, v in detected.items()},
#         "triggered_keywords": {k: sorted(set(v)) for k, v in triggered_keywords.items()},
#         "private_contexts": sorted(set(private_contexts)),
#         "sensitivity_score": round(min(sensitivity_score, 1.0), 2),
#         "sensitivity_level": sensitivity_level,
#         "detected_intents": [intent],
#         "status": "Sensitive personal data masked. Public figures preserved for informational queries. ✅"
#     }

# import re
# import spacy
# import requests
# from functools import lru_cache
# from rapidfuzz import fuzz

# # -------------------------- Load spaCy --------------------------
# try:
#     nlp = spacy.load("en_core_web_trf")
# except OSError:
#     raise OSError("Please install 'en_core_web_trf': python -m spacy download en_core_web_trf")

# # -------------------------- Patterns --------------------------
# EXTRA_PATTERNS = {
#     "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}",
#     "phone": r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b",
#     "upi": r"\b[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}\b",  # e.g. yeshwanth@okicici
#     "street_address": r"\d+\s[\w\s]+(?:Street|St|Road|Rd|Avenue|Ave|Lane|Ln|Boulevard|Blvd|Drive|Dr|Square|Sq)\b",
# }

# # 💰 Financial & ID patterns (context-aware)
# FINANCIAL_PATTERNS = {
#     # Aadhaar: 12-digit with nearby keyword "aadhaar"
#     "aadhaar": r"(?i)(?<=aadhaar(?:\s*number|\s*no|\s*:)?\s*)(\d{4}[-\s]?\d{4}[-\s]?\d{4})",
#     # Bank account number: 9–18 digits with "account" keyword
#     "account": r"(?i)(?<=account(?:\s*number|\s*no|\s*:)?\s*)(\d{9,18})",
#     # Credit card (full)
#     "credit_card": r"(?i)(?<=credit\s*card(?:\s*number|\s*no|\s*:)?\s*)(\d{12,19})",
#     # Last-4 digits pattern
#     "card_last4": r"(?i)(?:ending|ends with|last|last 4|last four)\s*(?:digits\s*)?[:\-\s]*([0-9]{4})",
# }

# PHONE_CONTEXT_KEYWORDS = ["call", "mobile", "phone", "contact", "reach", "number"]

# PUBLIC_LOCATIONS = {
#     "new york", "los angeles", "london", "paris", "india", "usa", "canada",
#     "tokyo", "japan", "germany", "australia", "italy", "france", "china",
#     "dubai", "brazil", "singapore", "new delhi", "chicago", "mumbai", "hyderabad"
# }

# COMMON_WORDS = {
#     "i", "you", "he", "she", "it", "we", "they", "my", "your", "his", "her",
#     "our", "their", "and", "the", "for", "in", "on", "at", "with", "to",
#     "from", "by", "a", "an", "of", "that"
# }

# RELATION_PATTERNS = {
#     "relation_pattern": r"\b(?:my|our)?\s*(?:child|son|daughter|kid|friend|brother|sister|wife|husband|mother|father)\s+([A-Z][a-z]+)\b",
#     "inlaw_pattern": r"\b(?:my|our)?\s*(?:in-?law|mother-?in-?law|father-?in-?law|brother-?in-?law|sister-?in-?law|spouse(?:'s)?(?: parent|relative)?|cousin)\s+([A-Z][a-z]+)\b",
# }

# PUBLIC_FIGURE_WHITELIST = {
#     "MS Dhoni", "Sachin Tendulkar", "Lionel Messi", "Cristiano Ronaldo",
#     "Elon Musk", "Narendra Modi", "Oprah Winfrey", "Virat Kohli", "Mike Tyson"
# }

# TEXTRAZOR_API_KEY = "37c1da92568a2afc9831fc080250a1e1e645d060c5b2b555b9026aa9"

# # -------------------------- Fame Detection --------------------------
# @lru_cache(maxsize=1000)
# def is_public_figure(name: str) -> bool:
#     name_clean = name.strip().lower()
#     for pf in PUBLIC_FIGURE_WHITELIST:
#         if name_clean == pf.lower():
#             return True

#     try:
#         textrazor_endpoint = "https://api.textrazor.com/"
#         headers = {"x-textrazor-key": TEXTRAZOR_API_KEY}
#         data = {"extractors": "entities", "text": name}
#         response = requests.post(textrazor_endpoint, headers=headers, data=data, timeout=5)
#         if response.status_code == 200:
#             result = response.json()
#             entities = result.get("response", {}).get("entities", [])
#             for entity in entities:
#                 types = entity.get("type", [])
#                 wiki_link = entity.get("wikiLink")
#                 if "Person" in types and wiki_link:
#                     return True
#     except Exception:
#         pass

#     candidates = [name.strip(), name.title(), name.upper()]
#     if len(name.split()) == 1:
#         candidates.extend(["MS " + name, "Mahendra Singh " + name])
#     for candidate in candidates:
#         url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{candidate.replace(' ', '_')}"
#         try:
#             response = requests.get(url, timeout=3)
#             if response.status_code != 200:
#                 continue
#             data = response.json()
#             if data.get("type") == "disambiguation":
#                 continue
#             desc = data.get("description", "").lower()
#             if any(w in desc for w in ["actor", "singer", "politician", "cricketer",
#                                        "footballer", "entrepreneur", "scientist",
#                                        "leader", "player", "boxer"]):
#                 return True
#             if fuzz.ratio(data.get("title", "").lower(), candidate.lower()) > 85:
#                 return True
#         except Exception:
#             continue
#     return False

# # -------------------------- Helpers --------------------------
# def is_phone_number_context(text, match_span):
#     context_window = 20
#     start, end = match_span
#     left = text[max(0, start - context_window):start].lower()
#     right = text[end:end + context_window].lower()
#     return any(k in left or k in right for k in PHONE_CONTEXT_KEYWORDS)

# def detect_intent(text: str):
#     info_keywords = ["know about", "tell me about", "information about", "who is", "what is", "details about"]
#     return "general" if any(k in text.lower() for k in info_keywords) else "personal"

# @lru_cache(maxsize=2000)
# def should_mask_person(name: str, intent: str) -> bool:
#     if intent == "general" and is_public_figure(name):
#         return False
#     return True

# # -------------------------- Main Masking --------------------------
# def mask_sensitive_data(text: str):
#     detected = {}
#     triggered_keywords = {}
#     masked_text = text
#     lower_text = text.lower()
#     entities_to_mask = []
#     sensitivity_score = 0
#     private_contexts = []

#     intent = detect_intent(text)

#     # ---------- FINANCIAL ID MASKING ----------
#     for label, pattern in FINANCIAL_PATTERNS.items():
#         for match in re.finditer(pattern, masked_text, flags=re.IGNORECASE):
#             value = match.group(1)
#             detected.setdefault(label, []).append(value)
#             triggered_keywords.setdefault(label, []).append("regex")

#             if label == "aadhaar":
#                 entities_to_mask.append((value, "[MASKED_AADHAAR]"))
#             elif label == "credit_card":
#                 entities_to_mask.append((value, "[MASKED_CARD]"))
#             elif label == "account":
#                 entities_to_mask.append((value, "[MASKED_ACCOUNT_NUMBER]"))
#             elif label == "card_last4":
#                 entities_to_mask.append((value, "[MASKED_CARD_LAST4]"))

#             sensitivity_score += 0.5

#     # ---------- Relation-based names ----------
#     for keyword, pattern in RELATION_PATTERNS.items():
#         for match in re.finditer(pattern, text, re.IGNORECASE):
#             name = match.group(1).strip()
#             if name.lower() in COMMON_WORDS or not should_mask_person(name, intent):
#                 continue
#             detected.setdefault("name", []).append(name)
#             triggered_keywords.setdefault("name", []).append(keyword)
#             entities_to_mask.append((name, "[MASKED_NAME]"))
#             sensitivity_score += 0.3

#     # ---------- spaCy NER ----------
#     doc = nlp(text)
#     for ent in doc.ents:
#         entity_text = ent.text.strip()
#         if not entity_text or entity_text.lower() in COMMON_WORDS:
#             continue
#         if ent.label_ == "PERSON" and should_mask_person(entity_text, intent):
#             detected.setdefault("name", []).append(entity_text)
#             entities_to_mask.append((entity_text, "[MASKED_NAME]"))
#             sensitivity_score += 0.3
#         elif ent.label_ == "ORG":
#             detected.setdefault("company", []).append(entity_text)
#             entities_to_mask.append((entity_text, "[MASKED_COMPANY]"))
#         elif ent.label_ in ["GPE", "LOC", "FAC"]:
#             detected.setdefault("address", []).append(entity_text)
#             entities_to_mask.append((entity_text, "[MASKED_ADDRESS]"))
#             sensitivity_score += 0.3

#     # ---------- Regex patterns (phone/email/upi/address) ----------
#     for label, pattern in EXTRA_PATTERNS.items():
#         for match in re.finditer(pattern, masked_text):
#             value = match.group(0)
#             if label == "phone" and not is_phone_number_context(masked_text, match.span()):
#                 continue
#             detected.setdefault(label, []).append(value)
#             triggered_keywords.setdefault(label, []).append("regex")
#             entities_to_mask.append((value, f"[MASKED_{label.upper()}]"))
#             sensitivity_score += 0.4

#     # ---------- Sensitive contexts ----------
#     CONTEXT_PATTERNS = {
#         "emotional": ["apology", "sorry", "regret", "fight", "argue"],
#         "relationship": ["friend", "family", "spouse", "colleague"],
#         "financial": ["money", "loan", "salary", "property"]
#     }
#     for category, words in CONTEXT_PATTERNS.items():
#         if any(re.search(rf"\b{re.escape(w)}\b", lower_text) for w in words):
#             private_contexts.append(category)
#             triggered_keywords.setdefault("context", []).append(category)
#             sensitivity_score += 0.2

#     # ---------- Non-overlapping masking ----------
#     entities_to_mask = sorted(entities_to_mask, key=lambda x: len(x[0]), reverse=True)
#     for original, mask in entities_to_mask:
#         masked_text = re.sub(re.escape(original), mask, masked_text)

#     # ---------- Sensitivity level ----------
#     if sensitivity_score >= 0.6:
#         sensitivity_level = "High"
#     elif sensitivity_score >= 0.3:
#         sensitivity_level = "Medium"
#     else:
#         sensitivity_level = "Low"

#     return {
#         "original_text": text,
#         "masked_text": masked_text,
#         "detected_entities": {k: sorted(set(v)) for k, v in detected.items()},
#         "triggered_keywords": {k: sorted(set(v)) for k, v in triggered_keywords.items()},
#         "private_contexts": sorted(set(private_contexts)),
#         "sensitivity_score": round(min(sensitivity_score, 1.0), 2),
#         "sensitivity_level": sensitivity_level,
#         "detected_intents": [intent],
#         "status": "Sensitive personal data masked. Public figures preserved for informational queries. ✅"
#     }

# import re
# import spacy
# import requests
# from functools import lru_cache
# from rapidfuzz import fuzz

# # -------------------------- Load spaCy --------------------------
# try:
#     nlp = spacy.load("en_core_web_trf")
# except OSError:
#     raise OSError("Please install 'en_core_web_trf': python -m spacy download en_core_web_trf")

# # -------------------------- Patterns --------------------------
# EXTRA_PATTERNS = {
#     "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}",
#     "phone": r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b",
#     "upi": r"\b[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}\b",
#     "street_address": r"\d+\s[\w\s]+(?:Street|St|Road|Rd|Avenue|Ave|Lane|Ln|Boulevard|Blvd|Drive|Dr|Square|Sq)\b",
# }

# # 💰 Financial & ID patterns (no variable lookbehind)
# FINANCIAL_PATTERNS = {
#     # Aadhaar: 12-digit with or without spaces/hyphens
#     "aadhaar": r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",

#     # Bank account number (9–18 digits) — with preceding keywords like "account", "acc no", etc.
#     "account": r"\b(?:account|a/c|acc(?:ount)?(?:\s*no\.?| number)?)[^\d]{0,5}(\d{9,18})\b",

#     # Credit card (full)
#     "credit_card": r"\b(?:credit\s*card(?:\s*number|\s*no|\s*:)?)[^\d]{0,5}(\d{12,19})\b",

#     # Last-4 digits
#     "card_last4": r"\b(?:ending|ends with|last|last 4|last four)\s*(?:digits\s*)?[:\-\s]*([0-9]{4})\b",
# }

# PHONE_CONTEXT_KEYWORDS = ["call", "mobile", "phone", "contact", "reach", "number"]

# PUBLIC_LOCATIONS = {
#     "new york", "los angeles", "london", "paris", "india", "usa", "canada",
#     "tokyo", "japan", "germany", "australia", "italy", "france", "china",
#     "dubai", "brazil", "singapore", "new delhi", "chicago", "mumbai", "hyderabad"
# }

# COMMON_WORDS = {
#     "i", "you", "he", "she", "it", "we", "they", "my", "your", "his", "her",
#     "our", "their", "and", "the", "for", "in", "on", "at", "with", "to",
#     "from", "by", "a", "an", "of", "that"
# }

# RELATION_PATTERNS = {
#     "relation_pattern": r"\b(?:my|our)?\s*(?:child|son|daughter|kid|friend|brother|sister|wife|husband|mother|father)\s+([A-Z][a-z]+)\b",
#     "inlaw_pattern": r"\b(?:my|our)?\s*(?:in-?law|mother-?in-?law|father-?in-?law|brother-?in-?law|sister-?in-?law|spouse(?:'s)?(?: parent|relative)?|cousin)\s+([A-Z][a-z]+)\b",
# }

# PUBLIC_FIGURE_WHITELIST = {
#     "MS Dhoni", "Sachin Tendulkar", "Lionel Messi", "Cristiano Ronaldo",
#     "Elon Musk", "Narendra Modi", "Oprah Winfrey", "Virat Kohli", "Mike Tyson"
# }

# TEXTRAZOR_API_KEY = "37c1da92568a2afc9831fc080250a1e1e645d060c5b2b555b9026aa9"

# # -------------------------- Fame Detection --------------------------
# @lru_cache(maxsize=1000)
# def is_public_figure(name: str) -> bool:
#     name_clean = name.strip().lower()
#     for pf in PUBLIC_FIGURE_WHITELIST:
#         if name_clean == pf.lower():
#             return True

#     try:
#         textrazor_endpoint = "https://api.textrazor.com/"
#         headers = {"x-textrazor-key": TEXTRAZOR_API_KEY}
#         data = {"extractors": "entities", "text": name}
#         response = requests.post(textrazor_endpoint, headers=headers, data=data, timeout=5)
#         if response.status_code == 200:
#             result = response.json()
#             entities = result.get("response", {}).get("entities", [])
#             for entity in entities:
#                 types = entity.get("type", [])
#                 wiki_link = entity.get("wikiLink")
#                 if "Person" in types and wiki_link:
#                     return True
#     except Exception:
#         pass

#     candidates = [name.strip(), name.title(), name.upper()]
#     if len(name.split()) == 1:
#         candidates.extend(["MS " + name, "Mahendra Singh " + name])
#     for candidate in candidates:
#         url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{candidate.replace(' ', '_')}"
#         try:
#             response = requests.get(url, timeout=3)
#             if response.status_code != 200:
#                 continue
#             data = response.json()
#             if data.get("type") == "disambiguation":
#                 continue
#             desc = data.get("description", "").lower()
#             if any(w in desc for w in ["actor", "singer", "politician", "cricketer",
#                                        "footballer", "entrepreneur", "scientist",
#                                        "leader", "player", "boxer"]):
#                 return True
#             if fuzz.ratio(data.get("title", "").lower(), candidate.lower()) > 85:
#                 return True
#         except Exception:
#             continue
#     return False

# # -------------------------- Helpers --------------------------
# def is_phone_number_context(text, match_span):
#     context_window = 20
#     start, end = match_span
#     left = text[max(0, start - context_window):start].lower()
#     right = text[end:end + context_window].lower()
#     return any(k in left or k in right for k in PHONE_CONTEXT_KEYWORDS)

# def detect_intent(text: str):
#     info_keywords = ["know about", "tell me about", "information about", "who is", "what is", "details about"]
#     return "general" if any(k in text.lower() for k in info_keywords) else "personal"

# @lru_cache(maxsize=2000)
# def should_mask_person(name: str, intent: str) -> bool:
#     if intent == "general" and is_public_figure(name):
#         return False
#     return True

# # -------------------------- Main Masking --------------------------
# def mask_sensitive_data(text: str):
#     detected = {}
#     triggered_keywords = {}
#     masked_text = text
#     lower_text = text.lower()
#     entities_to_mask = []
#     sensitivity_score = 0
#     private_contexts = []

#     intent = detect_intent(text)

#     # ---------- FINANCIAL ID MASKING ----------
#     for label, pattern in FINANCIAL_PATTERNS.items():
#         for match in re.finditer(pattern, masked_text, flags=re.IGNORECASE):
#             if label in ["account", "credit_card", "card_last4"]:
#                 value = match.group(1)
#             else:
#                 value = match.group(0)

#             detected.setdefault(label, []).append(value)
#             triggered_keywords.setdefault(label, []).append("regex")

#             if label == "aadhaar":
#                 entities_to_mask.append((value, "[MASKED_AADHAAR]"))
#             elif label == "credit_card":
#                 entities_to_mask.append((value, "[MASKED_CARD]"))
#             elif label == "account":
#                 entities_to_mask.append((value, "[MASKED_ACCOUNT_NUMBER]"))
#             elif label == "card_last4":
#                 entities_to_mask.append((value, "[MASKED_CARD_LAST4]"))

#             sensitivity_score += 0.5

#     # ---------- Relation-based names ----------
#     for keyword, pattern in RELATION_PATTERNS.items():
#         for match in re.finditer(pattern, text, re.IGNORECASE):
#             name = match.group(1).strip()
#             if name.lower() in COMMON_WORDS or not should_mask_person(name, intent):
#                 continue
#             detected.setdefault("name", []).append(name)
#             triggered_keywords.setdefault("name", []).append(keyword)
#             entities_to_mask.append((name, "[MASKED_NAME]"))
#             sensitivity_score += 0.3

#     # ---------- spaCy NER ----------
#     doc = nlp(text)
#     for ent in doc.ents:
#         entity_text = ent.text.strip()
#         if not entity_text or entity_text.lower() in COMMON_WORDS:
#             continue
#         if ent.label_ == "PERSON" and should_mask_person(entity_text, intent):
#             detected.setdefault("name", []).append(entity_text)
#             entities_to_mask.append((entity_text, "[MASKED_NAME]"))
#             sensitivity_score += 0.3
#         elif ent.label_ == "ORG":
#             detected.setdefault("company", []).append(entity_text)
#             entities_to_mask.append((entity_text, "[MASKED_COMPANY]"))
#         elif ent.label_ in ["GPE", "LOC", "FAC"]:
#             detected.setdefault("address", []).append(entity_text)
#             entities_to_mask.append((entity_text, "[MASKED_ADDRESS]"))
#             sensitivity_score += 0.3

#     # ---------- Regex patterns (phone/email/upi/address) ----------
#     for label, pattern in EXTRA_PATTERNS.items():
#         for match in re.finditer(pattern, masked_text):
#             value = match.group(0)
#             if label == "phone" and not is_phone_number_context(masked_text, match.span()):
#                 continue
#             detected.setdefault(label, []).append(value)
#             triggered_keywords.setdefault(label, []).append("regex")
#             entities_to_mask.append((value, f"[MASKED_{label.upper()}]"))
#             sensitivity_score += 0.4

#     # ---------- Sensitive contexts ----------
#     CONTEXT_PATTERNS = {
#         "emotional": ["apology", "sorry", "regret", "fight", "argue"],
#         "relationship": ["friend", "family", "spouse", "colleague"],
#         "financial": ["money", "loan", "salary", "property"]
#     }
#     for category, words in CONTEXT_PATTERNS.items():
#         if any(re.search(rf"\b{re.escape(w)}\b", lower_text) for w in words):
#             private_contexts.append(category)
#             triggered_keywords.setdefault("context", []).append(category)
#             sensitivity_score += 0.2

#     # ---------- Non-overlapping masking ----------
#     entities_to_mask = sorted(entities_to_mask, key=lambda x: len(x[0]), reverse=True)
#     for original, mask in entities_to_mask:
#         masked_text = re.sub(re.escape(original), mask, masked_text)

#     # ---------- Sensitivity level ----------
#     if sensitivity_score >= 0.6:
#         sensitivity_level = "High"
#     elif sensitivity_score >= 0.3:
#         sensitivity_level = "Medium"
#     else:
#         sensitivity_level = "Low"

#     return {
#         "original_text": text,
#         "masked_text": masked_text,
#         "detected_entities": {k: sorted(set(v)) for k, v in detected.items()},
#         "triggered_keywords": {k: sorted(set(v)) for k, v in triggered_keywords.items()},
#         "private_contexts": sorted(set(private_contexts)),
#         "sensitivity_score": round(min(sensitivity_score, 1.0), 2),
#         "sensitivity_level": sensitivity_level,
#         "detected_intents": [intent],
#         "status": "Sensitive personal data masked. Public figures preserved for informational queries. ✅"
#     }

# import logging
# import re
# import spacy
# import requests
# from functools import lru_cache
# from rapidfuzz import fuzz
# import os
# from dotenv import load_dotenv
# load_dotenv()


# # -------------------------- Load spaCy --------------------------
# try:
#     nlp = spacy.load("en_core_web_trf")
# except OSError:
#     raise OSError("Please install 'en_core_web_trf': python -m spacy download en_core_web_trf")

# # -------------------------- Patterns --------------------------
# EXTRA_PATTERNS = {
#     "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}",
#     "phone": r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b",
#     "upi": r"\b[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}\b",
#     "street_address": r"\d+\s[\w\s]+(?:Street|St|Road|Rd|Avenue|Ave|Lane|Ln|Boulevard|Blvd|Drive|Dr|Square|Sq)\b",
# }

# TEXTRAZOR_API_KEY = "37c1da92568a2afc9831fc080250a1e1e645d060c5b2b555b9026aa9"

# # 💰 Financial & ID patterns (no variable lookbehind)
# FINANCIAL_PATTERNS = {
#     # Aadhaar: 12-digit with or without spaces/hyphens
#     "aadhaar": r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",

#     # Bank account number (9–18 digits) — with preceding keywords like "account", "acc no", etc.
#     "account": r"\b(?:account|a/c|acc(?:ount)?(?:\s*no\.?| number)?)[^\d]{0,5}(\d{9,18})\b",

#     # Credit card (full)
#     "credit_card": r"\b(?:credit\s*card(?:\s*number|\s*no|\s*:)?)[^\d]{0,5}(\d{12,19})\b",

#     # Last-4 digits
#     "card_last4": r"\b(?:ending|ends with|last|last 4|last four)\s*(?:digits\s*)?[:\-\s]*([0-9]{4})\b",
# }

# PHONE_CONTEXT_KEYWORDS = ["call", "mobile", "phone", "contact", "reach", "number"]

# PUBLIC_LOCATIONS = {
#     "new york", "los angeles", "london", "paris", "india", "usa", "canada",
#     "tokyo", "japan", "germany", "australia", "italy", "france", "china",
#     "dubai", "brazil", "singapore", "new delhi", "chicago", "mumbai", "hyderabad"
# }

# COMMON_WORDS = {
#     "i", "you", "he", "she", "it", "we", "they", "my", "your", "his", "her",
#     "our", "their", "and", "the", "for", "in", "on", "at", "with", "to",
#     "from", "by", "a", "an", "of", "that"
# }

# RELATION_PATTERNS = {
#     "relation_pattern": r"\b(?:my|our)?\s*(?:child|son|daughter|kid|friend|brother|sister|wife|husband|mother|father)\s+([A-Z][a-z]+)\b",
#     "inlaw_pattern": r"\b(?:my|our)?\s*(?:in-?law|mother-?in-?law|father-?in-?law|brother-?in-?law|sister-?in-?law|spouse(?:'s)?(?: parent|relative)?|cousin)\s+([A-Z][a-z]+)\b",
# }

# PUBLIC_FIGURE_WHITELIST = {
#     "MS Dhoni", "Sachin Tendulkar", "Lionel Messi", "Cristiano Ronaldo",
#     "Elon Musk", "Narendra Modi", "Oprah Winfrey", "Virat Kohli", "Mike Tyson"
# }

# # TEXTRAZOR_API_KEY = os.getenv("TEXTRAZOR_API_KEY")

# # -------------------------- Fame Detection --------------------------
# @lru_cache(maxsize=1000)
# def is_public_figure(name: str) -> bool:
#     name_clean = name.strip()
    
#     # 1️⃣ Check whitelist first
#     for pf in PUBLIC_FIGURE_WHITELIST:
#         if name_clean.lower() == pf.lower():
#             return True

#     # 2️⃣ Try TextRazor if API key exists
#     if TEXTRAZOR_API_KEY:
#         try:
#             textrazor_endpoint = "https://api.textrazor.com/"
#             headers = {
#                 "x-textrazor-key": TEXTRAZOR_API_KEY,
#                 "Content-Type":"application/x-www-form-urlencoded"   
#             }
#             data = {"extractors": "entities", "text": name_clean}
#             response = requests.post(textrazor_endpoint, headers=headers, data=data, timeout=5)
#             response.raise_for_status()
#             result = response.json()
#             entities = result.get("response", {}).get("entities", [])
#             for entity in entities:
#                 types = entity.get("type", [])
#                 wiki_link = entity.get("wikiLink")
#                 if "Person" in types and wiki_link:
#                     return True
#         except Exception as e:
#             print(f"[TextRazor Error] Could not verify '{name_clean}': {e}")

#     # 3️⃣ Wikipedia fallback
#     candidates = [name_clean.strip(), name_clean.title(), name_clean.upper()]
#     if len(name_clean.split()) == 1:
#         candidates.extend(["MS " + name_clean, "Mahendra Singh " + name_clean])

#     for candidate in candidates:
#         url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{candidate.replace(' ', '_')}"
#         try:
#             response = requests.get(url, timeout=3)
#             if response.status_code != 200:
#                 continue
#             data = response.json()
#             if data.get("type") == "disambiguation":
#                 continue
#             desc = data.get("description", "").lower()
#             if any(w in desc for w in ["actor", "singer", "politician", "cricketer",
#                                        "footballer", "entrepreneur", "scientist",
#                                        "leader", "player", "boxer"]):
#                 return True
#             # Fuzzy match to allow minor spelling differences
#             if fuzz.ratio(data.get("title", "").lower(), candidate.lower()) > 85:
#                 return True
#         except Exception as e:
#             print(f"[Wikipedia Error] Could not verify '{candidate}': {e}")

#     # 4️⃣ Not a public figure
#     return False


# # -------------------------- Helpers --------------------------
# def is_phone_number_context(text, match_span):
#     context_window = 20
#     start, end = match_span
#     left = text[max(0, start - context_window):start].lower()
#     right = text[end:end + context_window].lower()
#     return any(k in left or k in right for k in PHONE_CONTEXT_KEYWORDS)

# def detect_intent(text: str):
#     info_keywords = ["know about", "tell me about", "information about", "who is", "what is", "details about"]
#     return "general" if any(k in text.lower() for k in info_keywords) else "personal"

# @lru_cache(maxsize=2000)
# def should_mask_person(name: str, intent: str) -> bool:
#     if intent == "general" and is_public_figure(name):
#         return False
#     return True

# # # -------------------------- Main Masking --------------------------
# # def mask_sensitive_data(text: str):
# #     detected = {}
# #     triggered_keywords = {}
# #     masked_text = text
# #     lower_text = text.lower()
# #     entities_to_mask = []
# #     sensitivity_score = 0
# #     private_contexts = []

# #     intent = detect_intent(text)

# #     # ---------- FINANCIAL ID MASKING ----------
# #     for label, pattern in FINANCIAL_PATTERNS.items():
# #         for match in re.finditer(pattern, masked_text, flags=re.IGNORECASE):
# #             if label in ["account", "credit_card", "card_last4"]:
# #                 value = match.group(1)
# #             else:
# #                 value = match.group(0)

# #             detected.setdefault(label, []).append(value)
# #             triggered_keywords.setdefault(label, []).append("regex")

# #             if label == "aadhaar":
# #                 entities_to_mask.append((value, "[MASKED_AADHAAR]"))
# #             elif label == "credit_card":
# #                 entities_to_mask.append((value, "[MASKED_CARD]"))
# #             elif label == "account":
# #                 entities_to_mask.append((value, "[MASKED_ACCOUNT_NUMBER]"))
# #             elif label == "card_last4":
# #                 entities_to_mask.append((value, "[MASKED_CARD_LAST4]"))

# #             sensitivity_score += 0.5

# #     # ---------- Relation-based names ----------
# #     for keyword, pattern in RELATION_PATTERNS.items():
# #         for match in re.finditer(pattern, text, re.IGNORECASE):
# #             name = match.group(1).strip()
# #             if name.lower() in COMMON_WORDS or not should_mask_person(name, intent):
# #                 continue
# #             detected.setdefault("name", []).append(name)
# #             triggered_keywords.setdefault("name", []).append(keyword)
# #             entities_to_mask.append((name, "[MASKED_NAME]"))
# #             sensitivity_score += 0.3

# #     # ---------- spaCy NER ----------
# #     doc = nlp(text)
# #     for ent in doc.ents:
# #         entity_text = ent.text.strip()
# #         if not entity_text or entity_text.lower() in COMMON_WORDS:
# #             continue
# #         if ent.label_ == "PERSON" and should_mask_person(entity_text, intent):
# #             detected.setdefault("name", []).append(entity_text)
# #             entities_to_mask.append((entity_text, "[MASKED_NAME]"))
# #             sensitivity_score += 0.3
# #         elif ent.label_ == "ORG":
# #             detected.setdefault("company", []).append(entity_text)
# #             entities_to_mask.append((entity_text, "[MASKED_COMPANY]"))
# #         elif ent.label_ in ["GPE", "LOC", "FAC"]:
# #             detected.setdefault("address", []).append(entity_text)
# #             entities_to_mask.append((entity_text, "[MASKED_ADDRESS]"))
# #             sensitivity_score += 0.3

# #     # ---------- Regex patterns (phone/email/upi/address) ----------
# #     for label, pattern in EXTRA_PATTERNS.items():
# #         for match in re.finditer(pattern, masked_text):
# #             value = match.group(0)
# #             if label == "phone" and not is_phone_number_context(masked_text, match.span()):
# #                 continue
# #             detected.setdefault(label, []).append(value)
# #             triggered_keywords.setdefault(label, []).append("regex")
# #             entities_to_mask.append((value, f"[MASKED_{label.upper()}]"))
# #             sensitivity_score += 0.4

# #     # ---------- Sensitive contexts ----------
# #     CONTEXT_PATTERNS = {
# #         "emotional": ["apology", "sorry", "regret", "fight", "argue"],
# #         "relationship": ["friend", "family", "spouse", "colleague"],
# #         "financial": ["money", "loan", "salary", "property"]
# #     }
# #     for category, words in CONTEXT_PATTERNS.items():
# #         if any(re.search(rf"\b{re.escape(w)}\b", lower_text) for w in words):
# #             private_contexts.append(category)
# #             triggered_keywords.setdefault("context", []).append(category)
# #             sensitivity_score += 0.2

# #     # ---------- Non-overlapping masking ----------
# #     entities_to_mask = sorted(entities_to_mask, key=lambda x: len(x[0]), reverse=True)
# #     for original, mask in entities_to_mask:
# #         masked_text = re.sub(re.escape(original), mask, masked_text)

# #     # ---------- Sensitivity level ----------
# #     if sensitivity_score >= 0.6:
# #         sensitivity_level = "High"
# #     elif sensitivity_score >= 0.3:
# #         sensitivity_level = "Medium"
# #     else:
# #         sensitivity_level = "Low"

# #     return {
# #         "original_text": text,
# #         "masked_text": masked_text,
# #         "detected_entities": {k: sorted(set(v)) for k, v in detected.items()},
# #         "triggered_keywords": {k: sorted(set(v)) for k, v in triggered_keywords.items()},
# #         "private_contexts": sorted(set(private_contexts)),
# #         "sensitivity_score": round(min(sensitivity_score, 1.0), 2),
# #         "sensitivity_level": sensitivity_level,
# #         "detected_intents": [intent],
# #         "status": "Sensitive personal data masked. Public figures preserved for informational queries. ✅"
# #     }

# def mask_sensitive_data(text: str):
#     detected = {}
#     triggered_keywords = {}
#     masked_text = text
#     lower_text = text.lower()
#     entities_to_mask = []
#     sensitivity_score = 0
#     private_contexts = []

#     intent = detect_intent(text)

#     # ---------- FINANCIAL ID MASKING ----------
#     for label, pattern in FINANCIAL_PATTERNS.items():
#         for match in re.finditer(pattern, masked_text, flags=re.IGNORECASE):
#             value = match.group(1) if label in ["account", "credit_card", "card_last4"] else match.group(0)
#             detected.setdefault(label, []).append(value)
#             triggered_keywords.setdefault(label, []).append("regex")
#             mask_map = {
#                 "aadhaar": "[MASKED_AADHAAR]",
#                 "credit_card": "[MASKED_CARD]",
#                 "account": "[MASKED_ACCOUNT_NUMBER]",
#                 "card_last4": "[MASKED_CARD_LAST4]"
#             }
#             if label in mask_map:
#                 entities_to_mask.append((value, mask_map[label]))
#             sensitivity_score += 0.5

#     # ---------- Relation-based names ----------
#     for keyword, pattern in RELATION_PATTERNS.items():
#         for match in re.finditer(pattern, text, re.IGNORECASE):
#             name = match.group(1).strip()
#             if name.lower() in COMMON_WORDS or not should_mask_person(name, intent):
#                 continue
#             detected.setdefault("name", []).append(name)
#             triggered_keywords.setdefault("name", []).append(keyword)
#             entities_to_mask.append((name, "[MASKED_NAME]"))
#             sensitivity_score += 0.3

#     # ---------- spaCy NER ----------
#     doc = nlp(text)
#     for ent in doc.ents:
#         entity_text = ent.text.strip()
#         if not entity_text or entity_text.lower() in COMMON_WORDS:
#             continue

#         # Preserve public figures first
#         if ent.label_ == "PERSON" and not should_mask_person(entity_text, intent):
#             logging.info(f"[Preserved Public Figure] {entity_text}")
#             detected.setdefault("name", []).append(entity_text)
#             continue  # Skip masking

#         if ent.label_ == "PERSON":
#             detected.setdefault("name", []).append(entity_text)
#             entities_to_mask.append((entity_text, "[MASKED_NAME]"))
#             sensitivity_score += 0.3
#         elif ent.label_ == "ORG":
#             detected.setdefault("company", []).append(entity_text)
#             entities_to_mask.append((entity_text, "[MASKED_COMPANY]"))
#         elif ent.label_ in ["GPE", "LOC", "FAC"]:
#             detected.setdefault("address", []).append(entity_text)
#             entities_to_mask.append((entity_text, "[MASKED_ADDRESS]"))
#             sensitivity_score += 0.3

#     # ---------- Regex patterns (phone/email/upi/address) ----------
#     for label, pattern in EXTRA_PATTERNS.items():
#         for match in re.finditer(pattern, masked_text):
#             value = match.group(0)
#             if label == "phone" and not is_phone_number_context(masked_text, match.span()):
#                 continue
#             detected.setdefault(label, []).append(value)
#             triggered_keywords.setdefault(label, []).append("regex")
#             entities_to_mask.append((value, f"[MASKED_{label.upper()}]"))
#             sensitivity_score += 0.4

#     # ---------- Sensitive contexts ----------
#     CONTEXT_PATTERNS = {
#         "emotional": ["apology", "sorry", "regret", "fight", "argue"],
#         "relationship": ["friend", "family", "spouse", "colleague"],
#         "financial": ["money", "loan", "salary", "property"]
#     }
#     for category, words in CONTEXT_PATTERNS.items():
#         if any(re.search(rf"\b{re.escape(w)}\b", lower_text) for w in words):
#             private_contexts.append(category)
#             triggered_keywords.setdefault("context", []).append(category)
#             sensitivity_score += 0.2

#     # ---------- Non-overlapping masking ----------
#     entities_to_mask = sorted(entities_to_mask, key=lambda x: len(x[0]), reverse=True)
#     for original, mask in entities_to_mask:
#         masked_text = re.sub(re.escape(original), mask, masked_text)

#     # ---------- Sensitivity level ----------
#     if sensitivity_score >= 0.6:
#         sensitivity_level = "High"
#     elif sensitivity_score >= 0.3:
#         sensitivity_level = "Medium"
#     else:
#         sensitivity_level = "Low"

#     return {
#         "original_text": text,
#         "masked_text": masked_text,
#         "detected_entities": {k: sorted(set(v)) for k, v in detected.items()},
#         "triggered_keywords": {k: sorted(set(v)) for k, v in triggered_keywords.items()},
#         "private_contexts": sorted(set(private_contexts)),
#         "sensitivity_score": round(min(sensitivity_score, 1.0), 2),
#         "sensitivity_level": sensitivity_level,
#         "detected_intents": [intent],
#         "status": "Sensitive personal data masked. Public figures preserved for informational queries. ✅"
#     }

import logging
import re
import spacy
import requests
from functools import lru_cache
from rapidfuzz import fuzz
import os
from dotenv import load_dotenv
load_dotenv()

# -------------------------- Load spaCy --------------------------
try:
    nlp = spacy.load("en_core_web_trf")
except OSError:
    raise OSError("Please install 'en_core_web_trf': python -m spacy download en_core_web_trf")

# -------------------------- Patterns --------------------------
EXTRA_PATTERNS = {
    "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}",
    "phone": r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b",
    "upi": r"\b[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}\b",
    "street_address": r"\d+\s[\w\s]+(?:Street|St|Road|Rd|Avenue|Ave|Lane|Ln|Boulevard|Blvd|Drive|Dr|Square|Sq)\b",
}

TEXTRAZOR_API_KEY = "37c1da92568a2afc9831fc080250a1e1e645d060c5b2b555b9026aa9"

FINANCIAL_PATTERNS = {
    "aadhaar": r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",
    "account": r"\b(?:account|a/c|acc(?:ount)?(?:\s*no\.?| number)?)[^\d]{0,5}(\d{9,18})\b",
    "credit_card": r"\b(?:credit\s*card(?:\s*number|\s*no|\s*:)?)[^\d]{0,5}(\d{12,19})\b",
    "card_last4": r"\b(?:ending|ends with|last|last 4|last four)\s*(?:digits\s*)?[:\-\s]*([0-9]{4})\b",
}

PHONE_CONTEXT_KEYWORDS = ["call", "mobile", "phone", "contact", "reach", "number"]

PUBLIC_LOCATIONS = {
    "new york", "los angeles", "london", "paris", "india", "usa", "canada",
    "tokyo", "japan", "germany", "australia", "italy", "france", "china",
    "dubai", "brazil", "singapore", "new delhi", "chicago", "mumbai", "hyderabad"
}

COMMON_WORDS = {
    "i", "you", "he", "she", "it", "we", "they", "my", "your", "his", "her",
    "our", "their", "and", "the", "for", "in", "on", "at", "with", "to",
    "from", "by", "a", "an", "of", "that"
}

RELATION_PATTERNS = {
    "relation_pattern": r"\b(?:my|our)?\s*(?:child|son|daughter|kid|friend|brother|sister|wife|husband|mother|father)\s+([A-Z][a-z]+)\b",
    "inlaw_pattern": r"\b(?:my|our)?\s*(?:in-?law|mother-?in-?law|father-?in-?law|brother-?in-?law|sister-?in-?law|spouse(?:'s)?(?: parent|relative)?|cousin)\s+([A-Z][a-z]+)\b",
}

PUBLIC_FIGURE_WHITELIST = {
    "MS Dhoni", "Sachin Tendulkar", "Lionel Messi", "Cristiano Ronaldo",
    "Elon Musk", "Narendra Modi", "Oprah Winfrey", "Virat Kohli", "Mike Tyson"
}

# -------------------------- Fame Detection --------------------------
@lru_cache(maxsize=1000)
def is_public_figure(name: str) -> bool:
    name_clean = name.strip()
    logging.info(f"[Fame Check] Starting fame detection for: '{name_clean}'")

    # 1️⃣ Whitelist check
    for pf in PUBLIC_FIGURE_WHITELIST:
        if name_clean.lower() == pf.lower():
            logging.info(f"[Whitelist] '{name_clean}' found in whitelist as public figure.")
            return True
    logging.info(f"[Whitelist] '{name_clean}' not in whitelist.")

    # 2️⃣ TextRazor API check
    if TEXTRAZOR_API_KEY:
        try:
            headers = {"x-textrazor-key": TEXTRAZOR_API_KEY, "Content-Type": "application/x-www-form-urlencoded"}
            data = {"extractors": "entities", "text": name_clean}
            response = requests.post("https://api.textrazor.com/", headers=headers, data=data, timeout=5)
            response.raise_for_status()

            raw_json = response.json()
            logging.info(f"[TextRazor] Raw response for '{name_clean}': {raw_json}")

            entities = raw_json.get("response", {}).get("entities", [])
            logging.info(f"[TextRazor] Extracted entities: {entities}")

            for entity in entities:
                types = entity.get("type", [])
                wiki_link = entity.get("wikiLink")
                if "Person" in types and wiki_link:
                    logging.info(f"[TextRazor] '{name_clean}' identified as public figure via TextRazor (wikiLink: {wiki_link})")
                    return True
            logging.info(f"[TextRazor] No public figure entity detected for '{name_clean}'")
        except Exception as e:
            logging.warning(f"[TextRazor Error] Could not verify '{name_clean}': {e}")

    # 3️⃣ Wikipedia fallback
    candidates = [name_clean, name_clean.title(), name_clean.upper()]
    if len(name_clean.split()) == 1:
        candidates.extend(["MS " + name_clean, "Mahendra Singh " + name_clean])

    for candidate in candidates:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{candidate.replace(' ', '_')}"
        try:
            response = requests.get(url, timeout=3)
            if response.status_code != 200:
                logging.info(f"[Wikipedia] '{candidate}' page not found (status {response.status_code})")
                continue

            data = response.json()
            title = data.get("title", "")
            desc = data.get("description", "").lower()

            logging.info(f"[Wikipedia] Checking candidate '{candidate}' with description: '{desc}'")

            if any(w in desc for w in ["actor", "singer", "politician", "cricketer",
                                       "footballer", "entrepreneur", "scientist",
                                       "leader", "player", "boxer"]):
                logging.info(f"[Wikipedia] '{candidate}' detected as public figure based on description.")
                return True

            if fuzz.ratio(title.lower(), candidate.lower()) > 85:
                logging.info(f"[Wikipedia] '{candidate}' title similarity {fuzz.ratio(title.lower(), candidate.lower())} suggests public figure.")
                return True
        except Exception as e:
            logging.warning(f"[Wikipedia Error] Could not check '{candidate}': {e}")

    logging.info(f"[Fame Check] '{name_clean}' determined NOT a public figure.")
    return False


# @lru_cache(maxsize=1000)
# def is_public_figure(name: str) -> bool:
#     name_clean = name.strip()
    
#     # 1️⃣ Whitelist
#     for pf in PUBLIC_FIGURE_WHITELIST:
#         if name_clean.lower() == pf.lower():
#             return True

#     # 2️⃣ TextRazor API
#     if TEXTRAZOR_API_KEY:
#         try:
#             headers = {"x-textrazor-key": TEXTRAZOR_API_KEY, "Content-Type": "application/x-www-form-urlencoded"}
#             data = {"extractors": "entities", "text": name_clean}
#             response = requests.post("https://api.textrazor.com/", headers=headers, data=data, timeout=5)
#             response.raise_for_status()
#             entities = response.json().get("response", {}).get("entities", [])
#             for entity in entities:
#                 types = entity.get("type", [])
#                 if "Person" in types and entity.get("wikiLink"):
#                     return True
#         except Exception as e:
#             logging.warning(f"[TextRazor Error] Could not verify '{name_clean}': {e}")

#     # 3️⃣ Wikipedia fallback
#     candidates = [name_clean, name_clean.title(), name_clean.upper()]
#     if len(name_clean.split()) == 1:
#         candidates.extend(["MS " + name_clean, "Mahendra Singh " + name_clean])
#     for candidate in candidates:
#         url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{candidate.replace(' ', '_')}"
#         try:
#             response = requests.get(url, timeout=3)
#             if response.status_code != 200:
#                 continue
#             data = response.json()
#             desc = data.get("description", "").lower()
#             if any(w in desc for w in ["actor", "singer", "politician", "cricketer",
#                                        "footballer", "entrepreneur", "scientist",
#                                        "leader", "player", "boxer"]):
#                 return True
#             if fuzz.ratio(data.get("title", "").lower(), candidate.lower()) > 85:
#                 return True
#         except Exception:
#             continue

#     return False

# -------------------------- Helpers --------------------------
def is_phone_number_context(text, match_span):
    context_window = 20
    start, end = match_span
    left = text[max(0, start - context_window):start].lower()
    right = text[end:end + context_window].lower()
    return any(k in left or k in right for k in PHONE_CONTEXT_KEYWORDS)

def detect_intent(text: str):
    info_keywords = ["know about", "tell me about", "information about", "who is", "what is", "details about"]
    return "general" if any(k in text.lower() for k in info_keywords) else "personal"

@lru_cache(maxsize=2000)
def should_mask_person(name: str, intent: str) -> bool:
    if intent == "general" and is_public_figure(name):
        return False
    return True

# -------------------------- Main Masking --------------------------
def mask_sensitive_data(text: str):
    detected = {}
    triggered_keywords = {}
    masked_text = text
    lower_text = text.lower()
    entities_to_mask = []
    sensitivity_score = 0
    private_contexts = []

    intent = detect_intent(text)

    # ---------- Financial & ID Masking ----------
    for label, pattern in FINANCIAL_PATTERNS.items():
        for match in re.finditer(pattern, masked_text, flags=re.IGNORECASE):
            value = match.group(1) if label in ["account", "credit_card", "card_last4"] else match.group(0)
            detected.setdefault(label, []).append(value)
            triggered_keywords.setdefault(label, []).append("regex")
            mask_map = {
                "aadhaar": "[MASKED_AADHAAR]",
                "credit_card": "[MASKED_CARD]",
                "account": "[MASKED_ACCOUNT_NUMBER]",
                "card_last4": "[MASKED_CARD_LAST4]"
            }
            if label in mask_map:
                entities_to_mask.append((value, mask_map[label]))
            sensitivity_score += 0.5

    # ---------- Relation-based names ----------
    for keyword, pattern in RELATION_PATTERNS.items():
        for match in re.finditer(pattern, text, re.IGNORECASE):
            name = match.group(1).strip()
            if name.lower() in COMMON_WORDS or not should_mask_person(name, intent):
                continue
            detected.setdefault("name", []).append(name)
            triggered_keywords.setdefault("name", []).append(keyword)
            entities_to_mask.append((name, "[MASKED_NAME]"))
            sensitivity_score += 0.3

    # ---------- spaCy NER ----------
    doc = nlp(text)
    for ent in doc.ents:
        entity_text = ent.text.strip()
        if not entity_text or entity_text.lower() in COMMON_WORDS:
            continue

        # Preserve public figures
        if ent.label_ == "PERSON" and not should_mask_person(entity_text, intent):
            logging.info(f"[Preserved Public Figure] {entity_text}")
            detected.setdefault("name", []).append(entity_text)
            continue

        if ent.label_ == "PERSON":
            detected.setdefault("name", []).append(entity_text)
            entities_to_mask.append((entity_text, "[MASKED_NAME]"))
            sensitivity_score += 0.3
        elif ent.label_ == "ORG":
            detected.setdefault("company", []).append(entity_text)
            entities_to_mask.append((entity_text, "[MASKED_COMPANY]"))
        elif ent.label_ in ["GPE", "LOC", "FAC"]:
            detected.setdefault("address", []).append(entity_text)
            entities_to_mask.append((entity_text, "[MASKED_ADDRESS]"))
            sensitivity_score += 0.3

    # ---------- Regex patterns ----------
    for label, pattern in EXTRA_PATTERNS.items():
        for match in re.finditer(pattern, masked_text):
            value = match.group(0)
            if label == "phone" and not is_phone_number_context(masked_text, match.span()):
                continue
            detected.setdefault(label, []).append(value)
            triggered_keywords.setdefault(label, []).append("regex")
            entities_to_mask.append((value, f"[MASKED_{label.upper()}]"))
            sensitivity_score += 0.4

    # ---------- Sensitive contexts ----------
    CONTEXT_PATTERNS = {
        "emotional": ["apology", "sorry", "regret", "fight", "argue"],
        "relationship": ["friend", "family", "spouse", "colleague"],
        "financial": ["money", "loan", "salary", "property"]
    }
    for category, words in CONTEXT_PATTERNS.items():
        if any(re.search(rf"\b{re.escape(w)}\b", lower_text) for w in words):
            private_contexts.append(category)
            triggered_keywords.setdefault("context", []).append(category)
            sensitivity_score += 0.2

    # ---------- Apply masking ----------
    entities_to_mask = sorted(entities_to_mask, key=lambda x: len(x[0]), reverse=True)
    for original, mask in entities_to_mask:
        masked_text = re.sub(re.escape(original), mask, masked_text)

    # ---------- Sensitivity level ----------
    if sensitivity_score >= 0.6:
        sensitivity_level = "High"
    elif sensitivity_score >= 0.3:
        sensitivity_level = "Medium"
    else:
        sensitivity_level = "Low"

    return {
        "original_text": text,
        "masked_text": masked_text,
        "detected_entities": {k: sorted(set(v)) for k, v in detected.items()},
        "triggered_keywords": {k: sorted(set(v)) for k, v in triggered_keywords.items()},
        "private_contexts": sorted(set(private_contexts)),
        "sensitivity_score": round(min(sensitivity_score, 1.0), 2),
        "sensitivity_level": sensitivity_level,
        "detected_intents": [intent],
        "status": "Sensitive personal data masked. Public figures preserved for informational queries. ✅"
    }

