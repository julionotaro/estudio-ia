# Continuidad — Conectores genéricos de oficina

> Documento de traspaso. Estado al cierre de la sesión de julio 2026.
> Investigación `[HERRAMIENTAS] Conectores genéricos como activos MCP para la oficina`.

## Qué se hizo esta sesión

Se construyó el catálogo completo de conectores genéricos para la Oficina de
agentes, en `estudio-ia/templates/conectores-oficina/`. 8 de 10 conectores
construidos (los T3 quedan solo contemplados). El de aprobación quedó VALIDADO
punta a punta; el resto esqueletado y listo para enchufar credenciales.

## Estado de cada conector

| # | Conector | Tier | Estado | Workflow ID |
|---|---|---|---|---|
| 1 | aprobacion | T1 | VALIDADO punta a punta | `0yMYAybDFKtZFayh` (Solicitar) + `kuFWgWvjTVJZStWM` (Resolver) |
| 2 | mail | T1 | esqueletado | `0NOMSF3TgxGFibBj` |
| 3 | sheets | T1 | esqueletado | `ZYagCbVDMwJwqQu3` |
| 4 | storage | T1 | esqueletado | `R6w6Og7BQxYPOFmG` |
| 5 | chat-coordinador | T1 | esqueletado, INACTIVO | `gcKsrboh2i3t8QwO` |
| 6 | calendario | T2 | esqueletado | `6Ae4XCaiWBX0xwJs` |
| 7 | gen-documentos | T2 | esqueletado | `oRl4jRXvuKnDKMvO` |
| 8 | extraccion-documentos | T2 | esqueletado | `Cn75FQkKjbAlKCp8` |
| 9 | contactos | T3 | contemplado, no construido | — |
| 10 | tareas-recordatorios | T3 | contemplado, no construido | — |

Todos en el proyecto n8n personal (`grgBpWySVCpXvuii`).

## Decisiones de arquitectura tomadas

- **Contrato JSON único** para todos los conectores (`CONTRATO.md`):
  entrada `{ herramienta, accion, parametros, area_origen, suite }`,
  salida `{ ok, resultado, error }`.
- **Suites, no herramientas sueltas.** Una oficina es Google Workspace o
  Microsoft 365. `NEGOCIO.md` define `suite: google | microsoft`. Doble backend
  donde no hay protocolo común (sheets, storage, calendario). Mail: envío
  genérico SMTP + lectura por suite. Telegram transversal (aprobación + chat).
- **Patrón común:** Entrada → Router Accion (switch) → Suite <Accion> (switch)
  → nodo proveedor → Merge → Salida Normalizada. Rama de suite no usada = inerte.
- **Frontera lectura/escritura:** solo escritura en sistema externo requiere
  aprobación. Lectura (leer mail, listar archivos, buscar) no.
- **Credenciales placeholder** `CRED_<CONECTOR>_<CLIENTE>`, IDs inválidos a
  propósito: no ejecutan hasta apuntar. Ensamblar = crear credencial + apuntar.

## Integración con el router

- El conector **aprobacion YA está integrado** en el Oficina Router v0
  (`6LjeVR7Nl2RheUY9`): se reemplazó `Preparar Aprobacion` por
  `Preparar Aprobacion → Solicitar Aprobacion (Execute Sub-workflow) →
  Esperar Aprobacion (Wait)`. Validado: encargo → botón Telegram → aprobar →
  router reanuda → Ejecutar Acción. Ejecución 253 en success.
- El resto de conectores NO están integrados aún. El "Ejecutar Acción" del
  router sigue siendo placeholder para las demás herramientas. Falta construir
  el dispatcher que lea `instruccion_accion.herramienta` y llame al conector.

## Infraestructura del VPS (cambios hechos)

Para que Telegram funcione (exige HTTPS en webhooks), se configuró:
- `/opt/estudio-ia/n8n/.env`: `N8N_HOST=studio-julio.duckdns.org`,
  `N8N_PROTOCOL=https`, `WEBHOOK_URL=https://studio-julio.duckdns.org/`.
- nginx de Dify (`docker-nginx-1`, conf en
  `/opt/estudio-ia/dify/dify/docker/nginx/conf.d/mcp-ssl.conf`): se añadieron
  `location /webhook/` y `location /webhook-waiting/` proxy a `172.17.0.1:5678`.
- El bot de aprobación (credencial `Telegram account`, `RgoHER0Ej0SkXMM2`)
  escucha `callback_query`. Webhook registrado OK.

## Pendiente de tu lado (bloqueantes de activación)

1. **2º bot de Telegram** para chat-coordinador (el actual lo usa aprobación).
   Crear con @BotFather → credencial n8n `CRED_CHAT_<CLIENTE>` → reapuntar los
   nodos `Mensaje Telegram` y `Responder Telegram` → activar workflow.
2. **Gotenberg** (Docker) para gen-documentos rama PDF. YAML listo en
   `gen-documentos/README.md`. La rama HTML funciona sin esto.
3. **Chatflow Dify de extracción** para extraccion-documentos + su app key.

## Pendientes técnicos (sin cliente, se pueden hacer ya)

- Construir el **dispatcher** en el router (reemplazar Ejecutar Acción
  placeholder por switch de conectores según `herramienta` + `suite`).
- Normalizar el shape de salida entre proveedores donde difiere (mail, storage,
  sheets, calendario devuelven estructuras Google vs Microsoft distintas).
- Migrar la URL del router de HTTP por IP a HTTPS dominio.
- Mover app keys / tokens hardcoded a credenciales n8n (pendiente #3 histórico).

## Aprendizajes técnicos de la sesión

- **GitHub Write requiere `sha` fresco** para actualizar archivos existentes
  (falla sin él). El workflow Read v2 no lo expone (usa raw+json). Obtenerlo con
  GET a la contents API con `Accept: application/vnd.github+json` antes de cada
  update. El `repo` en el Write necesita owner completo (`julionotaro/estudio-ia`).
- **Telegram publish falla con 400 si `WEBHOOK_URL` es HTTP.** Es error de HTTPS,
  no de credencial. Y el proxy debe enrutar `/webhook/*` explícitamente.
- **mail no es backend único** como decía el plan inicial: envío SMTP sí es
  genérico, pero lectura/búsqueda necesita API nativa por suite (n8n no tiene
  lector IMAP bajo demanda, solo trigger). Anotado en mail/README, contrato sin tocar.
- **Un bot Telegram = un webhook.** Dos Telegram Triggers del mismo bot compiten;
  por eso chat-coordinador necesita bot separado del de aprobación.

## Cómo retomar

1. Chat nuevo en el Laboratorio.
2. Pasar este documento + decir "continuamos los conectores de la oficina".
3. Decidir: activar lo pendiente (2º bot, Gotenberg, Dify) o construir el
   dispatcher del router, o promover aprobacion a activos/.

## Workflows n8n de referencia
- GitHub Write: `05hNhH7nbtXsXL9M` | GitHub Read: `OtNo3Tk6Qu2R91rp`
- Oficina Router v0: `6LjeVR7Nl2RheUY9`
- Data table aprobaciones_pendientes: `FFBSRcSjMVfcBipK`
- Credencial Telegram (aprobación): `RgoHER0Ej0SkXMM2`
- Credencial Header Auth (GitHub): `R9j3KGkJ6PjHCb6d`
