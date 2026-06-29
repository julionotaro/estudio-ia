# Colegio de Gestores de Pontevedra

Primer cliente del estudio. Producto construido: **Tyrion**, sistema de gestion
documental y verificacion de tramites de vehiculos (transferencias, matriculaciones,
bajas) para el Colegio.

## Datos del cliente

- Entidad: Colegio Oficial de Gestores Administrativos de Pontevedra.
- Volumen: ~200 tramites/dia entre ~70 gestorias, SLA mismo dia.
- Canales de entrada: ~60% fisico, ~40% email.
- Plataforma externa obligatoria: Tempus (web, sin API).
- Contabilidad: SAGE.

## Producto

- Repo: `julionotaro/tyrion` (privado).
- Stack: FastAPI + PostgreSQL, n8n, Dify, clasificador OpenAI.
- Estado: en construccion especulativa (demo/portfolio, sin contrato formal).

## Que de aqui es reutilizable (promovido a /activos)

- Patron RPA Playwright para plataformas sin API (ver `activos/rpa-playwright/`).
- Metodo de encargos a Claude Code.
- Patron de motor de cruce declarativo (tabla de reglas).

## Que NO sale de aqui (especifico de dominio)

- Reglas de tramites de trafico (CTI, modelo 620/650, planillas, cotejo documental).
- Terminologia y flujos del Colegio.
