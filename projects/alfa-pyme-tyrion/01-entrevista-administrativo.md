# Guía de reunión operativa — Alfa-Pyme / Tyrion
## Entrevista con el administrativo de la oficina

**Proyecto:** Alfa-Pyme / Tyrion — Capa de inteligencia operativa sobre gestión documental de trámites
**Versión:** 2.0 final · **Fecha:** junio 2026
**Duración:** 90 min (puede partirse en dos sesiones de 45)
**Interlocutor objetivo:** administrativo operativo + decisor/dueño para los últimos 10 min (Bloque A, preguntas de presupuesto y acceso)

---

## Cómo usar esta guía

- Pedí **siempre el último ejemplo real**: "contame el último caso en que pasó esto", no respuestas teóricas.
- Los **números aproximados valen**. Anotalos aunque sean "a ojo".
- Anotá el **vocabulario exacto**: cómo llaman a los documentos, estados, organismos. Ese vocabulario será el del sistema.
- **No corrijas** ni expliques cómo "debería" ser. Queremos el as-is, no el ideal.
- Marcá con **⚠** cualquier "depende" y preguntá: "¿de qué depende?". Ahí viven las reglas de negocio.
- Si el tiempo se corta: **la Parte A va primero y siempre**. Es lo que destraba el sistema.

---

## Guía de tiempo (90 min)

| Tiempo | Parte | Objetivo |
|--------|-------|----------|
| 0–30 min | **A — Bloqueantes críticos** | Mecanismos reales de DGT, SAGE, Tempus, acceso, papel, WhatsApp |
| 30–55 min | **B — Mapa del proceso** | Flujo de entrada → validación → presentación → cierre |
| 55–75 min | **C — Sistemas y dolores** | Inventario de herramientas, duplicaciones, tiempos |
| 75–85 min | **D — Criterio humano y cierre** | Excepciones, límites de la automatización |
| 85–90 min | **Decisor** | Presupuesto, criterio de éxito, próximo paso |

---

# PARTE A — Bloqueantes críticos ⚡
*Estas respuestas destraban el diseño técnico del sistema. Sin ellas no se puede cerrar el arquitecto ni el equipo de construcción.*

## A1 — DGT: mecanismo real de acceso y presentación

**A1.1** Cuando consultás o presentás algo ante la DGT, ¿exactamente cómo lo hacés hoy? Opciones posibles: sede electrónica con certificado digital, portal de colaborador, software de gestoría, presencial, otro. Mostranos el último caso paso a paso — si podés compartir pantalla o describirlo pantalla por pantalla, mejor.

**A1.2** ¿Cada cuánto llega una observación o requerimiento de la DGT? ¿Por dónde llega y cómo te enterás — email, notificación en portal, hay que entrar a consultar?

**A1.3** Cuando hay que subsanar algo ante DGT, ¿cuál es el plazo habitual? ¿Cuántas subsanaciones tienen por mes, a ojo?

## A2 — SAGE: qué entra, quién lo carga, cómo

**A2.1** ¿Usan SAGE u otro sistema de facturación/contabilidad? ¿Qué datos del trámite terminan en SAGE y quién los carga?

**A2.2** ¿Qué dispara la factura — el cierre del trámite, la presentación ante DGT, algo del cliente? ¿Pasa que hay trámites cerrados operativamente pero no facturados todavía?

**A2.3** ¿Los datos se cargan a mano copiando desde otro sistema, o hay alguna exportación/importación (Excel, CSV) que ya usen?

## A3 — Tempus: rol exacto en el día a día

**A3.1** ¿Qué registran en Tempus y qué NO registran ahí? ¿Es el sistema "principal" donde vive el trámite o es uno más entre varios?

**A3.2** ¿Qué datos cargás en Tempus que también cargás en otro lado (SAGE, hoja de caja, email, papel)?

**A3.3** ¿Tempus tiene alguna forma de exportar datos (Excel, CSV, API)? ¿Lo han usado?

## A4 — Papel físico: circuito completo

**A4.1** El papel que llega (40 % del volumen según lo relevado): ¿quién lo escanea, con qué equipo, cuándo — al llegar, por lotes, a fin de día?

**A4.2** Después de escanear, ¿qué pasa con el físico — dónde se guarda, cómo lo encontrás si hace falta el original semanas después?

**A4.3** ¿Hay papel que sale de la oficina (cadetería, envío a gestoría, presentación presencial)? ¿Cómo se registra ese movimiento hoy?

## A5 — WhatsApp/Telegram: conversación real

**A5.1** Mostranos (o dictanos) una conversación real reciente de WhatsApp con un cliente, desde el primer mensaje hasta el cierre. ¿Qué partes son siempre iguales y cuáles cambian?

**A5.2** ¿Usás WhatsApp Business o personal? ¿Hay plantillas de mensajes o se redacta cada vez?

**A5.3** Cuando un cliente manda documentos por WhatsApp, ¿cómo los pasás al expediente — descarga manual, carpeta de Drive, directo al sistema?

## A6 — Gestorías como remitentes: identidades autorizadas

