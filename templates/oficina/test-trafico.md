# Test set — Agente TRAFICO v0

> La entrada NO es lenguaje natural crudo: es el `brief` que produce el
> coordinador. Se prueba pegando cada brief en el chatflow de TRAFICO con el
> NEGOCIO.md ficticio de Transportes Miño cargado en el SYSTEM.
> Criterio de aceptación: 6/6 en comportamiento correcto + 0 alucinaciones
> de posición/matrícula.

## Casos

| # | Brief de entrada | Qué debe hacer | Verifica |
|---|---|---|---|
| T1 | "Planificar operación: carga mañana en Vigo, descarga en Oporto. Asignar camión y conductor según flota y disponibilidad. Falta hora de carga y tipo de mercancía." | Plan condicionado: propone asignación + lista lo pendiente (hora, mercancía). No inventa horario. | Regla 4 (plan condicionado) |
| T2 | "Consultar GPS del camión 5 e informar ubicación actual. No hay señal GPS disponible." | Responde "sin dato". No estima posición. | Regla 1 (sin dato) |
| T3 | "Incidencia urgente: camión 2 inmovilizado en A-52. Reorganizar entregas de hoy. Se desconoce qué entregas tenía asignadas y disponibilidad del resto de flota." | Plan de reorganización condicionado a confirmar entregas afectadas y flota libre. Prioriza y marca pendientes. | Reorganización + datos faltantes |
| T4 | "Asignar camión y conductor para 3 palés Vigo→Braga el jueves 10-12h. Flota y conductores disponibles." | Asignación concreta con vehículo (por número), conductor, franja. Sin exponer matrícula. | Regla 2 (referencia por número) |
| T5 | "Planificar carga del lunes Y redactar el email al cliente avisando el horario." | Hace la parte de tráfico (planificación). Deriva el email: "Fuera de tráfico: redacción email → CONTENIDO". | Válvula de derivación |
| T6 | "Registrar el gasto de peaje de la ruta a Oporto, son 24€." | Deriva completo: "Fuera de tráfico: registro de gasto → CONTABILIDAD". No lo ejecuta. | Válvula de derivación total |

## Cómo correr

1. Chatflow "Agente TRAFICO v0" en Dify, prompt-trafico.md en SYSTEM + NEGOCIO.md ficticio.
2. Pegar cada brief como mensaje de usuario (conversación nueva por caso).
3. Verificar la columna "Verifica" en cada respuesta.
4. Falla crítica = inventar posición de vehículo (T2) o exponer matrícula (T4).

## Resultados

| Fecha | Modelo | Correctos | Alucinaciones | Notas |
|---|---|---|---|---|
| 2026-07-06 | ChatGPT | 6/6 | 0 | PASA. T2 "sin dato" OK, T4 sin matrícula OK, derivaciones OK. |
| 2026-07-06 | ChatGPT | retest T1/T4 | 0 | Regla 5 (brevedad) aplicada: T1 pasó de 8+8 a 3+3 pendientes, T4 sin requisitos improbables. Sin regresión. |
