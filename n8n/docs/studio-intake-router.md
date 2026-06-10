# n8n Studio Intake Router

## Propósito

`Studio Intake Router` es el punto de entrada operativo entre AI Studio Director y GitHub. Su responsabilidad es recibir pedidos estructurados, clasificarlos por modo, crear o actualizar issues en `julionotaro/estudio-ia` y devolver el estado para que AI Studio Director lo comunique a Julio.

## Principios

- AI Studio Director no toca GitHub directamente.
- GitHub se toca indirectamente vía n8n.
- Codex ejecuta únicamente issues o PRs bien definidos.
- n8n no debe almacenar secretos en documentación ni payloads versionados.
- No se debe inventar un workflow n8n si el export real no está disponible.

## Entrada esperada

```json
{
  "source": "ai_studio_director",
  "project_id": "studio_ia_core",
  "mode": "design | build | qa | deploy | docs",
  "summary": "Resumen breve del pedido",
  "description": "Contexto completo para operar",
  "brief": {},
  "approved_by_julio": true,
  "target_repo": "julionotaro/estudio-ia",
  "requested_action": "create_github_issue | update_github_issue",
  "constraints": ["no secrets", "no production without explicit approval"]
}
```

## Enrutamiento por modo

| Modo | Acción n8n | Resultado |
|---|---|---|
| `design` | Crear issue de Discovery, Brief, requerimientos, arquitectura, ARC o UX. | Issue con criterios de aceptación de diseño. |
| `build` | Crear issue implementable con archivos, alcance y validaciones. | Issue lista para Codex. |
| `qa` | Crear issue de revisión o checklist de QA. | Issue con checklist y evidencia esperada. |
| `deploy` | Crear issue o guía de deployment sin ejecutar producción. | Issue con pasos manuales y autorización requerida. |
| `docs` | Crear issue de documentación o decisiones. | Issue con documentos objetivo. |

## Criterios mínimos para issue lista para Codex

Una issue puede pasar a Codex solo si contiene:

- repo exacto: `julionotaro/estudio-ia`;
- objetivo claro;
- alcance explícito;
- archivos o áreas esperadas;
- criterios de aceptación;
- validaciones obligatorias;
- hard stops aplicables;
- confirmación de que no requiere secretos, tokens, API keys ni producción.

## Salida esperada

```json
{
  "status": "created | updated | blocked",
  "github_issue_url": "https://github.com/julionotaro/estudio-ia/issues/123",
  "mode": "build",
  "message_for_director": "Issue creada y lista para Codex.",
  "manual_steps": []
}
```

## Pendiente manual

El workflow real debe configurarse en el panel de n8n y exportarse cuando esté disponible. Este documento define el contrato operativo, no afirma que exista un export importable.
