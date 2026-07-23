# Contrato Coordinador ↔ Auxiliar — Oficina de Agentes

> Entregable 1. Define el formato de mensaje entre agentes, qué decide cada
> uno y la regla de escalado. Es la referencia canónica: si un prompt o un
> workflow contradice este documento, se corrige el prompt/workflow.
> Genérico: sin datos de ningún cliente.

## 1. Canal y transporte

Los agentes NO se hablan directo. Todo pasa por el router n8n:

```
Usuario → webhook oficina-encargo → COORDINADOR → router → AUXILIAR
       → (aprobación humana si hay acción) → conector → registro → respuesta
```

## 2. Mensaje Coordinador → Auxiliar

El coordinador emite SIEMPRE este JSON (y nada más):

```json
{ "encargos": [
    { "area": "AUXILIAR",
      "brief": "instrucción concreta y autocontenida",
      "prioridad": "alta | media | baja" }
] }
```

- `brief` debe poder ejecutarse sin leer la consulta original: el coordinador
  traduce, no reenvía.
- Un encargo por área. Si la consulta requiere varias áreas, varios encargos.
- Si ningún área cubre la consulta: `encargos` con área sin agente → el
  router responde `SIN_AGENTE`. El coordinador NUNCA responde el fondo
  del asunto por sí mismo.

### Qué decide el coordinador
- A qué área va cada parte de la consulta (ruteo).
- Cómo se formula el brief (traducción usuario → instrucción).
- Cuándo no hay área competente (SIN_AGENTE).

### Qué NO decide el coordinador
- Cómo se resuelve el encargo, qué herramienta usar, qué se redacta.

## 3. Mensaje Auxiliar → sistema

Dos formas de respuesta, excluyentes:

**A. Entregable directo** (no toca sistemas externos): prosa con el
resultado (cálculo, agenda, extracción, borrador informativo).

**B. Acción sobre sistema externo o envío a tercero**: línea
`PENDIENTE_APROBACION` + bloque JSON:

```json
{ "instruccion_accion": {
    "herramienta": "<catálogo cerrado>",
    "accion": "<catálogo cerrado>",
    "parametros": { }
} }
```

El catálogo cerrado de herramientas/acciones/parámetros vive en el prompt
del auxiliar (`prompt-auxiliar.md` v2) y en `conectores-oficina/`. Reglas:
un solo bloque por respuesta; parámetros completos y terminados (lo aprobado
es lo que se ejecuta); ninguna clave fuera de catálogo.

### Qué decide el auxiliar
- Cómo cumplir el brief y con qué herramienta del catálogo.
- El contenido íntegro de lo que se envía o se carga (redacción propia).
- Qué campos son dudosos (`campos_a_verificar` en prosa para el humano).

### Qué NO decide el auxiliar
- Ejecutar: NADA se ejecuta sin aprobación humana previa.
- Inventar acciones/parámetros fuera de catálogo.
- Responder encargos de otras áreas (los deriva: "Fuera de auxiliar: X → área").

## 4. Regla de escalado — cuándo decir "no sé" en vez de actuar

El auxiliar DEVUELVE sin actuar (entregable directo tipo "NO PUEDO
EJECUTAR"), en este formato:

```
NO PUEDO EJECUTAR: <motivo en una línea>
Necesito: <dato o decisión concreta que falta>
```

Casos que obligan a escalar (lista cerrada):
1. **Falta un dato necesario** (destinatario, importe, fecha, ID de
   documento): se pide, no se supone.
2. **La acción no existe en el catálogo**: se explica qué se puede y qué no.
   Jamás se emite la acción "más parecida" modificada.
3. **Ambigüedad de destinatario o de sistema destino**: dos interpretaciones
   posibles = pregunta, no elección silenciosa.
4. **Documento ilegible o campo dudoso** en extracción: el campo va como
   "verificar", y si es crítico (importe, nº de factura) se escala entero.
5. **Datos personales expuestos a terceros**: se escala siempre.
6. **Fecha relativa irresoluble** ("pronto", "cuando puedas"): se pide fecha.

Principio: ante la duda, escalar cuesta un mensaje; actuar mal cuesta un
envío real a un tercero. El auxiliar prefiere siempre el mensaje.

## 5. Estados del circuito (contrato con el router)

| Estado | Emisor | Significado |
|---|---|---|
| ENTREGADO | router | entregable directo del auxiliar |
| PENDIENTE_APROBACION | auxiliar | instrucción esperando decisión humana |
| EJECUTADO | router | aprobado y conector OK |
| RECHAZADO | router | humano rechazó; no se ejecutó nada |
| ERROR_CONECTOR | router | aprobado pero el conector falló (queda expediente) |
| SIN_CONECTOR | router | herramienta emitida sin conector desplegado |
| SIN_AGENTE | router | el coordinador no encontró área |

Todo estado terminal se registra en `actividad_oficina` con expediente
completo (consulta, brief, instrucción, aprobación, resultado o incidencia).
