# Herramientas Oficina — activos reutilizables

> Tres herramientas genéricas parametrizadas + el contrato entre agentes.
> Cada una probada de forma unitaria con datos dummy.
> **Cero contenido de dominio de ningún cliente.** Todo parámetro entra por
> el webhook; nada hardcodeado.
>
> Origen: Laboratorio Estudio Desarrollo IA, jul 2026.

## Contenido

| Archivo | Qué es |
|---|---|
| `CONTRATO-coordinador-auxiliar.md` | Contrato de mensajes entre agentes, decisiones y regla de escalado |
| `lector-buzon.json` | Export del workflow Lector de Buzón |
| `archivador-drive.json` | Export del workflow Archivador Drive |
| `aprobacion-telegram.md` | Patrón del loop de aprobación (vive en el router) |

---

## 1. Lector de Buzón

Lee un buzón Gmail con filtros, descarga los adjuntos como binarios y
devuelve metadatos estructurados.

**Endpoint:** `POST /webhook/lector-buzon`
**Workflow n8n:** `[ACTIVO] Lector Buzon`
**Credencial:** Gmail OAuth2

### Parámetros (body JSON, todos opcionales)

| Parámetro | Tipo | Defecto | Qué hace |
|---|---|---|---|
| `filtro_remitente` | string | — | `from:` de Gmail |
| `filtro_asunto` | string | — | `subject:` de Gmail |
| `con_adjuntos` | bool | false | solo mensajes con adjunto |
| `recibido_despues` | string | — | fecha `AAAA/MM/DD` |
| `limite` | number | 10 | máximo de mensajes |
| `solo_no_leidos` | bool | false | solo no leídos |
| `descargar_adjuntos` | bool | true | descarga binarios |

### Respuesta

```json
{ "ok": true, "cantidad": 2,
  "mensajes": [
    { "id": "...", "hilo": "...", "de": "...", "para": "...",
      "asunto": "...", "fecha": "ISO",
      "adjuntos": [ { "campo_binario": "adjunto_0", "nombre": "x.pdf",
                      "mime": "application/pdf", "tamano": 12345 } ] }
  ] }
```

Los binarios quedan disponibles en el nodo `Leer Buzon` con prefijo
`adjunto_` (adjunto_0, adjunto_1...) para encadenar con otra herramienta.

### Adaptación a un proyecto nuevo
Cambiar la credencial Gmail por la del cliente. Nada más.

---

## 2. Archivador Drive

Recibe un archivo en base64 y lo archiva bajo una ruta lógica
`{raiz}/{año}/{mes}/{cliente}`, creando las carpetas que falten. Idempotente:
si las carpetas existen, las reutiliza.

**Endpoint:** `POST /webhook/archivador-drive`
**Workflow n8n:** `[ACTIVO] Archivador Drive`
**Credencial:** Google Drive OAuth2

### Parámetros (body JSON)

| Parámetro | Tipo | Req | Defecto | Qué hace |
|---|---|---|---|---|
| `contenido_b64` | string | Sí | — | contenido del archivo en base64 |
| `nombre_archivo` | string | Sí | — | nombre final |
| `carpeta_raiz_id` | string | No | `root` | **parámetro de instalación**: ID de la carpeta raíz |
| `cliente` | string | No | `general` | último nivel de la ruta |
| `anio` | string | No | año actual | nivel 1 |
| `mes` | string | No | mes actual (2 dígitos) | nivel 2 |
| `mime_type` | string | No | `application/octet-stream` | MIME del archivo |

### Respuesta

```json
{ "ok": true, "file_id": "1EU...", "nombre": "x.pdf",
  "enlace": null, "carpeta_id": "1lK...",
  "ruta": "2026/07/cliente-test", "error": null }
```

### Estructura interna
Por cada nivel (año, mes, cliente): Buscar → Resolver → IF existe? →
(tomar existente | crear) → Merge. Luego Convertir base64 a binario → Subir.

### Adaptación a un proyecto nuevo
Cambiar la credencial de Drive y pasar `carpeta_raiz_id` del cliente.
Si la jerarquía deseada es otra, se replica el bloque de 6 nodos por nivel.

---

## 3. Loop de aprobación Telegram

Envía un mensaje con botones Aprobar/Rechazar, suspende la ejecución hasta
la respuesta humana y continúa por la rama correspondiente.

**Ubicación:** nodos `Solicitar Aprobacion` + `Esperar Aprobacion` +
`Resolver Aprobacion` dentro del router de la oficina.
**Credencial:** Telegram Bot API

### Parámetros

| Parámetro | Qué hace |
|---|---|
| `chat_id` | destino del mensaje (parámetro de instalación) |
| `texto` | cuerpo del mensaje de aprobación |
| `resume_url` | URL de reanudación que n8n inyecta en los botones |

### Respuesta
`{ decision: "aprobar" | "rechazar" }` — la rama continúa según el valor.

### Reglas operativas (aprendidas en producción)
- `parse_mode: HTML` explícito y escapar `& < >` de cualquier texto
  interpolado. Sin esto, contenido con guiones bajos rompe el envío (400
  "can't parse entities").
- Tras cualquier cambio de credencial o ciclo de publicación, verificar
  `getWebhookInfo` de todos los bots afectados. `url:""` = n8n no registró.

---

## Pruebas unitarias realizadas

| Herramienta | Prueba | Resultado |
|---|---|---|
| Lector de Buzón | lectura con `limite: 2` sobre buzón real | 2 mensajes con metadatos completos |
| Archivador Drive | archivo dummy → `2026/07/cliente-test` | carpetas creadas + file ID devuelto |
| Archivador Drive | segundo archivo, misma ruta | mismo `carpeta_id`, sin duplicar carpetas (idempotencia) |
| Aprobación Telegram | aprobado | acción ejecutada, envio real |
| Aprobación Telegram | rechazado | estado RECHAZADO, nada ejecutado |

## Verificación de neutralidad de dominio

Revisado: los tres workflows y el contrato no contienen nombres de clientes,
terminología de negocio, direcciones reales ni identificadores de carpetas
de producción. Los únicos valores de ejemplo son `cliente-test` y
`prueba-archivador.txt`, usados en las pruebas unitarias.
