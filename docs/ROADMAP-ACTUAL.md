# ROADMAP Y ESTADO ACTUAL — Estudio IA
**Actualizado:** 2026-06-15 · **Función:** memoria compartida. Pegar en cualquier chat nuevo para retomar contexto.

---

## 1. EL ESTUDIO — Estado de la fábrica

### Infraestructura ✅
- Dify + n8n self-hosted en Hostinger KVM2 (`187.127.233.43`)
- Repo `julionotaro/estudio-ia` como fuente de verdad

### Equipo de Diseño ✅ — EN USO ACTIVO
7 agentes + 3 nodos Knowledge Retrieval (BA, Architect, Tech Lead).
YAML canónico: `dify/apps/design-team-chatflow.v3.yml` (commit `2f9e377c`).
Fixes v3: ARC_STATUS al inicio del Architect, gate tolerante del Tech Lead,
Critic con check WhatsApp condicional.
Score verificado en test de generalización: 9.5/11.

Invocar vía n8n:
- Brief corto (<2K): `execute_workflow` sobre Studio Intake Router (`WxTdNZUAGZjPbYH6`)
- Brief largo: workflow temporal "Tyrion Design Run (temp)" (`lbzEIUgvtGZTpkdv`)
  con brief en Set node (publicar después de cada update).

