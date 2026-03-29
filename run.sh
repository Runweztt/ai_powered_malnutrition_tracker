#!/bin/bash

# run.sh
# AI-Powered Malnutrition Tracker — startup script
# Usage: bash run.sh

set -e

echo "============================================"
echo "   AI-Powered Malnutrition Tracker"
echo "============================================"

# 1. Check Python is available
if command -v python3 &> /dev/null; then
  PY=python3
elif command -v python &> /dev/null; then
  PY=python
else
  echo "[ERROR] Python not found. Install Python 3.9+ and try again."
  exit 1
fi

echo "[OK] Python found: $($PY --version)"

# 2. Check .env exists
if [ ! -f ".env" ]; then
  echo ""
  echo "[ERROR] .env file not found."
  echo "  Create a .env file in the project root with the following:"
  echo ""
  echo "    SUPABASE_URL=https://your-project-id.supabase.co"
  echo "    SUPABASE_KEY=your_supabase_publishable_key_here"
  echo "    ANTHROPIC_API_KEY=your_anthropic_api_key_here"
  echo ""
  echo "  Then run this script again."
  exit 1
fi

echo "[OK] .env file found."

# 3. Create virtual environment if missing
if [ ! -d "venv" ]; then
  echo "[SETUP] Creating virtual environment..."
  $PY -m venv venv
fi

# 4. Activate virtual environment (Windows Git Bash / WSL)
echo "[SETUP] Activating virtual environment..."
source venv/Scripts/activate 2>/dev/null || source venv/bin/activate

# 5. Install dependencies
echo "[SETUP] Installing dependencies..."
pip install -r requirements.txt -q

# 6. Check Supabase connection
echo "[CHECK] Testing database connection..."
$PY - <<PYEOF
import sys
try:
    from database.db_connect import get_client
    client = get_client()
    client.table("users").select("id").limit(1).execute()
    print("[OK] Supabase connection successful.")
except Exception as e:
    print(f"[ERROR] Could not connect to Supabase: {e}")
    print("  Check SUPABASE_URL and SUPABASE_KEY in your .env file.")
    sys.exit(1)
PYEOF

# 7. Start the app
echo ""
echo "Starting app..."
echo ""
$PY main.py
