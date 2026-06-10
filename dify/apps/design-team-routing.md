# Design Team — Routing Dify

## Alcance

Este archivo documenta el routing del equipo de diseño dentro de Dify. No copia ni modifica los prompts canónicos de diseño.

## Agentes y prompts canónicos

| Agente Dify | Prompt canónico | Rol en routing |
|---|---|---|
| AI Project Manager | `prompts/design-phase/08_project_manager.md` | Coordina el flujo interno de diseño y controla entregables. |
| Business Analyst | `prompts/design-phase/01_business_analyst.md` | Convierte el Brief en requerimientos y reglas de negocio. |
| System Architect | `prompts/design-phase/02_system_architect.md` | Diseña arquitectura y completa ARC antes de presentar. |
| Tech Lead | `prompts/design-phase/03_tech_lead.md` | Traduce arquitectura aprobada en specs técnicas y tareas. |
| UX Architect | `prompts/design-phase/04_ux_architect.md` | Define UX, pantallas, navegación, estados y flujos. |

## Entrada requerida

- Brief aprobado por Julio.
- `project_id` y nombre del proyecto.
- Restricciones conocidas del proyecto.
- Decisiones previas relevantes.
- Objetivo de la etapa de diseño.

## Secuencia recomendada

1. `AI Project Manager` recibe el Brief aprobado desde AI Studio Director.
2. `Business Analyst` produce requerimientos funcionales, actores, datos y reglas de negocio.
3. `System Architect` recibe Brief y requerimientos; produce arquitectura y ARC completo.
4. `Tech Lead` recibe arquitectura aprobada, ARC y requerimientos; produce specs técnicas y división de trabajo.
5. `UX Architect` trabaja en paralelo o después de requerimientos para producir estructura UX y flujos.
6. `AI Project Manager` consolida entregables y detecta bloqueos antes de pasar a construcción.

## Rutas de salida

| Condición | Destino | Resultado esperado |
|---|---|---|
| Requerimientos incompletos | AI Project Manager | Solicitud de aclaración hacia AI Studio Director. |
| ARC incompleto | System Architect | Corrección antes de cualquier handoff técnico. |
| Specs técnicas listas | Builder Team o n8n | Pedido de construcción dividido por especialidad o issue operable. |
| UX lista para validar | Builder Team | Insumos para UI Designer y Frontend Builder. |
| Decisión de negocio pendiente | AI Studio Director | Pregunta concreta para Julio. |

## Contrato conceptual de handoff a construcción

```text
source_app: Design Team
project_id: proyecto activo
mode: build
brief_status: approved
summary: alcance de construcción solicitado
context: Brief aprobado; requerimientos; ARC; arquitectura; specs técnicas; UX
approved_by_julio: true
requested_action: prepare_builder_tasks | send_to_n8n
constraints: no secrets; no producción; repo julionotaro/estudio-ia
```

## Validaciones antes de salir de diseño

- Brief aprobado explícitamente.
- Requerimientos funcionales disponibles.
- ARC completo y arquitectura aprobada.
- Specs técnicas suficientemente precisas para construir.
- UX y flujos principales documentados o bloqueo declarado.
- Riesgos y decisiones pendientes identificados.

## Qué queda manual en Dify

- Crear o ajustar cada agente de diseño.
- Pegar el prompt canónico correcto en cada agente.
- Configurar handoffs entre Project Manager, BA, Architect, Tech Lead y UX Architect.
- Probar que los agentes no avancen si faltan aprobaciones.
