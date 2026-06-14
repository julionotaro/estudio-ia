# Proceso Operativo Documental — Especificación v2.1
**Proyecto:** Alfa-Pyme / Tyrion
**Estado:** Actualizada con resultados de entrevista sesión 1 (13/06/2026). Los puntos `[PENDIENTE sesión 2]` se validan en la segunda sesión con el administrativo.
**Reemplaza a:** v2.0 (borrador con supuestos).

---

## 1. Propósito y modelo de negocio

La oficina es un **Colegio de Gestores** que tramita gestiones administrativas de vehículos ante DGT **para gestorías** — modelo B2B. Volumen real confirmado: **~200 trámites/día** (170 transferencias + 30 matriculaciones) operados por **4 administrativos**, con SLA de **cierre en el mismo día**.

**Finalidad del sistema:** automatizar al máximo el procesamiento repetitivo para liberar carga de los administrativos. **Tyrion** gestiona el flujo documental, el cruce con Tempus y la preparación de expedientes para presentación física ante DGT.

## 2. Actores

| Actor | Rol |
|---|---|
| **Gestoría** (cliente) | Envía solicitudes y documentación (70 gestorías registradas por email y teléfono fijo). Nunca llega documentación de remitentes no reconocidos. |
| **Tyrion** (agente IA) | Dueño primario del flujo: recibe, clasifica, coteja, asigna estados, conversa con la gestoría, prepara expedientes y apoya la carga en sistemas externos. |
| **Administrativo** (×4) | Supervisión y excepciones. Usan el sistema desde PC de oficina con login individual. Acceso: misma vista para todos + dueño. |
| **DGT / Tráfico** | Destino de presentaciones físicas y origen de observaciones. Sin sede electrónica — presentación presencial o por nube compartida. |
| **Cadetería** | Empleado del Colegio que lleva físicamente los expedientes a DGT. |

## 3. Canales — confirmados en entrevista

**Entrada:**
- **Email:** ~50% transferencias, ~10% matriculaciones.
- **Papel físico:** ~50% transferencias, ~90% matriculaciones.
- **WhatsApp / Telegram: NO SE USAN** — confirmado en entrevista. Eliminado del modelo.
- Todo remitente se matchea contra el registro de las 70 gestorías. No llega documentación de remitentes desconocidos.

**Salida:** email + cadetería para documentación física.

**Canal con DGT:**
- **Presencial** (empleado del Colegio lleva expediente físico a tráfico) o **nube compartida** con DGT (para observaciones y respuestas).
- Sin integración electrónica ni certificado digital — presentación siempre requiere paso humano.
- Comprobante de entrega: `[PENDIENTE sesión 2 — A4.4/A4.5]`

## 4. Las cuatro capas documentales

Se mantienen de v2.0:
1. **Documento requerido** — lo que el trámite necesita (checklist por tipo).
2. **Documento recibido** — el archivo/papel que llegó.
3. **Documento detectado** — lo que Tyrion interpreta que contiene, con nivel de confianza.
4. **Documento válido** — el que efectivamente desbloquea ESE trámite.

**Evidencia compatible ≠ documento válido** (regla de oro, se mantiene).

La lista de documentos requeridos está formalizada en **Reglamentación general de vehículos título IV**. Puede cambiar a mitad del trámite — ejemplo confirmado: en herencias el sistema puede pedir certificado de defunción tras validar la documentación inicial.

Catálogo completo de checklists por tipo: `[PENDIENTE — listado prometido por el administrativo, sesión 2]`

## 5. Modelo de datos conceptual

