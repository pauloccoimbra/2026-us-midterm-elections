#!/usr/bin/env bash
# Collect from the AP and publish to GitHub Pages every 60 s (run on your computer on election night).
# Usage: export AP_API_KEY=...; bash publish_loop.sh
set -u
cd "$(dirname "$0")"
while true; do
  python3 ap_collector.py --once && \
  git add data/results.json && \
  git commit -m "data $(date -u +%H:%M:%SZ)" -q && git push -q || true
  sleep 60
done
