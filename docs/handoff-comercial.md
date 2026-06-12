# Informe de estado — Estudio IA / Alfa-Pyme / Tyrion

## Handoff para análisis comercial y orientación de venta

**Fecha de corte:** 12 de junio de 2026 · **Versión:** 1.0 (final)
**Proyecto mayor:** Estudio IA
**Subproducto / caso piloto:** Alfa-Pyme / Tyrion
**Objetivo del nuevo análisis:** definir cómo orientar comercialmente la venta de soluciones digitales y sistémicas a empresas/profesionales, usando Alfa-Pyme como caso demostrador, no como único producto.

---

# 1. Visión general

Estudio IA es el proyecto mayor.

La visión no es construir solo una app aislada. La visión es crear un estudio capaz de diseñar, construir y automatizar soluciones digitales para empresas y profesionales usando:

* IA;
* agentes especializados;
* automatización;
* análisis de procesos;
* desarrollo web/app;
* integración de sistemas;
* documentación operativa;
* control de flujos.

Alfa-Pyme / Tyrion es el primer subproducto concreto y sirve como vertical de validación.

El aprendizaje principal hasta ahora es que el valor no está solo en "usar IA", sino en entender procesos reales, detectar fricción operativa y convertirlos en sistemas que reduzcan carga administrativa.

---

# 2. Qué es Alfa-Pyme / Tyrion

Alfa-Pyme es una solución para oficinas administrativas, gestorías, colegios profesionales o áreas de tramitación que trabajan con documentación, expedientes, sistemas externos y seguimiento operativo.

Tyrion es el agente IA operativo visible dentro del sistema.

Su función esperada:

* recibir documentación;
* clasificar documentos;
* detectar faltantes;
* cotejar datos;
* identificar conflictos;
* preparar mensajes;
* gestionar primero con el cliente o gestoría;
* escalar al administrativo solo cuando corresponde;
* resumir por qué un trámite no avanza;
* indicar quién debe actuar;
* controlar estados, plazos y cierres.

El principio central:

> La intervención administrativa debe ser el último recurso, no el primer paso.

---

# 3. Caso vertical actual

El caso actual se orienta a una oficina vinculada a Colegio de Gestores / Gestorías / DGT.

El flujo observado incluye:

* transferencias;
* matriculaciones;
* documentación enviada por gestorías;
* presentación o consulta en DGT;
* facturación en SAGE;
* hoja de caja;
* cadetería documental;
* uso consolidado de Tempus como sistema compartido de gestión diaria;
* comunicación con gestorías;
* seguimiento de observaciones y subsanaciones;
* archivo y cierre.

Este descubrimiento cambió el enfoque.

Antes Alfa-Pyme podía entenderse como gestor documental inteligente. Ahora debe entenderse como:

> Capa de inteligencia operativa entre documentos, trámites y sistemas existentes.

> **Nota técnica (agregado 12/06):** el descubrimiento de Tempus como sistema consolidado tiene impacto directo en el diseño técnico: pasa a ser una integración con estado A VERIFICAR junto a DGT y SAGE, y se incorporó a la guía de entrevista (Bloque 14). El rol exacto de Tempus (qué datos viven ahí, si tiene exportación/API, quién lo administra) es hoy el dato individual de mayor impacto en producto y en discurso comercial: define si Alfa-Pyme "lee" Tempus, lo complementa o convive con doble carga puntual.

---

# 4. Problema comercial detectado

El riesgo principal es que Alfa-Pyme se perciba como "otro sistema más".

La oficina ya trabaja con:

* Tempus;
* DGT;
* SAGE;
* hoja de caja;
* email;
* WhatsApp;
* papel físico;
* carpetas;
* posibles Excel internos.

Si Alfa-Pyme exige cargar lo mismo otra vez, puede fracasar aunque técnicamente funcione.

La propuesta comercial debe evitar vender "una nueva plataforma de gestión" sin matices.

Debe vender:

