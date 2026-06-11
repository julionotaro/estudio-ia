# ROADMAP Y ESTADO ACTUAL — Estudio IA
**Actualizado:** 2026-06-11 (noche) · **Función:** memoria compartida del proyecto. Cualquier conversación nueva con Claude debe empezar leyendo este documento (o pegándolo) para retomar contexto.

## Estado actual (qué funciona hoy)

- **Infraestructura:** Dify + n8n self-hosted en Hostinger (`187.127.233.43`), repo GitHub `estudio-ia` como fuente de verdad.
- **Equipo de Diseño (Dify):** 7 agentes + 3 nodos Knowledge Retrieval vinculados a BA, Architect y Tech Lead (Knowledge "Estudio": proceso operativo v2 + arc-master). Prompts con reglas de razonamiento endurecidas + plantillas reforzadas. Fix de fidelidad del veredicto en Synthesis **verificado funcionando**.
- **Calidad medida (test de generalización, brief maquinaria):** run 1 = 4,5/11 → run 2 (fix veredicto) = 6,5/11 → run 3 (refuerzos) = **9,5/11** → generalización confirmada. Conocimiento del KB verificado activo (el Architect citó el presupuesto IA de 150-200€/mes que solo existe en el knowledge).
- **Corrida Tyrion #1 (exec #42, 11/06 21:57):** `VEREDICTO: APROBADO CON CORRECCIONES`. Dominio bien modelado (4 capas, validez en el vínculo N:M, 2 máquinas de estados, macro-estados respetados, DGT/SAGE A VERIFICAR). **Fallo detectado y corregido:** el Tech Lead se declaró bloqueado falsamente ("falta ARC_STATUS" cuando sí estaba) → sin schema ni plan de fases; el Critic NO detectó el entregable ausente.
- **Fix post-corrida (commit `8faf3b04`, PENDIENTE de importar en Dify):** ARC_STATUS ahora va al INICIO del output del Architect; gate del Tech Lead tolerante (ante la duda, continuar); check del Critic: entregable ausente/bloqueado = violación CRÍTICA + RECHAZADO obligatorio.
- **Bridge n8n → Dify:** workflow "Dify Bridge - Equipo Diseño" (`0tGxducQ0fq5uKbs`), webhook `/webhook/dify-design`, key actualizada. ⚠ Limitación conocida: briefs largos (>2-3K chars) fallan vía MCP execute_workflow; workaround usado: workflow temporal "Tyrion Design Run (temp)" (`lbzEIUgvtGZTpkdv`) con el brief hardcodeado en un Set node + Code node con `JSON.stringify($json)` → ese patrón debe incorporarse al bridge definitivo.
- **Equipo Constructor (10 nodos):** prompts canónicos + cadena de contexto. AÚN SIN endurecimiento (reglas de razonamiento + críticos reales).
- **Conector MCP n8n ("Studio-julio"):** funcionando, da control total de n8n a Claude (crear/editar/ejecutar/publicar workflows).

## Cómo invocar al Equipo de Diseño desde Claude
1. Brief corto (<2K chars): `execute_workflow` sobre el bridge `0tGxducQ0fq5uKbs` con `{"type":"webhook","webhookData":{"body":{"query":"..."},"method":"POST"}}`.
2. Brief largo: crear/editar workflow temporal con el brief en un Set node → Code node `JSON.stringify($json)` → HTTP Request a `http://187.127.233.43/v1/chat-messages` con la key de la app.
3. La ejecución tarda 80-95s. Leer resultado con `get_execution` + `includeData:true`. Costo ~$0.14/run.

## Fases por delante

### FASE 1.5 — Cerrar correcciones de la corrida Tyrion (inmediato)
1. **[Julio, 2 min]** Importar el YAML actualizado (commit `8faf3b04`) DESDE DENTRO de la app en Dify (menú de la app → Import DSL → Publish). NUNCA importar desde Studio home (crea app nueva y mata la API key).
2. **[Julio]** Entrevista con el administrativo: las **50 preguntas** de `01-entrevista-administrativo.md` + prioridad máxima a los 6 bloqueantes de diseño que surgieron de la corrida #42: mecanismo DGT, mecanismo SAGE, plazos de subsanación, frecuencia de observaciones DGT, retención legal, presupuesto IA real.
3. **[Claude]** Re-correr Tyrion con los fixes → verificar que el Tech Lead entrega schema + plan de fases y el Critic audita los 7 entregables.

### FASE 2 — Equipo Constructor al mismo nivel
4. **[Claude]** Aplicar al builder las reglas de razonamiento + plantillas reforzadas + endurecer los 3 QA como críticos reales (mismo método que funcionó en diseño: reglas DENTRO de las plantillas, checks espejo en los críticos).
5. **[Ambos]** Pipeline completo: diseño APROBADO → constructor → auditar resultado.

### FASE 3 — Proyecto Tyrion de verdad
6. **[Julio]** Actualizar spec v2 con respuestas de la entrevista (resolver los `[PENDIENTE]`).
7. **[Julio]** Re-subir spec validada al Knowledge "Estudio" en Dify.
8. **[Ambos]** Corrida definitiva de Tyrion → diseño aprobado limpio.
9. **[Decisión]** Construcción: specs/código guía del constructor → implementación real en repo `alfa-pyme` (evaluar Claude Code).

### FASE 4 — Operación del estudio
10. Orquestador con criterio: Client Liaison como Agent app en Dify.
11. Deploy Agent + Documenter (modelos ligeros).
12. URL estable para el MCP de Dify (dominio + SSL o Cloudflare Tunnel con nombre).
13. Bridge n8n definitivo con soporte de briefs largos (patrón Code node).
14. n8n: triggers de entrada (email → pipeline) cuando Tyrion v1 exista.

## Limpieza pendiente
- Borrar el workflow temporal "Tyrion Design Run (temp)" (`lbzEIUgvtGZTpkdv`) en n8n cuando el bridge definitivo soporte briefs largos.

## Seguridad
- ⚠ **Token de GitHub** (`ghp_FaGk...`, clásico, acceso a todos los repos): Julio decidió mantenerlo activo hasta que la estructura esté aceitada. Compartido en chats del 10/06 y 11/06. **Revocar y pasar a fine-grained cuando termine la fase de setup.**
- ⚠ El endpoint de la app Dify (`app-4gdi...`) está hardcodeado en los workflows de n8n. No compartir las URLs públicamente.
- Lección aprendida: borrar una app en Dify mata su API key → el bridge muere. Siempre actualizar apps con Import DSL desde dentro de la app.

## Cómo retomar contexto en un chat nuevo
1. Activar el conector "Studio-julio" (n8n) en el chat (+ → conectores).
2. Pegar este documento (o dar el token de GitHub para que Claude lea el repo).
3. Indicar la fase y el paso en el que estamos.
