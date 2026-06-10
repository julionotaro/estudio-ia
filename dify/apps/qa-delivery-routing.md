# QA Delivery — Routing Dify

## Alcance

Este archivo documenta el routing de QA, deploy guiado y documentación de entrega. No contiene prompts canónicos ni exports de Dify.

## Agentes y prompts canónicos

| Agente Dify | Prompt canónico | Responsabilidad |
|---|---|---|
| Backend QA | `prompts/support-phase/09_backend_qa.md` | Validar backend contra specs y contratos. |
| UX QA | `prompts/support-phase/12_ux_qa.md` | Evaluar experiencia, flujos, mensajes y estados. |
| Integration QA | `prompts/support-phase/13_integration_qa.md` | Probar sistema completo frontend + backend. |
| Deploy Agent | `prompts/support-phase/14_deploy_agent.md` | Generar guía paso a paso de deployment; no ejecutar. |
| Documenter | `prompts/support-phase/15_documenter.md` | Crear manuales, troubleshooting y documentación final. |

## Entrada requerida

- Entregable o código a validar.
- Specs técnicas y contratos esperados.
- UX o flujos principales.
- Reportes previos de QA si existen.
- Estado de aprobación del sistema.
- Restricciones operativas y plataforma objetivo cuando aplique.

## Secuencia recomendada

1. `Backend QA` valida endpoints, contratos, seguridad y manejo de errores.
2. `UX QA` valida flujos principales desde perspectiva de usuario final.
3. `Integration QA` se ejecuta solo cuando Backend QA y UX QA están aprobados o existe excepción humana documentada.
4. `Deploy Agent` genera guía de publicación únicamente si el sistema está aprobado para release.
5. `Documenter` prepara documentación final con Brief, arquitectura, specs, decisiones y resultados de QA.

## Rutas de salida

| Condición | Destino | Resultado esperado |
|---|---|---|
| Backend falla | Builder Team | Lista accionable de correcciones backend. |
| UX falla | Builder Team | Lista accionable de correcciones frontend/UI. |
| Integración falla | Builder Team | Diagnóstico de contrato, datos o flujo roto. |
| QA aprobado | Deploy Agent | Guía manual de deployment. |
| Entrega lista | Documenter | Manuales y documentación de cierre. |
| Decisión humana pendiente | AI Studio Director | Pregunta concreta para Julio. |

## Contrato conceptual de cierre

```text
source_app: QA Delivery
project_id: proyecto activo
mode: qa | deploy | docs
summary: resultado de validación o entrega
context: reportes QA; criterios aprobados; fallas; decisiones; guía o documentación generada
approved_by_julio: true | false
requested_action: request_fixes | prepare_deploy_guide | generate_docs | ask_human
constraints: no secrets; no ejecución en producción; no paneles externos
```

## Criterios para deploy guiado

- Backend QA aprobado o excepción documentada.
- UX QA aprobado o excepción documentada.
- Integration QA aprobado para los flujos principales.
- Plataforma objetivo confirmada.
- Variables de entorno identificadas por nombre, pero sin valores secretos.
- Autorización humana para cualquier paso de producción.

## Qué queda manual en Dify

- Crear o actualizar agentes de QA y entrega con sus prompts canónicos.
- Configurar handoffs de fallas hacia Builder Team.
- Configurar handoff de decisiones hacia AI Studio Director.
- Ejecutar pruebas reales, revisar resultados y exportar desde el panel cuando corresponda.
