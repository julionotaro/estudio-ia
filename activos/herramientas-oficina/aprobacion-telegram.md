# Loop de aprobación Telegram

> Patrón reutilizable de aprobación humana en medio de un flujo automatizado.
> Validado en producción en ambos caminos (aprobado y rechazado).

## Qué hace

Suspende la ejecución de un workflow, envía un mensaje a Telegram con dos
botones (Aprobar / Rechazar), espera la decisión humana y continúa por la
rama correspondiente. Sin decisión no hay ejecución.

## Estructura (3 nodos)

```
[cualquier nodo] → Solicitar Aprobacion (HTTP Telegram sendMessage)
                 → Esperar Aprobacion   (Wait, resume: webhook)
                 → Resolver Aprobacion  (IF sobre decision)
                      ├─ true  → rama aprobada
                      └─ false → rama rechazada
```

### 1. Solicitar Aprobacion
Nodo HTTP Request → `https://api.telegram.org/bot<TOKEN>/sendMessage`

Body:
```json
{
  "chat_id": "<CHAT_ID>",
  "parse_mode": "HTML",
  "text": "<texto del mensaje>",
  "reply_markup": {
    "inline_keyboard": [[
      { "text": "Aprobar",  "url": "<RESUME_URL>?decision=aprobar" },
      { "text": "Rechazar", "url": "<RESUME_URL>?decision=rechazar" }
    ]]
  }
}
```

`RESUME_URL` es la URL de reanudación que expone el nodo Wait
(`$execution.resumeUrl`).

### 2. Esperar Aprobacion
Nodo Wait con `resume: webhook`. Suspende la ejecución hasta que se llame la
resume URL. La decisión llega en `$json.query.decision`.

### 3. Resolver Aprobacion
Nodo IF: `{{ $json.query.decision }}` equals `aprobar`.

## Parámetros de instalación

| Parámetro | Dónde | Qué es |
|---|---|---|
| Token del bot | credencial Telegram / URL | bot que envía el mensaje |
| `chat_id` | body de Solicitar Aprobacion | destino de la solicitud |
| `texto` | body de Solicitar Aprobacion | contenido a aprobar |

## Reglas operativas (aprendidas en producción)

1. **Escapar el texto interpolado.** `parse_mode: HTML` explícito y escapar
   `&`, `<`, `>` de cualquier contenido dinámico. Sin esto, un texto con
   guiones bajos o símbolos rompe el envío con error 400
   ("can't parse entities"). Nunca interpolar texto libre sin escapar.

2. **Verificar el webhook tras cada cambio.** Después de cualquier cambio de
   credencial o ciclo de publicación, comprobar `getWebhookInfo` de todos los
   bots afectados:
   - `url: ""` → n8n no registró el webhook (credencial o token inválido).
   - URL de otro bot → credencial con el token equivocado.

3. **Un bot por función.** Conviene separar el bot de chat del bot de
   aprobaciones: evita colisiones de webhook y hace el diagnóstico trivial.

## Pruebas realizadas

| Caso | Resultado |
|---|---|
| Aprobado | la acción se ejecutó (envío real de mail confirmado) |
| Rechazado | estado RECHAZADO, ninguna acción ejecutada |
