#!/bin/sh
cd "$(dirname "$0")" || exit 1
if ! command -v node >/dev/null 2>&1; then
  echo "Install Node.js 22 or newer from https://nodejs.org/ first."
  exit 1
fi
node -e "if(Number(process.versions.node.split('.')[0])<22)process.exit(1)" || { echo "Node.js 22 or newer is required."; exit 1; }
exec node server.mjs
