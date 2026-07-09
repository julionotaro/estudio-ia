# Dispatcher del Oficina Router v0

> Añadido jul 2026. Reemplaza el placeholder "Ejecutar Accion" del router
> (`6LjeVR7Nl2RheUY9`). VALIDADO punta a punta (ejecución 295, con Dify
> pineado y aprobación Telegram real).

## Qué hace

Tras la aprobación humana, lee la `instruccion_accion` emitida por el agente
de área y la despacha al conector correspondiente con el contrato de
`conectores-oficina`.

## Flujo (rama post-aprobación del router)

```
Aprobado? (sí)
  → Parsear Instruccion   (Code: extrae instruccion_accion del entregable)
  → Dispatcher Herramienta (Switch por $json.herramienta)
      ├─ mail → Conector Mail (Execute Sub-workflow → 0NOMSF3TgxGFibBj)
      │          → Salida Ejecucion { estado, herramienta, resultado, error }
      └─ fallback → Sin Conector { estado: SIN_CONECTOR, herramienta, mensaje }
```

## Contrato que espera del agente de área

Cuando el agente marca `PENDIENTE_APROBACION`, su respuesta debe incluir un
bloque JSON con:

```json
{ "instruccion_accion": {
    "herramienta": "mail",
    "accion": "enviar",
    "parametros": { "para": "...", "asunto": "...", "cuerpo": "..." }
} }
```

`Parsear Instruccion` es tolerante: si no hay JSON o falta `herramienta`,
cae a `SIN_CONECTOR` sin romper la ejecución. La `suite` se fija hoy como
placeholder `google` en ese nodo (con cliente: leer de NEGOCIO.md).

## Estados de salida del router (shape completo confirmado)

| Rama | Shape |
|---|---|
| Entrega directa | `{ estado: ENTREGADO, entregable }` |
| Sin agente | `{ estado: SIN_AGENTE, mensaje }` |
| Ejecutado vía conector | `{ estado: EJECUTADO, herramienta, resultado, error: null }` |
| Conector falló | `{ estado: ERROR_CONECTOR, herramienta, resultado, error }` |
| Sin conector para la herramienta | `{ estado: SIN_CONECTOR, herramienta, mensaje }` |
| Rechazado | `{ estado: RECHAZADO }` |

`Conector Mail` tiene `onError: continueRegularOutput`: un fallo del conector
no tumba la ejecución, devuelve ERROR_CONECTOR.

## Validación (ejecución 295, jul 2026)

Método: `test_workflow` con pin data en los 3 nodos Dify/webhook (Entrada,
Coordinador, Agente) y TODO lo demás real: solicitud de aprobación por
Telegram, botón Aprobar real, resume del Wait, dispatch, sub-workflow Mail.
Resultado: cadena completa OK; falló exactamente en la credencial
`PLACEHOLDER_SMTP` del nodo `Enviar SMTP` — el punto de fallo esperado por
diseño. El dispatch y el mapeo de parámetros quedaron probados.

## Conectores integrados al dispatcher

| Herramienta | Estado |
|---|---|
| mail | Integrado y publicado. Falta credencial SMTP real para envío efectivo. |
| sheets, storage, calendario, gen-documentos, extraccion-documentos | NO integrados aún: añadir regla al Switch + nodo Execute Sub-workflow mapeando `parametros` al schema plano de cada conector (ver Entrada de cada workflow). Publicar cada sub-workflow antes de publicar el router. |

## Decisiones de diseño de la sesión

- **Frontera AUXILIAR/CONTENIDO:** toda acción cuyo resultado va a un sistema
  externo o a un tercero (enviar mail, cargar datos) es de AUXILIAR, incluida
  la redacción de lo que se envía. CONTENIDO queda para material sin
  destinatario externo. **CONTENIDO se mantiene en el catálogo de áreas**
  (decisión de Julio: no retirarlo; construir su agente bien en el futuro).
- Herramienta desconocida NO rompe: SIN_CONECTOR informativo.

## Pendientes

- [ ] Corregir prompts en Dify (mañana): Regla 6 del Coordinador ampliada a
      envío de comunicaciones; AUXILIAR no deriva redacción+envío a CONTENIDO
      y emite `instruccion_accion` con el contrato de arriba.
- [ ] Prueba natural completa: encargo por chat → AUXILIAR real → aprobación
      → dispatch (validar shape real del `instruccion_accion` que emite Dify).
- [ ] Credencial SMTP real en `Enviar SMTP` del conector Mail.
- [ ] Integrar el resto de conectores al Switch.
- [ ] Respuesta al chat tras aprobación: el webhook responde al reanudar; el
      chat-coordinador ya cubre los shapes nuevos (EJECUTADO usa `resultado`
      objeto — revisar cómo se muestra en Telegram).

## Incidente registrado (aprendizaje operativo)

Durante la sesión, el webhook de Telegram del bot de aprobación quedó borrado
como secuela de ciclos publish/unpublish ejecutados mientras una credencial
tenía el token equivocado (el token del bot 1 estaba pegado en la credencial
del bot 2). Síntoma: botón de aprobar sin efecto; Resolver sin ejecuciones.
**Regla operativa:** tras cualquier cambio de credenciales Telegram o ciclo de
publicación, verificar `getWebhookInfo` de TODOS los bots afectados (url y
`allowed_updates` correctos). Un webhook vacío = n8n no registró; url ajena =
credencial con token equivocado.
