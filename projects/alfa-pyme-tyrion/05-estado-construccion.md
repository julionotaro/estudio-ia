# Tyrion — Estado de construcción
**Actualizado:** 2026-06-15 · **Repo del producto:** `julionotaro/tyrion`

## Decisión de arquitectura
Tyrion se construye en su propio repo (`julionotaro/tyrion`), separado del Estudio.
El Estudio (`estudio-ia`) es la fabrica; Tyrion es el producto. No se mezclan.

Stack confirmado: FastAPI + PostgreSQL + Claude API. Deploy en Hostinger KVM2.
- Clasificacion masiva: Claude Haiku (economico, ~4-6k docs/mes dentro de EUR150/mes).
- Conflictos y escalados: Claude Opus (premium, solo cuando hace falta).

## Construido (sesion 1 de construccion, 15/06)
Commit `63863e8a` en `julionotaro/tyrion`:
- Schema PostgreSQL completo (8 tablas, 46 statements validados).
  - Validez en el vinculo documento-tramite (N:M), NUNCA en el documento.
  - 4 estados confirmados: PENDIENTE / EN_REVISION / PRESENTADO / FINALIZADO.
  - Campo num_comprobante_dgt (confirmado: DGT entrega comprobante fisico).
  - Cuarentena de identidad para remitentes no reconocidos.
- Clasificador documental con Claude (primer modulo — cuello de botella: 80% del tiempo es cotejo).
- Catalogo del dominio DGT con confusiones frecuentes (permiso vs 620 vs CTI).
- 15 tests pasando (cliente mockeado).

## PRINCIPIO DE DISEÑO CRITICO para el motor de cotejo (proximo modulo)
El escalado al administrativo es el ULTIMO recurso, no el primero. Orden obligatorio:
1. Tyrion intenta resolver por sus medios.
2. Si falta un documento o hay un error -> Tyrion pide a la GESTORIA directamente
   (mensaje preparado, reintentos dentro de la ventana del SLA).
3. Solo si la gestoria no responde o el caso se traba -> escala al administrativo
   con resumen completo.

Distinguir dos casos que el codigo actual no separa bien:
- Confianza BAJA de clasificacion (Tyrion no sabe QUE es) -> puede requerir ojo humano.
- Documento faltante o erroneo (Tyrion entendio bien) -> pedir a la gestoria, NO escalar.

## Proximos modulos (en Claude Code, sobre este fundamento)
1. Motor de cotejo: detectado -> valido/evidencia/rechazado contra checklist del tramite.
   Implementa el principio de escalado de arriba.
2. Ingesta de email (canal de entrada principal).
3. Pantalla Control (6 macro-estados).
4. Cruce hoja de caja vs listado de Tempus -> preparar albaran para SAGE.

## Pendiente de sesion 2 (no bloqueante para clasificador y cotejo basico)
- Vocabulario completo de estados de Tempus (confirmados los 4 principales).
- Flujo especifico de matriculaciones (en v1 = identico a transferencias).
- Tiempos reales por tramite (define metricas de exito).
