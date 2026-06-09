# Decisiones de Plataforma — Estudio IA

## Decisión actual

Trabajar primero en Dify Cloud para validar apps, chatflows, prompts y estructura operativa.

## Migración futura

Migrar a Dify self-hosted en Hostinger VPS cuando la estructura esté validada.

## Stack previsto

- Dify self-hosted para agentes y chatflows.
- n8n self-hosted para automatización entre sistemas.
- GitHub para versionado de prompts, DSL, documentación y código.
- Supabase por proyecto cuando se requiera base de datos.
- Vercel por proyecto cuando se requiera deploy frontend.
- Hostinger VPS KVM 2 como servidor previsto para Dify + n8n.

## Criterio operativo

1. Validar apps base en Dify Cloud.
2. Exportar DSL/YAML desde Dify.
3. Versionar los DSL/YAML en GitHub.
4. Preparar infraestructura Hostinger.
5. Instalar Dify + n8n self-hosted.
6. Importar apps Dify.
7. Conectar n8n con GitHub, Vercel y Supabase según proyecto.

## Advertencia

Dify Cloud no debe asumir conexiones reales con n8n, GitHub, Vercel, Supabase o Hostinger hasta que esas integraciones existan.
