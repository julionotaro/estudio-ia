# Matriz de prompts canónicos y agentes Dify

## Regla principal

Los prompts canónicos existentes en `prompts/` son la fuente de verdad. Dify debe actualizarse manualmente con esos prompts y luego exportarse. Esta matriz no reemplaza los prompts: solo documenta qué agente debe usar cada archivo.

## Agentes de dirección y diseño

| Agente Dify | Prompt canónico | Fase | Responsabilidad |
|---|---|---|---|
| AI Studio Director | `prompts/design-phase/00_client_liaison.md` | Todas | Interlocutor principal de Julio, Discovery, Brief, coordinación interna y comunicación final. |
| AI Project Manager | `prompts/design-phase/08_project_manager.md` | Diseño / Construcción | Recibe el Brief aprobado y coordina BA, Architect, Tech Lead y UX. |
| Business Analyst | `prompts/design-phase/01_business_analyst.md` | Diseño | Convierte el Brief en requerimientos funcionales y reglas de negocio. |
| System Architect | `prompts/design-phase/02_system_architect.md` | Diseño | Diseña arquitectura y completa ARC antes de presentarla. |
| Tech Lead | `prompts/design-phase/03_tech_lead.md` | Diseño | Traduce arquitectura aprobada en especificaciones técnicas y tareas para constructores. |
| UX Architect | `prompts/design-phase/04_ux_architect.md` | Diseño | Define experiencia de usuario, pantallas, navegación, estados y flujos. |

## Agentes de construcción

| Agente Dify | Prompt canónico | Modo router | Responsabilidad |
|---|---|---|---|
| Backend Builder | `prompts/builder-phase/05_backend_builder.md` | `build` | Construye APIs, lógica de servidor y conexiones a datos desde specs del Tech Lead. |
| Database Agent | `prompts/builder-phase/06_database_agent.md` | `build` | Genera esquema, relaciones, índices, políticas y datos iniciales. |
| Integration Agent | `prompts/builder-phase/07_integration_agent.md` | `build` | Conecta servicios externos, autenticación, pagos, email, APIs y storage. |
| UI Designer | `prompts/builder-phase/10_ui_designer.md` | `build` | Convierte wireframes en componentes visuales React/Tailwind de alta fidelidad. |
| Frontend Builder | `prompts/builder-phase/11_frontend_builder.md` | `build` | Construye páginas, rutas, estado, formularios e integración con backend. |

## Agentes de soporte, QA, deploy y documentación

| Agente Dify | Prompt canónico | Modo router | Responsabilidad |
|---|---|---|---|
| Backend QA | `prompts/support-phase/09_backend_qa.md` | `qa` | Verifica que backend cumpla specs antes de integración. |
| UX QA | `prompts/support-phase/12_ux_qa.md` | `qa` | Evalúa experiencia de usuario como usuario final. |
| Integration QA | `prompts/support-phase/13_integration_qa.md` | `qa` | Prueba sistema completo frontend + backend e integraciones. |
| Deploy Agent | `prompts/support-phase/14_deploy_agent.md` | `deploy` | Genera guía paso a paso para despliegue; no ejecuta comandos por el usuario. |
| Documenter | `prompts/support-phase/15_documenter.md` | `docs` | Genera manuales, troubleshooting y registro de decisiones. |

## Orden operativo mínimo

1. AI Studio Director conversa con Julio.
2. En proyecto nuevo, AI Studio Director activa Discovery y genera Brief.
3. Julio aprueba el Brief.
4. AI Project Manager recibe el Brief aprobado.
5. AI Project Manager coordina BA, Architect, Tech Lead y UX.
6. n8n crea issues operables en GitHub.
7. Codex ejecuta únicamente issues o PRs bien definidos.
8. AI Studio Director comunica el estado final.

## Notas de activación manual

- Crear o actualizar cada agente en Dify copiando el prompt correspondiente.
- No pegar secretos, tokens ni API keys en prompts o variables.
- No inventar exports de Dify si no fueron generados desde el panel.
- Registrar cada actualización relevante en `projects/studio_ia_core/decisions.md`.
