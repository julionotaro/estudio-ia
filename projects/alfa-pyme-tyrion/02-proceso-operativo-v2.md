# Proceso Operativo Documental — Especificación v2
**Proyecto:** Alfa-Pyme / Tyrion
**Estado:** Borrador de trabajo con supuestos marcados. Los puntos `[PENDIENTE]` se validan en la entrevista con el administrativo (ver `01-entrevista-administrativo.md`).
**Reemplaza a:** descripción operativa v1 (narrativa original).

---

## 1. Propósito y modelo de negocio

La oficina es una **tramitadora de alto volumen** que procesa gestiones administrativas (principalmente de vehículos ante DGT) **para gestorías** — sus clientes son B2B. Volumen de referencia: **~250 trámites/día** operados por **4 administrativos**, con SLA de **cierre en el mismo día**.

**Finalidad del sistema:** automatizar al máximo el procesamiento repetitivo para liberar carga de los administrativos. **Tyrion** (agente IA) es la base del sistema: gestiona el 100% de los trámites salvo excepciones, que escala con contexto completo.

## 2. Actores

| Actor | Rol |
|---|---|
| **Gestoría** (cliente) | Envía solicitudes y documentación; consulta estados; solicita devolución física de documentación. |
| **Tyrion** (agente IA) | Dueño primario del flujo: recibe, clasifica, coteja, asigna estados, conversa con la gestoría hasta agotar recursos, escala, prepara expedientes, y (óptimo) carga datos en sistemas externos y confirma por canales de salida. |
| **Administrativo** (×4) | Supervisión y excepciones. Usuario principal de la pantalla Control. No es el primer dueño de ningún problema documental. |
| **Organismos** | DGT principalmente; destino de presentaciones y origen de observaciones. |
| **Cadetería** | Servicio de envío físico de documentación a gestorías, coordinado vía Tyrion. |

## 3. Canales

**Entrada** (mezcla actual aproximada):
- Email: ~50%
- Papel físico: ~40% → requiere **proceso de digitalización por lote** (escaneo) como puerta de entrada al pipeline. La ubicación física del papel se registra (ver §5, entidad Documento).
- WhatsApp / Telegram: ~10%
- Calidad de archivos: ~70% PDF nativo, ~30% foto de móvil, calidad buena/muy buena.

**Salida:** mismos canales digitales (confirmaciones, solicitudes, resultados) + **cadetería** para documentación física.

**Regla de identidad:** todo remitente se matchea contra las identidades registradas de cada gestoría (números, emails autorizados). Remitente no reconocido → documento queda en cuarentena de identidad y no se asocia a ningún trámite hasta resolverse (Tyrion pregunta; si no resuelve, escala).

## 4. Las cuatro capas documentales (regla estructural)

Se mantienen y formalizan los cuatro conceptos de la v1:
1. **Documento requerido** — lo que el trámite necesita (definido por el checklist del tipo).
2. **Documento recibido** — el archivo/papel que llegó.
3. **Documento detectado** — lo que Tyrion interpreta que contiene, con un **nivel de confianza**. Nota: el "tipo declarado por el cliente" es también una detección (parsing del mensaje), no un dato confiable.
4. **Documento válido** — el que efectivamente desbloquea ESE trámite.

**Evidencia compatible ≠ documento válido** (regla de oro v1, se mantiene). Caso canónico: trámite requiere Permiso de circulación, llega Modelo 620 → evidencia compatible, el requerido sigue faltante.

## 5. Modelo de datos conceptual

Tres entidades núcleo + soporte:

