"""MIT License"""

"""Copyright (c) 2026 [TeamJapanese](https://github.com/TeamJapanese)"""

"""Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:"""

"""The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software."""

"""THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

import os
from typing import Optional


# -------------------------
# Helper to read env vars
# -------------------------
def _env(key: str, default: Optional[str] = None, required: bool = False) -> Optional[str]:
    val = os.getenv(key, default)
    if required and (val is None or val.strip() == ""):
        raise RuntimeError(f"Missing required environment variable: {key}")
    return val


# -------------------------
# Telegram credentials (required)
# -------------------------
API_ID = int(_env("API_ID", required=True))
API_HASH = _env("API_HASH", required=True)
BOT_TOKEN = _env("BOT_TOKEN", required=True)
MONGO_URL = _env("MONGO_URL", required=True)

# -------------------------
# GROQ AI SETTINGS (FREE)
# -------------------------
GROQ_API_KEY = _env("GROQ_API_KEY", required=True)

# Groq API endpoint
AI_URL = "https://api.groq.com/openai/v1/chat/completions"

# Best free model for chatbot
AI_MODEL = _env("AI_MODEL", "llama-3.3-70b-versatile")

# Request config
AI_MAX_TOKENS = int(_env("AI_MAX_TOKENS", 200))
AI_TIMEOUT = int(_env("AI_TIMEOUT", 30))  # HTTP timeout


# -------------------------
# Bot behavior
# -------------------------
TYPING_DELAY_SECONDS = float(_env("TYPING_DELAY_SECONDS", 1.0))
MAX_INPUT_LENGTH = int(_env("MAX_INPUT_LENGTH", 2000))


# -------------------------
# Language + Features
# -------------------------
ENABLE_HINGLISH_DETECTION = _env("ENABLE_HINGLISH_DETECTION", "true").lower() in ("1", "true", "yes")
ENABLE_MEMORY = _env("ENABLE_MEMORY", "false").lower() in ("1", "true", "yes")


# -------------------------
# Logging & Debugging
# -------------------------
LOG_LEVEL = _env("LOG_LEVEL", "INFO")
ENABLE_DEBUG = _env("ENABLE_DEBUG", "false").lower() in ("1", "true", "yes")


# -------------------------
# Render Ping URL (for keepalive)
# -------------------------
PING_URL = _env("PING_URL", "https://your-render-url.onrender.com")


# -------------------------
# Misc
# -------------------------
ENV = _env("ENV", "production")
PROJECT_NAME = _env("PROJECT_NAME", "JapaneseXChatbot")


# -------------------------
# Debug Preview
# -------------------------
if ENABLE_DEBUG:
    print("⚙️ Loaded Config:")
    print(f"API_ID OK: {bool(API_ID)}")
    print(f"GROQ MODEL: {AI_MODEL}")
    print(f"PING_URL: {PING_URL}")
    print(f"HINGLISH DETECTION: {ENABLE_HINGLISH_DETECTION}")
