# Dify Routing Strategy — Estudio IA

## Propósito

Este documento separa la orquestación de Dify del contenido de los prompts canónicos. La lógica de routing define qué app, agente o flujo debe recibir una tarea, con qué contexto mínimo y bajo qué condiciones debe detenerse.

Los prompts canónicos siguen viviendo únicamente en `prompts/`. Esta documentación no reemplaza, resume ni reescribe esos prompts: solo describe cómo conectarlos manualmente dentro de Dify.

## Principios de separación

1. **Prompts canónicos como fuente de verdad:** cada agente usa el archivo correspondiente documentado en `dify/docs/prompt-agent-matrix.md`.
2. **Routing como documentación operativa:** los archivos en `dify/apps/*-routing.md` documentan conexiones, entradas, salidas y handoffs esperados.
3. **Sin exports inventados:** no se crean archivos YAML/JSON de Dify si no fueron exportados desde el panel.
4. **Sin secretos:** la configuración no debe incluir tokens, API keys, credenciales, variables sensibles ni valores de producción.
5. **Sin operación directa sobre paneles:** cualquier configuración real en Dify, n8n, Hostinger o producción queda como tarea manual autorizada.
6. **GitHub indirecto:** Dify no debe tocar GitHub directamente; los pedidos operativos se derivan hacia n8n cuando corresponda.

## Capas de routing

| Capa | Archivo | Responsabilidad |
|---|---|---|
| Dirección | `dify/apps/studio-director-routing.md` | Entrada conversacional, identificación de proyecto, modo operativo y cierre con Julio. |
| Diseño | `dify/apps/design-team-routing.md` | Handoff desde Brief aprobado hacia Business Analyst, Architect, Tech Lead, UX Architect y Project Manager. |
| Construcción | `dify/apps/builder-team-routing.md` | Derivación de specs aprobadas hacia Backend, Database, Integration, UI y Frontend Builders. |
| QA / Entrega | `dify/apps/qa-delivery-routing.md` | Validación backend, UX, integración, deployment guiado y documentación final. |

## Modos operativos recomendados

| Modo | Entrada mínima | Ruta Dify | Resultado esperado |
|---|---|---|---|
| `discovery` | Intención de proyecto nuevo o proyecto ambiguo | AI Studio Director | Brief completo pendiente de aprobación humana. |
| `design` | Brief aprobado | Design Team | Requerimientos, arquitectura con ARC, specs técnicas y UX. |
| `build` | Specs técnicas aprobadas | Builder Team | Entregables técnicos por especialidad para ejecución por issues/PRs. |
| `qa` | Código o entregables listos para validar | QA Delivery | Reportes de Backend QA, UX QA e Integration QA. |
| `deploy` | Sistema aprobado para publicación | QA Delivery | Guía de deployment; no ejecución directa. |
| `docs` | Sistema validado o decisión documentable | QA Delivery | Manuales, troubleshooting y registro de decisiones. |

## Contrato común de routing

Cada handoff documentado para Dify debería transportar, como mínimo, estos campos conceptuales. No es un export de Dify ni una configuración lista para importar; es una guía para configurar variables o inputs manualmente en el panel.

```text
source_app: nombre de la app o agente que deriva la tarea
project_id: identificador del proyecto activo
project_name: nombre humano del proyecto, si existe
mode: discovery | design | build | qa | deploy | docs
brief_status: draft | pending_approval | approved | not_required
summary: resumen claro de la intención o tarea
context: referencias a Brief, decisiones, ARC, specs o reportes disponibles
approved_by_julio: true | false
requested_action: acción esperada por el siguiente agente o por n8n
constraints: restricciones operativas aplicables
```

## Reglas de aprobación

- Dify puede avanzar de `discovery` a `design` solo con Brief aprobado explícitamente por Julio.
- Dify puede avanzar de `design` a `build` solo con arquitectura y specs técnicas aprobadas.
- Dify puede avanzar de `build` a `qa` solo con entregables concretos para validar.
- Dify puede avanzar de `qa` a `deploy` solo con QA aprobado o con una excepción humana documentada.
- Dify puede crear pedidos operativos hacia n8n solo si el pedido incluye repo, contexto, restricción de no secretos y aprobación cuando aplique.

## Hard stops globales

Dify debe detenerse y pedir intervención humana si aparece cualquiera de estos casos:

- Falta proyecto activo o existe ambigüedad no resuelta.
- Falta aprobación explícita del Brief, ARC, specs o release según la etapa.
- Se solicita usar secretos, tokens, credenciales, `.env` o datos sensibles.
- Se solicita tocar Hostinger, n8n, panel de Dify, producción o repos externos desde la conversación.
- Se solicita modificar prompts canónicos sin una issue explícita para ese cambio.
- Se solicita generar o asumir un export YAML/JSON de Dify no descargado desde el panel.

## Qué queda manual en Dify

- Crear o actualizar apps/agentes en el panel de Dify.
- Pegar manualmente el contenido vigente de cada prompt canónico.
- Configurar variables, nodos, tools, permisos y credenciales reales sin guardarlas en este repo.
- Probar conversaciones end-to-end y exportar desde el panel cuando exista una exportación real.
- Registrar decisiones relevantes en la documentación del proyecto.