- **Documento**: archivo (o papel digitalizado), hash, fecha y canal de recepción, remitente, tipo detectado + confianza, versión (un reenvío corregido **sustituye** y conserva el anterior como historial), y **ubicación física** si existe papel (bandeja/caja/lote — necesario para cadetería y devoluciones).
- **Trámite**: tipo, gestoría, identificadores del caso (p. ej. matrícula/bastidor), estado (ver §6), relojes activos, responsable actual (Tyrion | administrativo concreto), trazabilidad.
- **Vínculo Documento↔Trámite** (relación N:M): aquí vive el estado de validez — `válido / evidencia compatible / rechazado / no aplica`. **Un mismo documento puede ser válido en dos trámites del mismo cliente** (confirmado). La validez nunca es propiedad del documento: es propiedad de la relación.
- **Mensaje**: canal, trámite, contenido, estado `preparado / enviado / respondido`. **Mensaje preparado ≠ mensaje enviado** (regla de oro v1, se mantiene): si no hay integración real de envío en un canal, el sistema dice "preparado".
- **Solicitud de envío físico** (cadetería): documentos incluidos, dirección de la gestoría, estado `solicitada / en preparación / retirada / entregada / incidencia`.
- **Identidades de gestoría**: emails, números de WhatsApp/Telegram autorizados, personas de contacto.

## 6. Estados — arquitectura de dos capas

Decisión de diseño (a pedido del dueño): **simplicidad en pantalla, precisión por dentro**. La máquina de estados completa existe, pero Control muestra solo macro-estados.

### Capa visible (Control) — 6 macro-estados + 1
| Macro-estado | Significado operativo |
|---|---|
| 🆕 **Entrada** | Llegó, identificándose cliente y tipo. |
| ⚙️ **En proceso** | Tyrion trabajando: clasifica, coteja, prepara. |
| ⏳ **Esperando gestoría** | Falta algo; Tyrion ya lo pidió y gestiona la respuesta. |
| 🔴 **Requiere administrativo** | Excepción real escalada con resumen. Única bandeja de acción humana. |
| 📤 **En organismo** | Presentado; pendiente de respuesta/justificante. |
| ✅ **Cerrado** | Resuelto (con sub-resultado) y archivado. |
| ⛔ **Cancelado** | Posible desde cualquier estado previo al cierre. |

### Capa interna (sub-estados, no visibles por defecto)
- *Entrada*: `recibido` → `identidad verificada` → `tipificado` | `tipo ambiguo (pregunta en curso)` | `posible duplicado`.
- *En proceso*: `clasificando documentos` → `cotejando checklist` → `expediente completo` → `cargando en sistemas (DGT)` → `listo para presentar`.
- *Esperando gestoría*: `solicitud enviada` → `reintento 1` → `reintento 2` (todo dentro de la ventana de ~1 hora, ver §7).
- *Requiere administrativo*: motivo = `sin respuesta en SLA` | `conflicto documental` | `baja confianza de clasificación` | `datos incompatibles entre documentos` | `excepción normativa` | `imposibilidad técnica`.
- *En organismo*: `presentado` → `justificante registrado` | `observado → subsanación` (la subsanación reabre el ciclo documental del §8 con reloj propio `[PENDIENTE: plazos reales]`).
- *Cerrado*: resultado = `favorable / desfavorable / parcial / cancelado`. **Reapertura: el mismo trámite se reabre** (no se crea uno nuevo) y vuelve a ⚙️ En proceso, conservando todo el historial.

### Estados del documento (máquina propia)
`recibido` → `clasificado (confianza alta/media/baja)` → por cada vínculo a trámite: `válido / evidencia / rechazado` — más `duplicado` y `sustituido (versión nueva disponible)`.

## 7. Relojes (SLA intradía)

- **Regla madre: el trámite debe cerrarse en el día.** Las gestorías deben enviar la información completa.
- Si falta documentación: Tyrion solicita de inmediato → **reintentos dentro de ~1 hora** (2 intentos) → sin respuesta → **escala a administrativo**.
- Lo no cerrado al fin del día pasa como **"arrastre"** visible y priorizado en Control a la mañana siguiente. *(Propuesta — validar con la oficina.)*
- Subsanaciones del organismo: reloj legal propio, prioridad máxima en Control. `[PENDIENTE: plazos y frecuencia reales — preguntas 35–36 de la entrevista]`
- **Retención:** documentación huérfana (no asociada a trámite) y expedientes cerrados se purgan a **1 semana**. `[PENDIENTE: validar contra obligaciones legales de conservación de justificantes; posible excepción para justificantes de presentación]`
- Priorización en Control: `plazo legal > SLA del día > antigüedad del arrastre`.

