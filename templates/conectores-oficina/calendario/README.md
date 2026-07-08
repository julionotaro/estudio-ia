# Conector — Calendario

> Tier 2. Estado: ESQUELETADO — backends Google Calendar + Outlook Calendar
> listos para apuntar credencial. Sin cuenta real todavía.

## Qué hace

Calendario de la oficina: citas, vencimientos, plazos. Cuatro acciones sobre
un contrato JSON: crear, listar, actualizar y eliminar evento.

## Backends

| Acción | Google | Microsoft |
|---|---|---|
| crear | Calendar event:create | Outlook event:create |
| listar | Calendar event:getAll | Outlook event:getAll |
| actualizar | Calendar event:update | Outlook event:update |
| eliminar | Calendar event:delete | Outlook event:delete |

Dispatcher: `Router Accion (switch 4) → Suite <Accion> (switch 2) → nodo`.
Convergen en `Juntar (merge 8) → Salida Normalizada`.

## Workflow

| Workflow | ID |
|---|---|
| `[CONECTOR] Calendario` | `6Ae4XCaiWBX0xwJs` |

## Contrato de entrada

```json
{
  "accion": "crear | listar | actualizar | eliminar",
  "suite": "google | microsoft",
  "calendario_id": "string  ('primary' por defecto en Google)",
  "evento_id": "string  (actualizar/eliminar)",
  "titulo": "string  (crear/actualizar)",
  "inicio": "string ISO 8601  (crear/actualizar)",
  "fin": "string ISO 8601  (crear/actualizar)",
  "descripcion": "string  (crear/actualizar)",
  "limite": "number  (listar)"
}
```

## Contrato de salida

```json
{ "ok": true, "resultado": { "cantidad": N, "eventos": [ ... ] }, "error": null }
```

## Diferencias por proveedor (documentadas)

- **titulo**: Google lo llama `summary`; Outlook `subject`. El conector mapea
  ambos desde `titulo`.
- **descripcion**: Google `description`; Outlook `body`.
- **listar Outlook**: usa `fromAllCalendars: false` + `calendarId`. Google usa
  `timeMin`/`timeMax` con defaults (ahora → +1 semana); si se necesita rango
  explícito, añadir esos campos al contrato.
- **fechas**: ambos esperan ISO 8601. Outlook además maneja timezone por campo;
  hoy se usa el default de la cuenta.

## Credenciales (placeholders)

| Backend | Tipo credencial | Nombre convención |
|---|---|---|
| Google Calendar | `googleCalendarOAuth2Api` | `CRED_CALENDARIO_GOOGLE_<CLIENTE>` |
| Outlook Calendar | `microsoftOutlookOAuth2Api` | `CRED_CALENDARIO_OUTLOOK_<CLIENTE>` |

Nota: el backend Outlook de calendario usa el MISMO tipo de credencial que el
conector mail-Outlook (`microsoftOutlookOAuth2Api`). Con cliente Microsoft, una
sola credencial Outlook puede servir para mail, calendario y (vía OneDrive) parte
de storage — según los scopes que tenga la app registrada en Azure.

## Ensamblaje con cliente real

Según `suite` en NEGOCIO.md:
- **google:** credencial Google Calendar OAuth2, apuntar los 4 nodos Google.
- **microsoft:** credencial Outlook OAuth2, apuntar los 4 nodos Outlook.

## Pendiente antes de promover a activos/

- [ ] Test real de las 4 acciones con la suite que corresponda.
- [ ] Normalizar shape de `eventos` entre proveedores (Google usa start.dateTime,
      Outlook igual pero con estructura propia).
- [ ] Manejo de timezone explícito si el cliente opera en varias zonas.
- [ ] Integrar en el router: listar es lectura (sin aprobación); crear/actualizar/
      eliminar son escritura (requieren aprobación).