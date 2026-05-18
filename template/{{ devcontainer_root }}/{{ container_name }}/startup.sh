#!/bin/bash
set -euo pipefail

sudo EXTRA_ALLOWED_DOMAINS="${EXTRA_ALLOWED_DOMAINS:-}" /usr/local/bin/init-firewall.sh

if [ -n "${GH_TOKEN:-}" ]; then
    gh auth setup-git
else
    echo "Warning: GH_TOKEN is not set — GitHub auth skipped. Run 'gh auth login' to authenticate manually."
fi
