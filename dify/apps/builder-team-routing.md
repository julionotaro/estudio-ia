# Builder Team — Routing Dify

## Alcance

Este archivo documenta cómo enrutar tareas de construcción dentro de Dify. No contiene exports de Dify ni reemplaza los prompts canónicos de construcción.

## Agentes y prompts canónicos

| Agente Dify | Prompt canónico | Especialidad |
|---|---|---|
| Backend Builder | `prompts/builder-phase/05_backend_builder.md` | APIs, lógica de servidor y contratos backend. |
| Database Agent | `prompts/builder-phase/06_database_agent.md` | Esquema, relaciones, índices, políticas y datos iniciales. |
| Integration Agent | `prompts/builder-phase/07_integration_agent.md` | Servicios externos, auth, email, pagos, APIs y storage. |
| UI Designer | `prompts/builder-phase/10_ui_designer.md` | Componentes visuales y diseño de interfaz. |
| Frontend Builder | `prompts/builder-phase/11_frontend_builder.md` | Páginas, rutas, estado, formularios e integración con backend. |

## Entrada requerida

- Specs técnicas aprobadas por Tech Lead.
- Arquitectura y ARC aprobados.
- Requerimientos funcionales.
- UX, wireframes o flujos disponibles cuando aplique.
- Alcance claro por componente o issue.
- Restricciones: no secretos, no producción y repo permitido.

## Decisión de routing por tipo de tarea

| Tipo de tarea | Destino primario | Destinos relacionados |
|---|---|---|
| Modelo de datos o migraciones | Database Agent | Backend Builder, Integration QA |
| API, lógica server-side o validaciones | Backend Builder | Database Agent, Backend QA |
| Servicio externo, auth o webhook | Integration Agent | Backend Builder, Integration QA |
| Diseño visual o componentes de UI | UI Designer | UX QA, Frontend Builder |
| Rutas, estado, formularios o consumo de API | Frontend Builder | Backend Builder, UX QA, Integration QA |

## Secuencia recomendada

1. Validar que las specs estén aprobadas y que la tarea sea construible.
2. Dividir por especialidad sin mezclar responsabilidades innecesariamente.
3. Enviar a cada agente solo el contexto necesario: Brief, specs, contratos, UX y restricciones.
4. Consolidar entregables para QA.
5. Derivar a QA Delivery con reportes o artefactos concretos.

## Contrato conceptual de handoff a QA

```text
source_app: Builder Team
project_id: proyecto activo
mode: qa
summary: componente o flujo construido para validar
context: specs técnicas; código o entregable; contratos de datos; UX esperada; riesgos conocidos
approved_by_julio: true | false
requested_action: validate_backend | validate_ux | validate_integration
constraints: no secrets; no producción; no paneles externos
```

## Hard stops específicos

- No construir si falta la spec técnica o el alcance de la issue.
- No asumir credenciales, URLs privadas, tokens ni variables de entorno reales.
- No tocar Hostinger, n8n, Dify panel ni producción.
- No cambiar prompts canónicos como parte del trabajo de construcción.
- No generar exports Dify desde documentación.

## Qué queda manual en Dify

- Configurar cada agente constructor con su prompt canónico vigente.
- Definir nodos/handoffs según la granularidad que permita el panel.
- Conectar el routing con n8n solo mediante credenciales gestionadas fuera del repo.
- Exportar la app desde Dify únicamente cuando el panel produzca un export real.
