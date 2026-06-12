# Changelog

## v0.5.0 — Endurecimiento del Equipo Constructor

- Builder agents (05, 06, 07, 10, 11): agregadas REGLAS DE RAZONAMIENTO + estructura obligatoria de output con BUILD_STATUS al inicio (inventario extraído de specs, gate tolerante "ante la duda, continuar", supuestos declarados) y VERIFICACIÓN al cierre (cobertura 100% del inventario + deuda técnica declarada).
- QA agents (09, 12, 13) transformados en auditores reales: check espejo de entregables (specs ↔ BUILD_STATUS ↔ código), entregable ausente o bloqueo falso = violación CRÍTICA = RECHAZADO obligatorio, línea de VEREDICTO en formato exacto.
- Mismo método verificado en el Equipo de Diseño (generalización 9,5/11; fix corrida Tyrion #42 → #46).


## v0.4.1

- Inicialización del repositorio del Estudio IA.
- Separación de prompts por fase.
- Preparación para exportar/importar apps Dify como DSL/YAML.
- Preparación para migración futura a Hostinger VPS.
- Estructura inicial para n8n self-hosted.
- ARC obligatorio como plantilla base.