- **Documento**: archivo o papel digitalizado, tipo detectado + confianza, versión (reenvío corregido sustituye y conserva anterior como historial), ubicación física si existe papel.
- **Trámite**: tipo (transferencia / matriculación / baja / otros), gestoría, matrícula/bastidor, estado Tempus, estado Tyrion, relojes activos, responsable actual.
- **Vínculo Documento↔Trámite** (N:M): validez vive en el vínculo (`válido / evidencia compatible / rechazado / no aplica`).
- **Mensaje**: canal, trámite, contenido, estado `preparado / enviado / respondido`.
- **Albarán**: registro diario por gestoría para carga en SAGE (número de serie, fecha, gestor, tipos de trámite por código).
- **Solicitud de envío físico**: expedientes incluidos, estado `preparada / llevada a DGT / entregada / incidencia`. Comprobante de entrega: `[PENDIENTE sesión 2]`

## 6. Estados — dos capas

### Tempus (sistema actual del Colegio)
Sistema central donde vive el trámite. Los gestores cargan los trámites y documentación; el Colegio avanza los estados hasta finalizar.

Estado confirmado: **"Finalizado"** — se asigna cuando se presenta toda la documentación sin errores y se imprimen los permisos.

Vocabulario completo de estados en Tempus: `[PENDIENTE sesión 2 — B6, CRÍTICO para el modelo de datos]`

### Capa visible en Tyrion (Control) — 6 macro-estados
| Macro-estado | Significado operativo |
|---|---|
| 🆕 **Entrada** | Llegó, identificándose gestoría y tipo. |
| ⚙️ **En proceso** | Tyrion trabajando: clasifica, coteja, prepara. |
| ⏳ **Esperando gestoría** | Falta algo; Tyrion ya lo pidió. |
| 🔴 **Requiere administrativo** | Excepción escalada con resumen completo. |
| 📤 **En organismo** | Presentado físicamente a DGT; pendiente respuesta. |
| ✅ **Cerrado** | Resuelto y archivado. |

### Capa interna (sub-estados)
Se mantiene la arquitectura de v2.0. Pendiente: alinear con vocabulario real de Tempus tras sesión 2.

## 7. Relojes (SLA)

- **Regla madre: cierre en el mismo día.** Todos los trámites tienen la misma prioridad — se realizan en el día.
- Los trámites pendientes (documentación incompleta o incorrecta de la gestoría) son visibles en Tempus.
- Si falta documentación: Tyrion solicita de inmediato → reintentos → sin respuesta → escala a administrativo.
- Lo no cerrado al fin del día aparece como **arrastre** priorizado en Control a la mañana siguiente.
- Subsanaciones DGT: se gestiona en el día de la observación. La gestión con la gestoría también se hace el mismo día; el plazo de cierre real depende de la respuesta del cliente final o de la gestoría.
- Plazos legales exactos de subsanación: `[PENDIENTE sesión 2 — B9]`

## 8. Flujo principal confirmado (end-to-end)

**Inicio del día:**
1. Abrir sistema Gestión Tráfico → descargar listado de trámites (matriculaciones, transferencias, bajas) → exportar a Excel.
2. Las gestorías envían la **"Relación de transmisiones"** o **"Relación de matriculaciones"** (formulario duplicado) junto con la documentación de cada trámite.
3. Cruzar el formulario de relación contra el listado de Gestión Tráfico.

**Procesamiento:**
4. Ordenar trámites por gestoría.
5. Cotejar documentación de cada trámite contra checklist.
6. Los trámites que llegan incompletos o con error → notificar a la gestoría (por Tempus, email o teléfono).
7. Documentos que llegan por email → imprimir, ordenar, cotejar.
8. Documentos que llegan físicamente → ordenar, cotejar.
9. Cuando el expediente está completo → empleado lo lleva físicamente a DGT.
10. Tempus avanza a **"Finalizado"** cuando se imprimen los permisos.

**Facturación:**
11. La gestoría envía por email la **hoja de caja** (listado de trámites realizados en el día) → cargar manualmente en SAGE como albarán (número de serie, fecha, gestor, tipos por código).
12. A fin de mes → emitir factura desde SAGE de forma manual con los albaranes del mes.
13. Cruce de control: hoja de caja vs. listado de Gestión Tráfico. Sin mayores problemas — excepción: trámites bloqueados/devueltos donde la gestoría factura antes del cierre real.

