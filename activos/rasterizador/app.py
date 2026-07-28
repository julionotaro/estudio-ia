# activos/rasterizador/app.py
import base64
import io
import json
from typing import List, Optional

from fastapi import FastAPI, File, UploadFile, HTTPException, Query, Form
from pydantic import BaseModel, ValidationError
from PIL import Image
from pdf2image import convert_from_bytes, pdfinfo_from_bytes
from pdf2image.exceptions import PDFPageCountError, PDFSyntaxError

app = FastAPI(title="Rasterizador", version="1.1.0")

DPI_DEFAULT = 300
DPI_MIN = 72
DPI_MAX = 600
MAX_PAGES = 20  # guarda contra PDFs anómalos
MAX_REGIONES = 60  # guarda contra payloads anómalos de regiones

# Heurística de recorte vacío: si un escaneo viene desplazado/rotado el recorte
# puede caer sobre margen en blanco. No decidimos el fallback acá (eso es del
# llamador), pero exponemos la señal `parece_vacio` para que decida.
TINTA_UMBRAL = 160     # px de gris por debajo de esto = "tinta"
VACIO_UMBRAL = 0.003   # ratio de tinta por debajo de esto = recorte vacío


class Region(BaseModel):
    nombre: str
    x0: float
    y0: float
    x1: float
    y1: float
    pagina: Optional[int] = None  # 1-based; si falta, aplica a todas las páginas


def _rasterizar_paginas(data: bytes, dpi: int, paginas: Optional[List[int]]) -> dict:
    """Rasteriza el PDF y devuelve {n_pagina: PIL.Image}.

    Si `paginas` es None rasteriza todo el documento; si es una lista de números
    de página (1-based), rasteriza solo esas (optimización para la relectura
    focalizada, que pide una sola página a mayor DPI).
    """
    try:
        if paginas is None:
            imgs = convert_from_bytes(data, dpi=dpi, fmt="png")
            return {i: img for i, img in enumerate(imgs, start=1)}
        salida = {}
        for p in paginas:
            imgs = convert_from_bytes(data, dpi=dpi, fmt="png", first_page=p, last_page=p)
            salida[p] = imgs[0]
        return salida
    except (PDFPageCountError, PDFSyntaxError):
        raise HTTPException(status_code=400, detail="PDF ilegible o corrupto.")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno al rasterizar.")


def _png_b64(img: Image.Image) -> str:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("ascii")


def _tinta_ratio(img: Image.Image) -> float:
    """Fracción de píxeles oscuros (tinta) sobre el total del recorte.

    Se calcula sobre una versión reducida en escala de grises: barato y estable.
    Un recorte en blanco (escaneo desplazado) da ~0; uno con dígitos, mucho más.
    """
    chico = img.convert("L")
    if chico.width > 400:
        escala = 400 / chico.width
        chico = chico.resize((400, max(1, int(chico.height * escala))))
    histograma = chico.histogram()
    total = chico.width * chico.height
    if total == 0:
        return 0.0
    oscuros = sum(histograma[:TINTA_UMBRAL])
    return oscuros / total


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/rasterizar")
async def rasterizar(
    file: UploadFile = File(...),
    dpi: int = Query(DPI_DEFAULT, ge=DPI_MIN, le=DPI_MAX),
):
    if file.content_type not in ("application/pdf", "application/octet-stream"):
        raise HTTPException(status_code=400, detail="El archivo debe ser un PDF.")

    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Archivo vacío.")

    try:
        images = convert_from_bytes(data, dpi=dpi, fmt="png")
    except (PDFPageCountError, PDFSyntaxError):
        raise HTTPException(status_code=400, detail="PDF ilegible o corrupto.")
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno al rasterizar.")

    if len(images) > MAX_PAGES:
        raise HTTPException(
            status_code=400,
            detail=f"El PDF excede el máximo de {MAX_PAGES} páginas.",
        )

    paginas: List[dict] = []
    for idx, img in enumerate(images, start=1):
        paginas.append(
            {
                "pagina": idx,
                "ancho": img.width,
                "alto": img.height,
                "png_base64": _png_b64(img),
            }
        )

    return {"dpi": dpi, "num_paginas": len(paginas), "paginas": paginas}