* menos persecución manual;
* menos errores documentales;
* menos olvidos;
* menos trámites bloqueados sin dueño;
* menos doble carga;
* mejor control entre sistemas;
* mejor trazabilidad;
* mejor priorización;
* mejor preparación de acciones.

---

# 5. Posicionamiento recomendado

No vender inicialmente como:

> "Reemplazamos Tempus."

Vender como:

> "Una capa de inteligencia y control que se apoya sobre los sistemas existentes y ayuda a que los trámites avancen sin depender de memoria, persecución manual o revisión repetitiva."

Frase comercial posible:

> "Alfa-Pyme no viene a sumar otra pantalla de carga. Viene a mirar lo que ya ocurre entre documentos, Tempus, DGT, SAGE y la oficina, detectar lo que bloquea cada trámite y preparar la próxima acción para que el administrativo intervenga solo cuando aporta valor."

---

# 6. Estado funcional del producto Alfa-Pyme

Se trabajó durante varias fases en un prototipo funcional con backend y frontend.

Estado técnico conocido:

* backend FastAPI;
* frontend React;
* MongoDB;
* OpenAI SDK directo integrado en etapas previas;
* endpoints de trámites, documentos, checklist, cotejo, decisión e historial;
* tests backend previamente reportados como estables;
* CI básico en GitHub Actions;
* consola operativa con mejoras visuales;
* pantalla de detalle de trámite mejorada;
* documentos y trámites visibles;
* lógica de caso Permiso / Modelo 620 / CTI trabajada;
* Tyrion visible como agente operativo;
* ajustes para evitar falsos positivos en detección Permiso / Modelo 620;
* validaciones frontend con build OK en tareas previas.

> **Aclaración de versiones (agregado 12/06):** conviven dos artefactos que no deben confundirse en una conversación comercial:
>
> 1. **Prototipo previo** (lo descripto arriba: FastAPI + MongoDB + OpenAI SDK): funcional, útil como demo visual y prueba de concepto de Tyrion.
> 2. **Diseño validado por el estudio** (junio 2026): el Equipo de Diseño produjo specs formales con otro stack (Node.js/Express + PostgreSQL + React), schema de datos con la regla de oro del dominio (la validez del documento vive en el vínculo documento-trámite, N:M), contratos de API, máquina de 6 macro-estados y plan de 5 semanas. Es la base de la construcción real.
>
> Para la venta: el prototipo demuestra "esto se ve así"; el diseño validado demuestra "esto se construye con método y control de calidad". Son dos activos distintos y complementarios.

Limitación actual:

* el producto no debe seguir avanzando solo por desarrollo técnico;
* necesita validación de proceso real;
* necesita definición comercial clara;
* necesita entender convivencia con sistemas existentes.

---

# 7. Estado del proyecto Estudio IA

Estudio IA se orientó como plataforma interna para desarrollar soluciones.

Componentes trabajados:

* repositorio `julionotaro/estudio-ia`;
* prompts canónicos de agentes;
* Dify como entorno de agentes;
* n8n como router/automatizador;
* GitHub como fuente de verdad;
* Codex como brazo operativo sobre repos;
* Hostinger VPS como entorno self-hosted;
* workflow `Studio Intake Router`;
* integración de Dify/n8n/GitHub en pruebas;
* idea de AI Studio Director como interlocutor principal;
* equipo de agentes por fases: diseño, build, QA, deploy, documentación.

Estado conceptual:

* el proyecto pasó de "app Alfa-Pyme" a "estudio capaz de construir soluciones digitales/sistémicas".
* Alfa-Pyme funciona como primer vertical demostrador.
* El reto actual ya no es solo técnico, sino comercial y metodológico.