### Equipo Constructor de Dify ✅ — VERIFICADO, ROL REDEFINIDO
10 nodos. Pipeline diseño → constructor → auditoría verificado (exec #48-50).
ROL EN ADELANTE: prototipado rápido de proyectos pequeños y demostración del Estudio.
Para proyectos reales como Tyrion → Claude Code construye sobre las specs del Diseño.
El Constructor no queda obsoleto; cambia de rol.

### Pipeline del Estudio (flujo canónico)
```
Entrevista → Spec → Equipo de Diseño → spec APROBADA → Claude Code construye
```
El Equipo de Diseño sigue siendo el primer paso. Su output es lo que consume
Claude Code para construir, en lugar del Equipo Constructor.

### Bridge n8n → Dify
- "Dify Bridge - Equipo Diseño" (`0tGxducQ0fq5uKbs`), webhook `/webhook/dify-design`
- "Studio Intake Router" (`WxTdNZUAGZjPbYH6`), webhook `/webhook/studio-intake`
- Keys actualizadas (builder: regenerada 12/06)
- ⚠ Briefs largos (>2-3K chars): usar workflow temporal con Set node + Code node JSON.stringify

### Conector MCP n8n ("Studio-julio")
Funcionando. Control total de n8n desde Claude.ai. Limit: ~2-2.5K chars en execute_workflow.

---

## 2. TYRION — Proyecto Alfa-Pyme

### Cliente
Colegio de Gestores. 70 gestorías. ~200 trámites/día (170 transferencias + 30 matriculaciones).
4 administrativos + dueño. SLA: cierre en el día. Presupuesto sistema: €150/mes.

### Diseño completado ✅
Corridas del Equipo de Diseño:
- exec #46 (12/06): RECHAZADO — brief sin datos reales
- exec #51 (14/06): RECHAZADO — KB desactualizado
- exec #54 (14/06): APROBADO CON CORRECCIONES — KB actualizado, score 9/10
- exec #55 (15/06): RECHAZADO — YAML viejo (bug ARC_STATUS)
- exec #56 (15/06): APROBADO CON CORRECCIONES — YAML v3, score 9.5/10

Spec canónica: `projects/alfa-pyme-tyrion/02-proceso-operativo-v2.md` (v2.1)
Brief listo para diseño: §15 del spec.

### Entrevista con el administrativo
Sesión 1 completada (13/06). Resultados: `projects/alfa-pyme-tyrion/04-resultados-entrevista-sesion1.md`
Sesión 2 pendiente. Guía: `entrevista-tyrion-sesion2.docx`

Preguntas CRITICAS para sesión 2 (no olvidar):
1. ¿Qué dato lleva el comprobante físico de DGT? (número, sello, fecha)
2. Tiempos reales: ¿cuánto tarda un trámite limpio? ¿Cuáles son las 3 tareas que más consumen?
3. Canal oficial de comunicación con gestorías: ¿Tempus, email o teléfono?
4. ¿Cuántos recordatorios y cada cuánto antes de escalar?
5. % de documentación que llega mal y error más frecuente
6. ¿Reenvío corregido reemplaza o conviven las dos versiones?
7. ¿Flujo de matriculaciones = transferencias? ¿Qué se imprime al finalizar?
8. Listado de documentos requeridos por tipo de trámite (PROMETIDO en B3.2) → carga en tabla requisitos_tramite
9. Cadetería: ¿comprobante de envío a DGT antes de salir?
10. ¿Qué estados ambiguos existen en Tempus además de los 4 confirmados?

### Construcción iniciada ✅
Repo: `julionotaro/tyrion` (privado, creado 15/06)
Commit fundamento: `63863e8a`

Construido:
- Schema PostgreSQL completo (8 tablas, 46 statements, validados con parser real)
- Clasificador documental con Claude API (Haiku para clasificación masiva)
- Catálogo del dominio DGT (tipos documentales + confusiones frecuentes)
- 15 tests pasando (cliente mockeado)

PRINCIPIO DE ESCALADO (confirmado en sesión):
1. Tyrion intenta resolver solo
2. Si falta doc → pide a la GESTORÍA (mensaje PREPARADO, reintentos)
3. Solo si gestoría no responde → escala al ADMINISTRATIVO
El administrativo es el ÚLTIMO recurso, no el primero.

### Próximos módulos (Claude Code sobre fundamento)
1. Motor de cotejo: detectado → válido/evidencia/rechazado contra checklist
2. Ingesta de email (canal principal de entrada)
3. Pantalla Control (6 macro-estados)
4. Cruce hoja de caja vs Tempus → preparar albarán para SAGE

---

## 3. HOJA DE RUTA

### Completado
- [x] Infraestructura Dify + n8n
- [x] Equipo de Diseño (7 agentes, prompts endurecidos, KB activo)
- [x] Equipo Constructor verificado (pipeline completo, rol redefinido)
- [x] Entrevista Tyrion sesión 1 (bloqueantes críticos resueltos)
- [x] Spec Tyrion v2.1 con datos reales
- [x] Corrida de diseño APROBADA (exec #56, score 9.5/10)
- [x] Fundamento de construcción: schema + clasificador + tests

### En curso
- [ ] Entrevista Tyrion sesión 2 (10 preguntas documentadas)
- [ ] Motor de cotejo (siguiente módulo en Claude Code)

### Pendiente — Tyrion
- [ ] Ingesta de email
- [ ] Pantalla Control + Trámites
- [ ] Cruce hoja de caja / SAGE
- [ ] Integración con Tempus (cuando haya API o mecanismo alternativo)
- [ ] Deploy en Hostinger KVM2

### Pendiente — Estudio
- [ ] Client Liaison como Agent app independiente en Dify
- [ ] Deploy Agent + Documenter (prompts ya en `prompts/support-phase/`)
- [ ] URL estable para el MCP de Dify (Cloudflare Tunnel o dominio propio)
- [ ] Bridge n8n definitivo con soporte briefs largos → borrar workflows temporales
- [ ] Triggers de entrada: email → pipeline automático

---

## 4. SEGURIDAD ⚠

- Token GitHub (`ghp_FaGk...`, clásico, todos los repos): activo por decisión de Julio.
  **Revocar y pasar a fine-grained al terminar la sesión de construcción.**
- Keys Dify hardcodeadas en workflows n8n. Key builder regenerada 12/06.
- CLAUDE.md en `julionotaro/tyrion` contiene instrucciones de contexto para Claude Code
  (no contiene credenciales; el token se configura en git remote localmente).

---

## 5. CÓMO RETOMAR CONTEXTO

### En esta conversación (diseño + estrategia)
1. Activar conector "Studio-julio" (n8n).
2. Pegar este documento.
3. Indicar fase y paso.

### En Claude Code (construcción)
```bash
git clone https://github.com/julionotaro/tyrion.git
cd tyrion
git remote set-url origin https://TOKEN@github.com/julionotaro/tyrion.git
claude
```
El CLAUDE.md del repo da el contexto completo al abrir el proyecto.
