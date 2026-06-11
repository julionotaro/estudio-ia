# ROADMAP Y ESTADO ACTUAL — Estudio IA
**Actualizado:** 2026-06-11 · **Función:** memoria compartida del proyecto. Cualquier conversación nueva con Claude debe empezar leyendo este documento (o pegándolo) para retomar contexto.

## Estado actual (qué funciona hoy)

- **Infraestructura:** Dify + n8n self-hosted en Hostinger, repo GitHub `estudio-ia` como fuente de verdad.
- **Equipo de Diseño (7 nodos):** Liaison, BA, Architect, Tech Lead, UX (gpt-4o, prompts canónicos + reglas de razonamiento) + **Design Critic** (auditor) + Synthesis (gpt-4o-mini, fidelidad literal del veredicto). Modo evaluación activo en el Answer.
- **Calidad medida:** run 1 = 4,5/10 → run 2 (endurecido) = 6/10. El Critic emitió RECHAZADO correctamente. Bug de síntesis (suavizaba el veredicto) corregido en commit `800f460` — **pendiente re-importar ese YAML en Dify**.
- **Equipo Constructor (10 nodos):** prompts canónicos + cadena de contexto conectada. AÚN SIN el endurecimiento (reglas de razonamiento + crítico) que recibió el de diseño.
- **Conector MCP:** "Equipo de Diseño Dify" registrado en Claude vía túnel `trycloudflare.com` (⚠ URL efímera, ver Seguridad). Funciona solo en chats nuevos con el conector activado (+ → conectores).
- **Proyecto real en curso:** Alfa-Pyme / Tyrion (oficina tramitadora, 250 trámites/día). Spec v2 en `projects/alfa-pyme-tyrion/02-proceso-operativo-v2.md` con pendientes de validación. Entrevista al administrativo lista en `01-entrevista-administrativo.md`.

## Fases por delante

### FASE 1 — Cerrar el ciclo de calidad del diseño (esta semana)
1. **[Julio, 2 min]** Re-importar `dify/prototypes/design-team-chatflow.prototype.yml` (incluye fix de veredicto + checks nuevos del Critic).
2. **[Julio, 1 min]** Abrir chat nuevo en Claude con el conector activado y pedir: *"corré el test de generalización"* (brief en `projects/alfa-pyme-tyrion/03-brief-generalizacion.md`).
3. **[Claude, vía MCP]** Invocar al Equipo de Diseño con ese brief, auditar contra los criterios del documento, reportar si las conductas generalizan.
4. **[Julio, 10 min]** Knowledge bases en Dify: crear Knowledge "Estudio", subir `02-proceso-operativo-v2.md` + `templates/arc-master.md`, vincular en los nodos BA, Architect y Tech Lead (sección Context del nodo). Es la palanca de 6 → 8 en profundidad de dominio.

### FASE 2 — Equipo Constructor al mismo nivel
5. **[Claude]** Aplicar al builder las reglas de razonamiento + endurecer los 3 QA como críticos reales (vía GitHub, requiere token vigente o uno nuevo).
6. **[Ambos]** Prueba de pipeline completo: diseño APROBADO por el Critic → entra al constructor → auditar el resultado.

### FASE 3 — Proyecto Tyrion de verdad
7. **[Julio]** Entrevista al administrativo (50 preguntas) → validar los `[PENDIENTE]` de la spec v2 (estados reales, plazos de subsanación, retención legal, mecanismo DGT).
8. **[Ambos]** Corrida de diseño definitiva de Tyrion con spec validada + knowledge → diseño aprobado.
9. **[Decisión]** Construcción: el equipo constructor genera specs/código guía; implementación real sobre el repo `alfa-pyme` (evaluar Claude Code para la ejecución).

### FASE 4 — Operación del estudio
10. Orquestador con criterio: Client Liaison como **Agent app** en Dify (decide solo qué agente llamar) — el "gestor autónomo" objetivo.
11. Deploy Agent + Documenter (Sprint 3 original, modelos ligeros).
12. URL estable para el MCP: dominio propio + SSL o Cloudflare Tunnel con nombre (la actual muere al reiniciar el VPS).
13. n8n: triggers de entrada (email → pipeline) cuando Tyrion v1 exista.

## Seguridad (no postergar)
- ⚠ **Token de GitHub:** el token clásico compartido en la conversación del 10/06 tiene acceso a TODOS los repos. Revocarlo al pausar el trabajo (GitHub → Settings → Developer settings) y crear uno **fine-grained** (solo `estudio-ia`, Contents read-write, 7 días) para cada sesión de trabajo futura con Claude.
- ⚠ **Túnel efímero:** `trycloudflare.com` cambia de URL en cada reinicio → el conector de Claude queda muerto y hay que re-agregarlo. Migrar a URL estable en Fase 4.
- El endpoint MCP de Dify: no compartir la URL públicamente (da acceso a invocar los agentes con tu API key).

## Cómo retomar contexto en un chat nuevo
1. Activar el conector "Equipo de Diseño Dify" (botón +).
2. Pegar este documento o dar acceso al repo con un token fine-grained.
3. Indicar la fase y el paso en el que estamos.
