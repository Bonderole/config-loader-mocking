#!/bin/bash
# Подставляет варианты src/service.py, запускает тесты, возвращает оригинал
cd "$(dirname "$0")/.." || exit 1
orig=$(mktemp); cp src/service.py "$orig"
run(){ cp "experiments/$1" src/service.py; echo "== $1"; python -m pytest tests -q 2>&1 | tail -1; }
run m1_no_exists_check.py; run m2_wrong_mode.py; run m3_swallow_json_error.py; run refactor_pathlib.py
cp "$orig" src/service.py; rm -f "$orig"
