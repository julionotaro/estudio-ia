# Estado — Estudio IA Core

## Fecha

2026-06-10

## Estado actual

`operating_system_initial`

El Estudio IA cuenta con documentación mínima para operar con AI Studio Director, agentes canónicos, router n8n, Registro de Proyectos, reglas de enrutamiento y hard stops.

## Flujo activo documentado

```text
Julio
→ AI Studio Director
→ n8n Studio Intake Router
→ Equipo Dify correspondiente
→ GitHub issue
→ Codex
→ PR
→ estado final devuelto por AI Studio Director
```

## Listo

- AI Studio Director definido como interlocutor principal de Julio.
- Brief definido como salida del modo Discovery del AI Studio Director.
- AI Project Manager definido como receptor del Brief aprobado.
- GitHub definido como acceso indirecto vía n8n.
- Codex limitado a issues/PRs bien definidos.
- Matriz de agentes Dify documentada con prompts canónicos.
- Registro mínimo de proyecto creado.
- Hard stops documentados.

## Manual pendiente

- Actualizar Dify manualmente con los prompts canónicos de `prompts/`.
- Exportar configuración real desde Dify cuando esté disponible.
- Crear/configurar el workflow real `Studio Intake Router` en n8n.
- Exportar workflow real desde n8n cuando esté disponible.
- Configurar credenciales de GitHub en n8n sin versionar secretos.

## Riesgos

- Dify y n8n pueden quedar desalineados si se editan manualmente sin exportar cambios.
- Una issue mal definida puede hacer que Codex ejecute un alcance incorrecto.
- Producción, secretos y datos reales requieren controles manuales explícitos.
