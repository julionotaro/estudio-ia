from pathlib import Path

def write(path, content):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content.strip() + "\n", encoding="utf-8")

def touch(path):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.touch()

dirs = [
    ".github/workflows",
    "docs",
    "infra/hostinger",
    "infra/docker",
    "infra/env-examples",
    "scripts",
    "templates/arc",
    "templates/project-brief",
    "templates/automatizacion_oficina",
    "n8n/docs",
    "dify/apps",
    "dify/exports",
    "dify/prototypes",
    "prompts/design-phase",
    "prompts/builder-phase",
    "prompts/support-phase",
    "prompts/operations-phase",
    "projects",
]

for d in dirs:
    Path(d).mkdir(parents=True, exist_ok=True)

for f in [
    "dify/apps/.gitkeep",
    "dify/exports/.gitkeep",
    "dify/prototypes/.gitkeep",
    "n8n/workflows/.gitkeep",
    "n8n/docs/.gitkeep",
    "projects/.gitkeep",
    "prompts/design-phase/.gitkeep",
    "prompts/builder-phase/.gitkeep",
    "prompts/support-phase/.gitkeep",
    "prompts/operations-phase/.gitkeep",
    "templates/automatizacion_oficina/.gitkeep",
    "infra/docker/.gitkeep",
]:
    touch(f)

write("README.md", """
# Estudio de Desarrollo IA v0.4.1

Repositorio central del Estudio IA para diseñar, construir y automatizar sistemas, apps, webs y procesos.

## Dirección estratégica

El estudio se valida primero en Dify Cloud y luego se migrará a una instalación self-hosted en Hostinger VPS.

Arquitectura prevista:

- Dify: cerebro conversacional y equipos de agentes.
- n8n: automatización, triggers, webhooks y conexión entre sistemas.
- GitHub: fuente de verdad para prompts, DSL/YAML, documentación, scripts y código.
- Supabase: base de datos por proyecto cuando aplique.
- Vercel: deploy frontend por proyecto cuando aplique.
- Hostinger VPS KVM 2: servidor previsto para alojar Dify + n8n.

## Estado actual

- Equipo de Diseño validado como prototipo en Dify Cloud.
- Equipo Constructor validado como prototipo en Dify Cloud.
- Prompts actuales en Dify son temporales de prueba.
- Los prompts definitivos deben vivir versionados en este repositorio.

## Estructura

- /prompts: system prompts de agentes por fase.
- /dify: apps y exportaciones DSL/YAML de Dify.
- /n8n: workflows futuros de automatización.
- /templates: ARC, briefs y plantillas reutilizables.
- /docs: decisiones y documentación operativa.
- /infra: preparación futura de Hostinger/Docker.
- /projects: documentación por proyecto.
- /scripts: scripts auxiliares.

## Regla de seguridad

Nunca subir .env, API keys, tokens, contraseñas, secretos ni credenciales reales.
""")

write("CHANGELOG.md", """
# Changelog

## v0.4.1 — Actual

- Inicialización del repositorio del Estudio IA.
- Separación de prompts por fase.
- Preparación para exportar/importar apps Dify como DSL/YAML.
- Preparación para migración futura a Hostinger VPS.
- Estructura inicial para n8n self-hosted.
- ARC obligatorio como plantilla base.
""")

write(".gitignore", """
.env
.env.*
!.env.example

*.log
logs/

node_modules/
dist/
build/

__pycache__/
.pytest_cache/
.venv/
venv/

.DS_Store
Thumbs.db

.vscode/settings.json
.idea/

tmp/
temp/
""")

write("templates/arc/arc-master.md", """
# Architecture Review Checklist (ARC) — Master

Completar para cada proyecto antes de aprobar arquitectura.

## GRUPO A — Siempre requerido

- A1. Cost Controls
- A2. Seguridad básica
- A3. Manejo de errores
- A4. Observabilidad mínima
- A5. Checkpoints humanos

## GRUPO B — Evaluar para este proyecto

- B1. Filtro de Código Rígido
- B2. Circuit Breakers
- B3. State Persistence
- B4. Audit Trail
- B5. Escalabilidad
- B6. Multi-usuario
- B7. Privacidad de datos
- B8. Dependencia de vendors
- B9. Agentes IA en producción
""")

write("templates/project-brief/project-brief-template.md", """
# Project Brief — Plantilla

## 1. Nombre del proyecto

## 2. Problema que resuelve

## 3. Usuarios principales

## 4. Funcionalidades mínimas

## 5. Funcionalidades deseables

## 6. Restricciones

## 7. Stack preferido o existente

## 8. Integraciones necesarias

## 9. Criterio de éxito

## 10. Decisiones pendientes
""")

