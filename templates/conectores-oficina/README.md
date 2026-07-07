# Conectores genéricos de oficina

> Investigación `[HERRAMIENTAS] Conectores genéricos como activos MCP para la oficina`
> (Laboratorio, jul 2026). Estado: EN CONSTRUCCIÓN — templates/, no activos/.

## Qué es

Catálogo de conectores reutilizables para la Oficina de agentes (templates/oficina/).
Cubren las herramientas básicas de cualquier oficina, independientes del dominio del
cliente. Contrato único en `CONTRATO.md` — leerlo antes de tocar cualquier conector.

Lo específico del cliente (su ERP, su RPA, su sistema contable) NO va acá: va en el
repo del cliente, apoyándose en `activos/rpa-playwright/` cuando toque.

## Catálogo

| # | Conector | Tier | Estado | Backends |
|---|---|---|---|---|
| 1 | aprobacion | T1 | pendiente | Telegram (transversal) |
| 2 | mail | T1 | pendiente | IMAP/SMTP (único, cubre Gmail y Outlook) |
| 3 | sheets | T1 | pendiente | Google Sheets / Excel 365 (doble) |
| 4 | storage | T1 | pendiente | Drive / OneDrive (doble) |
| 5 | chat-coordinador | T1 | pendiente | Telegram (transversal) |
| 6 | calendario | T2 | pendiente | Google Calendar / Outlook (doble) |
| 7 | gen-documentos | T2 | pendiente | Interno (plantilla → PDF/docx) |
| 8 | extraccion-documentos | T2 | pendiente | Interno (Dify con ficheros) |
| 9 | contactos | T3 | contemplado, no construido | — |
| 10 | tareas-recordatorios | T3 | contemplado, no construido | — |

Orden de construcción: `aprobacion` primero (convierte la URL manual del Router v0
en botón Telegram y desbloquea el resto), luego resto de T1, dispatcher, T2.

## Arquitectura

- Un conector = un subworkflow n8n. Contrato JSON único (`CONTRATO.md`).
- El nodo "Ejecutar Acción" del Oficina Router v0 (`6LjeVR7Nl2RheUY9`) se reemplaza
  por un **dispatcher**: lee `instruccion_accion`, resuelve `suite` desde NEGOCIO.md,
  llama al conector correspondiente.
- Backend por suite: `NEGOCIO.md` define `suite: google | microsoft`. Doble
  implementación donde no hay protocolo común (sheets, storage, calendario).
- Credenciales: placeholders `CRED_<CONECTOR>_<CLIENTE>`. Nunca hardcodear.
- Doble consumo: dispatcher (producción) + MCP Studio-julio (diseño/debug).

## Estructura

```
conectores-oficina/
  README.md                  ← este archivo
  CONTRATO.md                ← spec entrada/salida, suites, errores, credenciales
  aprobacion/                ← por conector: README + export workflow + tests
  mail/
  sheets/
  storage/
  chat-coordinador/
  calendario/
  gen-documentos/
  extraccion-documentos/
```

Cada carpeta de conector debe tener: README (acciones + parametros + credencial),
el export del workflow n8n, y casos de test con cuenta dummy.

## Ensamblaje con cliente real

1. Crear `NEGOCIO.md` del cliente (incluye campo `suite` y `canal_aprobacion`).
2. Crear las credenciales `CRED_*_<CLIENTE>` en n8n.
3. Apuntar los conectores a esas credenciales.
4. Activar. Sin editar workflows ni prompts.

## Promoción a activos/

Conector por conector, no en bloque. Criterio en `CONTRATO.md` § final:
tests dummy OK + README completo + cero dominio de cliente.