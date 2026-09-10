#!/usr/bin/env bash
# One entry point for every check. Stops at the first failure and prints that check's full output.
#   scripts/run_checks.sh              all suites; a missing dependency (node, Playwright) is a failure
#   scripts/run_checks.sh --no-browser skip the two Playwright suites on purpose (the summary says so)
#   scripts/run_checks.sh --build      rebuild site/data first (build_bundles.py already runs the payload checker)
# Browser suites need a server: set STOCKGAME_URL, or the script serves site/ on a free port itself.
# Playwright: set PLAYWRIGHT_MODULE to a checkout that has it (e.g. another repo's node_modules/playwright) if it is not installed here.
set -uo pipefail
cd "$(dirname "$0")/.."
BROWSER=1; BUILD=0
for a in "$@"; do case "$a" in --no-browser) BROWSER=0;; --build) BUILD=1;; *) echo "unknown flag $a"; exit 2;; esac; done
LOG=$(mktemp); trap 'rm -f "$LOG"; [ -n "${SERVER_PID:-}" ] && kill "$SERVER_PID" 2>/dev/null' EXIT
SERVER_PID=""

run() {   # run "<name>" <command...>: on success print the last output line; on failure print everything and stop
  local name="$1"; shift
  printf '== %s\n' "$name"
  if "$@" >"$LOG" 2>&1; then
    tail -n 1 "$LOG"
  else
    local rc=$?
    printf '\n!! %s FAILED (exit %s). Full output:\n' "$name" "$rc"; cat "$LOG"; exit "$rc"
  fi
}
need() { command -v "$1" >/dev/null 2>&1 || { echo "!! missing dependency: $1"; exit 3; }; }
need python3; need node

if [ "$BUILD" = 1 ]; then run "build_bundles.py" python3 scripts/build_bundles.py; fi
run "verify_cases.py"                    python3 scripts/verify_cases.py
run "merge_dated_debrief.py --check-only" python3 scripts/merge_dated_debrief.py --check-only
run "merge_presentation.py --check-only"  python3 scripts/merge_presentation.py --check-only
run "test_returns.py"                    python3 scripts/test_returns.py
run "test_merge_dated_debrief.py"        python3 scripts/test_merge_dated_debrief.py
run "test_merge_presentation.py"         python3 scripts/test_merge_presentation.py
run "test_simulate.js"                   node scripts/test_simulate.js
run "test_dated_debrief.js"              node scripts/test_dated_debrief.js
run "test_story_dates.js"                node scripts/test_story_dates.js
run "test_payloads.js"                   node scripts/test_payloads.js
run "test_campaign.js"                   node scripts/test_campaign.js

if [ "$BROWSER" = 1 ]; then
  if ! node -e "require(process.env.PLAYWRIGHT_MODULE || 'playwright')" >/dev/null 2>&1; then
    echo "!! Playwright not found: set PLAYWRIGHT_MODULE, install it (npm install --no-save playwright && npx playwright install --with-deps chromium), or pass --no-browser to skip the browser suites on purpose"; exit 3
  fi
  if [ -z "${STOCKGAME_URL:-}" ]; then
    PORT=$(python3 -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1",0)); print(s.getsockname()[1]); s.close()')
    python3 -m http.server "$PORT" --directory site >/dev/null 2>&1 & SERVER_PID=$!
    export STOCKGAME_URL="http://127.0.0.1:$PORT"; sleep 1
  fi
  run "test_story_ui.cjs"        node scripts/test_story_ui.cjs
  run "test_presentation_ui.cjs" node scripts/test_presentation_ui.cjs
  run "test_campaign_ui.cjs"     node scripts/test_campaign_ui.cjs
  printf '\nall checks passed (14 suites, browser suites included)\n'
else
  printf '\nall non-browser checks passed (11 suites; browser suites skipped by --no-browser)\n'
fi
