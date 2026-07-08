# Conector — Aprobacion

> Tier 1 — transversal (no depende de suite). Estado: construido, pendiente test punta a punta.

## Qué hace

Convierte la URL manual de reanudación del Oficina Router en un botón
Telegram. El humano recibe un mensaje con ✅ Aprobar / ❌ Descartar;
su respuesta reanuda el router y actualiza el registro de estado.

## Workflows

| Workflow | ID | Activado |
|---|---|---|
| `[CONECTOR] Aprobacion - Solicitar` | `0yMYAybDFKtZFayh` | No (subworkflow, no necesita) |
| `[CONECTOR] Aprobacion - Resolver` | `kuFWgWvjTVJZStWM` | Sí |

## Data table

- Nombre: `aprobaciones_pendientes`
- ID: `FFBSRcSjMVfcBipK`
- Columnas: `id_aprobacion, resume_url, area_origen, resumen, estado`
- Estados posibles: `PENDIENTE → APROBADA | DESCARTADA`

## Contrato de entrada (Solicitar)

```json
{
  "resume_url": "string — URL de reanudación del Wait node del router",
  "area_origen": "string — TRAFICO | AUXILIAR | CONTABILIDAD | DATOS",
  "resumen": "string — descripción legible de la acción a aprobar"
}
```

El workflow Solicitar se llama como subworkflow desde el router, pasando
estos tres campos extraídos del bloque `instruccion_accion` del agente.

## Flujo completo

```
Router → [CONECTOR] Solicitar
  → genera id_aprobacion
  → guarda en data table (estado: PENDIENTE)
  → envía mensaje Telegram con botones

Humano pulsa botón → [CONECTOR] Resolver
  → parsea decisión (apr:/des: + id_aprobacion)
  → busca resume_url en data table
  → GET resume_url&decision=aprobar|descartar  ← reanuda el router
  → actualiza estado en data table (APROBADA|DESCARTADA)
  → responde callback (quita el spinner de Telegram)
  → edita mensaje original (añade ✅/❌ + texto)
```

## Credencial

`telegramApi` — convención de nombre: `CRED_APROBACION_<CLIENTE>`.
Con cliente real: crear credencial Telegram API en n8n con el token
del bot del cliente y reapuntar en ambos workflows.

El `chat_id` del aprobador está hardcoded en el nodo `Enviar Solicitud
Telegram` (campo `chatId`). Con cliente real: leer desde `NEGOCIO.md`
o inyectarlo como parámetro de entrada.

## Test con cliente dummy

1. Lanzar un encargo al Oficina Router que active PENDIENTE_APROBACION.
2. Confirmar que llega el mensaje Telegram con los botones.
3. Pulsar ✅ Aprobar — verificar que el router se reanuda y la rama
   `Ejecutar Acción` corre.
4. Repetir con ❌ Descartar — verificar rama `Descartar`.
5. Verificar estado en data table: `APROBADA` / `DESCARTADA`.

## Pendiente antes de promover a activos/

- [ ] Test punta a punta contra el Oficina Router v0 real.
- [ ] Parametrizar `chat_id` (leer de NEGOCIO.md en vez de hardcoded).
- [ ] Verificar comportamiento si el humano pulsa el botón dos veces
      (doble aprobación): el filtro `estado: PENDIENTE` en Buscar
      Aprobacion debería silenciar la segunda, confirmar.