# ROADMAP Y ESTADO ACTUAL — Estudio IA
**Actualizado:** 2026-06-14 (entrevista Tyrion sesión 1) · **Función:** memoria compartida del proyecto.

## Estado actual (qué funciona hoy)

- **Infraestructura:** Dify + n8n self-hosted en Hostinger (`187.127.233.43`), repo GitHub `estudio-ia` como fuente de verdad.
- **Equipo de Diseño (Dify):** 7 agentes + 3 nodos Knowledge Retrieval (BA, Architect, Tech Lead). Prompts endurecidos verificados: generalización 9,5/11, KB activo, fix corrida #42→#46 confirmado (ARC_STATUS al inicio, gate tolerante del Tech Lead, Critic con RECHAZADO obligatorio ante entregable ausente).
- **Corrida Tyrion #2 (diseño, exec #46, 12/06):** `VEREDICTO: RECHAZADO` — legítimo: DGT/SAGE sin mecanismo (PENDIENTE real del brief) + flujo conversacional incompleto. El Tech Lead entregó paquete completo (schema, contratos, plan 5 semanas).
- **Equipo Constructor (Dify) ENDURECIDO v0.5.0:** 10 nodos. Pipeline verificado en 3 corridas (exec #48/#49/#50, 12/06). Fidelidad de veredicto perfecta. 200-215s, ~$0.09/run.
- **Bridge n8n → Dify:** "Dify Bridge - Equipo Diseño" (`0tGxducQ0fq5uKbs`), webhook `/webhook/dify-design`. "Studio Intake Router" (`WxTdNZUAGZjPbYH6`), webhook `/webhook/studio-intake`, modos design/build, keys actualizadas (builder: regenerada 12/06). ⚠ Briefs largos (>2-3K chars) fallan vía MCP execute_workflow; workaround: workflows temporales con brief hardcodeado en Set node + Code node `JSON.stringify($json)`.
- **Workflows temporales activos (borrar cuando exista bridge definitivo):** "Tyrion Design Run (temp)" (`lbzEIUgvtGZTpkdv`, brief diseño) y "Builder Team Run (temp)" (`qkwMnSi23HVgIWgC`, specs constructor).
- **Conector MCP n8n ("Studio-julio"):** funcionando, control total de n8n desde Claude.
- **GitHub:** prompts canónicos endurecidos en `prompts/` (design + builder + QA). DSL canónicos en `dify/apps/` (`builder-team-chatflow.v1.yml`). Issues viejos (#1-8) cerrados; tracking activo en **#10**.

## Frente comercial
- **Handoff comercial v1.0:** `docs/handoff-comercial.md` — visión Estudio IA + Alfa-Pyme como caso demostrador.
- **Hallazgo clave:** la oficina usa **Tempus** como sistema consolidado. No hay WhatsApp/Telegram. DGT es siempre presencial.
- Regla: no prometer integraciones (DGT/SAGE/Tempus) hasta definir mecanismo; promesa segura = Tyrion prepara, humano ejecuta.

## Cómo invocar a los equipos desde Claude
1. Brief corto (<2K chars): `execute_workflow` sobre el Studio Intake Router (`WxTdNZUAGZjPbYH6`) con body `{query, mode: design|build}`.
2. Brief largo: editar el workflow temporal correspondiente (Set node con el brief) y ejecutarlo.
3. Diseño tarda 80-125s (~$0.14/run); constructor 200-210s (~$0.10/run). Leer resultado con `get_execution` + `includeData:true` filtrando el nodo HTTP.

## Fases por delante

### FASE 1.5 — Cerrar diseño Tyrion
1. ~~Importar YAML con fixes (commit 8faf3b04)~~ ✅
2. ~~Entrevista sesión 1 con el administrativo~~ ✅ (13/06/2026) — bloqueantes críticos resueltos. Spec v2.1 actualizada.
3. **[Julio, pendiente]** Entrevista sesión 2 (~75 min): estados Tempus (B6, CRÍTICO), flujo matriculaciones (B4), cadetería, errores docs, cierre proceso, automatización. Guía: `projects/alfa-pyme-tyrion/entrevista-tyrion-sesion2.docx`.
4. ~~Re-correr Tyrion con fixes~~ ✅ (exec #46)

### FASE 2 — Equipo Constructor al mismo nivel ✅ COMPLETA Y VERIFICADA
5. ~~Endurecer builder + 3 QA~~ ✅ (v0.5.0)
6. ~~Pipeline completo diseño → constructor → auditoría~~ ✅ (exec #48/#49/#50)

### FASE 3 — Proyecto Tyrion de verdad
7. **[Listo para ejecutar]** Corrida de diseño con spec v2.1. Brief en `02-proceso-operativo-v2.md` §15.
8. **[Julio, post sesión 2]** Completar spec v2.2 con estados Tempus y flujo matriculaciones → re-subir al Knowledge "Estudio" en Dify.
9. **[Ambos]** Corrida definitiva: diseño aprobado limpio → constructor aprobado limpio.
10. **[Decisión]** Construcción real en repo `alfa-pyme` (evaluar Claude Code).

### FASE 4 — Operación del estudio
11. Orquestador con criterio: Client Liaison como Agent app en Dify.
12. Deploy Agent + Documenter (modelos ligeros).
13. URL estable para el MCP de Dify.
14. Bridge n8n definitivo con soporte de briefs largos → borrar 2 workflows temporales.
15. n8n: triggers de entrada (email → pipeline) cuando Tyrion v1 exista.

## Documentos clave Tyrion
- `projects/alfa-pyme-tyrion/01-entrevista-administrativo.md` — guía completa de entrevista v2.2
- `projects/alfa-pyme-tyrion/02-proceso-operativo-v2.md` — spec v2.1 (actualizada 14/06, brief listo para diseño)
- `projects/alfa-pyme-tyrion/04-resultados-entrevista-sesion1.md` — respuestas capturadas sesión 1
- `docs/handoff-comercial.md` — visión comercial y posicionamiento

## Seguridad
- ⚠ **Token de GitHub** (`ghp_FaGk...`, clásico, todos los repos): activo por decisión de Julio hasta cerrar el setup. **Revocar y pasar a fine-grained al terminar.**
- ⚠ Keys de apps Dify hardcodeadas en workflows n8n. Key del builder regenerada el 12/06.
- Lección: borrar una app en Dify mata su API key. Importar DSL SIEMPRE desde dentro de la app (Import DSL → Publish).

## Cómo retomar contexto en un chat nuevo
1. Activar el conector "Studio-julio" (n8n) en el chat (+ → conectores).
2. Pegar este documento (o dar el token de GitHub para que Claude lea el repo).
3. Indicar la fase y el paso en el que estamos.
