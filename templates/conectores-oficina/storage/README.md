# Conector — Storage

> Tier 1. Estado: ESQUELETADO — backends Google Drive + OneDrive listos para
> apuntar credencial. Sin cuenta real todavía.

## Qué hace

Almacén documental de la oficina. Cinco acciones sobre un contrato JSON:
subir, listar, descargar, buscar (por nombre) y crear carpeta.

## Alcance (decisión de diseño)

Storage aquí = almacén documental de oficina (facturas, PDF, imágenes),
que vive en la suite del cliente. Drive/OneDrive cubre a la gran mayoría
de clientes-oficina reales.

NO se incluyen (a propósito): Dropbox/Box (minoritarios, sectores
regulados) ni S3/GCS/Azure Blob (almacenamiento técnico de aplicaciones,
no documental de oficina). La estructura de switch por suite permite
añadir un backend nuevo como una rama más el día que un cliente lo pida,
sin rediseñar.

## Backends

| Acción | Google | Microsoft |
|---|---|---|
| subir | Drive file:upload | OneDrive file:upload |
| listar | Drive fileFolder:search | OneDrive folder:getChildren |
| descargar | Drive file:download | OneDrive file:download |
| buscar | Drive fileFolder:search (name) | OneDrive file:search |
| crear_carpeta | Drive folder:create | OneDrive folder:create |

Dispatcher: `Router Accion (switch 5) → Suite <Accion> (switch 2) → nodo`.
Todas las ramas convergen en `Juntar (merge 10 inputs) → Salida Normalizada`.

## Workflow

| Workflow | ID |
|---|---|
| `[CONECTOR] Storage` | `R6w6Og7BQxYPOFmG` |

## Contrato de entrada

```json
{
  "accion": "subir | listar | descargar | buscar | crear_carpeta",
  "suite": "google | microsoft",
  "nombre": "string  (subir: nombre archivo; crear_carpeta: nombre carpeta)",
  "carpeta_id": "string  (subir/listar/crear: carpeta destino; 'root' por defecto en Drive)",
  "archivo_id": "string  (descargar: id del archivo)",
  "texto_busqueda": "string  (buscar: nombre a buscar)",
  "limite": "number  (listar/buscar: max resultados)"
}
```

El archivo binario a subir viaja en el campo binario `data` del item de entrada.
La descarga devuelve el binario en el campo `data`.

## Contrato de salida

```json
{ "ok": true, "resultado": { "cantidad": N, "items": [ ... ] }, "error": null }
```

## Credenciales (placeholders)

IDs placeholder INVÁLIDOS a propósito: no ejecuta hasta apuntar.

| Backend | Tipo credencial | Nombre convención |
|---|---|---|
| Google Drive | `googleDriveOAuth2Api` | `CRED_STORAGE_GDRIVE_<CLIENTE>` |
| OneDrive | `microsoftOneDriveOAuth2Api` | `CRED_STORAGE_ONEDRIVE_<CLIENTE>` |

## Ensamblaje con cliente real

Según `suite` en NEGOCIO.md:
- **google:** crear credencial Google Drive OAuth2, apuntar los 5 nodos Drive.
- **microsoft:** crear credencial OneDrive OAuth2, apuntar los 5 nodos OneDrive.
- La rama de la otra suite queda inerte. Cero cambios de lógica.

## Pendiente antes de promover a activos/

- [ ] Test real de las 5 acciones con la suite que corresponda.
- [ ] Normalizar shape de `items` — Drive y OneDrive devuelven estructuras
      distintas; si el agente necesita shape único, añadir mapeo en Salida
      Normalizada.
- [ ] OneDrive upload nativo limita a 4MB; para archivos grandes usar sesión
      de carga (upload session) — documentar o añadir rama si hace falta.
- [ ] Integrar en el router: subir/crear_carpeta son escritura → requieren
      aprobación; listar/descargar/buscar son lectura → no requieren.