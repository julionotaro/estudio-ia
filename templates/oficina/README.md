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
incluidos trámites y permisos DGT).

## Arquitectura de referencia

Coordinador (Dify) → áreas (agentes Dify con rol persistente) → entrega y
aprobación vía n8n + Telegram (patrón Tyrion). Sin Hermes/Aion: todo sobre
el stack del estudio.

## Criterio de promoción

Cuando se valide con el primer cliente, mover a `activos/oficina-minima/`
y actualizar la nota de origen con el cliente que lo validó.
