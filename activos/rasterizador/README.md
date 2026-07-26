# Rasterizador — activo transversal

> Microservicio HTTP sin estado que convierte un PDF en imágenes PNG a DPI
> configurable (default **300**). Entra PDF, sale imagen. Nada más.
>
> Origen: test controlado de lectura de fichas manuscritas, 26/07/2026.

## Por qué existe

Las fichas manuscritas escaneadas se leen bien cuando entran a un modelo como
**imagen rasterizada a 300 DPI**, y mal cuando entran como PDF-archivo
(`type:file`). n8n no rasteriza PDF de forma nativa: esta es la pieza que
faltaba en esa cadena.

Es un activo transversal: cualquier cliente con papel escaneado lo reutiliza tal
cual, por eso vive en `activos/` y no en el repo de un cliente.

## Qué NO hace

Es **agnóstico de dominio y sin credenciales**: no lee con IA, no hace barrido de
modelos, no correlaciona nada, no toca Drive. Quien lo llama (n8n) se encarga de
traer el PDF y de la pasada de modelos.

## Cómo se levanta

```bash
docker build -t rasterizador activos/rasterizador/
docker run -p 8000:8000 rasterizador
curl localhost:8000/health          # {"status":"ok"}
```

## Contrato

### `GET /health`

`200` → `{"status": "ok"}`

### `POST /rasterizar`

**Entrada**

| Dónde | Campo | Tipo | Defecto | Qué es |
|---|---|---|---|---|
| multipart | `file` | archivo | — | el PDF (`application/pdf` u `application/octet-stream`) |
| query | `dpi` | int | `300` | resolución de salida, entre `72` y `600` |

**Salida (`200`)**

```json
{
  "dpi": 300,
  "num_paginas": 3,
  "paginas": [
    { "pagina": 1, "ancho": 2480, "alto": 3508, "png_base64": "iVBORw0KG..." }
  ]
}
```

Una entrada por página, en orden; el llamador decide qué página usar.
A 300 DPI una A4 sale ~2480×3508 px.

**Errores**

| Código | Cuándo |
|---|---|
| `400` | archivo vacío, no es PDF, PDF ilegible o corrupto, o excede las 20 páginas |
| `422` | `dpi` fuera del rango 72–600 (validación de FastAPI) |
| `500` | fallo interno al rasterizar |

**Ejemplo**

```bash
curl -F "file=@fichas.pdf" "localhost:8000/rasterizar?dpi=300"
```

## Tests

```bash
pip install -r requirements-dev.txt
pytest -x -q
```

Los PDF de prueba se generan en el propio test con `reportlab` (sin fixtures
binarios). **Localmente hace falta `poppler-utils` instalado** — es la
dependencia de sistema que provee `pdftoppm`, la misma que instala el Dockerfile:

```bash
sudo apt-get install -y poppler-utils      # Debian/Ubuntu
brew install poppler                        # macOS
```

## Pendiente — v1.1

**Recorte por región/fila** (`POST /rasterizar-regiones`): el fallback de lectura
para cuando la página entera no alcanza. Fuera de alcance de v1; se añadirá
gobernado por la barra de corte del barrido de modelos.
