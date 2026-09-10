#!/usr/bin/env bash
# One entry point for every check. Stops at the first failure.
#   scripts/run_checks.sh              all suites, browser suites included when Playwright is available
#   scripts/run_checks.sh --no-browser skip the two Playwright suites
#   scripts/run_checks.sh --build      rebuild site/data first (build_bundles.py already runs the payload checker)
# Browser suites need a server: set STOCKGAME_URL, or the script serves site/ on a free port itself.
# Playwright: set PLAYWRIGHT_MODULE to a checkout that has it (e.g. another repo's node_modules/playwright) if it is not installed here.
set -euo pipefail
cd "$(dirname "$0")/.."
BROWSER=1; BUILD=0
for a in "$@"; do case "$a" in --no-browser) BROWSER=0;; --build) BUILD=1;; *) echo "unknown flag $a"; exit 2;; esac; done
step() { printf '\n== %s\n' "$1"; }

if [ "$BUILD" = 1 ]; then step "build_bundles.py"; python3 scripts/build_bundles.py | tail -1; fi
step "verify_cases.py";              python3 scripts/verify_cases.py | tail -1
step "merge_dated_debrief.py --check-only"; python3 scripts/merge_dated_debrief.py --check-only | head -1
step "merge_presentation.py --check-only";  python3 scripts/merge_presentation.py --check-only | head -1
step "test_returns.py";              python3 scripts/test_returns.py | tail -1
step "test_merge_dated_debrief.py";  python3 scripts/test_merge_dated_debrief.py 2>&1 | tail -1
step "test_merge_presentation.py";   python3 scripts/test_merge_presentation.py 2>&1 | tail -1
step "test_simulate.js";             node scripts/test_simulate.js | tail -1
step "test_dated_debrief.js";        node scripts/test_dated_debrief.js | tail -1
step "test_story_dates.js";          node scripts/test_story_dates.js | tail -1
step "test_payloads.js";             node scripts/test_payloads.js | tail -1

if [ "$BROWSER" = 1 ]; then
  if ! node -e "require(process.env.PLAYWRIGHT_MODULE || 'playwright')" 2>/dev/null; then
    step "browser suites SKIPPED: Playwright not found (set PLAYWRIGHT_MODULE or install it)"
  else
    SERVER_PID=""
    if [ -z "${STOCKGAME_URL:-}" ]; then
      PORT=$(python3 -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1",0)); print(s.getsockname()[1]); s.close()')
      python3 -m http.server "$PORT" --directory site >/dev/null 2>&1 & SERVER_PID=$!
      export STOCKGAME_URL="http://127.0.0.1:$PORT"; sleep 1
      trap '[ -n "$SERVER_PID" ] && kill "$SERVER_PID" 2>/dev/null' EXIT
    fi
    step "test_story_ui.cjs";        node scripts/test_story_ui.cjs | tail -1
    step "test_presentation_ui.cjs"; node scripts/test_presentation_ui.cjs | tail -1
  fi
fi
printf '\nall checks passed\n'
