import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL      = os.getenv("SUPABASE_URL")
SUPABASE_KEY      = os.getenv("SUPABASE_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL   = "claude-sonnet-4-20250514"

if not ANTHROPIC_API_KEY:
    print("[WARNING] ANTHROPIC_API_KEY not set — offline fallback plan will be used.")