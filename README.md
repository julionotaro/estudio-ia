# Estudio de Desarrollo IA v0.4.1

Repositorio central del Estudio IA para diseñar, construir y automatizar sistemas, apps, webs y procesos.

## Dirección estratégica

El estudio se valida primero en Dify Cloud y luego se migrará a una instalación self-hosted en Hostinger VPS.

Arquitectura prevista:

- Dify: cerebro conversacional y equipos de agentes.
- n8n: automatización, triggers, webhooks y conexión entre sistemas.
- GitHub: fuente de verdad para prompts, DSL/YAML, documentación, scripts y código.
- Supabase: base de datos por proyecto cuando aplique.
- Vercel: deploy frontend por proyecto cuando aplique.
- Hostinger VPS KVM 2: servidor previsto para alojar Dify + n8n.

## Estado actual

- Equipo de Diseño validado como prototipo en Dify Cloud.
- Equipo Constructor validado como prototipo en Dify Cloud.
- Prompts actuales en Dify son temporales de prueba.
- Los prompts definitivos deben vivir versionados en este repositorio.

## Estructura

- /prompts: system prompts de agentes por fase.
- /dify: apps y exportaciones DSL/YAML de Dify.
- /n8n: workflows futuros de automatización.
- /templates: ARC, briefs y plantillas reutilizables.
- /docs: decisiones y documentación operativa.
- /infra: preparación futura de Hostinger/Docker.
- /projects: documentación por proyecto.
- /scripts: scripts auxiliares.

## Regla de seguridad

Nunca subir .env, API keys, tokens, contraseñas, secretos ni credenciales reales.