## 8. Flujo principal (end-to-end, asíncrono)

1. **Entrada multicanal** — email / WhatsApp / Telegram / lote escaneado.
2. **Identificación del remitente** → matching contra identidades de gestoría. No reconocido → cuarentena + pregunta.
3. **Creación automática del trámite** (sin validación humana, decisión confirmada) con **detección de duplicados**: misma gestoría + misma matrícula/caso en ventana corta → Tyrion fusiona o pregunta antes de duplicar.
4. **Tipificación** — si el tipo es claro, se asigna checklist; si no, Tyrion pide aclaración (el pipeline documental NO se bloquea: los documentos se clasifican igual y el cotejo queda diferido).
5. **Clasificación documental** — tipo detectado + confianza por documento. Confianza baja → marca para validación.
6. **Cotejo contra checklist** — aplica las cuatro capas (§4). Resultado por documento requerido: `cubierto / faltante / en conflicto`.
7. **Gestión de faltantes y conflictos (Tyrion-first)** — solicitud específica, nunca genérica: qué falta, por qué, y por qué lo recibido no alcanza. Conversación multi-turno por el canal de la gestoría. Las respuestas con nuevos documentos entran por el paso 1 al MISMO trámite (historia documental continua).
8. **Escalado** — solo por excepción real (motivos en §6), siempre con resumen: qué pasó, qué documento, qué se pidió, qué respondió o no la gestoría, qué conflicto sigue abierto, qué recomienda Tyrion.
9. **Expediente completo** — verificación final: obligatorios presentes y válidos, sin conflictos abiertos, evidencias compatibles NO contadas como válidas.
10. **Carga en sistemas externos** (óptimo v1): datos del expediente cargados en el sistema DGT y facturación del servicio en SAGE. `[PENDIENTE: definir mecanismo — API/colaborador/RPA/carga asistida]`
11. **Presentación** — registro de qué, cuándo, por qué canal, con qué documentos, responsable, justificante/nº de expediente externo.
12. **Seguimiento** — respuesta favorable → resolución; observación → **subsanación**: Tyrion interpreta la observación (función v1 confirmada) y la traduce a acción documental concreta; el ciclo documental se reabre con reloj legal.
13. **Cierre** — resultado registrado, comunicación a la gestoría por su canal, y si corresponde **devolución física vía cadetería** (solicitud, retiro, tracking, entrega).
14. **Archivo y purga** — historia completa y auditable; purga según política de retención (§7).

## 9. Conversación Tyrion ↔ Gestoría (canal de servicio)

Además del flujo documental, Tyrion atiende por WhatsApp/Telegram/email:
- **Consulta de estado**: "¿cómo va la transferencia de la 1234-ABC?" → respuesta con estado visible y próxima acción.
- **Solicitud de envío físico**: dispara una Solicitud de cadetería.
- **Recepción de documentación** en respuesta a pedidos → entra al pipeline del trámite correspondiente.
Toda conversación queda registrada y asociada al trámite (Timeline).

## 10. Pantallas

- **Control** — torre del DÍA: los 6 macro-estados, contadores, el arrastre, y la bandeja 🔴 como única lista de acción humana. No es un histórico.
- **Trámites** — búsqueda e histórico de expedientes (por matrícula, gestoría, fecha, tipo, estado).
- **Detalle del trámite** — pantalla de resolución: qué pasa, por qué no avanza, qué detectó Tyrion, qué falta, quién actúa ahora, acción recomendada, y conversación asociada.
- **Documentos** — fuente de verdad documental, independiente del trámite: todo lo recibido/detectado/validado/rechazado/duplicado/sustituido + ubicación física del papel.
- **Timeline/Auditoría** — historia cronológica completa por trámite: eventos, mensajes (preparado/enviado/respondido), escalados, presentación, subsanaciones, cierre.

