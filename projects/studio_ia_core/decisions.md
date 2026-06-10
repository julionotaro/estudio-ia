# Decisiones — Estudio IA Core

## DECISIÓN 001: AI Studio Director como interlocutor principal

**Fecha:** 2026-06-10

**Contexto:** El Estudio IA necesitaba pasar de router funcional de prueba a sistema operativo inicial con un punto de contacto claro para Julio.

**Decisión tomada:** AI Studio Director queda definido como interlocutor principal de Julio y coordinador de entrada/salida.

**Justificación:** El prompt canónico `prompts/design-phase/00_client_liaison.md` ya define este rol como Director del Estudio de Desarrollo IA, único punto de contacto y coordinador interno.

**Consecuencias:** Julio no conversa directamente con agentes internos; el Director centraliza Discovery, confirmaciones y comunicación final.

## DECISIÓN 002: Brief generado por AI Studio Director en Discovery

**Fecha:** 2026-06-10

**Contexto:** Los proyectos nuevos necesitan una entrada estructurada antes de diseño, build o QA.

**Decisión tomada:** El Brief lo genera AI Studio Director en modo Discovery y requiere aprobación explícita de Julio.

**Justificación:** Evita construir sobre supuestos y preserva el formato canónico de Brief del Client Liaison.

**Consecuencias:** Sin Brief aprobado no se activa AI Project Manager para diseño formal.

## DECISIÓN 003: AI Project Manager coordina tras Brief aprobado

**Fecha:** 2026-06-10

**Contexto:** La coordinación interna requiere separar conversación con Julio de gestión del equipo técnico.

**Decisión tomada:** AI Project Manager recibe el Brief aprobado y coordina Business Analyst, System Architect, Tech Lead y UX Architect.

**Justificación:** El prompt canónico `prompts/design-phase/08_project_manager.md` define al Project Manager como coordinador de diseño y construcción, no ejecutor técnico.

**Consecuencias:** El Director mantiene comunicación externa; Project Manager coordina ejecución interna.

## DECISIÓN 004: GitHub indirecto vía n8n

**Fecha:** 2026-06-10

**Contexto:** Se necesitaba una frontera clara entre conversación, automatización e implementación.

**Decisión tomada:** AI Studio Director no toca GitHub directamente. GitHub se toca indirectamente vía n8n Studio Intake Router.

**Justificación:** n8n permite auditar y estructurar la creación/actualización de issues antes de que Codex ejecute.

**Consecuencias:** Los pedidos operativos pasan por n8n y deben convertirse en issues bien definidas.

## DECISIÓN 005: Codex solo ejecuta issues o PRs bien definidos

**Fecha:** 2026-06-10

**Contexto:** Codex necesita alcance claro para evitar cambios ambiguos o inseguros.

**Decisión tomada:** Codex queda limitado a ejecutar issues o PRs bien definidos dentro de `julionotaro/estudio-ia`.

**Justificación:** Mantiene trazabilidad, reduce alcance accidental y respeta hard stops.

**Consecuencias:** Si falta contexto, criterios de aceptación o validación, la tarea vuelve a diseño/documentación en vez de ejecutarse.

## DECISIÓN 006: Dify se actualiza manualmente desde prompts canónicos

**Fecha:** 2026-06-10

**Contexto:** El repo contiene prompts canónicos, pero no necesariamente exports actualizados de Dify.

**Decisión tomada:** Dify debe actualizarse manualmente con prompts canónicos y luego exportarse desde el panel cuando esté disponible.

**Justificación:** Evita inventar exports o declarar configuraciones no verificadas.

**Consecuencias:** La sincronización Dify/repositorio queda como paso manual hasta contar con export real versionado.
