# AI Studio Director — Routing Dify

## Alcance

Este archivo documenta cómo debe rutear Dify la entrada principal del Estudio IA. No contiene el prompt canónico del Director; ese contenido sigue en `prompts/design-phase/00_client_liaison.md`.

## App o agente recomendado

- **Nombre Dify:** `AI Studio Director`
- **Prompt canónico:** `prompts/design-phase/00_client_liaison.md`
- **Tipo de uso:** punto de entrada conversacional y coordinador externo con Julio
- **No debe hacer:** escribir código, diseñar arquitectura en detalle, tocar GitHub directamente, operar paneles externos o ejecutar acciones de producción

## Entradas mínimas

| Campo | Uso |
|---|---|
| `project_id` | Identificar el proyecto activo cuando exista. |
| `project_name` | Nombre visible para confirmar contexto con Julio. |
| `last_active_project` | Resolver referencias como “el de siempre” solo si no hay ambigüedad. |
| `mode` | Detectar `discovery`, `design`, `build`, `qa`, `deploy` o `docs`. |
| `brief_status` | Bloquear avance cuando el Brief no esté aprobado. |
| `last_decision` | Evitar repetir decisiones ya tomadas. |

## Decisión de routing inicial

1. Si Julio menciona un proyecto existente, cargar ese contexto.
2. Si Julio se refiere al último proyecto activo y no hay ambigüedad, confirmar el contexto.
3. Si el pedido corresponde a un proyecto nuevo, activar `discovery`.
4. Si el pedido requiere trabajo operativo, verificar si existe Brief aprobado.
5. Si falta aprobación o contexto, preguntar antes de derivar.

## Rutas de salida

| Condición | Destino | Resultado esperado |
|---|---|---|
| Proyecto nuevo o idea incompleta | AI Studio Director en `discovery` | Brief iterativo, una pregunta por vez. |
| Brief aprobado y pedido de diseño | Design Team | Solicitud estructurada para iniciar análisis, arquitectura, specs y UX. |
| Specs aprobadas y pedido de construcción | n8n Studio Intake Router | Pedido para crear o actualizar issue operable en GitHub. |
| Pedido de QA, deploy o docs | QA Delivery | Validación, guía de entrega o documentación según corresponda. |
| Pedido ambiguo o riesgoso | Intervención humana | Pregunta de aclaración o bloqueo explícito. |

## Contrato de salida hacia otros flujos

Usar este contrato conceptual al configurar handoffs en Dify. No es un export importable.

```text
source_app: AI Studio Director
project_id: proyecto activo confirmado
mode: discovery | design | build | qa | deploy | docs
summary: pedido resumido en lenguaje claro
brief_status: draft | pending_approval | approved
approved_by_julio: true | false
context: Brief, decisiones previas y restricciones relevantes
requested_action: handoff_to_design | handoff_to_qa_delivery | send_to_n8n | ask_human
constraints: no secrets; repo permitido julionotaro/estudio-ia; no producción sin autorización
```

## Hard stops específicos

- No avanzar a diseño sin Brief aprobado.
- No derivar a construcción sin specs técnicas aprobadas.
- No enviar pedidos a n8n si falta repo, contexto o aprobación requerida.
- No pedir ni almacenar secretos.
- No modificar prompts canónicos desde este flujo.

## Checklist de configuración manual

- Crear o actualizar la app `AI Studio Director` en Dify.
- Pegar manualmente el prompt canónico vigente.
- Configurar variables de proyecto y modo.
- Configurar salidas hacia Design Team, QA Delivery o n8n como handoffs documentados.
- Probar Discovery, Gestión, Consulta y Revisión antes de exportar desde el panel.
