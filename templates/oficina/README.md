# Oficina de agentes — plantillas (EN INVESTIGACIÓN)

**Estado: patrón validado técnicamente, sin cliente. No es un activo.**

Origen: investigación `[OFICINA] Oficina de agentes como producto vendible`,
Laboratorio, julio 2026.

## Qué hay acá

5 prompts de agente + sus test sets + plantilla de replicación por cliente:

- `prompt-coordinador.md` — clasifica el encargo y devuelve JSON con área + brief.
- `prompt-trafico.md` — coordinación de flota (planifica y propone).
- `prompt-auxiliar.md` — administración + RPA con aprobación previa.
- `prompt-contabilidad.md` — cálculo y preparación; registro con aprobación.
- `prompt-datos.md` — informes y foto de situación sobre datos aportados.
- `NEGOCIO-plantilla.md` — unidad de replicación: un archivo por cliente,
  inyectado como variables (nombre_negocio, contenido_negocio) en cada agente.
- `test-*.md` — baterías de prueba, todas PASA (validadas con ChatGPT).

## Áreas (v0)

COORDINADOR · TRAFICO (flota, cargas/descargas, seguimiento) · AUXILIAR
(administración + trámites) · CONTABILIDAD (facturación, cobros, gastos) ·
DATOS (métricas e informes). CONTENIDO está contemplado por el coordinador
pero aún sin chatflow montado.

## Regla de la plantilla

Acá solo vive estructura genérica. El dominio de cada cliente (sistemas,
organismos, terminología) va en el NEGOCIO.md de ese cliente, nunca en
estas plantillas.

## Estado técnico (jul 2026)

5 agentes validados en Dify (test sets en la carpeta, todos PASA).
Router n8n construido y validado de punta a punta:
  webhook → coordinador → área → aprobación humana (webhook plano) → ejecución.
  Workflow: "Oficina Router v0" (6LjeVR7Nl2RheUY9). Ambas ramas de aprobación
  (aprobar → Ejecutar Acción, rechazar → Descartar Acción) probadas OK con
  NEGOCIO.md ficticio (Transportes Miño).

## Pendiente de industrialización (no bloquea el patrón)

- Salida HTTP: limpiar respuesta cruda de Dify (extraer solo `answer`).
- Multi-área: el router v0 procesa el primer encargo; el coordinador ya divide.
- Credenciales: app-keys hardcoded → mover a credencial n8n.
- Canal de aprobación: hoy URL manual; convertir en botón (Telegram/email).
  Al construir la URL de aprobación, concatenar `&decision=...` a resume_url (no `?`).
- Agente CONTENIDO: contemplado por el coordinador, sin chatflow montado.

## Arquitectura de referencia

Coordinador (Dify) → áreas (agentes Dify con rol persistente) → entrega y
aprobación vía n8n. El coordinador es la puerta de la oficina; el Studio Intake
Router sigue siendo la puerta de la fábrica. Coexisten: necesidades distintas.

## Promoción a activos

Pendiente de validación con un cliente real. Cuando ocurra, mover a
`activos/oficina-minima/` y anotar el cliente que lo validó.
