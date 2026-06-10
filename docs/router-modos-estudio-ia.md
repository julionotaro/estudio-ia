# Router de modos del Estudio IA

## Objetivo

El router clasifica cada pedido para activar el equipo correcto sin saltar aprobaciones ni hard stops.

## Modos canónicos

| Modo | Cuándo usarlo | Equipo principal | Salida esperada |
|---|---|---|---|
| `design` | Discovery, Brief, requerimientos, arquitectura, ARC o UX. | AI Studio Director, AI Project Manager, BA, Architect, Tech Lead, UX Architect. | Brief aprobado, requerimientos, ARC, arquitectura, specs o UX. |
| `build` | Implementación frontend, backend, base de datos o integraciones. | Backend Builder, Database Agent, Integration Agent, UI Designer, Frontend Builder. | Código o especificación implementable asociada a issue/PR. |
| `qa` | Revisión, pruebas, validación técnica o visual. | Backend QA, UX QA, Integration QA. | Reporte QA con hallazgos, bloqueo o aprobación. |
| `deploy` | Publicación, Vercel, Supabase, Hostinger, variables o verificación post-deploy. | Deploy Agent. | Guía paso a paso o checklist de deployment. |
| `docs` | Documentación, manuales, decisiones y runbooks. | Documenter. | Documentos versionados o actualización de decisiones. |

## Reglas de decisión

### `design`

Usar `design` cuando el pedido requiera entender el problema, generar Brief, definir requerimientos, tomar decisiones de arquitectura, completar ARC o diseñar UX antes de construir.

### `build`

Usar `build` cuando ya exista contexto suficiente y el trabajo sea construir frontend, backend, base de datos o integraciones. Si falta Brief, requerimientos o specs, volver a `design`.

### `qa`

Usar `qa` cuando la tarea sea revisar, probar, validar o comparar contra criterios de aceptación. QA no debe ampliar alcance ni corregir sin issue específica.

### `deploy`

Usar `deploy` cuando el pedido trate sobre publicación, variables, Vercel, Supabase, Hostinger o verificación post-deploy. No publicar producción sin autorización explícita.

### `docs`

Usar `docs` cuando el pedido sea registrar decisiones, crear manuales, actualizar runbooks o documentar flujos.

## Reglas especiales

- Si el pedido menciona secretos, tokens o API keys, activar hard stop.
- Si el pedido requiere producción, pedir autorización explícita antes de avanzar.
- Si el pedido no pertenece a `julionotaro/estudio-ia`, detenerse.
- Si no hay export real de Dify o workflow real de n8n, documentar pendiente en vez de inventarlo.
