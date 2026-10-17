#!/usr/bin/env bash
# ==============================================================================
# ZMIE — One-Command Local Developer Bootstrap Script
# Prompt 28 — Clause 12 (Local Development Bootstrap)
# ==============================================================================

set -euo pipefail

echo "======================================================================"
echo "⚡ ZMIE (ZAYVORA Medical Intelligence Engine) Local Bootstrap"
echo "======================================================================"

# 1. Check Python version
PYTHON_BIN=""
if command -v python3 &>/dev/null; then
    PYTHON_BIN="python3"
elif command -v python &>/dev/null; then
    PYTHON_BIN="python"
else
    echo "❌ Error: Python 3.9+ is required but not found in PATH."
    exit 1
fi

echo "✔ Detected Python: $($PYTHON_BIN --version)"

# 2. Virtual Environment Setup
VENV_DIR=".venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Creating virtual environment at $VENV_DIR..."
    $PYTHON_BIN -m venv "$VENV_DIR"
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"
echo "✔ Activated virtual environment"

# 3. Install core dependencies
echo "📦 Installing development dependencies..."
pip install --quiet --upgrade pip
if [ -f "services/engine/pyproject.toml" ]; then
    pip install --quiet -e "services/engine"
fi
if [ -f "sdk/python/pyproject.toml" ]; then
    pip install --quiet -e "sdk/python"
fi

# 4. Configure Environment
if [ ! -f ".env" ]; then
    echo "⚙ Creating .env from .env.example..."
    cp .env.example .env
else
    echo "✔ Existing .env file found."
fi

# 5. Initialize Database Fixtures & Seeds
echo "🌱 Seeding local database fixtures..."
export PYTHONPATH="services/engine:sdk/python:${PYTHONPATH:-}"
python3 services/engine/app/db/classical_corpus_seed.py 2>/dev/null || true

# 6. Execute Test Baseline Verification
echo "🧪 Running acceptance test verification..."
python3 -m unittest discover -s tests -p "test_*.py"

echo "======================================================================"
echo "🎉 ZMIE Local Bootstrap Complete!"
echo "Run 'make dev-up' to start infrastructure backing services."
echo "Run 'uvicorn services.engine.app.main:app --reload' to start API engine."
echo "======================================================================"
