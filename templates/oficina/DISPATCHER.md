# Dispatcher del Oficina Router v0

> Añadido jul 2026. Reemplaza el placeholder "Ejecutar Accion" del router
> (`6LjeVR7Nl2RheUY9`). VALIDADO punta a punta (ejecución 295, con Dify
> pineado y aprobación Telegram real). Los 6 conectores integrados.

## Qué hace

Tras la aprobación humana, lee la `instruccion_accion` emitida por el agente
de área y la despacha al conector correspondiente con el contrato de
`conectores-oficina`.

## Flujo (rama post-aprobación del router)

```
Aprobado? (sí)
  → Parsear Instruccion   (Code: extrae instruccion_accion del entregable)
  → Dispatcher Herramienta (Switch por $json.herramienta)
      ├─ mail                  → Conector Mail (0NOMSF3TgxGFibBj)
      ├─ sheets                → Conector Sheets (ZYagCbVDMwJwqQu3)
      ├─ storage               → Conector Storage (R6w6Og7BQxYPOFmG)
      ├─ calendario            → Conector Calendario (6Ae4XCaiWBX0xwJs)
      ├─ gen-documentos        → Conector Gen Documentos (oRl4jRXvuKnDKMvO)
      ├─ extraccion-documentos → Conector Extraccion Documentos (Cn75FQkKjbAlKCp8)
      │    todos → Salida Ejecucion { estado, herramienta, resultado, error }
      └─ fallback → Sin Conector { estado: SIN_CONECTOR, herramienta, mensaje }
```

Todos los Execute Sub-workflow tienen `onError: continueRegularOutput` (un
fallo del conector devuelve ERROR_CONECTOR, no tumba la ejecución) y mapean
`$json.parametros.*` al schema plano de la Entrada de cada conector.

## Contrato que espera del agente de área

Cuando el agente marca `PENDIENTE_APROBACION`, su respuesta debe incluir un
bloque JSON con:

```json
{ "instruccion_accion": {
    "herramienta": "mail | sheets | storage | calendario | gen-documentos | extraccion-documentos",
    "accion": "acción del conector (ej. mail: enviar)",
    "parametros": { }
} }
```

`Parsear Instruccion` es tolerante: si no hay JSON o falta `herramienta`,
cae a `SIN_CONECTOR` sin romper la ejecución. La `suite` se fija hoy como
placeholder `google` en ese nodo (con cliente: leer de NEGOCIO.md).

### Parámetros por herramienta (mapeo del dispatcher)

| Herramienta | parametros esperados |
|---|---|
| mail | para, asunto, cuerpo, remitente?, texto_busqueda?, limite? |
| sheets | documento_id, hoja, fila (obj), columna_clave?, valor_busqueda? |
| storage | nombre, carpeta_id?, archivo_id?, texto_busqueda?, limite? |
| calendario | calendario_id?, evento_id?, titulo, inicio, fin, descripcion?, limite? |
| gen-documentos | formato (html/pdf), plantilla_html, datos (obj), nombre_archivo |
| extraccion-documentos | esquema, nombre_negocio? |

## Estados de salida del router (shape completo confirmado)

| Rama | Shape |
|---|---|
| Entrega directa | `{ estado: ENTREGADO, entregable }` |
| Sin agente | `{ estado: SIN_AGENTE, mensaje }` |
| Ejecutado vía conector | `{ estado: EJECUTADO, herramienta, resultado, error: null }` |
| Conector falló | `{ estado: ERROR_CONECTOR, herramienta, resultado, error }` |
| Sin conector para la herramienta | `{ estado: SIN_CONECTOR, herramienta, mensaje }` |
| Rechazado | `{ estado: RECHAZADO }` |

## Validación (ejecución 295, jul 2026)

Método: `test_workflow` con pin data en los 3 nodos Dify/webhook y TODO lo
demás real: aprobación por Telegram real, resume del Wait, dispatch,
sub-workflow Mail. Falló exactamente en la credencial `PLACEHOLDER_SMTP` —
el punto de fallo esperado por diseño. Dispatch y mapeo probados. Los otros
5 conectores usan el mismo mecanismo (Execute Sub-workflow + mapeo plano);
sus credenciales siguen en placeholder.

## Decisiones de diseño de la sesión

- **Frontera AUXILIAR/CONTENIDO:** toda acción cuyo resultado va a un sistema
  externo o a un tercero (enviar mail, cargar datos) es de AUXILIAR, incluida
  la redacción de lo que se envía. CONTENIDO queda para material sin
  destinatario externo. **CONTENIDO se mantiene en el catálogo de áreas**
  (decisión de Julio: no retirarlo; construir su agente bien en el futuro).
- Herramienta desconocida NO rompe: SIN_CONECTOR informativo.
- Prompts corregidos en repo (`prompt-coordinador.md`, `prompt-auxiliar.md`):
  Regla 6 por destino del resultado; AUXILIAR dueño de comunicaciones
  salientes; `instruccion_accion` alineada a este contrato. PENDIENTE pegar
  en Dify.

## Pendientes

- [ ] Pegar prompts corregidos en Dify (Coordinador + AUXILIAR).
- [ ] Prueba natural completa: encargo por chat → AUXILIAR real → aprobación
      → dispatch (validar shape real del `instruccion_accion` de Dify).
- [ ] Credencial SMTP real en `Enviar SMTP` del conector Mail.
- [ ] Credenciales reales del resto de conectores al ensamblar cliente.
- [ ] Respuesta al chat tras aprobación: revisar cómo se muestra `resultado`
      (objeto) en Telegram.

## Aprendizajes técnicos

- **Validador de publish y parámetros \_\_rl requeridos:** un valor estático
  placeholder en un parámetro resourceLocator requerido (ej. `table` de Excel
  lookup) bloquea el publish ("Missing or invalid required parameters"). Un
  placeholder dentro de una EXPRESIÓN sí pasa:
  `={{ $("Entrada").item.json.tabla_id || "PLACEHOLDER_TABLA" }}`.
- **Sub-workflows deben estar publicados** antes de publicar el workflow padre
  que los referencia (publish falla con error explícito si no).
- **Switch: añadir reglas desplaza el fallback.** Al pasar de 1 a 6 reglas, el
  fallback pasa del output 1 al 6; hay que quitar y recrear la conexión del
  fallback o queda apuntando a la salida de una regla nueva.

## Incidente registrado (aprendizaje operativo)

Durante la sesión, el webhook de Telegram del bot de aprobación quedó borrado
como secuela de ciclos publish/unpublish ejecutados mientras una credencial
tenía el token equivocado (el token del bot 1 estaba pegado en la credencial
del bot 2). Síntoma: botón de aprobar sin efecto; Resolver sin ejecuciones.
**Regla operativa:** tras cualquier cambio de credenciales Telegram o ciclo de
publicación, verificar `getWebhookInfo` de TODOS los bots afectados (url y
`allowed_updates` correctos). Un webhook vacío = n8n no registró; url ajena =
credencial con token equivocado.
