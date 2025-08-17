#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PROJECT_ROOT="${SCRIPT_DIR}/.."
cd "$PROJECT_ROOT"

export PYTHONUNBUFFERED=1

if [ -f ".env" ]; then
	set +a
	set -a
	. ./.env || true
	set +a
fi

command -v python3 >/dev/null 2>&1 && PY=python3 || PY=python
$PY -c "import sys;print(sys.version)" | sed 's/.*/[python] &/'

$PY -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload