# Hard stops del Estudio IA

## Objetivo

Los hard stops son límites no negociables para proteger seguridad, privacidad, producción y trazabilidad del Estudio IA.

## Hard stops obligatorios

El trabajo debe detenerse y reportar bloqueo si requiere cualquiera de los siguientes puntos:

1. No secrets.
2. No tokens.
3. No API keys.
4. No producción sin autorización explícita.
5. No datos reales.
6. No workflows críticos sin task específica.
7. No repos fuera de `julionotaro/estudio-ia`.
8. No inventar exports de Dify ni workflow n8n si no están disponibles.

## Cómo reportar un hard stop

El reporte debe incluir:

- qué acción se intentaba realizar;
- qué regla bloquea la acción;
- qué información o autorización falta;
- cuál es el próximo paso seguro.

## Ejemplos

### Ejemplo 1: se pide usar una API key

Bloqueo: la tarea requiere API key. Próximo paso seguro: Julio debe configurar el secreto manualmente en el panel correspondiente y confirmar que quedó disponible sin compartir el valor.

### Ejemplo 2: se pide publicar a producción

Bloqueo: producción requiere autorización explícita. Próximo paso seguro: solicitar confirmación concreta de entorno, alcance y ventana de despliegue.

### Ejemplo 3: se pide recrear un workflow n8n no disponible

Bloqueo: no se puede inventar un workflow crítico. Próximo paso seguro: documentar el contrato esperado y esperar export real o task específica para implementarlo.
