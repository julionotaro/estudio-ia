# Conector — Chat Coordinador

> Tier 1 — transversal (Telegram). Estado: ESQUELETADO — NO activar todavía
> (ver sección Bots). Datos de negocio en placeholder.

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
| `[CONECTOR] Chat Coordinador` | `gcKsrboh2i3t8QwO` | NO (ver Bots) |

## Datos de negocio (placeholder)

El nodo `Armar Encargo` rellena `nombre_negocio` y `contenido_negocio` con
valores placeholder. Con cliente real: leerlos de NEGOCIO.md o fijarlos en
ese nodo. El `encargo` sí sale del mensaje real.

## Bots de Telegram — IMPORTANTE

Un mismo bot de Telegram registra UN webhook en n8n. El conector de
**aprobación** ya usa el bot actual (credencial `Telegram account`,
`RgoHER0Ej0SkXMM2`) escuchando `callback_query`. Este conector escucha
`message`. Dos Telegram Triggers del mismo bot compiten por el webhook:
el último activado gana y desactiva al otro.

**Solución:** usar un BOT SEPARADO para la entrada de mensajes.
Pasos con cliente real:
1. Crear bot nuevo con @BotFather (p. ej. `OficinaEntradaBot`).
2. Crear credencial Telegram API en n8n con ese token
   (convención: `CRED_CHAT_<CLIENTE>`).
3. Reapuntar los nodos `Mensaje Telegram` y `Responder Telegram` a esa
   credencial.
4. Recién entonces activar el workflow.

Hoy el conector usa la credencial del bot de aprobación como placeholder
y queda INACTIVO para no romper el flujo de aprobación ya validado.

## Contrato hacia el Router

POST `http://187.127.233.43:5678/webhook/oficina-encargo`
```json
{ "encargo": "<texto del mensaje>", "nombre_negocio": "...", "contenido_negocio": "..." }
```

Nota: la URL del router es HTTP por IP. Al industrializar, migrar a
`https://studio-julio.duckdns.org/webhook/oficina-encargo` (ya hay ruta
nginx para `/webhook/`).

## Pendiente antes de promover a activos/

- [ ] Crear bot de entrada separado y validar recepción real.
- [ ] Parametrizar nombre_negocio/contenido_negocio desde NEGOCIO.md.
- [ ] Migrar URL del router a HTTPS.
- [ ] Manejar mensajes que no son texto (fotos, documentos) — hoy asume texto.
- [ ] Respuesta del router: hoy toma `answer`; confirmar shape real cuando
      el router extraiga solo answer (pendiente #1 de industrialización del router).