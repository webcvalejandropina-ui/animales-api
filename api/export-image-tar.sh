#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMAGE_NAME="${IMAGE_NAME:-alex-alimales-api}"
TAR_PATH="${TAR_PATH:-${SCRIPT_DIR}/alex-alimales-api.tar}"

cd "${SCRIPT_DIR}"

docker compose build
docker save -o "${TAR_PATH}" "${IMAGE_NAME}"

echo "Imagen Docker exportada en: ${TAR_PATH}"
