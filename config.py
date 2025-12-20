# Configuration for Web Scraper + LLM System

import os
from typing import Literal

# ============================================================================
# GPU & CUDA Configuration
# ============================================================================

# GPU Settings for RTX 2050
GPU_ENABLED = True
CUDA_DEVICE = 0  # Which GPU to use (0 = first GPU)

# Model quantization (Q4 recommended for RTX 2050)
MODEL_QUANTIZATION = "Q4"  # Options: Q2, Q3, Q4, Q5, Q8

# Max tokens for model
MAX_INPUT_TOKENS = 4000
MAX_OUTPUT_TOKENS = 1024

# ============================================================================
# LLM Model Configuration
# ============================================================================

# Choose LLM backend
LLM_BACKEND = "ollama"  # Options: "ollama", "huggingface"

# Ollama configuration
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral:7b-instruct-q4_0")

# Alternative models for Ollama
OLLAMA_MODELS = {
    "mistral": "mistral:7b-instruct-q4_0",      # Recommended
    "phi3": "phi3:3.8b-mini-4k-instruct-q4_0",  # If memory tight
    "orca2": "orca2:7b-q4",                      # Best reasoning
    "neural-chat": "neural-chat:7b-v3-q4",      # Good general purpose
}

# Hugging Face models
HF_MODELS = {
    "mistral": "mistralai/Mistral-7B-Instruct-v0.2",
    "phi3": "microsoft/phi-3",
    "orca2": "microsoft/orca-2-7b",
}

# LLM generation parameters
LLM_TEMPERATURE = 0.3        # Lower = more deterministic (good for extraction)
LLM_TOP_P = 0.9              # Nucleus sampling
LLM_TOP_K = 40               # Top-K sampling
LLM_TIMEOUT = 120            # Seconds

# ============================================================================
# Web Scraper Configuration
# ============================================================================

# Request headers
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# Scraping timeouts
SCRAPE_TIMEOUT = 10          # Seconds for requests
PLAYWRIGHT_TIMEOUT = 30      # Seconds for Playwright

# Scraping method priority
# "auto" = try static first, then Playwright if needed
# "static" = only requests + BeautifulSoup
# "playwright" = only Playwright
DEFAULT_SCRAPE_METHOD = "auto"

# ============================================================================
# Text Processing Configuration
# ============================================================================

# Chunking parameters
CHUNK_SIZE = 500             # Tokens per chunk
CHUNK_OVERLAP = 50           # Overlap between chunks

# Text cleaning
REMOVE_SCRIPTS_STYLES = True
REMOVE_HTML_COMMENTS = True
MIN_TEXT_LENGTH = 100        # Minimum scraped content length

# ============================================================================
# Database Configuration
# ============================================================================

# SQLite database
DATABASE_PATH = os.getenv("DATABASE_PATH", "companies.db")
DB_BACKUP_ENABLED = True
DB_BACKUP_INTERVAL = 3600   # Seconds (1 hour)

# FAISS Vector Store (optional)
USE_VECTOR_STORE = False     # Set to True to enable semantic search
FAISS_INDEX_PATH = "companies.faiss"
EMBEDDING_DIMENSION = 384    # For MiniLM models

# ============================================================================
# Logging Configuration
# ============================================================================

LOG_LEVEL = "INFO"           # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = "scraper.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# ============================================================================
# API Configuration
# ============================================================================

# API endpoints (if running as service)
API_HOST = "0.0.0.0"
API_PORT = 8000
API_DEBUG = False

# ============================================================================
# Data Processing Rules
# ============================================================================

# Null handling
RETURN_NULL_FOR_MISSING = True  # Return null instead of empty string

# Confidence scoring
MIN_CONFIDENCE = 0.4            # Minimum extraction confidence to save
AUTO_VALIDATE = True            # Validate extracted data

# Field requirements
REQUIRED_FIELDS = ["company_name", "website"]
OPTIONAL_FIELDS = ["industry", "email", "phone", "address", "products"]

# ============================================================================
# Performance Tuning
# ============================================================================

# Batch processing
BATCH_SIZE = 1                  # URLs to process in parallel
BATCH_TIMEOUT = 60             # Timeout per batch (seconds)

# Memory management
MAX_MEMORY_PERCENT = 80         # Stop if memory usage exceeds %
CLEAR_CACHE_INTERVAL = 10       # Clear cache every N extractions

# Connection pooling
REQUESTS_POOL_SIZE = 5
REQUESTS_POOL_TIMEOUT = 30

# ============================================================================
# Extraction Configuration
# ============================================================================

# System prompt (for LLM instructions)
SYSTEM_PROMPT_FILE = None  # Leave None to use default in extractor.py

# Extraction fields
EXTRACT_FIELDS = [
    "company_name",
    "industry",
    "products",
    "email",
    "phone",
    "address",
    "website",
    "description",
]

# ============================================================================
# UI Configuration (Streamlit)
# ============================================================================

STREAMLIT_THEME = "light"       # "light" or "dark"
STREAMLIT_PAGE_TITLE = "Company Info Extractor"
STREAMLIT_LAYOUT = "wide"       # "wide" or "centered"
STREAMLIT_SHOW_SIDEBAR = True

# ============================================================================
# Development/Debug
# ============================================================================

DEBUG_MODE = False
SAVE_INTERMEDIATE_RESULTS = False  # Save scraping output for debugging
SKIP_LLM_EXTRACTION = False        # Skip LLM, just scrape (for testing)

# ============================================================================
# Helper Functions
# ============================================================================

def get_model_by_capability(capability: Literal["fast", "balanced", "quality"]) -> str:
    """Get recommended model based on capability needs"""
    models = {
        "fast": "phi3:3.8b-mini-4k-instruct-q4_0",
        "balanced": "mistral:7b-instruct-q4_0",
        "quality": "orca2:7b-q4"
    }
    return models.get(capability, OLLAMA_MODEL)

def get_memory_config() -> dict:
    """Get memory configuration for current GPU"""
    import torch
    
    try:
        gpu_memory = torch.cuda.get_device_properties(CUDA_DEVICE).total_memory / 1024**3
    except:
        gpu_memory = 2.0  # Default for RTX 2050
    
    return {
        "gpu_memory_gb": gpu_memory,
        "chunk_size": max(256, int(CHUNK_SIZE * (gpu_memory / 4.0))),
        "batch_size": max(1, int(BATCH_SIZE * (gpu_memory / 4.0)))
    }

# ============================================================================

if __name__ == "__main__":
    # Display configuration
    print("=" * 70)
    print("Web Scraper + LLM Configuration")
    print("=" * 70)
    print(f"Backend: {LLM_BACKEND}")
    print(f"Model: {OLLAMA_MODEL}")
    print(f"Temperature: {LLM_TEMPERATURE}")
    print(f"Database: {DATABASE_PATH}")
    print(f"Scrape Method: {DEFAULT_SCRAPE_METHOD}")
    print(f"Chunk Size: {CHUNK_SIZE} tokens")
    print("=" * 70)
