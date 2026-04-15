#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMAGE_NAME="${IMAGE_NAME:-animales-api}"
TAR_PATH="${TAR_PATH:-${SCRIPT_DIR}/animales-api.tar}"

cd "${SCRIPT_DIR}"

# linux/amd64: compatible con la mayoría de servidores/Unraid (x86_64).
# Si construyes en Mac ARM sin esto, el .tar falla en el servidor con "exec format error".
docker compose build
docker save -o "${TAR_PATH}" "${IMAGE_NAME}"

echo "Imagen Docker exportada en: ${TAR_PATH}"
