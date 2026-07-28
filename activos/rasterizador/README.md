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

### `POST /rasterizar-regiones`

Recorta **regiones** (bounding boxes relativos, 0–1) de las páginas del PDF y las
devuelve en alta resolución. Dos usos:

1. **Leer el campo sobre su banda ampliada**, no sobre la A4 entera. La ficha es
   un formulario de layout fijo → las bandas (columna de km, matrícula, kg…) son
   estables y se definen una vez. Ver el número grande y aislado de su vecindario
   de ruido (OBSERVACIONES, GASTOS) mejora la lectura.
2. **Relectura focalizada**: cuando la primera lectura de un campo no cierra,
   pedir un recorte más ceñido **a mayor DPI** y volver a leer solo esa zona.

**Entrada**

| Dónde | Campo | Tipo | Defecto | Qué es |
|---|---|---|---|---|
| multipart | `file` | archivo | — | el PDF |
| form | `regiones` | JSON string | — | lista de regiones (ver abajo) |
| query | `dpi` | int | `300` | resolución de rasterizado (72–600); subir para relectura |
| query | `incluir_pagina_completa` | bool | `false` | si `true`, agrega también el PNG de la página entera (página + bandas en una sola llamada) |

Cada **región**: `{ "nombre": str, "x0": float, "y0": float, "x1": float, "y1": float, "pagina"?: int }`.
Coordenadas relativas 0–1 (`x0<x1`, `y0<y1`). `pagina` es 1-based y opcional: si
falta, la región se aplica a **todas** las páginas. Si todas las regiones fijan
`pagina` y no se pide la página completa, **solo se rasterizan esas páginas**
(clave para la latencia de la relectura).

**Salida (`200`)**

```json
{
  "dpi": 400,
  "num_paginas": 3,
  "paginas": [
    {
      "pagina": 1, "ancho": 3307, "alto": 4677,
      "regiones": [
        {
          "nombre": "km_v1",
          "x0": 0.04, "y0": 0.30, "x1": 0.99, "y1": 0.345,
          "ancho": 3141, "alto": 211,
          "tinta_ratio": 0.19923,
          "parece_vacio": false,
          "png_base64": "iVBORw0KG..."
        }
      ]
    }
  ]
}
```

**`parece_vacio` / `tinta_ratio`** son la **guarda del propio recorte**: si un
escaneo viene desplazado o rotado, el crop puede caer sobre margen en blanco.
`tinta_ratio` es la fracción de píxeles oscuros; `parece_vacio` es `true` cuando
cae por debajo del umbral. El servicio **no decide** el fallback (es agnóstico de
dominio): expone la señal para que el llamador reemplace ese campo por la página
completa y lo marque (`crop_fallback_pagina`). La **detección de rotación** queda
fuera de alcance: la guarda cubre el caso de recorte vacío, no el de recorte
inclinado con tinta.

**Errores**

| Código | Cuándo |
|---|---|
| `400` | archivo vacío / no PDF / PDF corrupto / >20 páginas / `regiones` no es JSON o lista vacía / `pagina` fuera de rango |
| `422` | `dpi` fuera de 72–600, o región con coordenadas inválidas (fuera de 0–1, `x0≥x1`, `y0≥y1`) |
| `500` | fallo interno |

**Ejemplo**

```bash
curl -F "file=@fichas.pdf" \
     -F 'regiones=[{"nombre":"km_v1","x0":0.04,"y0":0.30,"x1":0.99,"y1":0.345,"pagina":1}]' \
     "localhost:8000/rasterizar-regiones?dpi=400"
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

## Regiones de la ficha Transliquidos (referencia)

Las bandas relativas que cubren los campos que facturan en la ficha de viaje
(formulario de layout fijo, verificadas contra el raster real a 300/400 DPI):

| Banda | `x0` | `y0` | `x1` | `y1` | Cubre |
|---|---|---|---|---|---|
| `band_matricula` | 0.03 | 0.150 | 0.99 | 0.212 | CONDUCTOR / TRACTORA / REMOLQUE |
| `km_v1` | 0.04 | 0.300 | 0.99 | 0.345 | KM inicio · final · recorridos (viaje 1) |
| `km_v2` | 0.04 | 0.435 | 0.99 | 0.478 | ídem viaje 2 |
| `km_v3` | 0.04 | 0.572 | 0.99 | 0.616 | ídem viaje 3 |

Estas coordenadas son propias del cliente Transliquidos y viven de su lado
(el rasterizador es agnóstico de dominio); se documentan aquí solo como origen
de la feature. El consumidor (canal ficha en n8n) las envía en el campo
`regiones`.