**Excepción — antecedentes:**
- Tempus exporta a Excel el listado de trámites del mes → se usa para calcular y facturar el **pago de antecedentes** (cargo adicional al gestor según cantidad de trámites).

## 9. Integración con sistemas externos

| Sistema | Mecanismo real confirmado | Integración Tyrion |
|---|---|---|
| **Tempus** | Sistema central. Gestores cargan; Colegio avanza estados. Exporta a Excel. | Leer estados, cruzar con hoja de caja, detectar pendientes. |
| **DGT / Gestión Tráfico** | Presencial + nube compartida. Sin API ni certificado digital. | Preparar expediente; la presentación física es siempre humana. |
| **SAGE** | Carga manual diaria de albaranes. Factura mensual manual. | Asistir preparación del albarán; no reemplaza la carga manual en v1. |

Regla: **Tyrion prepara, el humano ejecuta** para las cargas en sistemas externos en v1.

## 10. Pantallas

- **Control** — torre del día: 6 macro-estados, contadores, arrastre, bandeja 🔴 como única lista de acción humana.
- **Trámites** — búsqueda e histórico (por matrícula, gestoría, fecha, tipo, estado).
- **Detalle del trámite** — qué falta, qué detectó Tyrion, qué se pidió, acción recomendada.
- **Documentos** — fuente de verdad documental; relación N:M con trámites.
- **Timeline/Auditoría** — historia cronológica completa por trámite.

**Acceso:** 4 administrativos + dueño. Todos desde PC de oficina. Misma vista para todos. Login requerido. Sin acceso móvil ni remoto.

## 11. Reglas de oro (v2.1)

1. **Tyrion prepara; el humano presenta.** La presentación física a DGT siempre requiere paso humano.
2. **Evidencia compatible ≠ documento válido.**
3. **Mensaje preparado ≠ mensaje enviado.**
4. **El trámite organiza la operación; Documentos conserva la verdad documental.**
5. **Estados simples afuera, precisión adentro.**
6. **El SLA del día manda.** Todos los trámites tienen la misma prioridad.
7. **Ningún documento se asocia a un trámite sin identidad de remitente resuelta.**
8. **WhatsApp/Telegram no forman parte del sistema.** Canal = email + físico.

## 12. Restricciones y costos

- **Presupuesto IA/sistema:** €150/mes confirmado. Aprueba el dueño.
- **Métrica de éxito:** horas ahorradas (confirmado con el dueño).
- **~200 trámites/día** → ~4.000–6.000 documentos/mes estimados (3–5 docs por trámite). Estrategia: modelo económico para clasificación masiva; modelo premium solo en conflictos y escalados.
- Presentación a DGT: siempre física/presencial — no hay integración electrónica que automatizar en v1.
- 40% papel en transferencias, 90% en matriculaciones → digitalización por lote es parte del sistema.

## 13. Pendientes para sesión 2

| # | Tema | Sección | Impacto |
|---|---|---|---|
| **1** | **Estados reales de Tempus** — nombre exacto, quién los mueve, ambigüedades | B6 | **CRÍTICO** — modelo de datos |
| **2** | **Flujo matriculaciones** — diferencias con transferencias, qué "se imprime" al finalizar | B4 | **CRÍTICO** — 30 trámites/día, 90% físico |
| **3** | Cadetería — comprobante de envío y confirmación de entrega a DGT | A4.4/A4.5 | Alto |
| **4** | Errores en documentación — % mal enviado, confusiones comunes | B2 | Medio |
| **5** | Catálogo de documentos por tipo de trámite | B3.2 | Medio (listado prometido) |
| **6** | Plazos exactos de subsanación DGT | B9 | Medio |
| **7** | Comunicación con gestoría ante faltantes — canal oficial, tiempos de respuesta | B7 | Medio |
| **8** | Archivo y retención de expedientes | B10 | Bajo |

