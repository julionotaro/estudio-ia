# Oficina de agentes — plantillas (EN INVESTIGACIÓN)

**Estado: sin validar con cliente. No es un activo.**

Origen: investigación `[OFICINA] Oficina de agentes como producto vendible`,
Laboratorio, julio 2026.

## Qué hay acá

- `prompt-coordinador.md` — system prompt del agente coordinador (Dify).
  Recibe encargos en lenguaje natural, clasifica por área y devuelve JSON
  para que n8n enrute.
- `NEGOCIO-plantilla.md` — plantilla de contexto por cliente. Es la unidad
  de replicación de la oficina: un archivo por cliente, inyectado en el
  system prompt del coordinador y de cada agente de área.

## Áreas definidas (v0)

CONTENIDO · DATOS · TRAFICO (coordinación de flota, cargas/descargas,
seguimiento de vehículos) · CONTABILIDAD · AUXILIAR (administración,
incluidos trámites y permisos).

## Regla de la plantilla

Acá solo vive estructura genérica. El dominio de cada cliente (sistemas,
organismos, terminología) va en el NEGOCIO.md de ese cliente, nunca en
estas plantillas.

## Arquitectura de referencia

Coordinador (Dify) → áreas (agentes Dify con rol persistente) → entrega y
aprobación vía n8n + Telegram (patrón validado en el estudio). El coordinador
es la puerta de la oficina; el Studio Intake Router sigue siendo la puerta de
la fábrica. Coexisten: son necesidades distintas.

## Criterio de promoción

Cuando se valide con el primer cliente, mover a `activos/oficina-minima/`
y actualizar la nota de origen con el cliente que lo validó.
