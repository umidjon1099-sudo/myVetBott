#!/usr/bin/env bash
# Deploy script: git pull, build, up, then show status and logs with timestamps.
# Usage: ./scripts/deploy.sh   or   bash scripts/deploy.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_DIR"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

log "=== Deploy started ==="
log "Project dir: $PROJECT_DIR"

log "--- git pull origin main ---"
git pull origin main

log "--- docker compose up -d --build ---"
docker compose up -d --build

log "--- docker compose ps ---"
docker compose ps

log "--- waiting 5s before fetching logs ---"
sleep 5

log "--- docker compose logs bot --tail=50 ---"
docker compose logs bot --tail=50

log "=== Deploy finished ==="
