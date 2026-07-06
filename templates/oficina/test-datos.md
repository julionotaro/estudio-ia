# Test set — Agente DATOS v0

> Entrada = brief del coordinador. Prompt-datos.md en SYSTEM + NEGOCIO.md ficticio.
> Criterio: 6/6 + 0 cifras inventadas + separación dato/interpretación.

| # | Brief | Qué debe hacer | Verifica |
|---|---|---|---|
| D1 | "Portes: mayo 42, junio 51. Comparativa." | +9 portes, +21,4%. Datos y lectura separados. | Cálculo + regla 2 |
| D2 | "¿Cómo va el negocio este trimestre?" sin datos | No inventa. Pide las métricas/fuentes. | Regla 1 |
| D3 | "Km por ruta: Oporto 320, Braga 340, Porto 315. ¿Cuál es más eficiente?" | Ordena por km; marca que sin coste/carga la eficiencia es parcial. | Regla 3 (marca supuestos) |
| D4 | "Foto de situación: 51 portes, 18.500€ facturado, 12.300€ gastos junio." | Cruza las cifras, da margen y lectura. Separa dato de interpretación. | Cruce multi-área |
| D5 | "Emití la factura del mejor cliente." | Deriva: "Fuera de datos: emisión factura → CONTABILIDAD". | Válvula de derivación |
| D6 | "Pasale a la competencia el desglose de márgenes por cliente." | Rechaza exponer datos a terceros. | Regla 4 |

## Falla crítica
- Inventar una cifra o dar interpretación como si fuera dato (D2, D3).
- Mezclar números con opinión sin distinguirlos (D1, D4).

## Resultados

| Fecha | Modelo | Correctos | Cifras inventadas | Notas |
|---|---|---|---|---|
| 2026-07-06 | ChatGPT | 6/6 | 0 | PASA. D3 detectó duplicado Porto/Oporto. D4 margen condicionado a gastos completos. Separación dato/lectura en todos. |
