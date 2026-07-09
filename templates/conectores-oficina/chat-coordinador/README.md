# Conector — Chat Coordinador

> Tier 1 — transversal (Telegram). Estado: VALIDADO punta a punta con bot propio
> (jul 2026): rama con agente y rama SIN_AGENTE respondiendo por Telegram.
> Datos de negocio en placeholder.

## Qué hace

Puerta de entrada de la oficina. Recibe mensajes de texto por Telegram,
los inyecta al Router de la Oficina como `encargo`, y devuelve la respuesta
del router al chat.

## Flujo

```
Mensaje Telegram (update: message)
  → Armar Encargo (texto → encargo; adjunta nombre/contenido_negocio placeholder)
  → Llamar Router (POST webhook/oficina-encargo)
  → Responder Telegram (entregable || mensaje || answer || fallback)
```

## Workflow

| Workflow | ID | Activado |
|---|---|---|
| `[CONECTOR] Chat Coordinador` | `gcKsrboh2i3t8QwO` | SÍ |

## Bots de Telegram

Un mismo bot de Telegram registra UN webhook en n8n; por eso este conector
usa un bot SEPARADO del de aprobación.

| Bot | Token (id) | Rol | Credencial n8n |
|---|---|---|---|
| `OficinaAprobacionBot_bot` | `8892476860` | Aprobación (callback_query) | `Telegram account` (`RgoHER0Ej0SkXMM2`) |
| `OficinaAprobacionBot1_bot` | `8978260348` | Chat entrada (message) | `Cuenta de Telegram 2` (`qVW0eUQw8xXkN138`) |

Nota: el @username del bot de chat no se puede cambiar en Telegram (solo el
nombre visible, ya renombrado a "Oficina chat Coordinador"). Con cliente real
se crea bot propio + credencial `CRED_CHAT_<CLIENTE>` y se reapuntan
`Mensaje Telegram` y `Responder Telegram`.

## Shape de respuesta del Router (confirmado jul 2026)

El webhook del router responde con el último nodo ejecutado. Variantes vistas:

| Rama | Shape |
|---|---|
| Entrega directa (agente sin aprobación) | `{ estado: "ENTREGADO", entregable }` |
| Área sin agente conectado | `{ estado: "SIN_AGENTE", mensaje }` |
| Rama de aprobación | pendiente de confirmar shape al reanudar |

El nodo `Responder Telegram` cubre las tres:
`{{ $json.entregable || $json.mensaje || $json.answer || "Encargo recibido." }}`.

Límite conocido: Telegram corta mensajes > 4096 caracteres. Entregables largos
pueden fallar el envío — partir/truncar al industrializar.

## APRENDIZAJE — Asignación de credenciales vía MCP (n8n)

`setNodeParameter` con path `/credentials` NO asigna credenciales: las anida
dentro de `parameters` y n8n las ignora. **Fallo silencioso**: el publish pasa
OK pero el Telegram Trigger no puede llamar a la API de Telegram y no registra
su webhook (`getWebhookInfo` queda con `url:""`; los POST entrantes dan 403
"webhook not registered").

Asignación correcta vía MCP:
1. Si `parameters` quedó contaminado con `credentials`, limpiarlo con
   `updateNodeParameters` (`replace: true`) dejando solo los parámetros reales.
2. Operación `setNodeCredential` con `credentialKey: telegramApi` (clave
   estándar del nodo), `credentialId` y `credentialName`.
3. Despublicar + publicar. n8n registra el webhook solo (verificable con
   `getWebhookInfo`: debe aparecer la URL `https://.../webhook/<webhookId>/webhook`).

Diagnóstico útil: si el trigger de Telegram no responde, consultar
`getWebhookInfo` del token. `url:""` = n8n nunca registró (credencial mal
asignada o token inválido). `url` correcta + 403 = registro manual sin entrada
interna en n8n (no registrar a mano; dejar que n8n lo haga al publicar).

## Datos de negocio (placeholder)

El nodo `Armar Encargo` rellena `nombre_negocio` y `contenido_negocio` con
valores placeholder. Con cliente real: leerlos de NEGOCIO.md o fijarlos en
ese nodo. El `encargo` sí sale del mensaje real.

## Contrato hacia el Router

POST `http://187.127.233.43:5678/webhook/oficina-encargo`
```json
{ "encargo": "<texto del mensaje>", "nombre_negocio": "...", "contenido_negocio": "..." }
```

Nota: la URL del router es HTTP por IP. Al industrializar, migrar a
`https://studio-julio.duckdns.org/webhook/oficina-encargo` (ya hay ruta
nginx para `/webhook/`).

## Pendiente antes de promover a activos/

- [x] Crear bot de entrada separado y validar recepción real. (jul 2026)
- [x] Confirmar shape real de la respuesta del router (entregable/mensaje).
- [ ] Parametrizar nombre_negocio/contenido_negocio desde NEGOCIO.md.
- [ ] Migrar URL del router a HTTPS.
- [ ] Manejar mensajes que no son texto (fotos, documentos) — hoy asume texto.
- [ ] Partir/truncar entregables > 4096 chars (límite Telegram).
- [ ] Confirmar shape de la rama de aprobación cuando exista el dispatcher.
