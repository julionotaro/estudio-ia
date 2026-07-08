# Conector — Sheets

> Tier 1. Estado: ESQUELETADO — backends Google Sheets + Excel 365 listos para
> apuntar credencial. Sin cuenta real todavía.

## Qué hace

Hoja de cálculo de la oficina, usada sobre todo por CONTABILIDAD y DATOS.
Cuatro acciones sobre un contrato JSON: leer, añadir fila, actualizar fila,
buscar fila por valor.

## Backends

| Acción | Google | Microsoft | Nota |
|---|---|---|---|
| leer | Sheets sheet:read | Excel worksheet:readRows | |
| anadir | Sheets sheet:append (autoMap) | Excel worksheet:append (autoMap) | |
| actualizar | Sheets sheet:update | Excel worksheet:update | requiere `columna_clave` para matchear la fila |
| buscar | Sheets sheet:read + filtro | Excel table:lookup | ver nota Excel abajo |

Dispatcher: `Router Accion (switch 4) → Suite <Accion> (switch 2) → nodo`.
Convergen en `Juntar (merge 8) → Salida Normalizada`.

## Workflow

| Workflow | ID |
|---|---|
| `[CONECTOR] Sheets` | `ZYagCbVDMwJwqQu3` |

## Contrato de entrada

```json
{
  "accion": "leer | anadir | actualizar | buscar",
  "suite": "google | microsoft",
  "documento_id": "string  (id del spreadsheet / workbook)",
  "hoja": "string  (nombre de hoja en Google; id de worksheet en Excel)",
  "fila": "object  (anadir/actualizar: datos de la fila, mapeo automático por nombre de columna)",
  "columna_clave": "string  (actualizar: columna que identifica la fila; buscar: columna donde buscar)",
  "valor_busqueda": "string  (buscar: valor a encontrar en columna_clave)"
}
```

Los datos de la fila para añadir/actualizar viajan como campos del item de
entrada (mapeo automático `autoMapInputData` / `autoMap`), no dentro de `fila`
como objeto anidado. Al integrar desde el router, aplanar `fila` al nivel del
item antes de invocar. (Ajuste pendiente de validar en test real.)

## Contrato de salida

```json
{ "ok": true, "resultado": { "cantidad": N, "filas": [ ... ] }, "error": null }
```

## Diferencias por proveedor (documentadas)

- **buscar**: en Google es un `read` con filtro por columna/valor (devuelve
  todas las coincidencias). En Excel es `table:lookup`, que **requiere que los
  datos estén formateados como Tabla de Excel** (no rango suelto). Si el cliente
  Microsoft usa rangos sueltos, cambiar a `worksheet:readRows` + filtro manual.
- **actualizar**: Google usa `matchingColumns` (array); Excel usa
  `columnToMatchOn` (string). Ambos alimentados desde `columna_clave`.
- **hoja**: Google acepta nombre de hoja; Excel espera id de worksheet.

## Credenciales (placeholders)

| Backend | Tipo credencial | Nombre convención |
|---|---|---|
| Google Sheets | `googleSheetsOAuth2Api` | `CRED_SHEETS_GOOGLE_<CLIENTE>` |
| Excel 365 | `microsoftExcelOAuth2Api` | `CRED_SHEETS_EXCEL_<CLIENTE>` |

## Ensamblaje con cliente real

Según `suite` en NEGOCIO.md:
- **google:** credencial Google Sheets OAuth2, apuntar los 4 nodos Sheets.
- **microsoft:** credencial Excel OAuth2, apuntar los 4 nodos Excel; y si se usa
  `buscar`, asegurar que la hoja tiene una Tabla de Excel definida.

## Pendiente antes de promover a activos/

- [ ] Test real de las 4 acciones con la suite que corresponda.
- [ ] Validar el aplanado de `fila` para anadir/actualizar (mapeo automático).
- [ ] Confirmar comportamiento de buscar en Excel con y sin Tabla definida.
- [ ] Normalizar shape de `filas` entre proveedores si el agente lo necesita.
- [ ] Integrar en el router: leer/buscar son lectura (sin aprobación);
      anadir/actualizar son escritura (requieren aprobación).