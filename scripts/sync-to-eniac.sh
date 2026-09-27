#!/usr/bin/env bash
#
# Syncs this site to your Penn eniac mirror (~mpig/public_html).
# Run this manually from your Mac, while connected to AirPennNet or the
# Penn VPN, any time after you push changes to GitHub Pages.
#
# Usage:
#   ./scripts/sync-to-eniac.sh          # actually sync
#   ./scripts/sync-to-eniac.sh --dry-run   # preview what would change, no changes made

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

DRY_RUN_FLAG=""
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN_FLAG="--dry-run"
  echo "== DRY RUN — no files will actually be changed on eniac =="
fi

echo "Adding canonical tags..."
python3 scripts/add_canonical.py

echo ""
echo "Syncing to eniac.seas.upenn.edu:~/public_html ..."
rsync -avz --delete $DRY_RUN_FLAG \
  --exclude '.git' \
  --exclude '.github' \
  --exclude '.gitignore' \
  --exclude '.idea' \
  --exclude '.DS_Store' \
  --exclude 'scripts' \
  --exclude 'README.md' \
  --exclude 'CNAME' \
  ./ eniac-mpig:~/public_html/

echo ""
echo "Done. Live at: https://engineering.upenn.edu/~mpig"