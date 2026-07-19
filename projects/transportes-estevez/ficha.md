# Ficha — Transportes Estevez

## Cliente
Grupo transportista de líquidos, Villagarcía de Arousa (Pontevedra).
Dos firmas: Hermanos Estevez Casal y Transliquidos Estevez.
Contacto interno: Julio (administrativo, con proyección a tráfico y facturación).

## Producto
**Arousa** (nombre provisional) — asistente administrativo agéntico para el puesto de
recepción documental, carga de viajes y facturación.

Primera validación real de la **Oficina de Agentes** (`templates/oficina/`):
AUXILIAR cubre administración hoy; TRÁFICO y CONTABILIDAD quedan alineados con la
evolución prevista del puesto (admin → tráfico → facturación).

## Estado
- Fase 0: definición de contrato de datos y catálogo maestro. **En curso.**
- Repo cliente: pendiente de creación.

## Alcance por fases
1. **F1 — Contrato de datos:** esquema de viaje, catálogo maestro (clientes, rutas, materiales, flota), reglas de cálculo (km cargados/vacíos, IVA P/PI, indexación).
2. **F2 — Extracción:** chatflow Dify foto/scan → JSON estructurado (hoja principal + albarán/CMR). Reutiliza el blocker pendiente de la Oficina.
3. **F3 — Validación y salida:** n8n valida contra tarifas/indexación, calcula km, y entrega por Telegram la "línea Gesruta" lista para cargar + propuesta de archivo.
4. **F4 — Facturación quincenal:** apoyo a pro-forma (chequeo referencia/placa/ruta/material/cantidad/indexación).

## Restricción clave
Gesruta es aplicación **Windows desktop en ordenador de la empresa**: sin API ni RPA web.
La automatización termina en "carga asistida" (línea lista para tipear). RPA desktop
queda aparcado hasta conocer permisos sobre el equipo.

## Regla de aislamiento
Todo el dominio (clientes, tarifas, Gesruta, rutas) vive en el repo del cliente.
A `estudio-ia` solo vuelven patrones estructurales validados.
