# Test set — Coordinador v0

> Criterio de aceptación del paso 1: ≥90% de clasificación correcta (17/18)
> y JSON parseable en el 100% de los casos.
> Cliente ficticio para las pruebas: transportista con 8 camiones, 3 conductores
> fijos, rutas Galicia–Portugal. Cargar un NEGOCIO.md ficticio coherente antes
> de correr la batería.

## Casos claros (1 área)

| # | Encargo | Esperado |
|---|---|---|
| 1 | "Escribime un post para LinkedIn contando que sumamos un camión nuevo a la flota" | CONTENIDO |
| 2 | "¿Cuántos portes hicimos en junio comparado con mayo?" | DATOS |
| 3 | "Asigná un camión y conductor para la carga de mañana en Vigo, descarga en Oporto" | TRAFICO |
| 4 | "Registrá la factura del taller, son 840€ de la reparación del camión 3" | CONTABILIDAD |
| 5 | "Recordame que el viernes vence el plazo para presentar la documentación del permiso de transporte" | AUXILIAR |

## Casos frontera (el clasificador tiene que elegir bien)

| # | Encargo | Esperado | Trampa |
|---|---|---|---|
| 6 | "Pasame el gasto total de gasoil del camión 3 este mes" | CONTABILIDAD | menciona camión, pero pide gasto |
| 7 | "¿Dónde está ahora el camión 5?" | TRAFICO | consulta de dato, pero es seguimiento de flota |
| 8 | "Escribí un email al cliente Lopes avisando que la entrega se retrasa 2 horas" | CONTENIDO | contexto de tráfico, pero el entregable es un texto |
| 9 | "Prepará el informe mensual de facturación para el gestor" | CONTABILIDAD | "informe" suena a DATOS, pero es facturación |
| 10 | "Organizá los albaranes de esta semana en la carpeta compartida" | AUXILIAR | documentos de transporte, pero es organización documental |

## Multi-área (debe dividir en sub-encargos)

| # | Encargo | Esperado |
|---|---|---|
| 11 | "Planificá las cargas del lunes y avisá por email a los tres clientes con su horario" | TRAFICO + CONTENIDO |
| 12 | "Sacá cuántos portes hicimos este trimestre y armá un post celebrándolo" | DATOS + CONTENIDO |

## Ambiguos (debe preguntar, NO delegar)

| # | Encargo | Esperado |
|---|---|---|
| 13 | "Ocupate del tema del camión" | aclaracion (¿qué tema, qué camión?) |
| 14 | "Necesito lo de siempre para el lunes" | aclaracion |

## Fuera de alcance

| # | Encargo | Esperado |
|---|---|---|
| 15 | "Contratame un conductor nuevo" | FUERA_DE_ALCANCE (decisión de contratación humana) |
| 16 | "¿Me conviene comprar otro camión o alquilar?" | FUERA_DE_ALCANCE o aclaracion (decisión estratégica; aceptable derivar a DATOS solo si pide los números) |

## Prioridad

| # | Encargo | Esperado |
|---|---|---|
| 17 | "URGENTE: el camión 2 quedó tirado en la A-52, reorganizá las entregas de hoy" | TRAFICO, prioridad alta |
| 18 | "Cuando puedas, armá el resumen de gastos del mes pasado" | CONTABILIDAD, prioridad normal |

## Cómo correr la batería

1. Montar el chatflow del coordinador en Dify con el prompt + NEGOCIO.md ficticio.
2. Pasar los 18 encargos uno por uno (conversaciones separadas: sin memoria entre casos).
3. Anotar por caso: área devuelta, ¿JSON parseable?, ¿brief completo?
4. Falla de formato (JSON roto) = falla del caso aunque el área sea correcta.
5. Resultado en tabla al pie de este archivo al cerrar la sesión de prueba.

## Resultados

| Fecha | Modelo | Aciertos | JSON OK | Notas |
|---|---|---|---|---|
| — | — | —/18 | —/18 | pendiente |