> **Estado verificado al 12/06/2026 (agregado):** los dos equipos de agentes están endurecidos y verificados con corridas reales:
>
> * **Equipo de Diseño** (7 agentes + Knowledge Base): calidad medida 9,5/11 en test de generalización; el Critic rechaza con motivos concretos cuando faltan definiciones de negocio.
> * **Equipo Constructor** (10 agentes): cada builder declara inventario y supuestos (BUILD_STATUS) y verifica cobertura 100% al cierre (VERIFICACIÓN); los 3 QA actúan como auditores reales con veredicto vinculante. En las corridas de prueba detectaron, sin intervención humana: ausencia de autenticación, circuit breakers implementados como stub, validaciones de tipos sin reglas de negocio, y una confirmación de cierre exigida por las specs que el frontend omitió.
> * **Métricas de operación:** corrida de diseño 80–125 s (~0,14 USD); corrida de construcción 200–215 s (~0,09 USD). Pipeline invocable vía n8n.
>
> Esto convierte al estudio mismo en un activo demostrable: no se vende "una IA", se muestra un sistema de producción con control de calidad auditable, donde los rechazos quedan documentados con evidencia. Encaja directo con el criterio "no vender humo".

---

# 8. Aprendizaje metodológico

El método que mejor funcionó:

1. Entender el proceso real.
2. Separar análisis de ejecución.
3. Usar especialistas/agentes para producir criterio.
4. Usar Codex/OpenHands como ejecutores, no como directores estratégicos.
5. Mantener repos como fuente de verdad.
6. Trabajar con tasks acotadas.
7. Evitar cambios amplios sin validación.
8. Buscar evidencia antes de construir.

Aprendizaje crítico:

> Documentar mucho no equivale a avanzar. El sistema debe reducir carga operativa real, no crear governance infinita.

---

# 9. Estado de la entrevista administrativa

Se partió de dos documentos:

1. Entrevista operativa larga al administrativo.
2. Cuaderno de reunión operativa Colegio / Gestorías / DGT.

Conclusión:

* el cuestionario largo es buen banco de profundidad;
* el cuaderno es buen mapa específico del Colegio;
* faltaba una guía profesional basada en modelo de proceso;
* se reforzó con matriz documental, matriz de sistemas, matriz de estados y matriz de cierre.

Nuevo enfoque de entrevista:

* no hacer solo preguntas;
* reconstruir casos reales;
* mapear trámite completo;
* mapear documento completo;
* mapear sistema por sistema;
* evitar que se escape salida/cierre;
* detectar riesgo de doble carga;
* definir quick win comercial.

> **Agregado 12/06:** la guía del repo (`projects/alfa-pyme-tyrion/01-entrevista-administrativo.md`) incorpora el **Bloque 14 — Bloqueantes de diseño, prioridad máxima** (preguntas 51–59), derivado de las corridas reales del estudio: mecanismo DGT paso a paso, SAGE, rol y datos de Tempus, autenticación y acceso al panel, circuito del papel físico (40 % del volumen), conversación WhatsApp real, y presupuesto/criterio de éxito para el decisor. Si el tiempo de entrevista se corta, ese bloque va primero: cada respuesta destraba una parte del sistema **y** una promesa comercial.

---

# 10. Hipótesis comercial actual

Hipótesis fuerte:

> Las oficinas no compran "IA documental". Compran alivio operativo, control, menos errores, menos seguimiento manual y seguridad de que nada queda perdido entre sistemas.

Hipótesis de venta:

Alfa-Pyme puede venderse mejor como:

* diagnóstico operativo + solución;
* automatización documental;
* control de trámites;
* capa de inteligencia sobre sistemas existentes;
* asistente de oficina administrativa;
* copiloto para expedientes;
* reducción de carga repetitiva;
* mejora de trazabilidad.

No debería venderse primero como:

* reemplazo de ERP;
* reemplazo de Tempus;
* sistema integral cerrado;
* robot que hace todo;
* IA autónoma sin control humano.

---

# 11. Clientes potenciales

Vertical inicial:

* colegios de gestores;
* gestorías de transporte;
* oficinas administrativas de alto volumen;
* asesorías con documentación repetitiva;
* empresas que gestionan expedientes;
* departamentos administrativos con varios sistemas desconectados.

Verticales futuros:

* logística;
* seguros;
* recursos humanos;
* legal/documental;
* administración de comunidades;
* tramitaciones públicas;
* backoffice de pymes;
* operaciones con facturación/documentos/plazos.

