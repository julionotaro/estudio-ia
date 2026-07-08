# Conector — Aprobacion

> Tier 1 — transversal (no depende de suite). Estado: VALIDADO punta a punta con cliente dummy.

## Qué hace

Convierte la URL manual de reanudación del Oficina Router en un botón
Telegram. El humano recibe un mensaje con ✅ Aprobar / ❌ Descartar;
su respuesta reanuda el router y actualiza el registro de estado.

## Workflows

| Workflow | ID | Activado |
|---|---|---|
| `[CONECTOR] Aprobacion - Solicitar` | `0yMYAybDFKtZFayh` | Sí |
| `[CONECTOR] Aprobacion - Resolver` | `kuFWgWvjTVJZStWM` | Sí |

## Data table

- Nombre: `aprobaciones_pendientes`
- ID: `FFBSRcSjMVfcBipK`
- Columnas: `id_aprobacion, resume_url, area_origen, resumen, estado`
- Estados posibles: `PENDIENTE → APROBADA | DESCARTADA`

## Contrato de entrada (Solicitar)

```json
{
  "resume_url": "string — URL de reanudación del Wait node del router",
  "area_origen": "string — TRAFICO | AUXILIAR | CONTABILIDAD | DATOS",
  "resumen": "string — descripción legible de la acción a aprobar"
}
```

Se integra en el Oficina Router v0 (`6LjeVR7Nl2RheUY9`) reemplazando el
nodo `Preparar Aprobacion` → `Solicitar Aprobacion` (Execute Sub-workflow)
→ `Esperar Aprobacion` (Wait). `Preparar Aprobacion` expone `resume_url`,
`area_origen` (desde Parse Coordinador) y `resumen` (el `answer` del agente).

## Flujo completo

```
Router → [CONECTOR] Solicitar
  → genera id_aprobacion
  → guarda en data table (estado: PENDIENTE)
  → envía mensaje Telegram con botones

Humano pulsa botón → [CONECTOR] Resolver
  → parsea decisión (apr:/des: + id_aprobacion)
  → busca resume_url en data table
  → GET resume_url + (? o & según corresponda) + decision=aprobar|descartar
  → actualiza estado en data table (APROBADA|DESCARTADA)
  → responde callback (quita el spinner de Telegram)
  → edita mensaje original (añade ✅/❌ + texto)
```

Nota técnica: el `resume_url` de n8n puede incluir ya un query string
(`?signature=...`), por eso el nodo `Reanudar Router` decide dinámicamente
si concatena con `?` o `&`.

## Credencial

`telegramApi` — convención de nombre: `CRED_APROBACION_<CLIENTE>`.
Con cliente real: crear credencial Telegram API en n8n con el token
del bot del cliente y reapuntar en ambos workflows.

El `chat_id` del aprobador está hardcoded en el nodo `Enviar Solicitud
Telegram` (campo `chatId`). Con cliente real: leer desde `NEGOCIO.md`
o inyectarlo como parámetro de entrada.

## Infraestructura requerida

Telegram exige HTTPS para webhooks. El nginx que sirve el dominio del
VPS (`docker-nginx-1`, parte del stack Dify) necesita rutas explícitas
para n8n además de `/mcp-server/`:

```nginx
# en conf.d/mcp-ssl.conf, dentro del server HTTPS existente
location /webhook/ {
    proxy_pass http://172.17.0.1:5678/webhook/;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_buffering off;
}
location /webhook-waiting/ {
    proxy_pass http://172.17.0.1:5678/webhook-waiting/;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_buffering off;
}
```

Y en `/opt/estudio-ia/n8n/.env`:
```
N8N_HOST=studio-julio.duckdns.org
N8N_PROTOCOL=https
WEBHOOK_URL=https://studio-julio.duckdns.org/
```

Esto ya quedó hecho en el VPS del estudio; documentado acá para
replicar en infraestructura de cliente si el n8n del cliente es
separado.

## Test validado (jul 2026)

Encargo real via Router → AUXILIAR devolvió `instruccion_accion`
PENDIENTE_APROBACION → llegó botón Telegram → aprobar → router se
reanudó (`Ejecutar Accion`) → ejecución completa en `success`.
Rama "Descartar" aún no probada explícitamente (lógica simétrica,
bajo riesgo).

## Pendiente antes de promover a activos/

- [ ] Probar rama Descartar explícitamente.
- [ ] Parametrizar `chat_id` (leer de NEGOCIO.md en vez de hardcoded).
- [ ] Verificar comportamiento ante doble aprobación (filtro `estado:
      PENDIENTE` en Buscar Aprobacion debería silenciar la segunda).
- [ ] Mover Authorization Bearer del nodo mcp-server fuera del nginx
      conf versionado (hoy expuesto en texto plano en el archivo).