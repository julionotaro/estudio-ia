# Contrato estándar — Conectores genéricos de oficina

> Spec v0 — investigación `[HERRAMIENTAS] Conectores genéricos como activos MCP para la oficina` (Laboratorio, jul 2026).
> Complementa el bloque `instruccion_accion` de la Oficina de agentes (templates/oficina/).

## Principio

Un conector = un subworkflow n8n con contrato JSON único. Los agentes y el router
hablan contra el contrato, nunca contra el proveedor. El backend (Google / Microsoft /
genérico) se resuelve por configuración, no por código.

## Entrada

```json
{
  "herramienta": "mail | sheets | storage | chat | aprobacion | calendario | gen_documentos | extraccion_documentos",
  "accion": "string (ver catálogo de acciones por conector)",
  "parametros": { },
  "area_origen": "TRAFICO | AUXILIAR | CONTABILIDAD | DATOS | CONTENIDO | COORDINADOR",
  "suite": "google | microsoft | generico"
}
```

- `suite` la inyecta el dispatcher leyendo NEGOCIO.md del cliente; el agente NO la emite.
- `parametros` es específico de cada acción y se documenta en el README de cada conector.

## Salida

```json
{
  "ok": true,
  "resultado": { },
  "error": null
}
```

- Si `ok: false` → `resultado: null` y `error: { codigo, mensaje, detalle }`.
- Códigos de error estándar: `CREDENCIAL_INVALIDA`, `PARAMETROS_INVALIDOS`,
  `NO_ENCONTRADO`, `PROVEEDOR_ERROR`, `NO_IMPLEMENTADO`.
- El router NUNCA interpreta errores de proveedor: los propaga tal cual al canal de aprobación/notificación.

## Suites y backends

| Conector | Backend Google | Backend Microsoft | Genérico |
|---|---|---|---|
| mail | Gmail | Outlook | IMAP/SMTP cubre ambos ✔ (backend único) |
| sheets | Google Sheets | Excel 365 (Graph API) | No existe — doble implementación |
| storage | Drive | OneDrive/SharePoint | WebDAV parcial — preferir nativo |
| calendario | Google Calendar | Outlook Calendar | CalDAV parcial — preferir nativo |
| chat | Telegram (transversal, no depende de suite) | | |
| aprobacion | Telegram (transversal) | | |
| gen_documentos | Interno (plantilla → PDF/docx), sin suite | | |
| extraccion_documentos | Interno (Dify soporta ficheros) — a decidir en Fase 3 | | |

Regla: `NEGOCIO.md` de cada cliente define `suite: google | microsoft`. El dispatcher
enruta al backend correcto. Añadir un backend nuevo no toca ni router ni agentes.

## Credenciales

Placeholders con nombre convenido, una credencial n8n por conector y cliente:

```
CRED_MAIL_<CLIENTE>
CRED_SHEETS_<CLIENTE>
CRED_STORAGE_<CLIENTE>
CRED_CALENDARIO_<CLIENTE>
CRED_CHAT_<CLIENTE>
```

Ensamblar con cliente real = crear credenciales + apuntar. Cero edición de workflow.
Prohibido hardcodear keys en nodos (aplica también al Router v0, pendiente #3 de continuidad).

## Relación con instruccion_accion

El bloque `instruccion_accion` que emiten los agentes (estado PENDIENTE_APROBACION)
es la capa de intención. Tras aprobación humana, el dispatcher lo traduce a una o
varias llamadas de este contrato. La aprobación sigue siendo regla dura universal:
ningún conector con efecto de escritura se invoca sin aprobación previa.

Acciones de solo lectura (leer mail, leer rango, listar archivos) NO requieren
aprobación: los agentes las necesitan para razonar. La frontera es escritura en
sistema externo.

## Doble consumo

Cada conector se expone por dos puertas sobre el mismo subworkflow:
1. **Producción:** llamado por el dispatcher del Oficina Router.
2. **MCP (Studio-julio):** para uso de Claude en diseño y debug.

## Criterio de promoción a activos/

Un conector se promueve individualmente cuando: (a) pasa tests con cuenta dummy,
(b) su README documenta acciones + parámetros + credencial, (c) no contiene nada
de dominio de cliente. No se promueve el paquete entero en bloque.