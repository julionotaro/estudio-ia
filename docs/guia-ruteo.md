# Guia de ruteo — donde trabajar cada cosa

## Al iniciar cualquier chat

Dos lineas siempre:
Proyecto: [Estudio / Colegio / Laboratorio / NuevoCliente]
Objetivo de este chat: [una linea]

## Donde arranco

Decision de arquitectura o diseno tecnico
  Chat en el proyecto del CLIENTE

Construir algo para un cliente
  Pipeline: Brief a Dify, spec aprobada, encargo a Claude Code. No disenar en el chat.

Explorar algo que no se si sirve
  Proyecto LABORATORIO. Contexto de 5 lineas + tema + pregunta central.

Algo reutilizable que ya funciono
  Promover a estudio-ia/activos/ diciendole a Claude: promove esto a activos.

Leer o escribir en Git
  Verificar que el conector Studio-julio este activo antes de pedirlo.

Ordenamiento, retrospectiva, estructura
  Chat en proyecto ESTUDIO DESARROLLO IA

## Senales de proyecto equivocado

- Hablas de matriculas y CTI en Laboratorio → ir al proyecto Colegio.
- Disenas en el chat en vez de mandar brief a Dify → cortar y mandar el brief.
- Preguntas algo generico de IA en el proyecto del cliente → ir al Laboratorio.

## Que va a Git

- Reutilizable entre clientes → estudio-ia/activos/
- Especifico del cliente → repo del cliente (tyrion/docs/)
- Metodo o infraestructura del estudio → estudio-ia/docs/
- Encargo ya ejecutado → tyrion/docs/encargos/

## Proyectos en Claude y Files recomendados

Estudio Desarrollo IA: contexto-estudio.md, aprendizajes-cursos.md
Colegio de Gestores: contexto-estudio.md, ROADMAP actualizado
Laboratorio: contexto-estudio.md, como-trabajar-laboratorio.md
Cliente nuevo: contexto-estudio.md, brief del cliente