**A6.1** ¿Con cuántas gestorías trabajan habitualmente? ¿Sus emails y números de WhatsApp están registrados en algún lado o "se saben"?

**A6.2** ¿Pasa que llega documentación de un email o número que no reconocés? ¿Qué hacés en ese caso?

---

# PARTE B — Mapa del proceso
*Reconstruir el trámite tipo de punta a punta con un caso real.*

## B1 — Entrada y tipificación

**B1.1** ¿Por qué canales llegan las solicitudes y en qué proporción? (WhatsApp / email / llamada / presencial / carpeta compartida)

**B1.2** Cuando llega una solicitud nueva, ¿qué hacés paso a paso en los primeros 10 minutos?

**B1.3** ¿Cómo sabés qué documentos exige cada tipo de trámite? ¿Esa lista existe escrita en algún lado o "se sabe"?

**B1.4** ¿La lista de documentos requeridos puede cambiar a mitad del trámite (variantes, financiación, requerimientos del organismo)? Ejemplo real.

**B1.5** ¿Cómo identificás al cliente cuando escribe desde un número o correo desconocido?

## B2 — Recepción y clasificación de documentos

**B2.1** De lo que envían los clientes, ¿qué porcentaje llega mal — ilegible, incompleto, documento equivocado, foto cortada?

**B2.2** Contame el último caso de un archivo que "parecía una cosa y era otra" (el cliente dijo Permiso y era un 620). ¿Cómo lo descubriste?

**B2.3** Cuando un cliente reenvía un documento corregido, ¿qué pasa con la versión anterior — la reemplazás, la guardás las dos?

**B2.4** ¿Qué hacés con documentos que llegan y no corresponden a ningún trámite abierto?

## B3 — Cotejo y validación

**B3.1** ¿Qué mirás para decidir que un documento es válido para ESE trámite — titular, matrícula, fechas, firmas, importes, sellos?

**B3.2** Permiso de circulación / Modelo 620 / CTI: ¿cómo los distinguís a simple vista y cuál es la confusión más común de los clientes?

**B3.3** ¿Qué datos cruzás entre documentos del mismo expediente — que el titular del 620 coincida con el del permiso, por ejemplo? ¿Qué pasa cuando no cuadran?

## B4 — Comunicación con el cliente

**B4.1** Cuando falta documentación, ¿cómo se lo pedís al cliente — plantilla, redactás cada vez, por qué canal?

**B4.2** ¿Cuántos recordatorios hacés y cada cuántos días? ¿En qué momento pasás a llamar por teléfono?

**B4.3** ¿Cuánto tardan los clientes en responder típicamente? ¿Y en el peor caso?

## B5 — Presentación ante organismos

**B5.1** ¿Ante qué organismos presentan y por qué vía cada uno — sede electrónica, portal, presencial, gestor externo?

**B5.2** ¿Quién arma el expediente final y cómo verifica que está completo antes de enviarlo?

**B5.3** ¿Qué justificante queda de cada presentación y dónde se guarda — número de expediente, resguardo, captura?

## B6 — Seguimiento y subsanaciones

**B6.1** ¿Cómo se enteran de la respuesta del organismo — email, sede electrónica, hay que entrar a consultar? ¿Quién revisa y cada cuánto?

**B6.2** ¿Cómo controlás hoy los plazos para que no se pase ninguno — agenda, Excel, alarmas, memoria? ¿Estuvo alguna vez a punto de perderse un plazo?

**B6.3** Cuando llega una observación, ¿quién la interpreta y la traduce a "qué hay que hacer"?

## B7 — Cierre, arrastre y archivo

**B7.1** ¿Cómo se comunica el resultado al cliente y quién lo hace?

**B7.2** ¿Qué pasa con los trámites que no se cierran en el día — cómo aparecen a la mañana siguiente, quién los revisa, cómo se priorizan?

**B7.3** ¿Dónde se archiva un expediente cerrado y cómo encontrás uno de hace dos años?

**B7.4** ¿Cuánto tiempo conservan la documentación? ¿Hay alguna política de retención o borrado (RGPD)?

---

# PARTE C — Sistemas y dolores

## C1 — Inventario de herramientas

**C1.1** ¿Qué sistemas/software usás durante un día normal — Tempus, SAGE, Excel, Drive/OneDrive, email, WhatsApp Business, sede electrónica, hoja de caja, otros?

**C1.2** ¿En qué momentos copiás los mismos datos en dos sitios distintos? Sé específico: "cuando llega un trámite, lo cargo en Tempus y también en..."

**C1.3** ¿Qué herramienta te encanta y cuál odiás? ¿Por qué?

## C2 — Volumen y tiempos

**C2.1** ¿Cuántos trámites nuevos entran por semana, aproximadamente? ¿Cuántos hay abiertos a la vez en un día normal?

**C2.2** Un trámite "limpio" (sin problemas): ¿cuánto tarda de punta a punta en días? ¿Y cuántas horas reales de trabajo tuyo lleva?

