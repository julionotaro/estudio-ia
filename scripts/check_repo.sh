#!/bin/bash
set -e

echo "Revisando estructura mínima..."

test -f README.md
test -f CHANGELOG.md
test -f .gitignore
test -f templates/arc/arc-master.md
test -f docs/decisiones_plataforma.md
test -f docs/estado_validacion_dify.md

test -d prompts/design-phase
test -d prompts/builder-phase
test -d dify
test -d n8n
test -d infra

echo "Estructura mínima OK"

echo "Buscando archivos .env prohibidos..."
if find . -name ".env" -o -name ".env.local" | grep -q .; then
  echo "ERROR: hay archivos .env en el repo"
  exit 1
fi

echo "Sin .env detectados"