## 14. Resueltos en sesión 1

| Pendiente v2.0 | Resolución |
|---|---|
| Mecanismo real DGT | Presencial + nube compartida. Sin certificado ni API. |
| Trigger de facturación | Albaranes diarios manuales → factura mensual manual. |
| Rol de Tempus | Sistema central. Sí exporta a Excel. |
| WhatsApp/Telegram | No se usan. Eliminado del modelo. |
| Volumen real | 170 transferencias + 30 matriculaciones/día = ~200/día. |
| Autenticación / acceso | 4 admins + dueño, PC oficina, misma vista, login, sin acceso remoto. |
| Presupuesto y éxito | €150/mes. Métrica = horas ahorradas. |
| Nº de gestorías | 70, registradas por email y teléfono fijo. |

---

## 15. BRIEF PARA EL EQUIPO DE DISEÑO (v2.1 — actualizado con datos reales)

> **Cliente:** Colegio de Gestores que tramita gestiones de vehículos ante DGT para 70 gestorías (B2B). Volumen: 170 transferencias + 30 matriculaciones por día = ~200 trámites/día. 4 administrativos + dueño. SLA: cierre en el mismo día. Todos los trámites tienen la misma prioridad.
>
> **Canal de entrada confirmado:** email (~50% transferencias, ~10% matriculaciones) y papel físico (~50% transferencias, ~90% matriculaciones). **WhatsApp/Telegram no se usan.** 70 gestorías registradas — no llega documentación de remitentes desconocidos.
>
> **Flujo diario real:** el Colegio descarga cada mañana el listado de Gestión Tráfico y lo cruza contra la "Relación de transmisiones/matriculaciones" que envían las gestorías. Coteja la documentación de cada trámite, imprime la que llega por email, y un empleado la lleva físicamente a DGT (presentación siempre presencial o por nube compartida — sin integración electrónica).
>
> **Sistemas:** Tempus (sistema central — gestores cargan trámites y documentación, el Colegio avanza estados, exporta a Excel), SAGE (albaranes diarios manuales, factura mensual manual), Gestión Tráfico (portal DGT para descarga de listados).
>
> **Quieren construir Tyrion**, un sistema que: (1) recibe y clasifica documentación distinguiendo tipo requerido / recibido / detectado / válido (un Modelo 620 NO sustituye un Permiso de circulación); (2) coteja contra el checklist del tipo de trámite (definido en Reglamentación general de vehículos título IV); (3) detecta pendientes y avisa a la gestoría; (4) prepara expedientes para que el humano los lleve a DGT; (5) asiste la carga en SAGE (Tyrion prepara, humano ejecuta en v1); (6) gestiona el arrastre de fin de día; (7) escala a administrativo con resumen completo cuando no hay respuesta o hay conflicto.
>
> **Pantalla Control:** 6 macro-estados (Entrada / En proceso / Esperando gestoría / Requiere administrativo / En organismo / Cerrado) con sub-estados internos. Vocabulario real de estados de Tempus: PENDIENTE sesión 2.
>
> **Acceso:** 4 admins + dueño, PC de oficina, misma vista para todos, login requerido. Sin acceso remoto ni móvil.
>
> **Presupuesto sistema:** €150/mes. Métrica de éxito: horas ahorradas. Integraciones DGT/SAGE: sin API — presentación siempre requiere paso humano en v1.
>
> **Quieren saber:** arquitectura propuesta, qué es viable en una v1 de 8 semanas, qué dejarían para v2, y los principales riesgos.

---

*Mantenido en: `projects/alfa-pyme-tyrion/02-proceso-operativo-v2.md` · repo `julionotaro/estudio-ia` · v2.1 — 14/06/2026*
