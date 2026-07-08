# Conector — Gen Documentos

> Tier 2 — interno (sin suite). Estado: ESQUELETADO. HTML funcional; PDF requiere
> Gotenberg en el VPS (pendiente de infra).

## Qué hace

Genera documentos de la oficina (facturas, informes, cartas) a partir de una
plantilla HTML con placeholders `{campo}` y un objeto de datos. Salida en HTML
o PDF.

## Workflow

| Workflow | ID |
|---|---|
| `[CONECTOR] Gen Documentos` | `oRl4jRXvuKnDKMvO` |

Flujo: `Entrada → Renderizar Plantilla (Code: reemplaza {campo} por datos)
→ Router Formato → Archivo HTML | Generar PDF Gotenberg → Salida`.

## Contrato de entrada

```json
{
  "accion": "generar",
  "formato": "html | pdf",
  "plantilla_html": "string con placeholders {campo}",
  "datos": { "campo": "valor", ... },
  "nombre_archivo": "string sin extension"
}
```

## Contrato de salida

```json
{ "ok": true, "resultado": { "generado": true, "formato": "...", "nombre_archivo": "..." }, "error": null }
```
+ binario `data` con el archivo generado.

## Infra pendiente: Gotenberg (para PDF)

n8n no genera PDF nativamente. La rama PDF llama a Gotenberg, un servicio
Docker de conversión HTML→PDF vía Chromium. Instalar en el VPS:

```yaml
# añadir al docker-compose de n8n (/opt/estudio-ia/n8n/)
  gotenberg:
    image: gotenberg/gotenberg:8
    restart: unless-stopped
```

Luego reemplazar en el nodo `Generar PDF Gotenberg` la URL placeholder
`http://PLACEHOLDER_GOTENBERG:3000/...` por `http://gotenberg:3000/...`
(mismo network de Docker) o la IP interna que corresponda.

NOTA: el envío multipart a Gotenberg requiere el HTML como archivo
`files` con nombre `index.html` — el nodo actual envía el HTML como campo
de formulario; al activar la rama PDF, ajustar a binario (pendiente de
test real, la rama HTML no tiene esta limitación).

## La rama HTML funciona sin infra extra

`formato: html` produce el archivo directamente con nodos nativos. Para
muchos casos de oficina (enviar por mail, archivar) el HTML es suficiente
y el PDF puede posponerse.

## Pendiente antes de promover a activos/

- [ ] Levantar Gotenberg en el VPS y probar rama PDF (ajustar multipart).
- [ ] Test real rama HTML.
- [ ] Plantillas de ejemplo (factura, informe) en esta carpeta.
- [ ] Integrar en el router: generar es interno (no toca sistema externo),
      NO requiere aprobación; lo que se haga con el documento después
      (enviarlo, subirlo) sí pasa por mail/storage con sus reglas.