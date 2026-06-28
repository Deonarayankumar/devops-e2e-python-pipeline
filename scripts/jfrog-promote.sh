#!/usr/bin/env bash
set -euo pipefail

ARTIFACT=""
VERSION=""
FROM_REPO="docker-local"
TO_REPO="docker-release"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --artifact) ARTIFACT="$2"; shift 2 ;;
    --version) VERSION="$2"; shift 2 ;;
    --from) FROM_REPO="$2"; shift 2 ;;
    --to) TO_REPO="$2"; shift 2 ;;
    *) echo "unknown arg: $1"; exit 1 ;;
  esac
done

[[ -n "${ARTIFACT}" && -n "${VERSION}" ]] || {
  echo "usage: jfrog-promote.sh --artifact NAME --version TAG [--from REPO] [--to REPO]"
  exit 1
}

echo "DRY-RUN promote ${ARTIFACT}:${VERSION} ${FROM_REPO} -> ${TO_REPO}"
echo "In CI, run: jfrog rt docker-promote ${ARTIFACT} ${FROM_REPO} --target-docker-repository=${TO_REPO} --tag=${VERSION}"
