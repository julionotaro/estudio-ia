# Operational Workflow - Prototype Pending

## Estado

Pendiente de construccion.

## Motivo

Este flujo requiere integracion operativa real con triggers, webhooks, email, almacenamiento, reglas rigidas, acciones externas y comunicaciones.

Debe construirse cuando el entorno Hostinger + Dify self-hosted + n8n este preparado.

## Pipeline previsto

Trigger webhook/email
-> Extraction Agent
-> Filtro Codigo Rigido
-> QA and Compliance Agent
-> Decision luz verde/freno
-> Action Execution
-> Communications Agent

## Componentes

### Trigger

Entrada desde webhook, email, formulario, carga documental o evento externo.

### Extraction Agent

Extrae datos de documentos, emails, adjuntos o payloads.

### Filtro Codigo Rigido

Nodo de codigo o reglas deterministicas para validar datos exactos.

Ejemplos:
- importes
- fechas
- documentos obligatorios
- campos fiscales
- identificadores
- duplicados
- reglas no interpretativas

### QA and Compliance Agent

Revisa consistencia, riesgo, completitud y cumplimiento antes de permitir acciones.

### Decision

Define si el flujo continua, se frena o escala a humano.

Estados esperados:
- green_light
- needs_human_review
- blocked
- retry
- failed

### Action Execution

Ejecuta acciones autorizadas:
- crear registro
- actualizar estado
- enviar a sistema externo
- preparar exportacion
- disparar n8n

### Communications Agent

Prepara o envia comunicaciones al cliente, segun permisos y fase.

## Restriccion actual

No conectar servicios reales todavia.
No usar credenciales.
No enviar emails reales.
No ejecutar acciones externas.
No automatizar decisiones irreversibles sin checkpoint humano.

## Proximo paso futuro

Construir este flujo cuando:
- Dify este exportado y versionado
- n8n este instalado
- Hostinger este preparado
- exista un primer caso operativo real