## 11. Reglas de oro (v2)

1. **Tyrion gestiona primero.** El administrativo interviene solo por excepción real.
2. **Evidencia compatible ≠ documento válido.**
3. **Mensaje preparado ≠ mensaje enviado.**
4. **El trámite organiza la operación; Documentos conserva la verdad documental.**
5. **Estados simples afuera, precisión adentro** (dos capas, §6).
6. **El SLA del día manda**; los relojes legales mandan sobre todo lo demás.
7. **Ningún documento se asocia a un trámite sin identidad de remitente resuelta.**

## 12. Restricciones y estrategia de costos

- Presupuesto IA/OCR: **mínimo posible ahora; 150–200 €/mes en producción.** Con ~250 trámites/día (~20–27 mil documentos/mes estimados a 3–5 docs por trámite), la estrategia es: **modelo económico de visión para clasificación masiva** (p. ej. Gemini Flash, free tier mientras dure), **extracción de datos solo selectiva** (campos del checklist, no OCR completo de todo), y **modelo premium únicamente en conflictos y escalados**.
- 40% papel → la digitalización por lote es parte del sistema, no un externo.
- Integraciones DGT/SAGE: definir mecanismo realista en diseño técnico; hasta entonces, "carga preparada" ≠ "carga realizada" (extensión de la regla 3).

## 13. Pendientes de validación (entrevista administrativo)

| # | Tema | Pregunta de referencia |
|---|---|---|
| 1 | Estados reales y vocabulario de la oficina | Bloques 3–10 |
| 2 | Catálogo de tipos de trámite + checklists | P.10, P.13 |
| 3 | Plazos y frecuencia de subsanaciones | P.35–36 |
| 4 | Política legal de retención/justificantes | P.41 |
| 5 | Mecanismo real de presentación/carga DGT | P.30–32 |
| 6 | Reglas de cruce de datos entre documentos | P.21–22 |
| 7 | Tratamiento del arrastre de fin de día | Bloque 12 |

---

## 14. BRIEF PARA EL EQUIPO DE DISEÑO (copiar y pegar como prueba)

> Cliente: oficina tramitadora de gestiones de vehículos ante DGT que trabaja para gestorías (B2B). Volumen: 250 trámites/día, 4 administrativos, SLA de cierre en el mismo día. Quieren construir un sistema cuyo núcleo es Tyrion, un agente IA que gestiona el 100% de los trámites salvo excepciones: recibe documentación por email (50%), papel escaneado (40%) y WhatsApp/Telegram (10%); identifica al remitente contra las identidades de cada gestoría; crea trámites automáticamente con detección de duplicados; clasifica documentos (70% PDF, 30% foto) con nivel de confianza; los coteja contra el checklist del tipo de trámite distinguiendo documento requerido, recibido, detectado y válido (un Modelo 620 NO sustituye un Permiso de circulación: es evidencia compatible); conversa con la gestoría por su canal para pedir faltantes (2 reintentos en 1 hora, luego escala al administrativo con resumen completo); prepara el expediente; carga datos en el sistema DGT y factura en SAGE; registra presentación y justificante; interpreta observaciones del organismo y gestiona subsanaciones; comunica el resultado; y coordina la devolución física de documentación por cadetería. El sistema necesita: pantalla Control con 6 macro-estados (con sub-estados internos), Trámites (histórico), Detalle, Documentos (verdad documental independiente, relación N:M documento-trámite donde la validez vive en el vínculo), y Timeline auditable. Reglas: mensaje preparado ≠ enviado; evidencia compatible ≠ válido; retención de huérfanos 1 semana; presupuesto IA máximo 150–200€/mes en producción (~25.000 documentos/mes). Quieren saber: arquitectura propuesta, qué es viable en una v1 de 8 semanas, qué dejarían para v2, y los principales riesgos.
