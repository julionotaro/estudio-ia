# Conector — Chat Coordinador

> Tier 1 — transversal (Telegram). Estado: ACTIVO — validado con bot propio
> (jul 2026). Datos de negocio en placeholder.

## Qué hace

Puerta de entrada de la oficina. Recibe mensajes de texto por Telegram,
los inyecta al Router de la Oficina como `encargo`, y devuelve la respuesta
del router al chat.

## Flujo

```
Mensaje Telegram (update: message)
  → Armar Encargo (texto → encargo; adjunta nombre/contenido_negocio placeholder)
  → Llamar Router (POST webhook/oficina-encargo)
  → Responder Telegram (devuelve answer al chat)
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

**Pendiente:** renombrar el bot de chat en @BotFather (el nombre
"AprobacionBot1" siendo el de chat es confuso). El renombre no afecta
token ni webhook.

Con cliente real: crear bot propio + credencial `CRED_CHAT_<CLIENTE>`
y reapuntar `Mensaje Telegram` y `Responder Telegram`.

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

- [x] Crear bot de entrada separado y validar recepción real. (jul 2026:
      mensaje → router → respuesta "Encargo recibido" OK)
- [ ] Renombrar bot de chat en @BotFather.
- [ ] Parametrizar nombre_negocio/contenido_negocio desde NEGOCIO.md.
- [ ] Migrar URL del router a HTTPS.
- [ ] Manejar mensajes que no son texto (fotos, documentos) — hoy asume texto.
- [ ] Respuesta del router: hoy toma `answer`; confirmar shape real cuando
      el router extraiga solo answer (pendiente #1 de industrialización del router).
