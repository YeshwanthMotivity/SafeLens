# import spacy
# import wikipedia

# # Use transformer model for best NER accuracy
# nlp = spacy.load("en_core_web_trf")

# def is_person_famous(name):
#     """
#     Check if a person is famous using Wikipedia search.
#     Only returns True if Wikipedia summary contains fame indicators.
#     """
#     name = name.strip()
#     fame_indicators = ["actor", "cricketer", "singer", "politician", "chef", "athlete", "footballer"]
#     try:
#         results = wikipedia.search(name, results=5)
#         for res in results:
#             if res.lower() == name.lower():
#                 summary = wikipedia.summary(res, sentences=1).lower()
#                 for word in fame_indicators:
#                     if word in summary:
#                         return True
#                 return False
#         return False
#     except:
#         return False

# def is_entity_famous(name):
#     """
#     Check fame for locations/organizations.
#     If a Wikipedia page exists, consider it famous.
#     """
#     name = name.strip()
#     try:
#         wikipedia.summary(name, sentences=1)
#         return True
#     except:
#         return False

# def check_fame_in_text(text):
#     """
#     Detect people, locations, and organizations in text.
#     Return list of entities with fame status (True/False).
#     """
#     doc = nlp(text)
#     results = []

#     for ent in doc.ents:
#         fame = False
#         if ent.label_ == "PERSON":
#             fame = is_person_famous(ent.text)
#         elif ent.label_ in ["GPE", "LOC", "ORG"]:
#             fame = is_entity_famous(ent.text)

#         results.append({
#             "name": ent.text,
#             "type": ent.label_,
#             "famous": fame
#         })

#     return results

# # Example usage
# text = "Hi i love cricket and my favorite indian cricket player is Rohit Sharama"
# fame_results = check_fame_in_text(text)

# for res in fame_results:
#     print(f"{res['name']} ({res['type']}) → {res['famous']}")

# import requests
# import os

# # ------------------------ Setup ------------------------
# TEXTRAZOR_API_KEY = "37c1da92568a2afc9831fc080250a1e1645d060c5b2b555b9026aa9"
# textrazor_endpoint = "https://api.textrazor.com/"

# # ------------------------ Test Text ------------------------
# test_texts = [
#     "Rohit Sharma is a famous cricketer from India.",
#     "Elon Musk is an entrepreneur.",
#     "I had lunch today."
# ]

# # ------------------------ Function ------------------------
# def check_entities(text):
#     headers = {"x-textrazor-key": TEXTRAZOR_API_KEY}
#     data = {
#         "extractors": "entities",
#         "text": text
#     }
#     try:
#         response = requests.post(textrazor_endpoint, headers=headers, data=data, timeout=10)
#         response.raise_for_status()
#         result = response.json()
#         entities = result.get("response", {}).get("entities", [])
#         if not entities:
#             print(f"No entities found for: {text}")
#         else:
#             print(f"Entities found for: {text}")
#             for ent in entities:
#                 print(f" - {ent.get('entityId')} | {ent.get('type')} | Wiki: {ent.get('wikiLink')}")
#     except Exception as e:
#         print(f"[Error] Could not process '{text}': {e}")

# # ------------------------ Test ------------------------
# for txt in test_texts:
#     check_entities(txt)

# import requests

# # ------------------------ Setup ------------------------
# TEXTRAZOR_API_KEY = "37c1da92568a2afc9831fc080250a1e1645d060c5b2b555b9026aa9"
# TEXTRAZOR_ENDPOINT = "https://api.textrazor.com/"

# # ------------------------ Test Text ------------------------
# test_texts = [
#     "Rohit Sharma is a famous cricketer from India.",
#     "Elon Musk is an entrepreneur.",
#     "I had lunch today."
# ]

# # ------------------------ Function ------------------------
# def check_entities(text):
#     headers = {"x-textrazor-key": TEXTRAZOR_API_KEY}
#     data = {
#         "extractors": "entities",
#         "text": text
#     }
#     try:
#         response = requests.post(TEXTRAZOR_ENDPOINT, headers=headers, data=data, timeout=10)
#         response.raise_for_status()
#         result = response.json()
#         entities = result.get("response", {}).get("entities", [])

#         print(f"\nText: {text}")
#         if not entities:
#             print("No entities found.")
#         else:
#             print("Entities found:")
#             for ent in entities:
#                 name = ent.get("entityId")
#                 types = ", ".join(ent.get("type", []))
#                 wiki = ent.get("wikiLink", "N/A")
#                 print(f" - Name: {name}\n   Type: {types}\n   Wiki: {wiki}\n")
#     except Exception as e:
#         print(f"[Error] Could not process '{text}': {e}")

# # ------------------------ Test ------------------------
# for txt in test_texts:
#     check_entities(txt)

import requests

API_KEY = "37c1da92568a2afc9831fc080250a1e1e645d060c5b2b555b9026aa9"
ENDPOINT = "https://api.textrazor.com/"

text = "Rohit Sharma is a famous cricketer from India."
data = {"extractors": "entities", "text": text}
headers = {
    "x-textrazor-key": API_KEY,
    "Content-Type": "application/x-www-form-urlencoded"
}

response = requests.post(ENDPOINT, headers=headers, data=data, timeout=10)
print(response.status_code)
print(response.text)
