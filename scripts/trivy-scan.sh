#!/usr/bin/env bash
set -euo pipefail

IMAGE="${1:?usage: trivy-scan.sh <image>}"
SEVERITY="${TRIVY_SEVERITY:-HIGH,CRITICAL}"
REPORT_DIR="${REPORT_DIR:-reports}"

mkdir -p "${REPORT_DIR}"
echo "Scanning ${IMAGE} (severity >= ${SEVERITY})"

trivy image \
  --severity "${SEVERITY}" \
  --exit-code 1 \
  --format json \
  --output "${REPORT_DIR}/trivy-$(echo "${IMAGE}" | tr '/:' '_').json" \
  "${IMAGE}"

echo "Trivy scan passed"
