# activos/rasterizador/app.py
import base64
import io
from typing import List

from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from pdf2image import convert_from_bytes
from pdf2image.exceptions import PDFPageCountError, PDFSyntaxError

app = FastAPI(title="Rasterizador", version="1.0.0")

DPI_DEFAULT = 300
DPI_MIN = 72
DPI_MAX = 600
MAX_PAGES = 20  # guarda contra PDFs anómalos

# TODO v1.1: POST /rasterizar-regiones — recorte por región/fila, fallback de
# lectura cuando la página entera no alcanza. Fuera de alcance de v1: se añade
# en un encargo posterior, gobernado por la barra de corte del barrido de modelos.


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
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        paginas.append(
            {
                "pagina": idx,
                "ancho": img.width,
                "alto": img.height,
                "png_base64": base64.b64encode(buf.getvalue()).decode("ascii"),
            }
        )

    return {"dpi": dpi, "num_paginas": len(paginas), "paginas": paginas}
