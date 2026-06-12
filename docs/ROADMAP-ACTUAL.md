# ROADMAP Y ESTADO ACTUAL — Estudio IA
**Actualizado:** 2026-06-12 (tarde) · **Función:** memoria compartida del proyecto. Cualquier conversación nueva con Claude debe empezar leyendo este documento (o pegándolo) para retomar contexto.

## Estado actual (qué funciona hoy)

- **Infraestructura:** Dify + n8n self-hosted en Hostinger (`187.127.233.43`), repo GitHub `estudio-ia` como fuente de verdad.
- **Equipo de Diseño (Dify):** 7 agentes + 3 nodos Knowledge Retrieval (BA, Architect, Tech Lead). Prompts endurecidos verificados: generalización 9,5/11, KB activo, fix corrida #42→#46 confirmado (ARC_STATUS al inicio, gate tolerante del Tech Lead, Critic con RECHAZADO obligatorio ante entregable ausente).
- **Corrida Tyrion #2 (diseño, exec #46, 12/06):** `VEREDICTO: RECHAZADO` — legítimo: DGT/SAGE sin mecanismo (PENDIENTE real del brief) + flujo conversacional incompleto. El Tech Lead entregó paquete completo (schema, contratos, plan 5 semanas). Pendiente menor: el Critic no detectó el plan de fases que sí estaba.
- **Equipo Constructor (Dify) ENDURECIDO v0.5.0:** 10 nodos. Los 5 builders con BUILD_STATUS al inicio (inventario de specs + gate tolerante + supuestos declarados) y VERIFICACIÓN al cierre; los 3 QA como auditores reales (check espejo specs ↔ BUILD_STATUS ↔ código, entregable ausente/bloqueo falso = RECHAZADO obligatorio, línea VEREDICTO exacta); Build Synthesis con fidelidad de veredicto + anexo de evidencia. Fix estructural: los QA e Integration Agent ahora reciben sys.query (antes no veían las specs de origen).
- **Pipeline verificado (exec #48, 12/06):** specs del Tech Lead #46 → constructor → `VEREDICTO: RECHAZADO` correcto (Backend QA y Integration QA rechazaron por falta de auth; UX QA aprobó; propagación de veredicto perfecta). 205s, ~$0.10/run, 54.8K prompt tokens. Fix posterior: max_tokens del synthesis 2048→16000 (anexo truncado) — reimportado.
- **Hallazgo de producto:** las specs de diseño NO definen autenticación → agregar a la entrevista (quién accede al panel, cómo se autentican los 4 administrativos).
- **Bridge n8n → Dify:** "Dify Bridge - Equipo Diseño" (`0tGxducQ0fq5uKbs`), webhook `/webhook/dify-design`. "Studio Intake Router" (`WxTdNZUAGZjPbYH6`), webhook `/webhook/studio-intake`, modos design/build, keys actualizadas (builder: regenerada 12/06). ⚠ Briefs largos (>2-3K chars) fallan vía MCP execute_workflow; workaround: workflows temporales con brief hardcodeado en Set node + Code node `JSON.stringify($json)`.
- **Workflows temporales activos (borrar cuando exista bridge definitivo):** "Tyrion Design Run (temp)" (`lbzEIUgvtGZTpkdv`, brief diseño) y "Builder Team Run (temp)" (`qkwMnSi23HVgIWgC`, specs constructor).
- **Conector MCP n8n ("Studio-julio"):** funcionando, control total de n8n desde Claude.
- **GitHub:** prompts canónicos endurecidos en `prompts/` (design + builder + QA). DSL canónicos en `dify/apps/` (`builder-team-chatflow.v1.yml`), exports crudos en `dify/exports/`, prototipos en `dify/prototypes/`. Issues viejos (#1-8) cerrados; tracking activo en **#10**.

## Cómo invocar a los equipos desde Claude
1. Brief corto (<2K chars): `execute_workflow` sobre el Studio Intake Router (`WxTdNZUAGZjPbYH6`) con body `{query, mode: design|build}`, o el bridge de diseño (`0tGxducQ0fq5uKbs`).
2. Brief largo: editar el workflow temporal correspondiente (Set node con el brief) y ejecutarlo.
3. Diseño tarda 80-125s (~$0.14/run); constructor 200-210s (~$0.10/run). Leer resultado con `get_execution` + `includeData:true` filtrando el nodo HTTP.

## Fases por delante

### FASE 1.5 — Cerrar diseño Tyrion
1. ~~Importar YAML con fixes (commit 8faf3b04)~~ ✅
2. **[Julio, en curso — 48hs]** Entrevista con el administrativo: las 50 preguntas de `01-entrevista-administrativo.md` + prioridad a los bloqueantes: mecanismo DGT, mecanismo SAGE, plazos de subsanación, frecuencia observaciones DGT, retención legal, presupuesto IA real, **+ NUEVO: autenticación y acceso al panel (quién, cómo)**.
3. ~~Re-correr Tyrion con fixes~~ ✅ (exec #46)

### FASE 2 — Equipo Constructor al mismo nivel ✅ COMPLETA
4. ~~Endurecer builder + 3 QA~~ ✅ (v0.5.0, commits 027b0a4 + ac04e30 + 45c2593)
5. ~~Pipeline completo diseño → constructor → auditoría~~ ✅ (exec #48)
Pendiente menor (no bloqueante): coherencia interna de tablas del Backend QA; el Design Critic no detectó un entregable presente (falso negativo benigno).

### FASE 3 — Proyecto Tyrion de verdad
6. **[Julio]** Actualizar spec v2 con respuestas de la entrevista (resolver los `[PENDIENTE]` + auth).
7. **[Julio]** Re-subir spec validada al Knowledge "Estudio" en Dify.
8. **[Ambos]** Corrida definitiva: diseño aprobado limpio → constructor aprobado limpio.
9. **[Decisión]** Construcción real en repo `alfa-pyme` (evaluar Claude Code).

### FASE 4 — Operación del estudio
10. Orquestador con criterio: Client Liaison como Agent app en Dify.
11. Deploy Agent + Documenter (modelos ligeros) — prompts ya en `prompts/support-phase/`.
12. URL estable para el MCP de Dify (dominio + SSL o Cloudflare Tunnel).
13. Bridge n8n definitivo con soporte de briefs largos (patrón Code node) → al terminarlo, borrar los 2 workflows temporales.
14. n8n: triggers de entrada (email → pipeline) cuando Tyrion v1 exista.

## Seguridad
- ⚠ **Token de GitHub** (`ghp_FaGk...`, clásico, todos los repos): activo por decisión de Julio hasta cerrar el setup. Compartido en chats del 10-12/06. **Revocar y pasar a fine-grained al terminar.**
- ⚠ Keys de apps Dify hardcodeadas en workflows n8n (router + bridges + temporales). Key del builder regenerada el 12/06 (la anterior quedó inválida). No compartir URLs públicamente.
- Lección: borrar una app en Dify mata su API key. Importar DSL SIEMPRE desde dentro de la app (Import DSL → Publish). El Publish es obligatorio: la API sirve la versión publicada, no el borrador.

## Cómo retomar contexto en un chat nuevo
1. Activar el conector "Studio-julio" (n8n) en el chat (+ → conectores).
2. Pegar este documento (o dar el token de GitHub para que Claude lea el repo).
3. Indicar la fase y el paso en el que estamos.
