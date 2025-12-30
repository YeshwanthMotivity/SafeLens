# SafeLens AI 🔐

**Privacy-Preserving Prompt Assistant with Intelligent PII Masking**

SafeLens is an advanced AI-powered system that automatically detects and masks sensitive personal information (PII) from user prompts before processing them through LLMs. It ensures privacy while providing intelligent, context-aware responses.

![SafeLens Banner](https://img.shields.io/badge/SafeLens-Privacy%20AI-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10+-green?style=flat-square)
![React](https://img.shields.io/badge/React-19.x-blue?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-teal?style=flat-square)

---

## 🌟 Features

### 🛡️ Privacy Protection
- **Named Entity Recognition (NER)**: Detects and masks personal names, addresses, phone numbers, emails, company names, and more
- **Public Figure Detection**: Preserves public figures (celebrities, politicians) using TextRazor + Wikipedia verification
- **Context-Aware Masking**: Only masks private information, not public entities or locations

### 🧠 Intelligent Prompt Processing
- **Intent Detection**: Hybrid ML + Rule-based system identifies user intent (QA, summarization, code, translation, etc.)
- **Prompt Optimization**: Automatically applies optimal prompting techniques (Chain-of-Thought, Few-shot, Zero-shot)
- **Groq Enhancement**: Advanced prompt engineering using Groq's compound model
- **Gemini Integration**: Generates high-quality responses via Google's Gemini 2.5 Flash

### 📷 Image Processing
- **OCR Extraction**: Extracts text from images using EasyOCR
- **Privacy Pipeline**: Same masking and optimization pipeline for image-based inputs

### 🎨 Modern React UI
- **Real-time Analysis**: Instant feedback on prompt processing
- **Markdown Rendering**: Beautiful formatted LLM responses
- **Sensitivity Scoring**: Visual indicators for privacy risk levels

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        SafeLens AI                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐     ┌──────────────┐     ┌──────────────────┐    │
│  │  React   │────▶│   FastAPI    │────▶│   NER Detector   │    │
│  │ Frontend │     │   Backend    │     │  (spaCy + Rules) │    │
│  └──────────┘     └──────────────┘     └──────────────────┘    │
│                           │                     │               │
│                           ▼                     ▼               │
│                   ┌──────────────┐     ┌──────────────────┐    │
│                   │   Prompt     │     │  Public Figure   │    │
│                   │  Optimizer   │     │    Detector      │    │
│                   └──────────────┘     │ (TextRazor/Wiki) │    │
│                           │            └──────────────────┘    │
│                           ▼                                     │
│                   ┌──────────────┐     ┌──────────────────┐    │
│                   │    Groq      │────▶│     Gemini       │    │
│                   │  Enhancer    │     │   (Response)     │    │
│                   └──────────────┘     └──────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📂 Project Structure

```
safelens/
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # API keys (not tracked)
│   ├── routers/
│   │   ├── text_router.py      # Text analysis endpoint
│   │   └── image_router.py     # Image analysis endpoint
│   ├── utils/
│   │   ├── ner_detector.py     # NER + PII masking logic
│   │   ├── prompt_optimizer.py # Intent detection + optimization
│   │   └── ocr_extractor.py    # Image text extraction
│   ├── models/                 # Data models
│   ├── uploads/                # Temporary file storage
│   └── yolov8*.pt              # YOLO models for object detection
│
├── frontend/
│   ├── package.json            # Node.js dependencies
│   ├── src/
│   │   ├── App.js              # Main React component
│   │   ├── App.css             # Styling
│   │   └── index.js            # Entry point
│   └── public/                 # Static assets
│
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Create .env file with your API keys
echo "GEMINI_API_KEY=your_gemini_api_key" > .env
echo "GROQ_API_KEY=your_groq_api_key" >> .env
echo "TEXTRAZOR_API_KEY=your_textrazor_api_key" >> .env

# Run the backend server
uvicorn main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

The application will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 🔌 API Endpoints

### Text Analysis
```http
POST /api/v1/text/analyze
Content-Type: application/json

{
  "text": "Hi, my name is John Doe and I live at 123 Main St."
}
```

**Response:**
```json
{
  "original_text": "Hi, my name is John Doe and I live at 123 Main St.",
  "masked_text": "Hi, my name is [MASKED_NAME] and I live at [MASKED_ADDRESS].",
  "detected_entities": {
    "name": ["John Doe"],
    "address": ["123 Main St"]
  },
  "sensitivity_score": 0.75,
  "sensitivity_level": "High",
  "detected_intents": ["general"],
  "llm_response": "...",
  "status": "Sensitive personal data masked. Public entities preserved. ✅"
}
```

### Image Analysis
```http
POST /api/v1/image/analyze_image
Content-Type: multipart/form-data

file: <image_file>
```

---

## 🔐 Entity Types Detected

| Entity Type | Mask Placeholder | Examples |
|-------------|------------------|----------|
| Personal Names | `[MASKED_NAME]` | John Doe, Sarah Smith |
| Street Addresses | `[MASKED_ADDRESS]` | 123 Main Street, Apt 4B |
| Phone Numbers | `[MASKED_PHONE]` | +1-555-123-4567 |
| Email Addresses | `[MASKED_EMAIL]` | john@example.com |
| Company Names | `[MASKED_COMPANY]` | Acme Corp, StartupXYZ |
| Credit Cards | `[MASKED_CARD]` | 4111-1111-1111-1111 |
| SSN/ID Numbers | `[MASKED_SSN]` | 123-45-6789 |

---

## 🎯 Intent Detection & Techniques

| Intent | Prompting Technique |
|--------|---------------------|
| Proposal | Role-based + Few-shot |
| Summarization | Zero-shot |
| Task Generation | Step-by-step + Few-shot |
| Educational | Chain-of-Thought |
| Translation | Zero-shot |
| Analysis | Chain-of-Thought |
| QA | Zero-shot |
| Code | Zero-shot |

---

## ⚙️ Environment Variables

Create a `.env` file in the `backend/` directory:

```env
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
TEXTRAZOR_API_KEY=your_textrazor_api_key
```

---

## 🛠️ Technologies Used

### Backend
- **FastAPI** - Modern Python web framework
- **spaCy** - NLP and Named Entity Recognition
- **Transformers** - DistilBERT for ML-based intent classification
- **Google Gemini** - LLM for response generation
- **Groq** - Advanced prompt engineering
- **TextRazor** - Entity recognition and public figure detection
- **EasyOCR** - Optical Character Recognition
- **YOLOv8** - Object detection in images

### Frontend
- **React 19** - UI framework
- **Axios** - HTTP client
- **React Markdown** - Markdown rendering

---

## 📊 Processing Pipeline

1. **Input Received** → User submits text or image
2. **OCR (images only)** → Extract text from image
3. **NER Detection** → Identify entities (names, addresses, etc.)
4. **Public Figure Check** → Verify if names are public figures
5. **PII Masking** → Replace private data with placeholders
6. **Intent Detection** → Determine user's goal
7. **Prompt Optimization** → Select best prompting technique
8. **Groq Enhancement** → Refine prompt using AI
9. **Gemini Generation** → Generate final response
10. **Response Delivery** → Return masked + processed output

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Yeshwanth**

---

## 🙏 Acknowledgments

- Google Gemini for LLM capabilities
- Groq for prompt optimization
- spaCy for NER
- TextRazor for entity recognition
