# Flujo operativo del Estudio IA

## Objetivo

Este documento define el flujo operativo inicial del Estudio IA para convertir el router funcional de prueba en un sistema operativo mínimo con AI Studio Director, agentes canónicos, n8n, GitHub, Codex y registro de proyectos.

## Flujo principal

```text
Julio
→ AI Studio Director
→ n8n Studio Intake Router
→ Equipo Dify correspondiente
→ GitHub issue
→ Codex
→ PR
→ estado final devuelto por AI Studio Director
```

## Responsabilidades por etapa

### 1. Julio

Julio inicia pedidos, aprueba Briefs, autoriza producción, valida decisiones sensibles y define prioridades.

### 2. AI Studio Director

AI Studio Director es el interlocutor principal de Julio. Identifica proyecto activo, activa Discovery cuando corresponde, genera el Brief, pide confirmación explícita y comunica el resultado final.

AI Studio Director no toca GitHub directamente. Tampoco entra a paneles externos ni usa secretos.

### 3. n8n Studio Intake Router

n8n recibe pedidos estructurados desde AI Studio Director, clasifica el modo de trabajo y crea o actualiza issues en GitHub dentro de `julionotaro/estudio-ia`.

GitHub se toca indirectamente vía n8n.

### 4. Equipo Dify correspondiente

Dify contiene los agentes canónicos. Cada agente debe usar el prompt versionado en `prompts/` como fuente de verdad.

- Diseño: Director, Project Manager, Business Analyst, System Architect, Tech Lead, UX Architect.
- Build: Backend Builder, Database Agent, Integration Agent, UI Designer, Frontend Builder.
- QA: Backend QA, UX QA, Integration QA.
- Deploy: Deploy Agent.
- Docs: Documenter.

### 5. GitHub issue

La issue debe contener contexto suficiente, alcance definido, criterios de aceptación, archivos esperados y validaciones. Si la issue es ambigua, Codex no debe inventar alcance.

### 6. Codex

Codex ejecuta únicamente issues o PRs bien definidos. Codex no debe operar paneles externos, no debe usar tokens, no debe tocar producción y no debe trabajar fuera del repo `julionotaro/estudio-ia`.

### 7. Pull Request

La PR debe resumir cambios, validaciones, riesgos y pendientes manuales. La PR se abre contra `main`.

### 8. Estado final

AI Studio Director devuelve a Julio:

- qué se hizo;
- qué quedó listo;
- qué falta hacer manualmente;
- riesgos;
- próximos pasos recomendados.

## Discovery y Brief

El Brief lo genera AI Studio Director en modo Discovery usando el formato canónico del prompt `prompts/design-phase/00_client_liaison.md`. El Brief no se considera válido hasta que Julio lo apruebe explícitamente.

Una vez aprobado, AI Project Manager recibe el Brief y coordina BA / Architect / Tech Lead / UX.

## Registro de Proyectos

El estado mínimo de cada proyecto se registra bajo `projects/`. El registro global está en `projects/registry.json` y el proyecto núcleo del estudio está en `projects/studio_ia_core/`.
