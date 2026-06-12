# ROADMAP Y ESTADO ACTUAL — Estudio IA
**Actualizado:** 2026-06-12 (cierre de jornada) · **Función:** memoria compartida del proyecto. Cualquier conversación nueva con Claude debe empezar leyendo este documento (o pegándolo) para retomar contexto.

## Estado actual (qué funciona hoy)

- **Infraestructura:** Dify + n8n self-hosted en Hostinger (`187.127.233.43`), repo GitHub `estudio-ia` como fuente de verdad.
- **Equipo de Diseño (Dify):** 7 agentes + 3 nodos Knowledge Retrieval (BA, Architect, Tech Lead). Prompts endurecidos verificados: generalización 9,5/11, KB activo, fix corrida #42→#46 confirmado (ARC_STATUS al inicio, gate tolerante del Tech Lead, Critic con RECHAZADO obligatorio ante entregable ausente).
- **Corrida Tyrion #2 (diseño, exec #46, 12/06):** `VEREDICTO: RECHAZADO` — legítimo: DGT/SAGE sin mecanismo (PENDIENTE real del brief) + flujo conversacional incompleto. El Tech Lead entregó paquete completo (schema, contratos, plan 5 semanas). Pendiente menor: el Critic no detectó el plan de fases que sí estaba.
- **Equipo Constructor (Dify) ENDURECIDO v0.5.0:** 10 nodos. Los 5 builders con BUILD_STATUS al inicio (inventario de specs + gate tolerante + supuestos declarados) y VERIFICACIÓN al cierre; los 3 QA como auditores reales (check espejo specs ↔ BUILD_STATUS ↔ código, entregable ausente/bloqueo falso = RECHAZADO obligatorio, línea VEREDICTO exacta); Build Synthesis con fidelidad de veredicto + anexo de evidencia. Fix estructural: los QA e Integration Agent ahora reciben sys.query (antes no veían las specs de origen).
- **Pipeline verificado en 3 corridas (exec #48/#49/#50, 12/06):** specs del Tech Lead #46 → constructor → `VEREDICTO: RECHAZADO` correcto y consistente. Fidelidad de veredicto perfecta (cualquier QA rechaza → rechazado final con correcciones textuales). En #50 (fix synthesis verificado): anexo completo sin truncar, los 3 reportes QA con línea VEREDICTO, tablas VERIFICACIÓN visibles; el Integration QA cruzó un hallazgo del UX QA (confirmación de cierre exigida por specs y omitida por el frontend) — el check espejo entre QAs funciona. 200-215s, ~$0.09/run.
- **Hallazgo de producto:** las specs de diseño NO definen autenticación → agregar a la entrevista (quién accede al panel, cómo se autentican los 4 administrativos).
- **Bridge n8n → Dify:** "Dify Bridge - Equipo Diseño" (`0tGxducQ0fq5uKbs`), webhook `/webhook/dify-design`. "Studio Intake Router" (`WxTdNZUAGZjPbYH6`), webhook `/webhook/studio-intake`, modos design/build, keys actualizadas (builder: regenerada 12/06). ⚠ Briefs largos (>2-3K chars) fallan vía MCP execute_workflow; workaround: workflows temporales con brief hardcodeado en Set node + Code node `JSON.stringify($json)`.
- **Workflows temporales activos (borrar cuando exista bridge definitivo):** "Tyrion Design Run (temp)" (`lbzEIUgvtGZTpkdv`, brief diseño) y "Builder Team Run (temp)" (`qkwMnSi23HVgIWgC`, specs constructor).
- **Conector MCP n8n ("Studio-julio"):** funcionando, control total de n8n desde Claude.
- **GitHub:** prompts canónicos endurecidos en `prompts/` (design + builder + QA). DSL canónicos en `dify/apps/` (`builder-team-chatflow.v1.yml`), exports crudos en `dify/exports/`, prototipos en `dify/prototypes/`. Issues viejos (#1-8) cerrados; tracking activo en **#10**.

## Cómo invocar a los equipos desde Claude
1. Brief corto (<2K chars): `execute_workflow` sobre el Studio Intake Router (`WxTdNZUAGZjPbYH6`) con body `{query, mode: design|build}`, o el bridge de diseño (`0tGxducQ0fq5uKbs`).
2. Brief largo: editar el workflow temporal correspondiente (Set node con el brief) y ejecutarlo.
3. Diseño tarda 80-125s (~$0.14/run); constructor 200-210s (~$0.10/run). Leer resultado con `get_execution` + `includeData:true` filtrando el nodo HTTP.

## Frente comercial (nuevo, 12/06)
- **Handoff comercial v1.0:** `docs/handoff-comercial.md` — visión Estudio IA + Alfa-Pyme como caso demostrador, posicionamiento "capa de inteligencia sobre sistemas existentes" (no reemplazo de Tempus), oferta en 4 fases (diagnóstico → prototipo → piloto → integración), prompt listo para abrir análisis comercial con consultor GTM.
- **Hallazgo clave:** la oficina usa **Tempus** como sistema consolidado → nueva integración A VERIFICAR (junto a DGT y SAGE) + pregunta 54-bis en la entrevista. El rol de Tempus es el dato de mayor impacto en producto y discurso comercial.
- Regla compartida técnica-comercial: no prometer integraciones (DGT/SAGE/Tempus) hasta validar mecanismo; promesa segura = abstracción + carga asistida.

## Fases por delante

### FASE 1.5 — Cerrar diseño Tyrion
1. ~~Importar YAML con fixes (commit 8faf3b04)~~ ✅
2. **[Julio, en curso — 48hs]** Entrevista con el administrativo usando la guía actualizada: **Bloque 14 primero si el tiempo se corta** (preguntas 51-59: mecanismo DGT paso a paso, SAGE, Tempus, autenticación/acceso, circuito del papel, conversación WhatsApp real, presupuesto/criterio de éxito).
3. ~~Re-correr Tyrion con fixes~~ ✅ (exec #46)

### FASE 2 — Equipo Constructor al mismo nivel ✅ COMPLETA Y VERIFICADA (issue #10 cerrado)
4. ~~Endurecer builder + 3 QA~~ ✅ (v0.5.0)
5. ~~Pipeline completo diseño → constructor → auditoría~~ ✅ (exec #48/#49/#50, fix synthesis verificado en #50)
Pendientes menores (no bloqueantes): coherencia interna de tablas del Backend QA; fechas alucinadas en reportes QA (cosmético); el Design Critic no detectó un entregable presente (falso negativo benigno).

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
