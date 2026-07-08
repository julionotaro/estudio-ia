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

| # | Conector | Tier | Estado | Workflow ID | Backends |
|---|---|---|---|---|---|
| 1 | aprobacion | T1 | VALIDADO punta a punta | `0yMYAybDFKtZFayh` + `kuFWgWvjTVJZStWM` | Telegram (transversal) |
| 2 | mail | T1 | esqueletado | `0NOMSF3TgxGFibBj` | SMTP envío + Gmail/Outlook lectura |
| 3 | sheets | T1 | esqueletado | `ZYagCbVDMwJwqQu3` | Google Sheets / Excel 365 |
| 4 | storage | T1 | esqueletado | `R6w6Og7BQxYPOFmG` | Drive / OneDrive |
| 5 | chat-coordinador | T1 | esqueletado (inactivo) | `gcKsrboh2i3t8QwO` | Telegram (requiere 2º bot) |
| 6 | calendario | T2 | esqueletado | `6Ae4XCaiWBX0xwJs` | Google Calendar / Outlook |
| 7 | gen-documentos | T2 | esqueletado | `oRl4jRXvuKnDKMvO` | Interno (HTML ok, PDF vía Gotenberg) |
| 8 | extraccion-documentos | T2 | esqueletado | `Cn75FQkKjbAlKCp8` | Interno (PDF nativo + Dify) |
| 9 | contactos | T3 | contemplado, no construido | — | — |
| 10 | tareas-recordatorios | T3 | contemplado, no construido | — | — |

## Arquitectura

- Un conector = un subworkflow n8n. Contrato JSON único (`CONTRATO.md`).
- El nodo "Ejecutar Acción" del Oficina Router v0 (`6LjeVR7Nl2RheUY9`) se reemplaza
  por un **dispatcher**: lee `instruccion_accion`, resuelve `suite` desde NEGOCIO.md,
  llama al conector correspondiente. (Aprobacion ya integrado; resto pendiente.)
- Backend por suite: `NEGOCIO.md` define `suite: google | microsoft`. Doble
  implementación donde no hay protocolo común (sheets, storage, calendario).
- Credenciales: placeholders `CRED_<CONECTOR>_<CLIENTE>`. Nunca hardcodear.
- Doble consumo: dispatcher (producción) + MCP Studio-julio (diseño/debug).

## Patrón común de los conectores con suite

`Entrada → Router Accion (switch) → Suite <Accion> (switch google/microsoft)
→ nodo del proveedor → Juntar (merge) → Salida Normalizada ({ ok, resultado, error })`.

La rama de la suite no usada queda inerte. Ensamblar = crear credencial + apuntar.

## Estructura

```
conectores-oficina/
  README.md                  ← este archivo
  CONTRATO.md                ← spec entrada/salida, suites, errores, credenciales
  aprobacion/  mail/  sheets/  storage/  chat-coordinador/
  calendario/  gen-documentos/  extraccion-documentos/
```

## Infra nueva identificada (pendiente)

- **Gotenberg** (Docker) para gen-documentos rama PDF. YAML en gen-documentos/README.
- **Chatflow Dify de extracción** para extraccion-documentos. Detalle en su README.
- **2º bot Telegram** para chat-coordinador (el actual lo usa aprobacion).

## Ensamblaje con cliente real

1. Crear `NEGOCIO.md` del cliente (incluye campo `suite` y `canal_aprobacion`).
2. Crear las credenciales `CRED_*_<CLIENTE>` en n8n.
3. Apuntar los conectores a esas credenciales.
4. Activar. Sin editar workflows ni prompts.

## Promoción a activos/

Conector por conector, no en bloque. Criterio en `CONTRATO.md` § final:
tests dummy OK + README completo + cero dominio de cliente.