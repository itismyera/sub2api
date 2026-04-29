#!/usr/bin/env bash
# Local image build helper for source-based deployments.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_NAME="${IMAGE_NAME:-sub2api}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
OUTPUT_TAR="${OUTPUT_TAR:-}"

docker build -t "${IMAGE_NAME}:${IMAGE_TAG}" \
    --build-arg GOPROXY=https://goproxy.cn,direct \
    --build-arg GOSUMDB=sum.golang.google.cn \
    -f "${REPO_ROOT}/Dockerfile" \
    "${REPO_ROOT}"

if [[ -n "${OUTPUT_TAR}" ]]; then
    docker save -o "${OUTPUT_TAR}" "${IMAGE_NAME}:${IMAGE_TAG}"
fi
