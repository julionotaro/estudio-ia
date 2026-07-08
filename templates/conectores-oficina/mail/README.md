# Conector — Mail

> Tier 1. Estado: ESQUELETADO — envío funcional, lectura/búsqueda con backends
> Gmail + Outlook listos para apuntar credencial. Sin cuenta real todavía.

## Qué hace

Conector único de correo para la Oficina. Tres acciones sobre un contrato JSON:
enviar, leer (bandeja reciente) y buscar (por remitente / texto).

## Arquitectura de backends

A diferencia de lo previsto inicialmente en CONTRATO.md, mail NO es un backend
único. El envío sí es genérico (SMTP sirve para Gmail, Outlook y cualquier
proveedor), pero la lectura/búsqueda no tiene backend genérico limpio en n8n
(el nodo IMAP nativo es solo trigger reactivo). Por eso:

| Acción | Backend | Depende de suite |
|---|---|---|
| enviar | SMTP (`emailSend`) | No — genérico |
| leer | Gmail API / Outlook API | Sí |
| buscar | Gmail API / Outlook API | Sí |

El dispatcher enruta por `accion` y, dentro de leer/buscar, por `suite`.

## Workflow

| Workflow | ID |
|---|---|
| `[CONECTOR] Mail` | `0NOMSF3TgxGFibBj` |

Estructura: `Entrada → Router Accion (switch) →`
- caso enviar: `Enviar SMTP → Salida Enviar`
- caso leer: `Suite Leer (switch) → Leer Gmail | Leer Outlook → Juntar → Salida Lectura`
- caso buscar: `Suite Buscar (switch) → Buscar Gmail | Buscar Outlook → Juntar → Salida Lectura`

## Contrato de entrada

```json
{
  "accion": "enviar | leer | buscar",
  "suite": "google | microsoft  (solo relevante en leer/buscar)",
  "para": "string  (enviar)",
  "asunto": "string  (enviar)",
  "cuerpo": "string  (enviar)",
  "remitente": "string  (enviar: from; buscar: filtro por remitente)",
  "texto_busqueda": "string  (buscar: query estilo Gmail)",
  "limite": "number  (leer/buscar: max resultados)"
}
```

## Contrato de salida

Enviar:
```json
{ "ok": true, "resultado": { "enviado": true, "para": "...", "messageId": "..." }, "error": null }
```

Leer / buscar:
```json
{ "ok": true, "resultado": { "cantidad": N, "mensajes": [ ... ] }, "error": null }
```

## Credenciales (placeholders)

Los tres nodos con credencial usan IDs placeholder INVÁLIDOS a propósito:
el workflow no ejecuta hasta apuntarlos. Convención de nombres:

| Nodo | Tipo credencial | Nombre convención |
|---|---|---|
| Enviar SMTP | `smtp` | `CRED_MAIL_<CLIENTE>` |
| Leer/Buscar Gmail | `gmailOAuth2` | `CRED_MAIL_GMAIL_<CLIENTE>` |
| Leer/Buscar Outlook | `microsoftOutlookOAuth2Api` | `CRED_MAIL_OUTLOOK_<CLIENTE>` |

## Ensamblaje con cliente real

Según la `suite` del cliente (definida en NEGOCIO.md):
1. **Siempre:** crear credencial SMTP con los datos de su cuenta (Gmail y
   Outlook aceptan SMTP; para Gmail con 2FA usar App Password).
2. **Si suite=google:** crear credencial Gmail OAuth2, apuntar Leer Gmail
   y Buscar Gmail.
3. **Si suite=microsoft:** crear credencial Outlook OAuth2, apuntar Leer
   Outlook y Buscar Outlook.
4. La rama de la otra suite queda inerte (nunca se enruta). No molesta.

Apuntar credencial = editar el nodo y seleccionar la credencial creada.
Cero cambios de lógica.

## Pendiente antes de promover a activos/

- [ ] Test real de envío con una cuenta SMTP dummy.
- [ ] Test real de lectura/búsqueda con la suite que corresponda.
- [ ] Confirmar shape de `mensajes` normalizado — hoy Gmail y Outlook
      devuelven estructuras distintas de `from`/`subject`; si el agente
      necesita un shape único, añadir normalización en Salida Lectura.
- [ ] Integrar en el router como conector invocable tras aprobación
      (enviar es acción de escritura → requiere aprobación; leer/buscar
      son solo-lectura → no requieren).