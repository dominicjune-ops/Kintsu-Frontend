#!/usr/bin/env bash
set -euo pipefail

RETRIES=3
DELAY=5

echo " Validating Docker status..."

for attempt in $(seq 1 $RETRIES); do
  if docker info >/dev/null 2>&1; then
    echo " Docker daemon is running and accessible"
    exit 0
  else
    echo " Attempt $attempt/$RETRIES: Docker not available"
    sleep $DELAY
  fi
done

echo " Docker validation failed after $RETRIES attempts"
echo "Diagnostics:"
echo " - Is Docker installed? $(command -v docker || echo 'not found')"
echo " - Current user: $(whoami)"
echo " - Groups: $(id -nG 2>/dev/null || echo 'N/A')"
echo " - Docker service status (Linux only): $(systemctl is-active docker 2>/dev/null || echo 'N/A')"
echo " - Docker socket permissions: $(ls -l /var/run/docker.sock 2>/dev/null || echo 'N/A')"

exit 1