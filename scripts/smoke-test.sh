#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${1:?usage: smoke-test.sh <base-url>}"
TIMEOUT="${SMOKE_TIMEOUT:-30}"

echo "Smoke testing ${BASE_URL}"

curl -fsS --max-time "${TIMEOUT}" "${BASE_URL}/health" | grep -q '"status":"ok"'

ORDER=$(curl -fsS --max-time "${TIMEOUT}" \
  -X POST "${BASE_URL}/orders" \
  -H "Content-Type: application/json" \
  -d '{"sku":"SMOKE-TEST","quantity":1}')
echo "${ORDER}" | grep -q '"status":"pending"'

echo "Smoke tests passed"