---

# 12. Dolor que probablemente vende mejor

Dolores comerciales principales:

1. "No sabemos qué está bloqueado hasta que alguien pregunta."
2. "Tenemos documentación en muchos canales."
3. "El administrativo pierde tiempo persiguiendo faltantes."
4. "Los sistemas no se hablan."
5. "Se copian datos varias veces."
6. "Hay trámites presentados pero no cerrados."
7. "Hay resueltos pero no facturados."
8. "Hay documentos físicos sin trazabilidad clara."
9. "Hay estados ambiguos."
10. "La información vive en la cabeza de una persona."

---

# 13. Oferta comercial posible

No ofrecer directamente "licencia mensual de software" sin diagnóstico.

Oferta inicial recomendada:

## Fase 1 — Diagnóstico operativo

Entrega:

* mapa de flujo;
* matriz documental;
* matriz de sistemas;
* matriz de bloqueos;
* quick wins;
* propuesta de automatización.

## Fase 2 — Prototipo específico

Entrega:

* consola visual;
* carga documental;
* detección de faltantes;
* resumen de bloqueos;
* flujo Tyrion;
* simulación con casos reales anonimizados.

## Fase 3 — Piloto controlado

Entrega:

* uso con un tipo de trámite;
* medición de tiempo;
* reducción de errores;
* validación con administrativos;
* decisión de integración.

## Fase 4 — Integración progresiva

Entrega:

* exportaciones;
* carga asistida;
* conexión con sistemas posibles;
* automatización por permisos;
* reporting.

---

# 14. Qué debe analizar el nuevo GPT comercial

Pedirle que analice:

1. Propuesta de valor.
2. Segmento de cliente inicial.
3. Dolor principal.
4. Mensaje comercial.
5. Oferta de entrada.
6. Pricing.
7. Modelo piloto.
8. Objeciones.
9. Riesgo de "otro sistema más".
10. Cómo vender Estudio IA sin limitarlo a Alfa-Pyme.
11. Cómo usar Alfa-Pyme como caso demostrador.
12. Qué prometer y qué no prometer.
13. Cómo estructurar una reunión comercial.
14. Qué materiales preparar.
15. Qué demo mostrar.

---

# 15. Prompt recomendado para abrir el nuevo chat

Usar este texto:

> Actúa como consultor senior de Product Marketing B2B, Go-to-Market y venta consultiva de soluciones digitales/IA para pymes y despachos profesionales.
>
> Necesito analizar comercialmente un proyecto llamado Estudio IA. Estudio IA no es solo una app: es un estudio que diseña y construye soluciones digitales, sistémicas y de automatización para empresas/profesionales usando IA, agentes, n8n, Dify, GitHub, desarrollo web y análisis de procesos.
>
> El primer caso demostrador es Alfa-Pyme / Tyrion, una solución para oficinas administrativas, gestorías o colegios profesionales que gestionan trámites documentales. Tyrion es un agente IA operativo que clasifica documentos, detecta faltantes, coteja datos, prepara mensajes, resume bloqueos, controla plazos y escala al administrativo solo cuando corresponde.
>
> El caso actual se centra en Colegio de Gestores / Gestorías / DGT. La oficina ya usa Tempus como sistema consolidado de gestión diaria, DGT para presentación/consulta, SAGE para facturación, hoja de caja, email, WhatsApp y documentación física. El riesgo principal es que Alfa-Pyme sea percibido como "otro sistema más". Por eso debe posicionarse como capa de inteligencia y control sobre sistemas existentes, no como reemplazo inicial.
>
> Necesito que analices cómo orientar la venta del producto y del proyecto mayor. Quiero una mirada crítica, no complaciente. Debes ayudarme a definir: cliente ideal, problema prioritario, propuesta de valor, mensaje comercial, oferta de entrada, pricing, piloto, objeciones, demo, materiales de venta y cómo presentar Estudio IA sin quedar encasillado solo en Alfa-Pyme.
>
> Criterios: no vender humo, no prometer integraciones sin validar, no presentar la IA como magia, priorizar reducción de carga operativa, trazabilidad, control entre sistemas, quick wins y adopción real por administrativos.

