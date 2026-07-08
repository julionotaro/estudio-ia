# Conector — Extraccion Documentos

> Tier 2 — interno (sin suite). Estado: ESQUELETADO. Extracción de texto PDF
> funcional (nodo nativo); estructuración vía Dify con app key placeholder.

## Qué hace

El inverso de gen-documentos: recibe un PDF (factura de proveedor, albarán,
contrato) y devuelve datos estructurados en JSON según un esquema pedido.
Alimenta a CONTABILIDAD (nadie tipea facturas a mano).

## Workflow

| Workflow | ID |
|---|---|
| `[CONECTOR] Extraccion Documentos` | `Cn75FQkKjbAlKCp8` |

Flujo: `Entrada (binario data = PDF) → Extraer Texto PDF (nodo nativo)
→ Estructurar con Dify (prompt de extracción + esquema) → Salida (parsea JSON)`.

## Contrato de entrada

```json
{
  "accion": "extraer",
  "esquema": "string — lista de campos deseados, ej: 'numero_factura, proveedor, fecha, total'",
  "nombre_negocio": "string — contexto para el extractor"
}
```
+ binario `data` con el PDF.

## Contrato de salida

```json
{ "ok": true, "resultado": { "datos": { "numero_factura": "...", ... } }, "error": null }
```

Si el extractor no devuelve JSON válido: `ok: false` con
`error.codigo: PROVEEDOR_ERROR` y el texto crudo en `detalle`.

## Decisión de diseño: Dify como estructurador

La extracción del TEXTO la hace el nodo nativo de n8n (extractFromFile:pdf,
sin costo, sin dependencia). La ESTRUCTURACIÓN (texto → campos) la hace un
LLM vía Dify, reutilizando el stack existente. Alternativas descartadas por
ahora: OCR dedicado (Tesseract, servicios cloud) — solo necesario si llegan
PDFs escaneados (imagen) en vez de PDFs con texto.

LIMITACIÓN CONOCIDA: PDFs escaneados (imagen pura) devuelven texto vacío.
Detectarlo (text.length < umbral) y en ese caso derivar a OCR es mejora v1.

## Configuración pendiente (con o sin cliente)

1. Crear un chatflow/agente en Dify para extracción (o reutilizar uno con
   variables nombre_negocio/contenido_negocio, como los 5 de la oficina).
2. Publicar con API y reemplazar `PLACEHOLDER_DIFY_APP_KEY_EXTRACCION` en el
   nodo `Estructurar con Dify`.
3. (Pendiente #3 del router aplica acá también: mover la key a credencial
   n8n httpHeaderAuth en vez de header hardcoded.)

## Pendiente antes de promover a activos/

- [ ] Crear el chatflow de extracción en Dify + app key.
- [ ] Test real con factura PDF de ejemplo.
- [ ] Manejo de PDF escaneado (detectar texto vacío → error claro o rama OCR).
- [ ] Mover app key a credencial n8n.
- [ ] Integrar en el router: extraer es lectura/interno, NO requiere aprobación.