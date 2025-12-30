# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from routers import text_router
# import logging

# app = FastAPI(
#     title="SafeLens AI API",
#     description="Privacy-Preserving Input Processing System for Text, Images, and Voice",
#     version="1.0.0",
# )

# # ---------------------- CORS ----------------------
# origins = [
#     "http://localhost:3000",
#     "http://127.0.0.1:3000",
# ]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ---------------------- Routers ----------------------
# # Mount the text_router at /api/v1/text so React frontend matches
# app.include_router(text_router.router, prefix="/api/v1/text", tags=["Text Processing"])

# @app.get("/")
# def root():
#     return {"message": "Welcome to SafeLens AI API 🚀"}

# import logging
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from routers import text_router # Assuming 'routers/text_router.py' exists

# # --- 1. LOGGING CONFIGURATION ---
# # Configure the root logger
# logging.basicConfig(
#     level=logging.INFO,
#     format="🧩 [%(levelname)s] → %(message)s"
# )

# # Suppress noisy external libraries and set Uvicorn to INFO level
# logging.getLogger("uvicorn.access").setLevel(logging.INFO)
# logging.getLogger("uvicorn.error").setLevel(logging.INFO)
# logging.getLogger("spacy").setLevel(logging.WARNING)


# # --- 2. FASTAPI APPLICATION SETUP ---
# app = FastAPI(
#     title="SafeLens AI API",
#     description="Privacy-Preserving Input Processing System for Text, Images, and Voice",
#     version="1.0.0",
# )


# # --- 3. CORS MIDDLEWARE ---
# # Define allowed origins for the frontend
# origins = [
#     "http://localhost:3000",
#     "http://127.0.0.1:3000",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"], # Allow all methods (GET, POST, etc.)
#     allow_headers=["*"], # Allow all headers
# )


# # --- 4. ROUTER INCLUSION ---
# # Mount the text_router at /api/v1/text
# app.include_router(
#     text_router.router, 
#     prefix="/api/v1/text", 
#     tags=["Text Processing"]
# )


# # --- 5. ROOT ENDPOINT ---
# @app.get("/", summary="Root Health Check")
# def root():
#     """Returns a simple welcome message for API health check."""
#     return {"message": "Welcome to SafeLens AI API 🚀"}


import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import text_router, image_router  # ✅ Include both routers

# --- 1. LOGGING CONFIGURATION ---
logging.basicConfig(
    level=logging.INFO,
    format="🧩 [%(levelname)s] → %(message)s"
)

# Reduce noise
logging.getLogger("uvicorn.access").setLevel(logging.INFO)
logging.getLogger("uvicorn.error").setLevel(logging.INFO)
logging.getLogger("spacy").setLevel(logging.WARNING)


# --- 2. FASTAPI APP SETUP ---
app = FastAPI(
    title="SafeLens AI API",
    description="Privacy-Preserving Input Processing System for Text, Images, and Voice",
    version="1.0.0",
)


# --- 3. CORS CONFIG ---
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- 4. ROUTER INCLUSION ---
# Mount both routers
app.include_router(
    text_router.router,
    prefix="/api/v1/text",
    tags=["Text Processing"]
)

app.include_router(
    image_router.router,
    prefix="/api/v1/image",
    tags=["Image Processing"]
)


# --- 5. ROOT ENDPOINT ---
@app.get("/", summary="Root Health Check")
def root():
    """Returns a simple welcome message for API health check."""
    return {"message": "Welcome to SafeLens AI API 🚀"}
