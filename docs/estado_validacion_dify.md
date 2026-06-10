# Estado de Validación Dify

## Equipo de Diseño

Estado: v0.2 — Prompts canónicos cargados, listo para re-import y prueba real.

Corregido (2026-06-10):

- Eliminado encabezado "MODO PRUEBA ACTIVO" de los 6 nodos LLM.
- System prompts reemplazados por los canónicos de /prompts/design-phase.
- Variables entre nodos corregidas a sintaxis válida {{#nodeId.text#}} (BA, Architect y UX recibían placeholders literales).
- Instrucciones ARC movidas del rol assistant al system prompt (Architect y Tech Lead).
- Modelos: gpt-4o en Liaison, BA, Architect, Tech Lead y UX; gpt-4o-mini en Final Synthesis.
- max_tokens explícito en todos los nodos (2048/4096) para evitar truncado.

Pendiente:

- Re-importar YAML en Dify (Hostinger) y archivar la app anterior.
- Prueba real de punta a punta con caso de cliente.
- Knowledge bases (ARC master, plantillas) en Architect y Tech Lead.

## Equipo Constructor

Estado: v0.2 — Prompts canónicos cargados, cadena de contexto conectada.

Corregido (2026-06-10):

- Prompts de prueba (~1.000 chars) reemplazados por los canónicos de /prompts/builder-phase y /prompts/support-phase.
- Reglas de consistencia (OBJETIVO_CONFIRMADO) preservadas al final de cada system prompt.
- Agregados user prompts con variables encadenadas en los 10 nodos: cada agente ahora recibe el output real de los anteriores (antes recibían solo su system prompt, sin input).
- Modelos: gpt-4o en PM, Frontend Builder, Backend Builder y Database; gpt-4o-mini en UI Designer, Integration, los 3 QA y Build Synthesis.
- max_tokens explícito en todos los nodos.

Pendiente:

- Re-importar YAML en Dify (Hostinger) y archivar la app anterior.
- Probar con especificaciones completas generadas por el Equipo de Diseño.
