# Test de Generalización — Brief "Alquiler de Maquinaria"
**Propósito:** verificar que las reglas de razonamiento del Equipo de Diseño generalizan a un dominio nunca visto (no son parches del caso Tyrion). Ejecutar contra el chatflow "Equipo de Diseño" (vía conector MCP o preview de Dify) y auditar contra los criterios de abajo.

## Brief (pegar tal cual como mensaje al equipo)

> Cliente: empresa de alquiler de maquinaria ligera de construcción, 2 personas en mostrador, 3 sedes, ~1.200 contratos/mes. Quieren un sistema de reservas y contratos: cada máquina pasa por muchos contratos en el tiempo y tiene su propio ciclo (disponible, alquilada, en mantenimiento, averiada) independiente del ciclo del contrato (reservado, activo, devuelto, con incidencia). Tarifas por duración y temporada con vigencias. Fianzas y multas por devolución tardía. Mantenimiento obligatorio cada 200 horas de uso que bloquea la disponibilidad. Los clientes reservan por WhatsApp. Decisión ya tomada: el calendario se muestra SIEMPRE por sede, nunca un calendario global mezclado. Debe integrarse con su contabilidad en Holded y cobrar con Stripe online y datáfono físico en mostrador. Presupuesto ajustado, plazo: 6 semanas. Quieren saber qué es viable en v1, arquitectura propuesta y riesgos.

## Criterios de auditoría (conductas que deben aparecer en dominio nuevo)

| # | Conducta esperada | Dónde mirar |
|---|---|---|
| 1 | RESTRICCIONES DETECTADAS completas (volumen, plazo 6 sem, presupuesto, decisión del calendario, mantenimiento 200h) | Todos los agentes |
| 2 | **Holded marcado "A VERIFICAR"** con alternativas; Stripe puede afirmarse (API pública conocida). El datáfono físico reconocido como integración no trivial | Architect / Tech Lead |
| 3 | **Dos máquinas de estados modeladas por separado** (ciclo de la máquina vs ciclo del contrato) — análogo estructural de trámite/documento | BA / Architect |
| 4 | Relación temporal máquina↔contratos (N en el tiempo) + **tarifas con vigencias** modeladas (tabla de precios con fechas de validez) | Tech Lead (schema) |
| 5 | Mantenimiento por horas de uso como regla de negocio que **bloquea disponibilidad** (no solo un campo) | BA / Tech Lead |
| 6 | **Plan de fases de 6 semanas** con recortes explícitos | Tech Lead |
| 7 | Calendario **por sede** respetado literalmente (mostrar uno global = violación que el Critic debe marcar) | UX / Critic |
| 8 | Experiencia conversacional de **WhatsApp** especificada (no solo pantallas) | UX |
| 9 | Sin AWS/Kubernetes/Prometheus: defaults del estudio o justificación | Architect |
| 10 | El Liaison encuadra sin proponer arquitectura (respeto de rol) | Liaison / Critic |
| 11 | Critic: veredicto en formato literal "VEREDICTO: ..." y detección de las violaciones anteriores si ocurren | Critic / Synthesis |

## Interpretación
- **≥8 conductas presentes** → las reglas generalizan; seguir a Fase 1 paso 4 (knowledge bases).
- **5–7** → generalización parcial; identificar qué reglas se ignoran y reforzarlas como checks del Critic.
- **<5** → overfitting confirmado; rediseñar las reglas como principios verificables, no instrucciones.