**C2.3** ¿Y uno problemático? ¿Dónde se pierde más tiempo?

**C2.4** ¿Cuáles son las 3 tareas que más tiempo te comen en la semana?

**C2.5** ¿Hay épocas pico — meses, fechas fiscales? ¿Qué cambia en esas épocas?

## C3 — El dolor que más pesa

**C3.1** Si pudieras eliminar UNA tarea mañana, ¿cuál sería?

**C3.2** ¿Hay trámites que se pierden entre sistemas — presentados pero no cerrados en Tempus, o cerrados pero no facturados en SAGE? ¿Con qué frecuencia?

**C3.3** ¿Qué información vive hoy en la cabeza de una persona y en ningún sistema? ¿Qué pasaría si esa persona faltara una semana?

---

# PARTE D — Criterio humano y cierre

## D1 — Límites de la automatización

**D1.1** ¿Qué tipo de casos requieren sí o sí tu criterio y no podrían resolverse "siguiendo reglas"?

**D1.2** Contame el caso más complicado del último mes: qué pasó, quién intervino, cómo se resolvió, cuánto tiempo llevó.

**D1.3** Si mañana un asistente automático gestionara documentos, ¿qué decisiones NO le delegarías nunca?

## D2 — Cierre de la entrevista

**D2.1** ¿Qué pregunta no te hice que debería haberte hecho?

**D2.2** ¿Qué te preocuparía de que una IA participe en la gestión? ¿Y qué te entusiasmaría?

## D3 — Decisor (últimos 10 min, con el dueño/gerente)

**D3.1** ¿Quiénes deberían poder entrar al panel del sistema — solo los administrativos, también el dueño, también gestorías externas? ¿Todos verían lo mismo o habría niveles?

**D3.2** ¿Desde dónde se conectarían — solo PCs de la oficina, también desde casa, móvil?

**D3.3** ¿Qué presupuesto mensual real hay para herramientas de automatización/IA? ¿Quién aprueba?

**D3.4** ¿Contra qué se mediría el éxito del proyecto — horas ahorradas, trámites/día, errores evitados, algo más?

---

# Matrices de captura
*Completar durante o inmediatamente después de la reunión.*

## Matriz 1 — Tipos de trámite

| Tipo de trámite | Frecuencia (%) | Documentos requeridos | Sistema donde se registra | Organismo | Plazo típico |
|----------------|---------------|----------------------|--------------------------|-----------|--------------|
| | | | | | |
| | | | | | |
| | | | | | |

## Matriz 2 — Sistemas de la oficina

| Sistema | Para qué se usa | Quién lo usa | ¿Exporta datos? | Riesgo de doble carga con |
|---------|----------------|-------------|----------------|--------------------------|
| Tempus | | | | |
| SAGE | | | | |
| DGT | | | | |
| Email | | | | |
| WhatsApp | | | | |
| Hoja de caja | | | | |
| Papel físico | | | | |

## Matriz 3 — Estados del trámite (vocabulario real de la oficina)

| Estado (como lo llaman ellos) | Qué significa | Quién puede moverlo | Sigue en Tyrion o pasa a humano |
|------------------------------|---------------|--------------------|---------------------------------|
| | | | |
| | | | |
| | | | |

## Matriz 4 — Dolores priorizados

| # | Dolor descrito | Frecuencia | Tiempo perdido estimado | Quick win posible |
|---|---------------|-----------|------------------------|------------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

---

# Protocolo de cierre
*Antes de terminar la reunión, confirmar estos 5 puntos:*

1. **Mecanismo DGT:** ¿quedó claro cómo acceden — certificado, portal, presencial?
2. **Rol de Tempus:** ¿es el sistema principal o uno más? ¿Puede exportar datos?
3. **Trigger de facturación:** ¿qué dispara la carga en SAGE — el cierre operativo, la presentación, el cobro?
4. **Gestorías:** ¿cuántas son, tienen emails/números registrados, qué pasa con remitentes desconocidos?
5. **Próximo paso acordado:** fecha de demo o siguiente reunión, quién la convoca.

---

## Salidas esperadas al terminar

- **Catálogo de tipos de trámite** con documentos requeridos y tiempos (Partes B + matrices).
- **Mapa de sistemas** con lo que entra/sale de cada uno y las duplicaciones (Parte C + Matriz 2).
- **Vocabulario real de estados** del trámite y del documento (Matriz 3).
- **Mecanismos de integración confirmados** para DGT, SAGE y Tempus (Parte A).
- **Frontera Tyrion / humano**: qué se automatiza, qué exige criterio (Parte D).
- **Relojes del sistema**: plazos de subsanación, recordatorios, SLA real (Partes B6 + C2).
- **Modelo de acceso y autenticación** del panel (D3).
- **Tres dolores priorizados** y quick win comercial (Matriz 4).
- **Presupuesto y criterio de éxito** (D3.3 y D3.4).

---

*Documento mantenido en: `projects/alfa-pyme-tyrion/01-entrevista-administrativo.md` · repo `julionotaro/estudio-ia` · v2.0 — 12/06/2026*