@app.post("/rasterizar-regiones")
async def rasterizar_regiones(
    file: UploadFile = File(...),
    regiones: str = Form(...),
    dpi: int = Query(DPI_DEFAULT, ge=DPI_MIN, le=DPI_MAX),
    incluir_pagina_completa: bool = Query(False),
):
    """Recorta regiones (bounding boxes relativos 0–1) de las páginas del PDF.

    Devuelve, por página referida, los recortes en alta resolución. Pensado para
    (a) leer los campos numéricos críticos sobre su banda ampliada, no sobre la
    A4 entera, y (b) la relectura focalizada: pedir un recorte más ceñido a mayor
    DPI cuando la primera lectura no cierra.

    - `regiones`: JSON array de {nombre, x0, y0, x1, y1, pagina?}. Coordenadas
      relativas (0–1). `pagina` (1-based) opcional: si falta, la región se aplica
      a todas las páginas.
    - `dpi`: resolución de rasterizado (subir para la relectura).
    - `incluir_pagina_completa`: si true, incluye también el PNG de la página
      completa (permite pedir página + bandas en una sola llamada).
    """
    if file.content_type not in ("application/pdf", "application/octet-stream"):
        raise HTTPException(status_code=400, detail="El archivo debe ser un PDF.")

    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Archivo vacío.")

    # Parsear y validar las regiones.
    try:
        crudas = json.loads(regiones)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="`regiones` no es JSON válido.")
    if not isinstance(crudas, list) or not crudas:
        raise HTTPException(status_code=400, detail="`regiones` debe ser una lista no vacía.")
    if len(crudas) > MAX_REGIONES:
        raise HTTPException(
            status_code=400,
            detail=f"Demasiadas regiones (máximo {MAX_REGIONES}).",
        )
    try:
        regs = [Region(**r) for r in crudas]
    except (ValidationError, TypeError):
        raise HTTPException(status_code=422, detail="Región con campos inválidos.")

    for r in regs:
        if not (0.0 <= r.x0 < r.x1 <= 1.0 and 0.0 <= r.y0 < r.y1 <= 1.0):
            raise HTTPException(
                status_code=422,
                detail=f"Región '{r.nombre}' con coordenadas fuera de rango (0–1, x0<x1, y0<y1).",
            )

    # Cuántas páginas tiene el PDF (sin rasterizar todavía).
    try:
        info = pdfinfo_from_bytes(data)
        num_paginas = int(info["Pages"])
    except (PDFPageCountError, PDFSyntaxError):
        raise HTTPException(status_code=400, detail="PDF ilegible o corrupto.")
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno al leer el PDF.")

    if num_paginas > MAX_PAGES:
        raise HTTPException(
            status_code=400,
            detail=f"El PDF excede el máximo de {MAX_PAGES} páginas.",
        )

    for r in regs:
        if r.pagina is not None and not (1 <= r.pagina <= num_paginas):
            raise HTTPException(
                status_code=400,
                detail=f"Región '{r.nombre}' referencia página {r.pagina}, fuera de 1–{num_paginas}.",
            )

    # Qué páginas hace falta rasterizar. Si alguna región no fija página, o se
    # pide la página completa, hacen falta todas; si no, solo las referidas.
    hay_region_global = any(r.pagina is None for r in regs)
    if incluir_pagina_completa or hay_region_global:
        paginas_necesarias = None  # todas
    else:
        paginas_necesarias = sorted({r.pagina for r in regs})

    imgs = _rasterizar_paginas(data, dpi, paginas_necesarias)

    # Agrupar regiones por página de salida.
    salida_paginas: List[dict] = []
    numeros = sorted(imgs.keys())
    for p in numeros:
        img = imgs[p]
        W, H = img.width, img.height
        regs_pagina = [r for r in regs if r.pagina in (None, p)]
        recortes = []
        for r in regs_pagina:
            caja = (int(r.x0 * W), int(r.y0 * H), int(r.x1 * W), int(r.y1 * H))
            crop = img.crop(caja)
            ratio = _tinta_ratio(crop)
            recortes.append(
                {
                    "nombre": r.nombre,
                    "x0": r.x0, "y0": r.y0, "x1": r.x1, "y1": r.y1,
                    "ancho": crop.width,
                    "alto": crop.height,
                    "tinta_ratio": round(ratio, 5),
                    "parece_vacio": ratio < VACIO_UMBRAL,
                    "png_base64": _png_b64(crop),
                }
            )
        entrada = {
            "pagina": p,
            "ancho": W,
            "alto": H,
            "regiones": recortes,
        }
        if incluir_pagina_completa:
            entrada["png_base64"] = _png_b64(img)
        salida_paginas.append(entrada)

    return {"dpi": dpi, "num_paginas": num_paginas, "paginas": salida_paginas}