write("docs/decisiones_plataforma.md", """
# Decisiones de Plataforma — Estudio IA

## Decisión actual

Trabajar primero en Dify Cloud para validar apps, chatflows, prompts y estructura operativa.

## Migración futura

Migrar a Dify self-hosted en Hostinger VPS cuando la estructura esté validada.

## Stack previsto

- Dify self-hosted para agentes y chatflows.
- n8n self-hosted para automatización entre sistemas.
- GitHub para versionado de prompts, DSL, documentación y código.
- Supabase por proyecto cuando se requiera base de datos.
- Vercel por proyecto cuando se requiera deploy frontend.
- Hostinger VPS KVM 2 como servidor previsto para Dify + n8n.

## Criterio operativo

1. Validar apps base en Dify Cloud.
2. Exportar DSL/YAML desde Dify.
3. Versionar los DSL/YAML en GitHub.
4. Preparar infraestructura Hostinger.
5. Instalar Dify + n8n self-hosted.
6. Importar apps Dify.
7. Conectar n8n con GitHub, Vercel y Supabase según proyecto.

## Advertencia

Dify Cloud no debe asumir conexiones reales con n8n, GitHub, Vercel, Supabase o Hostinger hasta que esas integraciones existan.
""")

write("docs/estado_validacion_dify.md", """
# Estado de Validación Dify

## Equipo de Diseño

Estado: Prototype v0.1 validado en Dify Cloud.

Validado:

- Ejecución en cadena.
- Paso de variables entre nodos.
- Final Synthesis.
- Answer con salida limpia.
- Prompts temporales de prueba.

Pendiente:

- Reemplazar prompts temporales por prompts canónicos versionados.
- Exportar DSL/YAML desde Dify.
- Guardar exportación en /dify/prototypes o /dify/apps.

## Equipo Constructor

Estado: Prototype v0.1 validado en Dify Cloud.

Validado:

- Ejecución en cadena.
- Paso de variables entre nodos.
- Build Synthesis.
- Criterio de bloqueo ajustado.
- Prompts temporales de prueba.

Pendiente:

- Probar con especificaciones completas del Equipo de Diseño.
- Reemplazar prompts temporales por prompts canónicos.
- Exportar DSL/YAML desde Dify.
""")

write("docs/arquitectura_hostinger.md", """
# Arquitectura Prevista — Hostinger VPS

## Objetivo

Alojar Dify y n8n self-hosted en un VPS para eliminar límites de Dify Cloud y permitir automatización operativa.

## Componentes

- Dify: equipos de agentes, chatflows y workflows IA.
- n8n: triggers, webhooks y automatización entre servicios.
- GitHub: fuente de verdad para prompts, DSL/YAML, workflows, scripts, documentación y código.
- Supabase: base de datos por proyecto cuando aplique.
- Vercel: deploy frontend por proyecto cuando aplique.
""")

write("dify/README.md", """
# Dify

Esta carpeta guarda las apps exportadas desde Dify.

## Carpetas

- /dify/apps: versiones canónicas aprobadas.
- /dify/exports: exportaciones originales desde Dify Cloud.
- /dify/prototypes: prototipos de prueba.

## Nomenclatura recomendada

- design-team-chatflow.prototype.yml
- builder-team-chatflow.prototype.yml
- design-team-chatflow.v1.yml
- builder-team-chatflow.v1.yml

## Regla

No guardar credenciales ni secretos en los archivos exportados.
""")

write("n8n/README.md", """
# n8n

Esta carpeta guardará workflows exportados desde n8n cuando se instale en Hostinger.

## Estado actual

Pendiente de instalación.

## Uso futuro

n8n será responsable de triggers, webhooks y conexión con GitHub, Vercel, Supabase y Dify.

## Regla

No subir credenciales ni valores reales de nodos con secrets.
""")

write("infra/hostinger/README.md", """
# Hostinger VPS

Preparación futura para instalar:

- Dify self-hosted.
- n8n self-hosted.
- Docker.
- Reverse proxy.
- Variables de entorno.
- Backups.

## Estado

Pendiente de contratación/configuración.
""")

write("infra/env-examples/.env.example", """
# Ejemplo de variables — NO usar valores reales

DIFY_DOMAIN=
DIFY_SECRET_KEY=

N8N_DOMAIN=
N8N_ENCRYPTION_KEY=

GITHUB_REPO=
GITHUB_TOKEN=

SUPABASE_URL=
SUPABASE_ANON_KEY=

VERCEL_PROJECT_ID=
VERCEL_TOKEN=
""")

write(".github/workflows/repo-check.yml", """
name: Repo Check

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:

jobs:
  repo-check:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Check required files
        run: |
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

      - name: Check no obvious env secrets committed
        run: |
          if find . -name ".env" -o -name ".env.local" | grep -q .; then
            echo "ERROR: .env file detected"
            exit 1
          fi
""")

write("scripts/check_repo.sh", """
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
""")

Path("scripts/check_repo.sh").chmod(0o755)

print("Estructura completada.")
