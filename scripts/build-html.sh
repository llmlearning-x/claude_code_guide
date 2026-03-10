#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="${SCRIPT_DIR}/.."

cd "${ROOT_DIR}/site"

if [ ! -d "node_modules" ]; then
  npm install
fi

npm run docs:build

# 复制构建产物到 build/html 以保持兼容性
rm -rf "${ROOT_DIR}/build/html"
mkdir -p "${ROOT_DIR}/build/html"
cp -r dist/* "${ROOT_DIR}/build/html/"

echo "HTML build finished at ${ROOT_DIR}/build/html"