---

# 16. Preguntas que el nuevo GPT debería responder

1. ¿Qué vendemos realmente?
2. ¿A quién se lo vendemos primero?
3. ¿Qué dolor tiene más fuerza comercial?
4. ¿Conviene vender diagnóstico, piloto o producto?
5. ¿Cómo evitar la objeción "ya tenemos Tempus"?
6. ¿Cómo explicar que Alfa-Pyme no es otro sistema más?
7. ¿Qué demo debería ver un cliente?
8. ¿Qué métricas prometibles podemos usar?
9. ¿Qué precio inicial sería razonable?
10. ¿Qué no debemos prometer todavía?
11. ¿Cómo convertir Alfa-Pyme en caso de éxito de Estudio IA?
12. ¿Qué otros verticales pueden salir después?

---

# 17. Recomendación estratégica actual

La recomendación actual es:

> Estudio IA debe vender capacidad de transformación operativa mediante soluciones digitales e IA. Alfa-Pyme debe usarse como primera prueba concreta en un vertical con dolor real: oficinas saturadas por trámites, documentos, sistemas inconexos y seguimiento manual.

El mensaje no debería ser:

> "Creamos una app con IA."

El mensaje debería ser:

> "Analizamos cómo trabaja tu oficina, detectamos dónde se pierden tiempo, documentos y seguimiento, y construimos una capa digital que ayuda a que los procesos avancen con menos carga humana."

---

# 18. Estado de decisión

Antes de vender, falta validar:

1. Matriz documental real.
2. Rol exacto de Tempus.
3. Qué datos se duplican.
4. Qué parte del cierre duele más.
5. Qué quick win tiene valor inmediato.
6. Qué demo mostrar.
7. Qué promesa comercial es creíble.
8. Qué precio puede aceptar un primer cliente.
9. *(Agregado 12/06)* Mecanismo real de acceso a DGT y SAGE — define qué integraciones se pueden prometer y cuáles solo como "carga asistida".
10. *(Agregado 12/06)* Modelo de acceso y autenticación del panel — quién entra, desde dónde, con qué permisos.

No conviene seguir construyendo muchas funciones antes de esta validación.

La próxima acción recomendada:

> realizar entrevista operativa con administrativo usando la guía actualizada (Bloque 14 primero si el tiempo es corto), completar matrices y luego definir oferta comercial inicial.

---

# 19. Riesgos comerciales desde la evidencia técnica (agregado 12/06)

Lecciones de las corridas del estudio aplicadas al discurso de venta:

1. **No prometer integración DGT/SAGE/Tempus hasta validar el mecanismo.** El propio sistema de QA del estudio rechaza construcciones que dependan de integraciones no verificadas; el discurso comercial debe tener la misma disciplina. Promesa segura hoy: capa de abstracción + carga asistida; promesa condicionada: integración directa "si el sistema lo permite, tras el diagnóstico".
2. **La seguridad/acceso no es un detalle de implementación.** El QA del estudio rechazó la primera construcción por ausencia de autenticación. En una oficina que maneja datos de clientes y matrículas, "quién ve qué" es pregunta de la primera reunión, no de la fase técnica.
3. **El control de calidad del estudio es argumento de venta.** Poder mostrar a un cliente que el sistema interno rechaza entregas incompletas con evidencia escrita diferencia la propuesta de la "IA mágica" que el mercado ya aprendió a desconfiar.
4. **El papel físico (40 % del volumen) es parte del producto, no una excepción.** El circuito de digitalización y la ubicación física trazable están en el schema de datos desde el diseño; comercialmente es respuesta directa al dolor 8 ("documentos físicos sin trazabilidad").

---

**Documento mantenido en:** `docs/handoff-comercial.md` del repo `julionotaro/estudio-ia` · Versión 1.0 — 12/06/2026
