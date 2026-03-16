#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
uvicorn nova_coldchain_guardian.main:app --reload --app-dir src
