#!/bin/bash

# run.sh
# AI-Powered Malnutrition Tracker — startup script
# Run this from the project root: bash run.sh

set -e


echo "   AI-Powered Malnutrition Tracker"


# ── 1. Check Python is available ──────────────────
if ! command -v python &> /dev/null; then
  echo "[ERROR] Python not found. Install Python 3.9+ and try again."
  exit 1
fi

PYTHON_VERSION=$(python -c "import sys; print(sys.version_info.minor)")
if [ "$PYTHON_VERSION" -lt 9 ]; then
  echo "[ERROR] Python 3.9 or higher is required."
  exit 1
fi

echo "[OK] Python found: $(python --version)"

# ── 2. Check .env exists ──────────────────────────
if [ ! -f ".env" ]; then
  echo ""
  echo "[WARNING] .env file not found."
  echo "  Copying .env.example to .env ..."
  cp .env.example .env
  echo "  Please edit .env and fill in your DB credentials and API key."
  echo "  Then run this script again."
  exit 1
fi

echo "[OK] .env file found."

# ── 3. Create virtual environment if missing ──────
if [ ! -d "venv" ]; then
  echo "[SETUP] Creating virtual environment..."
  python -m venv venv
fi

# ── 4. Activate virtual environment ───────────────
echo "[SETUP] Activating virtual environment..."
source venv/Scripts/activate

# ── 5. Install dependencies ───────────────────────
echo "[SETUP] Installing dependencies..."
pip install -r requirements.txt -q

# ── 6. Check MySQL is reachable ───────────────────
echo "[CHECK] Testing database connection..."
python - <<EOF
import sys
try:
    from database.db_connect import get_connection
    conn = get_connection()
    conn.close()
    print("[OK] Database connection successful.")
except Exception as e:
    print(f"[ERROR] Could not connect to database: {e}")
    print("  Check your DB_HOST, DB_USER, DB_PASS, DB_NAME in .env")
    sys.exit(1)
EOF

# ── 7. Run the app ────────────────────────────────
echo ""
echo "Starting app..."
echo ""
python main.py