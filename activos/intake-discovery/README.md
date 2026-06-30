# Intake Discovery — Formulario de descubrimiento

Artifact React standalone para levantar el intake inicial de un caso de uso
(cliente o interno) y generar un Brief estructurado listo para el pipeline
Diseño → Encargo.

## Qué hace

1. Formulario por bloques (Contexto, Problema, Criterio de éxito, Usuarios,
   Datos, Integraciones, Reglas de negocio, Alcance).
2. Dos modos:
   - **En vivo**: 5 bloques clave, pensado para completar junto al cliente en
     una llamada (~10 min).
   - **Self-service**: los 8 bloques completos, para que el cliente lo
     complete de forma asíncrona.
3. Al finalizar, genera localmente:
   - Brief en Markdown (formato compatible con el encargo estándar del Estudio).
   - JSON estructurado con todos los campos del intake.
4. Botón de copiar para pegar el resultado donde se necesite.

## Estado actual

Standalone — corre 100% en el cliente (React), sin llamadas a APIs externas
ni al MCP de Studio. La versión anterior intentaba llamar a la API de
Anthropic + MCP de Studio directo desde el artifact y quedaba colgada en
"Enviando a Studio" (problema de CORS/auth desde el entorno de artifacts).
Se simplificó a generación local pura.

## Próximo paso (pendiente)

Conectar el JSON de salida a un webhook de `[ESTUDIO] Studio Intake Router`
en n8n, para que el intake quede registrado automáticamente y dispare el
agente de discovery (resumen, complejidad estimada, agentes sugeridos).
Hasta entonces, el flujo es: completar formulario → copiar JSON/Brief →
pegar manualmente donde corresponda.

## Reutilización

Este componente no tiene nada específico de Tyrion ni de ningún cliente —
vive en `activos/` según el criterio del Estudio: sirve tal cual para el
próximo cliente sin modificaciones de dominio.

## Uso

Abrir `studio-discovery-intake.jsx` como artifact React en Claude
(pegar el código o subirlo a un proyecto). No requiere variables de entorno
ni configuración adicional.
